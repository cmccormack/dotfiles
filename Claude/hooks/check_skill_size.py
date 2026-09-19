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
AGENT_BODY_LINES = 60
AGENT_DESC_WORDS = 25


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


def lint_agents(dirs: list[str]) -> int:
    """CLI mode (`--agents [dir ...]`): enforce the agents-plan budgets on agent files.

    Body (after the frontmatter) at most AGENT_BODY_LINES, description at most
    AGENT_DESC_WORDS. Exit 1 on any violation, so /git-commit can stop. Not fail-open:
    this path never runs inside a hook.
    """
    home = os.path.expanduser("~")
    dirs = dirs or [os.path.join(home, ".claude", "agents"), os.path.join(".claude", "agents")]
    bad = 0
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".md") or name == "README.md":
                continue
            path = os.path.join(d, name)
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.read().split("\n")
            if lines[:1] != ["---"] or "---" not in lines[1:]:
                print(f"{path}: no frontmatter"); bad += 1
                continue
            end = lines.index("---", 1)
            desc = next((l[len("description:"):].strip() for l in lines[1:end] if l.startswith("description:")), "")
            body = [l for l in lines[end + 1:] if l.strip()]
            if len(desc.split()) > AGENT_DESC_WORDS:
                print(f"{path}: description {len(desc.split())} words (limit {AGENT_DESC_WORDS})"); bad += 1
            if len(body) > AGENT_BODY_LINES:
                print(f"{path}: body {len(body)} lines (limit {AGENT_BODY_LINES})"); bad += 1
    print(f"agents lint: {'FAIL' if bad else 'ok'}")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--agents":
        sys.exit(lint_agents(sys.argv[2:]))
    try:
        main()
    except Exception:
        sys.exit(0)
