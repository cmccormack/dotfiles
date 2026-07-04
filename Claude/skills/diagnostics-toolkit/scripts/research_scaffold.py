#!/usr/bin/env python3
"""Mint a research file per the agent-output convention, or validate existing ones.

Create mode: research_scaffold.py <topic> [--dir DIR]
  Generates a 6-hex token via os.urandom(3).hex(), writes
  DIR/YYYY-MM-DD-<topic-slug>-<token>.md with first line `agent-token: <token>`,
  prints the path and token.

Check mode: research_scaffold.py --check [--dir DIR]
  Validates every *.md in DIR: filename matches YYYY-MM-DD-<topic>-<6hex>.md
  and first line is `agent-token: <token>` matching the filename token.
  Exit 0 clean, 1 on violations.
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)-([0-9a-f]{6})\.md$")


def slugify(topic):
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    if not slug:
        raise SystemExit("error: topic slug is empty")
    return slug


def create(topic, directory):
    directory.mkdir(parents=True, exist_ok=True)
    token = os.urandom(3).hex()
    date = datetime.date.today().isoformat()
    path = directory / f"{date}-{slugify(topic)}-{token}.md"
    path.write_text(f"agent-token: {token}\n\n# {topic} — {date}\n", encoding="utf-8")
    print(f"path: {path}")
    print(f"token: {token}")
    return 0


def check(directory):
    if not directory.is_dir():
        print(f"error: not a directory: {directory}", file=sys.stderr)
        return 2
    violations = 0
    files = sorted(directory.glob("*.md"))
    for path in files:
        issues = []
        m = NAME_RE.match(path.name)
        if not m:
            issues.append("bad filename (want YYYY-MM-DD-topic-6hex.md)")
        with path.open(encoding="utf-8") as f:
            first = f.readline().rstrip("\n")
        fm = re.match(r"agent-token: ([0-9a-f]{6})$", first)
        if not fm:
            issues.append(f"bad first line: {first[:50]!r}")
        elif m and fm.group(1) != m.group(2):
            issues.append(f"token mismatch: file {m.group(2)} vs line {fm.group(1)}")
        status = "; ".join(issues) or "ok"
        if issues:
            violations += 1
        print(f"{path.name}: {status}")
    print(f"\n{len(files)} files, {violations} with violations")
    return 1 if violations else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("topic", nargs="?", help="research topic (slugified into the filename)")
    ap.add_argument(
        "--dir",
        default="./.claude/research",
        help="research directory (default: ./.claude/research)",
    )
    ap.add_argument("--check", action="store_true", help="validate existing files instead of creating")
    args = ap.parse_args()

    directory = Path(args.dir).expanduser()
    if args.check:
        return check(directory)
    if not args.topic:
        ap.error("topic is required unless --check")
    return create(args.topic, directory)


if __name__ == "__main__":
    sys.exit(main())
