# session.jsonl logging

## What it is
Per-project tool-call telemetry written by the two global hooks (see settings.md).
Opt-in: hooks exit 0 unless `$PWD/.claude/` exists. Lands at
`<project>/.claude/logs/session.jsonl`, append-only, one JSON object per line.

## Format (verified against live log)
```json
{"ts":"2026-07-03T18:43:19Z","session":"122e4bf8-...","tool":"Read","detail":{"file":"/abs/path"}}
{"ts":"...","session":"...","tool":"Bash","detail":{"cmd":"first 120 chars of command"}}
{"ts":"...","event":"session_stop"}
```
`detail` is `{cmd}` for Bash, `{file}` for Write/Edit/Read, `{prompt}` for Agent, else null.
Matched tools: `Bash|Write|Edit|Read|Agent|WebFetch|WebSearch`.

## Consumers
1. `/token-audit` (`~/.claude/skills/token-audit.md`) — reads the log, counts calls by tool,
   top repeated Bash commands, flags context bloat (same file read repeatedly, commands run
   >3x), recommends 1-3 fixes. Output capped under 200 words.
2. `/git-commit` Step 1 — `~/.claude/scripts/git-session-files.sh .claude/logs/session.jsonl`
   extracts `.detail.file` from Write/Edit events (plus `git status --short`) to discover
   which files this session touched, for staging.
3. `git-correlate.sh` — counts `.tool` lines for the `tool_calls` figure stored in git notes.

Status: production. The log is the backbone of session→commit correlation.

## Changing safely
- Never rename/move the log path — both consumer scripts default to
  `.claude/logs/session.jsonl` relative to `$PWD`.
- If you extend the logged fields, keep existing keys stable (`tool`, `detail.file` are
  load-bearing for git-session-files.sh; `tool` for git-correlate.sh).
- Log grows unbounded; safe to truncate between sessions, but doing so mid-session breaks
  /git-commit file discovery for that session.

## Provenance and maintenance
Verified 2026-07-03 by reading both hook scripts, both consumer skills, both scripts, and a
live log. Re-verify: `tail -3 .claude/logs/session.jsonl | jq .` in any project with `.claude/`.
