#!/usr/bin/env python3
"""Sync dotfiles into this repo via symlinks.

First run: moves the real file into the repo, replaces it with a symlink.
Subsequent runs: verifies symlinks are correct; no-ops if already linked.
"""

import argparse
from pathlib import Path

from check_credentials import scan as _cred_scan_impl
from credential_review import review, DELETED, SKIPPED

REPO_ROOT = Path(__file__).parent.parent.parent
MANIFEST = Path(__file__).parent / "manifest.conf"

_SRC_WIDTH   = 28  # left column padding
_REPO_PREFIX = f"./{REPO_ROOT.name}/"
_PATH_STATES = {"ok", "link", "move"}  # states whose dest is a repo path, not a message

_WHITE = "\033[97m"            # files
_CYAN  = "\033[96m"            # directories
_GREEN   = "\033[92m"
_YELLOW  = "\033[93m"
_RED     = "\033[91m"
_DIM     = "\033[2m"
_RESET   = "\033[0m"

# state → (color, emoji)
_GOLD = "\033[38;5;220m"  # gold — link emoji

_STATES = {
    "ok":      (_GOLD,   "🔗"),
    "link":    (_GOLD,   "🔗"),
    "move":    (_GOLD,   "🔗"),
    "skip":    (_DIM,    "·  "),   # pad to match emoji width
    "blocked": (_RED,    "⛓️‍💥"),
    "warn":    (_YELLOW, "⚠️ "),
}


def _row(state: str, src: str, dest: str = "", *, is_dir: bool = False) -> None:
    sym_color, symbol = _STATES.get(state, ("", "?"))
    path_color = _CYAN if is_dir else _WHITE
    icon       = "📁" if is_dir else "📄"
    dest_str   = (dest + "/") if is_dir and dest else dest
    src_col    = f"{path_color}{icon} {src:<{_SRC_WIDTH}}{_RESET}"
    if state in _PATH_STATES and dest_str:
        dest_col = f"{path_color}{_REPO_PREFIX}{dest_str}{_RESET}"
    else:
        dest_col = dest_str
    print(f"  {src_col}  {sym_color}{symbol}{_RESET}  {dest_col}")


def _cred_scan(path: Path) -> bool:
    """Launch credential review TUI if findings exist. Returns True if safe to sync."""
    results = _cred_scan_impl(path)
    if not results:
        return True

    all_hits = [hit for hits in results.values() for hit in hits]
    action = review(path, all_hits)

    if action == SKIPPED:
        _row("warn", str(path), "syncing with credentials (user override)")
        return True
    if action == DELETED:
        if _cred_scan_impl(path):
            _row("blocked", str(path), "credentials remain after deletion")
            return False
        return True

    _row("blocked", str(path), "credentials found  --skip-cred-check to override")
    return False


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    """Parse manifest into (src_raw, dest_rel) pairs, skipping comments and blanks."""
    entries = []
    for i, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            _row("warn", f"manifest:{i}", f"malformed entry (no colon): {line}")
            continue
        src, dest = line.split(":", 1)
        entries.append((src.strip(), dest.strip()))
    return entries


def link_entry(
    src_raw: str,
    dest_rel: str,
    *,
    dry_run: bool,
    skip_cred_check: bool,
    repo_root: Path = REPO_ROOT,
) -> str:
    """Process one manifest entry. Returns the action taken as a string."""
    src = Path(src_raw.replace("~", str(Path.home()), 1))
    dest = repo_root / dest_rel

    if src.is_symlink() and src.resolve() == dest.resolve():
        _row("ok", src_raw, dest_rel, is_dir=src.is_dir())
        return "ok"

    if src.is_symlink():
        _row("warn", src_raw, f"points to {src.readlink()} — skipping")
        return "warn"

    if dry_run:
        _row("link", src_raw, dest_rel, is_dir=dest.is_dir() or src.is_dir())
        return "dry-link"

    dest.parent.mkdir(parents=True, exist_ok=True)

    if src.exists():
        if not skip_cred_check and not _cred_scan(src):
            return "blocked"
        _row("move", src_raw, dest_rel, is_dir=src.is_dir())
        src.rename(dest)

    if dest.exists():
        src.symlink_to(dest)
        _row("link", src_raw, dest_rel, is_dir=dest.is_dir())
        return "linked"

    _row("skip", src_raw, "not found")
    return "skip"


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync dotfiles into repo via symlinks.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-cred-check", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("Dry run — no changes will be made\n")

    for src, dest in parse_manifest(MANIFEST):
        link_entry(src, dest, dry_run=args.dry_run, skip_cred_check=args.skip_cred_check)


if __name__ == "__main__":
    main()
