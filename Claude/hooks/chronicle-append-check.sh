#!/bin/bash
# Non-judging M3 reporter (fieldnotes automation plan, f73360): on session Stop,
# record whether this repo's chronicle was touched. Data only; measurement is
# chronicle_append_rate over the jsonl. Never blocks, never judges, always exits 0.
LOG="$HOME/.claude/logs/chronicle-append.jsonl"
mkdir -p "$(dirname "$LOG")" 2>/dev/null
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
chr="$repo_root/.claude/chronicle.md"
exists=false; dirty=false; mtime=""
if [ -f "$chr" ]; then
  exists=true
  mtime=$(stat -f %m "$chr" 2>/dev/null || stat -c %Y "$chr" 2>/dev/null)
  git -C "$repo_root" status --porcelain -- "$chr" 2>/dev/null | grep -q . && dirty=true
fi
printf '{"ts":%s,"repo":"%s","chronicle_exists":%s,"dirty":%s,"mtime":"%s"}\n' \
  "$(date +%s)" "$repo_root" "$exists" "$dirty" "$mtime" >> "$LOG"
exit 0
