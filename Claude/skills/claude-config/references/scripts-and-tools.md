# scripts/ and tools/

## scripts/ — the /git-commit plumbing (production)

All in `~/.claude/scripts/` (= `dotfiles/Claude/scripts`), bash, `set -euo pipefail`:

- `git-session-files.sh [session.jsonl]` — emits repo-relative paths of files changed this
  session: Write/Edit `.detail.file` entries from session.jsonl, unioned with
  `git status --short` (catches Bash-mutated files). /git-commit Step 1.
- `git-correlate.sh [session.jsonl]` — attaches `{"session","ts","tool_calls"}` to HEAD via
  `git notes --ref=claude add -f` (never touches the commit message); session id from
  `$CLAUDE_CODE_SESSION_ID`. /git-commit Step 6. View: `git notes --ref=claude show HEAD`.
- `git-push-notes.sh [remote]` — `git push` the branch, then push `refs/notes/claude`,
  warning (not failing) if the notes ref is rejected. /git-commit Step 7.

Changing safely: these are called by literal command lines quoted inside
`skills/git-commit.md` — update the skill in the same change if you rename flags or paths.

## tools/ — web_fetch.py (production, tested)

`~/.claude/tools/web_fetch.py` (~15 KB): Playwright headless-Chromium fetcher for
JS-rendered pages; always emits valid JSON
(`{url, final_url, http_status, title, body_markdown, content_warnings[], screenshot, fetch_ms, error}`).
SSRF guard blocks private IPs unless `WEB_FETCH_ALLOW_PRIVATE=1`. Options: `--output`,
`--timeout`, `--wait-for`, `--screenshot`, `--no-sandbox`, `--daemon` (no-op).
Fronted by the `/web_fetch` skill (`skills/web_fetch.md`); invoke as
`python3 ~/.claude/tools/web_fetch.py <url>`.

Tests: `tools/tests/` — `conftest.py` defines an `integration` marker with a real-network
auto-skip; `test_web_fetch.py` runs the tool as a subprocess and asserts the JSON contract.
Deps (pytest, playwright, html2text) pinned in dotfiles `pyproject.toml` (Python ≥3.13, uv).

Changing safely: edit, then run the unit tests before the session ends — the tool is live
the moment you save (symlinked dir). One-time setup on a new machine:
`cd ~/Projects/dotfiles && uv sync && uv run playwright install chromium`.

NOTE: the `~/.claude/tools` symlink is NOT in `manifest.conf` (see symlink-sync.md) —
recreate it manually on a new machine: `ln -s ~/Projects/dotfiles/Claude/tools ~/.claude/tools`.

## Provenance and maintenance
Verified 2026-07-03 by reading all three scripts, web_fetch.md, and listing tools/tests/.
Re-verify: `ls ~/.claude/scripts ~/.claude/tools` and
`cd ~/Projects/dotfiles && uv run pytest Claude/tools/tests/ -m "not integration" -q`.
