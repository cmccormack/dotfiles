## Summary
Fetch a JS-rendered URL via headless Chromium and get clean Markdown output.
Use for SPAs and dynamic pages where WebFetch returns empty/incomplete content.
Skip for static HTML (use WebFetch) or JSON APIs (use curl/httpx).
Output is always JSON; check `error` and `content_warnings` before reading `body_markdown`.

# web_fetch skill

## When to use
- Target is a SPA (React, Vue, Angular) or requires JS execution to render content
- WebFetch returns skeleton HTML or empty body
- Need to wait for a CSS selector or take a screenshot

## When NOT to use
- Static HTML pages — WebFetch is faster with no subprocess overhead
- JSON/REST APIs — use curl or httpx directly
- Pages behind real user auth / 2FA
- Private or internal IPs (blocked by default; set `WEB_FETCH_ALLOW_PRIVATE=1` env var only if intentional)

## Invocation
```bash
python3 ~/.claude/tools/web_fetch.py <url> [options]
```
Key options:
- `--output PATH` — write JSON to file instead of stdout
- `--timeout MS` — default 30000
- `--wait-for SELECTOR` — wait for CSS selector before extracting
- `--screenshot PATH` — save PNG screenshot
- `--no-sandbox` — required in CI/Docker environments
- `--daemon` — no-op placeholder (exits 0)

## Output schema
```json
{"url","final_url","http_status","title","body_markdown","content_warnings":[],"screenshot":null,"fetch_ms","error":null}
```
`body_markdown` is the useful field. Always check `error` (null on success) and `content_warnings` (login walls, bot challenges, consent gates) first.

## Setup (one-time)
```bash
cd ~/Projects/dotfiles && uv sync && uv run playwright install chromium
```
