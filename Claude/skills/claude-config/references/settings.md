# settings.json — every key

File: `~/Projects/dotfiles/Claude/settings.json` (live at `~/.claude/settings.json`).
Schema: `"$schema": "https://json.schemastore.org/claude-code-settings.json"`.

## Keys present (verified 2026-07-03)

| Key | Value / contents | Status |
|---|---|---|
| `permissions.allow` | ~70 rules: `WebSearch(*)`; ~24 `WebFetch(domain:...)` entries (github, reddit, steam/proton/gaming sites, archwiki); `Bash(python3 *)`, `Bash(python *)`; read-only bash (`ls`, `find`, `grep`, `cat`, `head`, `tail`, `wc`, `stat`, `file`, `echo`, `pwd`, `which`, `type`, `env`, `printenv`, `sed`, `awk`, `sort`, `uniq`, `cut`, `tr`, `jq`, `xargs`, `strings`, `curl`, `wget`, `tar`, `unzip`); git (`log/status/diff/show/branch/add/commit/push/notes`); `Write(/Users/chris/Projects/steamdeck/.claude/research/*)` and `.../cache/*` | production |
| `model` | `"sonnet"` | production |
| `hooks` | `PreToolUse` + `Stop` (below) | production |
| `statusLine` | `{"type":"command","command":"bash ~/.claude/statusline/statusline.sh"}` — script is machine-local, not synced | production |
| `effortLevel` | `"high"` | production |
| `voice` | `{"mode":"hold","autoSubmit":true}` + `voiceEnabled: true` | experimental (UI pref) |
| `theme` | `"dark"` | production (UI pref) |

Convention (from steamdeck memory): agents inherit only THIS global file, not project
settings — so agent-needed `WebFetch` domains and absolute-path `Write(...)` rules go here,
never `WebFetch(*)` in a project scope.

## Configured hooks

- `PreToolUse`, matcher `Bash|Write|Edit|Read|Agent|WebFetch|WebSearch`, async:
  `bash $HOME/.claude/hooks/log-tool-use.sh` — if `$PWD/.claude/` exists (opt-in), appends
  one JSON line per tool call to `$PWD/.claude/logs/session.jsonl`:
  `{ts, session, tool, detail}` where detail is `{cmd}` (first 120 chars), `{file}`, or
  `{prompt}` (first 80 chars).
- `Stop`, async: `bash $HOME/.claude/hooks/log-session-stop.sh` — same opt-in gate, appends
  `{ts, event: "session_stop"}`.

Both scripts live in `dotfiles/Claude/hooks/`, require `jq`, and fail silently (`|| true`).

## Changing safely
1. Route through change-control; for the edit itself use the `update-config` skill **via an
   Agent** (it is on the heavy-skill list — never load it inline).
2. Hooks config is read at session start — restart the session to pick up hook changes.
3. Test a new hook by running its matched tool once, then `tail -1 .claude/logs/session.jsonl`.
4. Commit via `/git-commit`.

## Provenance and maintenance
Verified 2026-07-03 by reading settings.json and both hook scripts. Re-verify:
`jq 'keys, .hooks' ~/.claude/settings.json && ls ~/.claude/hooks`.
