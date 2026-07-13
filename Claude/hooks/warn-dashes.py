#!/usr/bin/env python3
"""Warn when Write/Edit puts em/en dashes into prose files (user CLAUDE.md rule).

Warning-only by design: the rule has a judgment exception (verbatim quotes),
so this never blocks. Prose files only; code and vendored paths stay silent.
"""
import json
import sys

PROSE_EXT = (".md", ".html", ".txt")
SKIP_DIRS = ("/vendor/", "/node_modules/", "/site-packages/")
DASHES = "—–"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not path.lower().endswith(PROSE_EXT) or any(s in path for s in SKIP_DIRS):
        return 0
    text = tool_input.get("content") or tool_input.get("new_string") or ""
    count = sum(text.count(d) for d in DASHES)
    if count:
        print(
            f"warn-dashes: {count} em/en dash(es) written to {path}. "
            "User CLAUDE.md rule: restructure the sentence instead "
            "(comma, colon, parentheses); dashes only where required verbatim.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
