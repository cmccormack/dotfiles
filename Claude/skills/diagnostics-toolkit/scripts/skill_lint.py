#!/usr/bin/env python3
"""Audit Claude skills against the CLAUDE.md skill size gate.

Checks both flat <root>/*.md skills and <root>/*/SKILL.md skills:
  - body (non-frontmatter) line count vs the 30-line gate
  - ## Summary header present, section content <= 5 lines
  - SKILL.md-style: YAML frontmatter with name + description required
  - description trigger quality: nonempty, mentions "when" or "use"

Exit 0 clean, 1 on any violation, 2 on bad root.
"""

import argparse
import re
import sys
from pathlib import Path

BODY_MAX = 30
SUMMARY_MAX = 5


def split_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1 :]
    return None, lines


def parse_frontmatter(fm_lines):
    fields = {}
    key = None
    for ln in fm_lines:
        m = re.match(r"([A-Za-z_][\w-]*)\s*:\s*(.*)", ln)
        if m and not ln.startswith((" ", "\t")):
            key = m.group(1)
            val = m.group(2).strip().strip("\"'")
            fields[key] = "" if val in (">", ">-", "|", "|-") else val
        elif key is not None and ln.startswith((" ", "\t")) and ln.strip():
            fields[key] = (fields[key] + " " + ln.strip()).strip()
    return fields


def summary_section(body):
    start = None
    for i, ln in enumerate(body):
        if re.match(r"##\s+Summary\s*$", ln.strip()):
            start = i + 1
            break
    if start is None:
        return None
    section = []
    for ln in body[start:]:
        if ln.strip().startswith("#"):
            break
        if ln.strip():
            section.append(ln)
    return section


def audit(path, is_skill_md):
    lines = path.read_text(encoding="utf-8").splitlines()
    fm_lines, body = split_frontmatter(lines)
    while body and not body[-1].strip():
        body.pop()
    while body and not body[0].strip():
        body.pop(0)
    issues = []

    body_n = len(body)
    if body_n > BODY_MAX:
        issues.append(f"body {body_n}>{BODY_MAX}")

    summary = summary_section(body)
    if summary is None:
        issues.append("no ## Summary")
        summary_disp = "missing"
    else:
        summary_disp = str(len(summary))
        if len(summary) > SUMMARY_MAX:
            issues.append(f"summary {len(summary)}>{SUMMARY_MAX}")

    desc = None
    if fm_lines is not None:
        fields = parse_frontmatter(fm_lines)
        desc = fields.get("description")
        if is_skill_md and not fields.get("name"):
            issues.append("frontmatter missing name")
        if is_skill_md and not desc:
            issues.append("frontmatter missing description")
    elif is_skill_md:
        issues.append("no frontmatter")

    if desc is not None:
        if not desc:
            issues.append("empty description")
        elif not re.search(r"\b(when|use)\b", desc, re.IGNORECASE):
            issues.append("description lacks when/use trigger")
        desc_disp = "ok" if not any("description" in i for i in issues) else "weak"
    else:
        desc_disp = "-"

    return body_n, summary_disp, desc_disp, issues


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--root",
        default=str(Path.home() / ".claude" / "skills"),
        help="skills directory (default: ~/.claude/skills)",
    )
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    targets = []
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix == ".md":
            targets.append((p, False))
        elif p.is_dir() and (p / "SKILL.md").is_file():
            targets.append((p / "SKILL.md", True))

    if not targets:
        print(f"no skills found under {root}")
        return 0

    rows = []
    violations = 0
    for path, is_skill_md in targets:
        name = str(path.relative_to(root))
        body_n, summary_disp, desc_disp, issues = audit(path, is_skill_md)
        if issues:
            violations += 1
        rows.append((name, str(body_n), summary_disp, desc_disp, "; ".join(issues) or "ok"))

    widths = [max(len(r[i]) for r in rows + [("SKILL", "BODY", "SUMMARY", "DESC", "ISSUES")]) for i in range(5)]
    header = ("SKILL", "BODY", "SUMMARY", "DESC", "ISSUES")
    for r in [header] + rows:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(r)))
    print(f"\n{len(rows)} skills, {violations} with violations (gate: body<={BODY_MAX}, summary<={SUMMARY_MAX})")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
