#!/usr/bin/env python3
"""web_fetch.py — Playwright-based headless web fetcher.

Usage:
    python3 web_fetch.py <url> [options]

Outputs JSON to stdout (or --output file). Always valid JSON, even on error.
"""
import argparse
import ipaddress
import json
import os
import re
import socket
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------

def html_to_markdown(html: str) -> str:
    """Strip noise tags, extract <main> or <body>, return light markdown."""
    try:
        from html.parser import HTMLParser
    except ImportError:
        return html

    # Remove script, style, nav, footer, header, aside entirely (with content)
    noise_tags = re.compile(
        r"<(script|style|nav|footer|header|aside)(\s[^>]*)?>.*?</\1>",
        re.IGNORECASE | re.DOTALL,
    )
    cleaned = noise_tags.sub("", html)

    # Try to extract <main> first, then <body>
    main_match = re.search(r"<main(\s[^>]*)?>(.+?)</main>", cleaned, re.IGNORECASE | re.DOTALL)
    if main_match:
        cleaned = main_match.group(2)
    else:
        body_match = re.search(r"<body(\s[^>]*)?>(.+?)</body>", cleaned, re.IGNORECASE | re.DOTALL)
        if body_match:
            cleaned = body_match.group(2)

    try:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0
        h.unicode_snob = True
        return h.handle(cleaned).strip()
    except ImportError:
        pass

    # Minimal fallback: strip all remaining tags
    text = re.sub(r"<br\s*/?>", "\n", cleaned, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", lambda m: "#" * int(m.group(1)) + " " + m.group(2) + "\n", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Content warnings
# ---------------------------------------------------------------------------

def _strip_script_style(html: str) -> str:
    """Remove <script> and <style> blocks so their content isn't matched as visible text."""
    return re.sub(
        r"<(script|style)(\s[^>]*)?>.*?</\1>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )


def _input_has_type(tag: str, type_value: str) -> bool:
    """Return True if an <input ...> tag string has type=<type_value> (any attr order)."""
    return bool(re.search(
        rf'\btype\s*=\s*["\']?{re.escape(type_value)}["\']?',
        tag, re.IGNORECASE,
    ))


def detect_content_warnings(html: str) -> list:
    """Return list of warning strings for login walls, bot challenges, consent gates."""
    warnings = []
    lower = html.lower()

    # Bot challenge detection
    if any(phrase in lower for phrase in [
        "just a moment", "checking your browser", "ddos protection",
        "please wait", "ray id", "cloudflare", "checking if the site connection",
    ]):
        warnings.append("bot_challenge: possible Cloudflare or DDoS protection page")

    # Login wall detection — operate on HTML with scripts/styles stripped.
    visible = _strip_script_style(html)

    # Check for <input type="password"> or <input name="password"> (attribute order independent)
    _PASSWORD_ATTR = re.compile(
        r'\b(type|name)\s*=\s*["\']?password["\']?', re.IGNORECASE
    )
    has_password_input = any(
        bool(_PASSWORD_ATTR.search(m.group(0)))
        for m in re.finditer(r"<input\b[^>]*>", visible, re.IGNORECASE)
    )

    # Check visible text in interactive elements for login-related phrases.
    # Extract text from <button> and <a> tags, and also plain visible text.
    tag_text = " ".join(re.findall(
        r"<(?:button|a)\b[^>]*>(.*?)</(?:button|a)>",
        visible, re.IGNORECASE | re.DOTALL,
    ))
    # Strip any remaining tags from that text
    tag_text_clean = re.sub(r"<[^>]+>", "", tag_text).lower()

    _LOGIN_PHRASES = ("sign in", "log in", "login", "create account", "register")
    has_login_element = any(phrase in tag_text_clean for phrase in _LOGIN_PHRASES)

    # Also check submit inputs with value= attribute
    has_submit_input = any(
        _input_has_type(m.group(0), "submit")
        for m in re.finditer(r"<input\b[^>]*>", visible, re.IGNORECASE)
    )

    if has_password_input and (has_login_element or has_submit_input):
        warnings.append("login_wall: page appears to require authentication")

    # Consent gate
    if any(phrase in lower for phrase in ["accept all", "accept cookies", "cookie consent", "cookie-banner", "we use cookies", "manage preferences"]):
        warnings.append("consent_gate: cookie consent overlay detected")

    return warnings


# ---------------------------------------------------------------------------
# SSRF protection
# ---------------------------------------------------------------------------

_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("::ffff:0:0/96"),
    ipaddress.ip_network("64:ff9b::/96"),
    ipaddress.ip_network("100::/64"),
]

_BLOCKED_SCHEMES = {"file", "data", "javascript"}


def is_private_address(host: str, allow_private: bool = False) -> bool:
    """Return True if host resolves to a private/loopback address.

    allow_private=True always returns False (bypass the check).
    """
    if allow_private:
        return False
    if host.lower() in ("localhost", "localhost.", "localhost.localdomain", "0.0.0.0"):
        return True
    try:
        ip = ipaddress.ip_address(host)
        return any(ip in net for net in _PRIVATE_NETWORKS)
    except ValueError:
        pass
    try:
        resolved = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for _family, _type, _proto, _canonname, sockaddr in resolved:
            addr = sockaddr[0]
            try:
                ip = ipaddress.ip_address(addr)
                if any(ip in net for net in _PRIVATE_NETWORKS):
                    return True
            except ValueError:
                continue
    except socket.gaierror:
        pass
    return False


def _check_url_allowed(url: str, allow_private: bool = False) -> str | None:
    """Return an error string if the URL is blocked, else None."""
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    if scheme in _BLOCKED_SCHEMES:
        return f"blocked scheme: {scheme}://"

    if scheme not in ("http", "https"):
        return f"unsupported scheme: {scheme!r}"

    if not allow_private:
        host = parsed.hostname or ""
        if is_private_address(host, allow_private=False):
            return f"blocked: {host!r} resolves to a private/internal address (set WEB_FETCH_ALLOW_PRIVATE=1 to override)"

    return None


# ---------------------------------------------------------------------------
# Result builders
# ---------------------------------------------------------------------------

def build_result(
    *,
    url: str,
    final_url: str,
    http_status: int,
    title: str,
    body_markdown: str,
    content_warnings: list,
    screenshot,
    fetch_ms: int,
    error,
) -> dict:
    return {
        "url": url,
        "final_url": final_url,
        "http_status": http_status,
        "title": title,
        "body_markdown": body_markdown,
        "content_warnings": content_warnings,
        "screenshot": screenshot,
        "fetch_ms": fetch_ms,
        "error": error,
    }


def build_error_result(url: str, error: str) -> dict:
    return {
        "url": url,
        "final_url": url,
        "http_status": None,
        "title": None,
        "body_markdown": "",
        "content_warnings": [],
        "screenshot": None,
        "fetch_ms": 0,
        "error": error,
    }


# ---------------------------------------------------------------------------
# Core fetch
# ---------------------------------------------------------------------------

def fetch(url: str, args: argparse.Namespace, allow_private: bool = False) -> tuple[dict, int]:
    """Fetch url using Playwright. Returns (result_dict, exit_code)."""
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    t_start = time.monotonic()
    screenshot_path = getattr(args, "screenshot", None)
    browser_args = []
    if getattr(args, "no_sandbox", False):
        browser_args.append("--no-sandbox")
    browser_args.append("--disable-blink-features=AutomationControlled")

    ua = getattr(args, "user_agent", None) or (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    timeout_ms = getattr(args, "timeout", 30000)
    wait_for_selector = getattr(args, "wait_for", None)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=browser_args)
        try:
            context = browser.new_context(
                user_agent=ua,
                viewport={"width": 1280, "height": 900},
                java_script_enabled=True,
            )
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")

            # Intercept all navigation requests to prevent SSRF via redirects.
            def _ssrf_guard(route):
                req_url = route.request.url
                block = _check_url_allowed(req_url, allow_private=allow_private)
                if block:
                    route.abort("blockedbyclient")
                else:
                    route.continue_()

            page.route("**/*", _ssrf_guard)

            try:
                response = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            except PWTimeout:
                fetch_ms = int((time.monotonic() - t_start) * 1000)
                return build_error_result(url, "timeout: page load exceeded timeout"), 2
            except Exception as exc:
                fetch_ms = int((time.monotonic() - t_start) * 1000)
                err = build_error_result(url, f"navigation error: {exc}")
                err["fetch_ms"] = fetch_ms
                return err, 2

            if wait_for_selector:
                try:
                    page.wait_for_selector(wait_for_selector, timeout=timeout_ms)
                except PWTimeout:
                    fetch_ms = int((time.monotonic() - t_start) * 1000)
                    err = build_error_result(url, f"timeout: selector {wait_for_selector!r} not found")
                    err["fetch_ms"] = fetch_ms
                    return err, 4
                except Exception as exc:
                    fetch_ms = int((time.monotonic() - t_start) * 1000)
                    err = build_error_result(url, f"selector error: {exc}")
                    err["fetch_ms"] = fetch_ms
                    return err, 4

            http_status = response.status if response else None
            final_url = page.url
            title = page.title()
            html = page.content()
            fetch_ms = int((time.monotonic() - t_start) * 1000)

            body_markdown = html_to_markdown(html)
            content_warnings = detect_content_warnings(html)

            shot_path = None
            if screenshot_path:
                page.screenshot(path=screenshot_path, full_page=False)
                shot_path = screenshot_path

            result = build_result(
                url=url,
                final_url=final_url,
                http_status=http_status,
                title=title,
                body_markdown=body_markdown,
                content_warnings=content_warnings,
                screenshot=shot_path,
                fetch_ms=fetch_ms,
                error=None,
            )
            exit_code = 0
            return result, exit_code
        finally:
            browser.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="web_fetch.py",
        description="Fetch a URL via headless Chromium and return JSON.",
    )
    p.add_argument("url", nargs="?", help="URL to fetch")
    p.add_argument("--output", metavar="PATH", help="Write JSON to file instead of stdout")
    p.add_argument("--timeout", type=int, default=30000, metavar="MS", help="Page load timeout (ms, default 30000)")
    p.add_argument("--wait-for", metavar="SELECTOR", dest="wait_for", help="Wait for CSS selector before extracting")
    p.add_argument("--screenshot", metavar="PATH", help="Save screenshot to file")
    p.add_argument("--no-sandbox", action="store_true", dest="no_sandbox", help="Pass --no-sandbox to Chromium (for CI)")
    p.add_argument("--daemon", action="store_true", help="Placeholder: daemon mode not yet implemented")
    p.add_argument("--user-agent", metavar="STRING", dest="user_agent", help="Override User-Agent string")
    return p


def emit(data: dict, output_path: str | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if output_path:
        Path(output_path).write_text(text, encoding="utf-8")
    else:
        print(text)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # --daemon: placeholder
    if args.daemon:
        print("daemon mode not yet implemented")
        return 0

    if not args.url:
        parser.print_usage(sys.stderr)
        return 1

    url = args.url

    # Basic URL validation
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        result = build_error_result(url, f"invalid URL: no scheme or host in {url!r}")
        emit(result, args.output)
        return 1

    # SSRF check — allow_private gated behind env var, not CLI flag
    allow_private = os.environ.get("WEB_FETCH_ALLOW_PRIVATE", "") == "1"
    block_reason = _check_url_allowed(url, allow_private=allow_private)
    if block_reason:
        result = build_error_result(url, block_reason)
        emit(result, args.output)
        return 1

    try:
        result, exit_code = fetch(url, args, allow_private=allow_private)
    except Exception as exc:
        result = build_error_result(url, f"unexpected error: {exc}")
        exit_code = 2

    emit(result, args.output)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
