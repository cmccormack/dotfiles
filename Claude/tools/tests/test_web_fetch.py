"""Tests for ~/.claude/tools/web_fetch.py.

Run unit/security tests only:
    pytest tests/test_web_fetch.py -m "not integration"

Run everything (requires network):
    pytest tests/test_web_fetch.py
"""
import json
import os
import socket
import subprocess
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

TOOL = Path(__file__).parent.parent / "web_fetch.py"
PYTHON = sys.executable


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_tool(*args, input_text=None, env=None):
    """Run web_fetch.py as a subprocess and return (returncode, stdout, stderr)."""
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    result = subprocess.run(
        [PYTHON, str(TOOL), *args],
        capture_output=True,
        text=True,
        input=input_text,
        env=run_env,
    )
    return result.returncode, result.stdout, result.stderr


def parse_json_output(stdout: str) -> dict:
    """Parse JSON from tool stdout; fails the test clearly if invalid."""
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"Tool stdout is not valid JSON: {exc}\nstdout={stdout!r}")


# ---------------------------------------------------------------------------
# 1. SSRF / Security (unit tests, no network)
# ---------------------------------------------------------------------------

class TestSSRF:
    """URL scheme and private-IP blocking — all exercised without network."""

    BLOCKED_URLS = [
        "file:///etc/passwd",
        "file:///Users/chris/.ssh/id_rsa",
        "data:text/html,<h1>hi</h1>",
        "javascript:alert(1)",
        "http://192.168.1.1/",
        "http://192.168.0.100/admin",
        "http://127.0.0.1/",
        "http://localhost/",
        "http://10.0.0.1/",
        "http://10.255.255.255/",
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/",
        # IPv6 private ranges
        "http://[fe80::1]/",
        "http://[::1]/",
        "http://[fc00::1]/",
    ]

    @pytest.mark.parametrize("url", BLOCKED_URLS)
    def test_blocked_url_exits_nonzero(self, url):
        rc, stdout, stderr = run_tool(url)
        assert rc != 0, f"Expected non-zero exit for {url!r}, got 0"

    @pytest.mark.parametrize("url", BLOCKED_URLS)
    def test_blocked_url_returns_valid_json_with_error(self, url):
        _rc, stdout, _stderr = run_tool(url)
        data = parse_json_output(stdout)
        assert data.get("error"), f"Expected 'error' field set for {url!r}"

    def test_file_scheme_blocked(self):
        rc, stdout, _ = run_tool("file:///etc/passwd")
        assert rc != 0
        data = parse_json_output(stdout)
        assert data["error"]

    def test_data_uri_blocked(self):
        rc, stdout, _ = run_tool("data:text/html,<b>x</b>")
        assert rc != 0
        data = parse_json_output(stdout)
        assert data["error"]

    def test_javascript_uri_blocked(self):
        rc, stdout, _ = run_tool("javascript:void(0)")
        assert rc != 0
        data = parse_json_output(stdout)
        assert data["error"]

    def test_allow_private_bypasses_block(self):
        """WEB_FETCH_ALLOW_PRIVATE=1 env var should skip the private-IP check.

        Verifies the guard function honours the allow_private parameter, which
        is now sourced from the env var rather than the CLI.
        """
        import importlib.util

        spec = importlib.util.spec_from_file_location("web_fetch", TOOL)
        if spec is None:
            pytest.skip("web_fetch.py not yet implemented")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "is_private_address"):
            assert not mod.is_private_address("192.168.1.1", allow_private=True)
            assert mod.is_private_address("192.168.1.1", allow_private=False)

    def test_allow_private_env_var_bypasses_block(self):
        """WEB_FETCH_ALLOW_PRIVATE=1 should allow private IPs through the guard."""
        rc, stdout, stderr = run_tool(
            "http://192.168.1.1/",
            env={"WEB_FETCH_ALLOW_PRIVATE": "1"},
        )
        # Should NOT exit 1 (SSRF block); may exit 2 (network error).
        data = parse_json_output(stdout)
        assert "private" not in (data.get("error") or ""), (
            f"Expected SSRF guard bypassed, got error: {data.get('error')}"
        )


# ---------------------------------------------------------------------------
# 2. Output Schema (unit tests, mock Playwright)
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {
    "url", "final_url", "http_status", "title",
    "body_markdown", "content_warnings", "screenshot", "fetch_ms", "error",
}


def _make_mock_page(html="<html><head><title>Test</title></head><body><p>Hello</p></body></html>",
                    title="Test", url="https://example.com", status=200):
    page = MagicMock()
    page.title.return_value = title
    page.url = url
    page.content.return_value = html
    page.inner_text.return_value = "Hello"

    response = MagicMock()
    response.status = status
    page.goto.return_value = response
    return page


class TestOutputSchema:
    """Validate JSON envelope regardless of page content."""

    def _load_module(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("web_fetch", TOOL)
        if spec is None:
            pytest.skip("web_fetch.py not yet implemented")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_success_response_has_all_required_fields(self):
        mod = self._load_module()
        if not hasattr(mod, "build_result"):
            pytest.skip("build_result() not yet implemented")
        result = mod.build_result(
            url="https://example.com",
            final_url="https://example.com",
            http_status=200,
            title="Test",
            body_markdown="Hello",
            content_warnings=[],
            screenshot=None,
            fetch_ms=1234,
            error=None,
        )
        assert REQUIRED_FIELDS <= result.keys(), (
            f"Missing fields: {REQUIRED_FIELDS - result.keys()}"
        )

    def test_error_response_has_required_fields(self):
        mod = self._load_module()
        if not hasattr(mod, "build_error_result"):
            pytest.skip("build_error_result() not yet implemented")
        result = mod.build_error_result(error="timeout", url="https://example.com")
        assert "error" in result
        assert result["error"]

    def test_json_valid_on_exception(self):
        """Even if something goes wrong, stdout must be parseable JSON."""
        rc, stdout, _ = run_tool("https://!!invalid-hostname-that-will-error!!")
        # We accept any exit code; what matters is JSON.
        if stdout.strip():
            data = parse_json_output(stdout)
            assert "error" in data

    def test_success_fields_have_safe_defaults(self):
        """screenshot should be null (not absent) when not requested."""
        mod = self._load_module()
        if not hasattr(mod, "build_result"):
            pytest.skip("build_result() not yet implemented")
        result = mod.build_result(
            url="https://example.com",
            final_url="https://example.com",
            http_status=200,
            title="",
            body_markdown="",
            content_warnings=[],
            screenshot=None,
            fetch_ms=0,
            error=None,
        )
        assert result["screenshot"] is None
        assert isinstance(result["content_warnings"], list)
        assert result["error"] is None


# ---------------------------------------------------------------------------
# 3. Content Warnings (unit tests, mock page content)
# ---------------------------------------------------------------------------

class TestContentWarnings:
    """detect_content_warnings(html) → list of warning strings."""

    def _detect(self, html: str) -> list:
        import importlib.util
        spec = importlib.util.spec_from_file_location("web_fetch", TOOL)
        if spec is None:
            pytest.skip("web_fetch.py not yet implemented")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "detect_content_warnings"):
            pytest.skip("detect_content_warnings() not yet implemented")
        return mod.detect_content_warnings(html)

    LOGIN_WALL_HTML = textwrap.dedent("""
        <html><body>
          <form action="/login" method="post">
            <input name="username"><input name="password">
            <button>Sign in</button>
          </form>
        </body></html>
    """)

    CLOUDFLARE_HTML = textwrap.dedent("""
        <html><head><title>Just a moment...</title></head>
        <body>Checking if the site connection is secure</body></html>
    """)

    COOKIE_CONSENT_HTML = textwrap.dedent("""
        <html><body>
          <div class="cookie-banner">
            We use cookies. <button>Accept all</button>
            <button>Manage preferences</button>
          </div>
          <main>Real content here</main>
        </body></html>
    """)

    CLEAN_HTML = textwrap.dedent("""
        <html><head><title>Hello</title></head>
        <body><main><p>Clean content, no walls.</p></main></body></html>
    """)

    def test_login_wall_detected(self):
        warnings = self._detect(self.LOGIN_WALL_HTML)
        assert any("login" in w.lower() or "auth" in w.lower() for w in warnings), (
            f"Expected login-wall warning, got: {warnings}"
        )

    def test_bot_challenge_detected(self):
        warnings = self._detect(self.CLOUDFLARE_HTML)
        assert any("bot" in w.lower() or "challenge" in w.lower() or "captcha" in w.lower()
                   for w in warnings), f"Expected bot-challenge warning, got: {warnings}"

    def test_consent_gate_detected(self):
        warnings = self._detect(self.COOKIE_CONSENT_HTML)
        assert any("consent" in w.lower() or "cookie" in w.lower() for w in warnings), (
            f"Expected consent-gate warning, got: {warnings}"
        )

    def test_clean_page_no_warnings(self):
        warnings = self._detect(self.CLEAN_HTML)
        assert warnings == [], f"Expected no warnings for clean page, got: {warnings}"


# ---------------------------------------------------------------------------
# 4. HTML → Markdown extraction (unit tests)
# ---------------------------------------------------------------------------

class TestHTMLToMarkdown:
    """html_to_markdown(html) strips noise and preserves main content."""

    def _convert(self, html: str) -> str:
        import importlib.util
        spec = importlib.util.spec_from_file_location("web_fetch", TOOL)
        if spec is None:
            pytest.skip("web_fetch.py not yet implemented")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "html_to_markdown"):
            pytest.skip("html_to_markdown() not yet implemented")
        return mod.html_to_markdown(html)

    FULL_PAGE = textwrap.dedent("""
        <html>
        <head>
          <title>Article</title>
          <style>body { color: red; }</style>
          <script>var x = 1;</script>
        </head>
        <body>
          <nav><a href="/">Home</a><a href="/about">About</a></nav>
          <main>
            <h1>Real Article Title</h1>
            <p>This is the main content paragraph.</p>
          </main>
          <footer>Copyright 2026</footer>
          <script>analytics.track('view');</script>
        </body>
        </html>
    """)

    def test_script_tags_stripped(self):
        md = self._convert(self.FULL_PAGE)
        assert "var x = 1" not in md
        assert "analytics.track" not in md

    def test_style_tags_stripped(self):
        md = self._convert(self.FULL_PAGE)
        assert "color: red" not in md

    def test_nav_stripped(self):
        md = self._convert(self.FULL_PAGE)
        assert "Home" not in md or "About" not in md  # nav links gone

    def test_footer_stripped(self):
        md = self._convert(self.FULL_PAGE)
        assert "Copyright 2026" not in md

    def test_main_content_preserved(self):
        md = self._convert(self.FULL_PAGE)
        assert "Real Article Title" in md
        assert "main content paragraph" in md


# ---------------------------------------------------------------------------
# 5. CLI argument tests (subprocess, no real network needed for most)
# ---------------------------------------------------------------------------

class TestCLIArgs:

    def test_missing_url_exits_nonzero(self):
        rc, stdout, stderr = run_tool()
        assert rc != 0

    def test_invalid_url_no_scheme_exits_nonzero(self):
        rc, stdout, stderr = run_tool("not-a-url-at-all")
        assert rc != 0
        if stdout.strip():
            data = parse_json_output(stdout)
            assert data.get("error")

    def test_daemon_flag_exits_zero(self):
        rc, stdout, stderr = run_tool("--daemon")
        assert rc == 0, f"Expected exit 0 for --daemon, got {rc}\nstderr={stderr}"

    def test_daemon_flag_prints_not_implemented(self):
        _rc, stdout, stderr = run_tool("--daemon")
        combined = (stdout + stderr).lower()
        assert "daemon" in combined and (
            "not" in combined or "implement" in combined
        ), f"Expected 'daemon mode not yet implemented' message, got: {combined!r}"

    def test_timeout_flag_accepted(self):
        """--timeout should be parsed without error (even if fetch itself fails)."""
        rc, stdout, stderr = run_tool("https://example.com", "--timeout", "5000")
        # We accept network failure (rc=2) but not arg-parse failure (rc=1).
        assert rc != 1, f"--timeout caused arg-parse error\nstderr={stderr}"

    def test_no_sandbox_flag_accepted(self):
        rc, stdout, stderr = run_tool("https://example.com", "--no-sandbox")
        assert rc != 1, f"--no-sandbox caused arg-parse error\nstderr={stderr}"

    def test_output_to_file(self, tmp_path):
        out = tmp_path / "result.json"
        rc, stdout, stderr = run_tool(
            "https://example.com", "--output", str(out)
        )
        # If the tool ran far enough to write output, the file exists and is JSON.
        if out.exists():
            data = json.loads(out.read_text())
            assert isinstance(data, dict)
        # stdout should be empty or minimal when --output is used.

    def test_allow_private_env_bypasses_ssrf(self):
        rc, stdout, stderr = run_tool(
            "http://192.168.1.1/",
            env={"WEB_FETCH_ALLOW_PRIVATE": "1"},
        )
        # Should NOT exit 1 (SSRF block); may exit 2 (network error).
        if stdout.strip():
            data = parse_json_output(stdout)
            assert "private" not in (data.get("error") or ""), (
                f"Expected SSRF bypass, got: {data.get('error')}"
            )


# ---------------------------------------------------------------------------
# 6. Integration tests (real network)
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestIntegration:
    """Fetch real JS-rendered public sites and validate the response envelope."""

    SITES = [
        ("https://react.dev", "React SPA"),
        ("https://vuejs.org", "Vue SPA"),
        ("https://news.ycombinator.com", "Hacker News baseline"),
        ("https://github.com/trending", "GitHub dynamic"),
    ]

    @pytest.mark.parametrize("url,label", SITES)
    @pytest.mark.timeout(60)
    def test_site_returns_200_with_content(self, url, label):
        rc, stdout, stderr = run_tool(url, "--timeout", "45000")
        assert rc == 0, (
            f"{label}: expected exit 0, got {rc}\nstderr={stderr}\nstdout={stdout[:500]}"
        )
        data = parse_json_output(stdout)
        assert data.get("http_status") == 200, (
            f"{label}: http_status={data.get('http_status')}"
        )
        assert data.get("body_markdown", "").strip(), (
            f"{label}: body_markdown is empty"
        )
        assert data.get("title", "").strip(), (
            f"{label}: title is empty"
        )
        assert not data.get("error"), (
            f"{label}: unexpected error: {data.get('error')}"
        )
        assert REQUIRED_FIELDS <= data.keys(), (
            f"{label}: missing fields {REQUIRED_FIELDS - data.keys()}"
        )

    @pytest.mark.timeout(60)
    def test_react_dev_js_rendered_content(self):
        """react.dev is a React SPA — content must come from JS execution."""
        rc, stdout, _ = run_tool("https://react.dev", "--timeout", "45000")
        if rc != 0:
            pytest.skip("network or site unavailable")
        data = parse_json_output(stdout)
        md = data.get("body_markdown", "")
        # React's landing page always has "React" in the rendered content.
        assert "React" in md, f"JS-rendered content not found in body_markdown"

    @pytest.mark.timeout(60)
    def test_hn_baseline(self):
        """Hacker News is static — quick sanity check."""
        rc, stdout, _ = run_tool("https://news.ycombinator.com", "--timeout", "30000")
        if rc != 0:
            pytest.skip("network or site unavailable")
        data = parse_json_output(stdout)
        assert data.get("http_status") == 200
        assert "Hacker News" in data.get("title", "") or "Y Combinator" in data.get("body_markdown", "")

    @pytest.mark.timeout(60)
    def test_final_url_captured_after_redirect(self):
        """http:// → https:// redirect: final_url should differ from requested url."""
        rc, stdout, _ = run_tool("http://github.com/trending", "--timeout", "45000")
        if rc != 0:
            pytest.skip("network or site unavailable")
        data = parse_json_output(stdout)
        assert "final_url" in data
        # After redirect, final_url should be https.
        assert data["final_url"].startswith("https://"), (
            f"Expected https final_url, got: {data.get('final_url')}"
        )
