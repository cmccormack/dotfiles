#!/bin/bash
# Only log in projects that have opted in with a .claude/ directory
[[ -d "$PWD/.claude" ]] || exit 0
mkdir -p "$PWD/.claude/logs"
jq -c --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{ts: $ts, session: (.session_id // "?"), tool: .tool_name, detail: (.tool_input | if .command then {cmd: (.command[:120])} elif .file_path then {file: .file_path} elif .prompt then {prompt: (.prompt[:80])} else null end)}' \
  >> "$PWD/.claude/logs/session.jsonl" 2>/dev/null || true
