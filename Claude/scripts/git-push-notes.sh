#!/bin/bash
# Pushes the current branch and Claude session notes to remote.
# Usage: git-push-notes.sh [remote]
set -euo pipefail

REMOTE="${1:-origin}"

git push "$REMOTE"

if git notes --ref=claude show HEAD &>/dev/null; then
  git push "$REMOTE" refs/notes/claude 2>/dev/null && echo "Notes pushed to $REMOTE" || {
    echo "Warning: could not push refs/notes/claude to $REMOTE" >&2
    echo "To configure permanently: git config --add remote.$REMOTE.push refs/notes/claude" >&2
  }
fi
