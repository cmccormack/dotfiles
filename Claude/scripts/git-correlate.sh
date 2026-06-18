#!/bin/bash
# Attaches Claude session metadata to HEAD via git notes (refs/notes/claude).
# Does not modify the commit message.
# Usage: git-correlate.sh [path/to/session.jsonl]
set -euo pipefail

JSONL="${1:-.claude/logs/session.jsonl}"
SESSION_ID="${CLAUDE_CODE_SESSION_ID:-unknown}"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

TOOL_COUNT=0
if [[ -f "$JSONL" ]]; then
  TOOL_COUNT=$(jq -r '.tool' "$JSONL" 2>/dev/null | wc -l | tr -d ' ')
fi

NOTE=$(printf '{"session":"%s","ts":"%s","tool_calls":%s}' "$SESSION_ID" "$TS" "$TOOL_COUNT")

git notes --ref=claude add -f -m "$NOTE" HEAD
echo "Correlated: session=$SESSION_ID tool_calls=$TOOL_COUNT"
echo "View with: git notes --ref=claude show HEAD"
