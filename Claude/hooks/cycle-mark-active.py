#!/usr/bin/env python3
"""PreToolUse hook (matcher: Skill): mark a /cycle session as active.

Companion to cycle-stop-check.sh. Writes a small state file the moment the
`cycle` skill is invoked, recording which session_id claimed this scope and
when. cycle-stop-check.sh uses this to know whether the current Stop event
belongs to a session that has actually engaged in cycle work, so it can skip
the closing-line hard block on ordinary conversational turns where no cycle
work has happened yet.

State lives outside any repo (~/.claude/state/cycle-active/) so it never
needs a .gitignore entry and can't accidentally get committed.

Fail-open: any error exits 0 silently, same pattern as check_skill_size.py.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

STATE_DIR = Path.home() / ".claude" / "state" / "cycle-active"
TRACKER_FILES = ("TODO.md", "ISSUES.md", "RESUME.md")


def find_repo_root(cwd):
    out = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, timeout=5,
    )
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def find_scope(cwd, repo_root):
    d = Path(cwd).resolve()
    root = Path(repo_root).resolve()
    seen = set()
    while d not in seen:
        seen.add(d)
        if all((d / f).is_file() for f in TRACKER_FILES):
            return d
        if d == root or d.parent == d:
            return None
        d = d.parent
    return None


def main():
    payload = json.load(sys.stdin)
    if payload.get("tool_input", {}).get("skill") != "cycle":
        return

    cwd = payload.get("cwd") or "."
    repo_root = find_repo_root(cwd)
    if not repo_root:
        return
    scope = find_scope(cwd, repo_root)
    if scope is None:
        return

    session_id = payload.get("session_id")
    if not session_id:
        return

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(str(scope).encode()).hexdigest()
    marker = STATE_DIR / f"{key}.json"
    marker.write_text(json.dumps({
        "scope": str(scope),
        "session_id": session_id,
        "created_utc": subprocess.run(
            ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True,
        ).stdout.strip(),
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
