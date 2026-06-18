#!/bin/bash
# Outputs repo-relative paths of files changed this Claude session.
# Sources: Write/Edit tool calls in session.jsonl + git status (catches Bash-mutated files).
# Usage: git-session-files.sh [path/to/session.jsonl]
set -euo pipefail

JSONL="${1:-.claude/logs/session.jsonl}"
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "error: not a git repo" >&2; exit 1; }

{
  # Files from Write/Edit tool calls logged by hook
  if [[ -f "$JSONL" ]]; then
    jq -r 'select(.tool=="Write" or .tool=="Edit") | .detail.file // empty' "$JSONL" 2>/dev/null | \
      python3 -c "
import sys, os
root = sys.argv[1]
for line in sys.stdin:
    p = line.strip()
    if not p:
        continue
    try:
        rel = os.path.relpath(p, root)
        if not rel.startswith('..'):
            print(rel)
    except ValueError:
        pass
" "$REPO_ROOT"
  fi

  # Files from git status (catches Bash-mutated, generated, or externally changed files)
  git -C "$REPO_ROOT" status --short 2>/dev/null | awk '{print $NF}'

} | sort -u | grep -v '^$'
