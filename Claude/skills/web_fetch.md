# web_fetch skill

## Summary
Fetch a JS-rendered URL via headless Chromium and get clean Markdown output.
Use for SPAs and dynamic pages where WebFetch returns skeleton/empty content.
Skip for static HTML (use WebFetch) or JSON APIs (use curl/httpx).
Output is always JSON; check `error` and `content_warnings` before reading `body_markdown`.

## When NOT to use
- Static HTML (WebFetch is faster, no subprocess) or JSON/REST APIs (curl/httpx).
- Pages behind real user auth / 2FA.
- Private or internal IPs — blocked by default; set `WEB_FETCH_ALLOW_PRIVATE=1` env var
  only if intentional.

## Invocation
```bash
python3 ~/.claude/tools/web_fetch.py <url> [options]
```
Options: `--output PATH` (JSON to file instead of stdout); `--timeout MS` (default 30000);
`--wait-for SELECTOR` (wait for CSS selector before extracting); `--screenshot PATH` (save
PNG); `--no-sandbox` (required in CI/Docker); `--daemon` (no-op placeholder, exits 0).

## Output schema
```json
{"url","final_url","http_status","title","body_markdown","content_warnings":[],"screenshot":null,"fetch_ms","error":null}
```
`body_markdown` is the useful field; `error` null on success; `content_warnings` lists login walls, bot challenges, consent gates.

## Setup (one-time)
`cd ~/Projects/dotfiles && uv sync && uv run playwright install chromium`
