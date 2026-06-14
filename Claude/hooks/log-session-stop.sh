#!/bin/bash
# Only log in projects that have opted in with a .claude/ directory
[[ -d "$PWD/.claude" ]] || exit 0
mkdir -p "$PWD/.claude/logs"
jq -cn --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{ts: $ts, event: "session_stop"}' \
  >> "$PWD/.claude/logs/session.jsonl" 2>/dev/null || true
