#!/bin/bash
# Splits git-dirty files into this session's changes vs leftovers.
# Session-changed = logged by a Write/Edit call for CLAUDE_CODE_SESSION_ID
# in session.jsonl, or mtime at/after the session's first logged event
# (catches Bash-mutated files). Without a session id or log, everything
# lands under "## other".
# Usage: git-session-files.sh [path/to/session.jsonl]
set -euo pipefail

JSONL="${1:-.claude/logs/session.jsonl}"
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "error: not a git repo" >&2; exit 1; }

PORCELAIN=$(git -C "$REPO_ROOT" status --porcelain)

PORCELAIN="$PORCELAIN" REPO_ROOT="$REPO_ROOT" JSONL="$JSONL" \
  SID="${CLAUDE_CODE_SESSION_ID:-}" python3 - << 'EOF'
import json, os
from datetime import datetime, timezone

root, jsonl, sid = os.environ["REPO_ROOT"], os.environ["JSONL"], os.environ["SID"]

dirty = []
for line in os.environ["PORCELAIN"].splitlines():
    p = line[3:]
    if " -> " in p:
        p = p.split(" -> ")[-1]
    if p.startswith('"') and p.endswith('"'):
        try:
            p = json.loads(p)
        except ValueError:
            pass
    if p:
        dirty.append(p)

tool_files, start = set(), None
if sid and os.path.isfile(jsonl):
    with open(jsonl) as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("session") != sid:
                continue
            if start is None:
                start = datetime.strptime(rec["ts"], "%Y-%m-%dT%H:%M:%SZ") \
                    .replace(tzinfo=timezone.utc).timestamp()
            if rec.get("tool") in ("Write", "Edit"):
                f = (rec.get("detail") or {}).get("file")
                if f:
                    rel = os.path.relpath(f, root)
                    if not rel.startswith(".."):
                        tool_files.add(rel)

def session_changed(p):
    if p in tool_files:
        return True
    if start is None:
        return False
    try:
        return os.path.getmtime(os.path.join(root, p)) >= start
    except OSError:
        return False

sess = sorted(p for p in dirty if session_changed(p))
print("## session")
for p in sess:
    print(p)
print("## other")
for p in sorted(p for p in dirty if p not in sess):
    print(p)
EOF
