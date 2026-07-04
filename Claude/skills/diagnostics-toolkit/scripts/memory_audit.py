#!/usr/bin/env python3
"""Audit Claude memory dirs against the CLAUDE.md memory budget.

Scans <root>/*/memory/ (default root: ~/.claude/projects):
  - MEMORY.md <= 10 lines total
  - other .md files: body (non-frontmatter) <= 15 lines
  - forbidden YAML fields: top-level keys other than name/description/metadata,
    metadata keys other than type/node_type/originSessionId (the latter two are
    harness-managed, grandfathered 2026-07-04 — the memory daemon re-injects them)
  - dangling [[wiki]] links and relative (file.md) links

Exit 0 clean, 1 on any violation, 2 on bad root.
"""

import argparse
import re
import sys
from pathlib import Path

INDEX_MAX = 10
BODY_MAX = 15
ALLOWED_TOP = {"name", "description", "metadata"}
ALLOWED_META = {"type", "node_type", "originSessionId"}  # latter two harness-managed, grandfathered 2026-07-04


def split_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1 :]
    return None, lines


def forbidden_fields(fm_lines):
    bad = []
    in_metadata = False
    for ln in fm_lines:
        if not ln.strip():
            continue
        if not ln.startswith((" ", "\t")):
            m = re.match(r"([A-Za-z_][\w-]*)\s*:", ln)
            if m:
                key = m.group(1)
                in_metadata = key == "metadata"
                if key not in ALLOWED_TOP:
                    bad.append(key)
        elif in_metadata:
            m = re.match(r"\s+([A-Za-z_][\w-]*)\s*:", ln)
            if m and m.group(1) not in ALLOWED_META:
                bad.append(f"metadata.{m.group(1)}")
    return bad


def dangling_links(text, mem_dir):
    bad = []
    for target in re.findall(r"\[\[([^\]|#]+)", text):
        t = target.strip()
        if not ((mem_dir / t).exists() or (mem_dir / f"{t}.md").exists()):
            bad.append(f"[[{t}]]")
    for target in re.findall(r"\]\(([^)#:]+\.md)\)", text):
        if not (mem_dir / target).exists():
            bad.append(f"({target})")
    return bad


def audit_file(path, mem_dir):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues = []

    if path.name == "MEMORY.md":
        n = len(lines)
        if n > INDEX_MAX:
            issues.append(f"index {n}>{INDEX_MAX}")
    else:
        fm_lines, body = split_frontmatter(lines)
        while body and not body[-1].strip():
            body.pop()
        while body and not body[0].strip():
            body.pop(0)
        n = len(body)
        if n > BODY_MAX:
            issues.append(f"body {n}>{BODY_MAX}")
        if fm_lines is not None:
            bad = forbidden_fields(fm_lines)
            if bad:
                issues.append("forbidden: " + ",".join(bad))

    dl = dangling_links(text, mem_dir)
    if dl:
        issues.append("dangling: " + ",".join(dl))
    return n, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--root",
        default=str(Path.home() / ".claude" / "projects"),
        help="projects directory containing */memory/ (default: ~/.claude/projects)",
    )
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    rows = []
    violations = 0
    for mem_dir in sorted(root.glob("*/memory")):
        project = mem_dir.parent.name
        for path in sorted(mem_dir.glob("*.md")):
            n, issues = audit_file(path, mem_dir)
            if issues:
                violations += 1
            rows.append((project, path.name, str(n), "; ".join(issues) or "ok"))

    if not rows:
        print(f"no memory files found under {root}/*/memory")
        return 0

    header = ("PROJECT", "FILE", "LINES", "ISSUES")
    widths = [max(len(r[i]) for r in rows + [header]) for i in range(4)]
    for r in [header] + rows:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(r)))
    print(f"\n{len(rows)} files, {violations} with violations "
          f"(budget: MEMORY.md<={INDEX_MAX}, body<={BODY_MAX}, YAML only name/description/metadata.type)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
