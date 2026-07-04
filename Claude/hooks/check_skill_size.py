#!/usr/bin/env python3
"""PreToolUse guard (matcher: Skill): block heavy skills from loading inline.

Global promotion of macknet's .claude/hooks/check_skill_size.py (campaign Phase 1,
2026-07-04). Fail-open: any error exits 0 so a hook bug never blocks a session.
"""
import json
import os
import sys

HEAVY_BUNDLED = {"bundled:update-config", "bundled:code-review", "update-config", "code-review"}
WORD_LIMIT = 500


def word_count(skill: str) -> int:
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(".claude", "skills", f"{skill}.md"),
        os.path.join(".claude", "skills", skill, "SKILL.md"),
        os.path.join(home, ".claude", "skills", f"{skill}.md"),
        os.path.join(home, ".claude", "skills", skill, "SKILL.md"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            with open(path, encoding="utf-8", errors="replace") as f:
                return len(f.read().split())
    return 0


def main() -> None:
    data = json.load(sys.stdin)
    skill = data.get("tool_input", {}).get("skill", "")
    if not skill:
        return

    words = 0
    blocked = skill in HEAVY_BUNDLED
    if not blocked:
        words = word_count(skill)
        blocked = words > WORD_LIMIT

    if blocked:
        reason = (
            f"'{skill}' is a known heavy bundled skill"
            if skill in HEAVY_BUNDLED
            else f"'{skill}' is {words} words (limit: {WORD_LIMIT})"
        )
        print(json.dumps({
            "continue": False,
            "stopReason": f"Skill {reason} — invoke via Agent tool to keep it out of main context.",
        }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
