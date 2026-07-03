#!/usr/bin/env python3
"""Scan files for likely credentials before they enter the repo."""

import re
import sys
from pathlib import Path

# (regex, human-readable label)
PATTERNS: list[tuple[str, str]] = [
    (r'(?i)(password|passwd|secret|api[_-]?key|auth[_-]?token|access[_-]?token|private[_-]?key)\s*[=:]\s*(?![${\\])[^\s\'"]{6,}',
     "credential assignment"),
    (r'AKIA[0-9A-Z]{16}',                                    "AWS access key ID"),
    (r'(?i)aws_secret_access_key\s*=\s*[A-Za-z0-9+/]{40}',  "AWS secret key"),
    (r'(ghp_|gho_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{20,}', "GitHub token"),
    (r'Bearer\s+[A-Za-z0-9+/=_-]{20,}',                     "Bearer token"),
    (r'[a-zA-Z][a-zA-Z0-9+.-]*://[^/:@\s]+:[^/@\s]{4,}@',   "credential in URL"),
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----', "PEM private key"),
    (r'xox[baprs]-[A-Za-z0-9-]+',                            "Slack token"),
    (r'(sk|pk)_(live|test)_[A-Za-z0-9]{20,}',               "Stripe key"),
    (r'(?i)(token|key|secret)\s*=\s*[A-Fa-f0-9]{32,}',      "hex credential assignment"),
]

_COMPILED = [(re.compile(p), label) for p, label in PATTERNS]

_RED_BOLD = "\033[1;31m"
_RESET    = "\033[0m"

# (line_number, label, line_text, matched_text)
Finding = tuple[int, str, str, str]


def scan_file(path: Path) -> list[Finding]:
    """Return one finding per line that matches any credential pattern."""
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return []

    findings = []
    for i, line in enumerate(lines, 1):
        for pattern, label in _COMPILED:
            m = pattern.search(line)
            if m:
                findings.append((i, label, line.strip(), m.group(0)))
                break  # one report per line
    return findings


def highlight(line: str, match: str) -> str:
    """Wrap the first occurrence of match in red bold ANSI."""
    return line.replace(match, f"{_RED_BOLD}{match}{_RESET}", 1)


def scan(target: Path) -> dict[Path, list[Finding]]:
    """Scan a file or directory tree. Returns {path: [findings]}."""
    paths = sorted(target.rglob("*")) if target.is_dir() else [target]
    return {p: hits for p in paths if p.is_file() and (hits := scan_file(p))}


def filter_file(path: Path) -> list[Finding]:
    """Remove lines matching any credential pattern from path in-place. Returns removed findings."""
    hits = scan_file(path)
    if not hits:
        return []
    bad_lines = {line_num for line_num, *_ in hits}
    lines = path.read_text(errors="replace").splitlines(keepends=True)
    path.write_text("".join(ln for i, ln in enumerate(lines, 1) if i not in bad_lines))
    return hits


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scan files for credentials.")
    parser.add_argument("paths", nargs="+", metavar="path")
    parser.add_argument(
        "--filter",
        action="store_true",
        help="Remove flagged lines in-place instead of just reporting.",
    )
    args = parser.parse_args()

    found = False
    for arg in args.paths:
        target = Path(arg)
        results = scan(target)
        for path, hits in results.items():
            found = True
            if args.filter:
                removed = filter_file(path)
                print(f"FILTERED {len(removed)} line(s) from {path}:")
                for line_num, label, line, match in removed:
                    print(f"  line {line_num} [{label}]: {highlight(line, match)}")
            else:
                print(f"CREDENTIAL WARNING: {path}")
                for line_num, label, line, match in hits:
                    print(f"  line {line_num} [{label}]: {highlight(line, match)}")

    sys.exit(1 if found else 0)
