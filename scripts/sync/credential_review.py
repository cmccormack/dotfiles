#!/usr/bin/env python3
"""Interactive TUI for reviewing and deleting credential findings before sync."""

import curses
import sys
from pathlib import Path

from check_credentials import Finding, scan_file

DELETED = "deleted"  # user deleted lines; caller should rescan
SKIPPED = "skipped"  # user chose to sync the file as-is
ABORTED = "aborted"  # user chose not to sync this file


def delete_lines(path: Path, line_numbers: set[int]) -> None:
    """Remove 1-indexed line numbers from a file in-place."""
    lines = path.read_text().splitlines(keepends=True)
    path.write_text("".join(ln for i, ln in enumerate(lines, 1) if i not in line_numbers))


def review(path: Path, hits: list[Finding]) -> str:
    """Launch TUI to review credential findings. Returns DELETED, SKIPPED, or ABORTED."""
    if not sys.stdout.isatty():
        # Non-interactive: print findings and block
        for line_num, label, line, match in hits:
            print(f"  {path}:{line_num} [{label}]: {line}", file=sys.stderr)
        return ABORTED

    result = curses.wrapper(_ui, path, hits)

    if result is None:
        return ABORTED
    if result == "skip":
        return SKIPPED

    delete_lines(path, set(result))
    return DELETED


def _ui(stdscr, path: Path, hits: list[Finding]) -> list[int] | str | None:
    """
    Curses checkbox UI.
    Returns list of 1-based line numbers to delete, 'skip', or None (abort).
    Controls: ↑↓/jk navigate · SPACE toggle · A select all · D delete · S skip · Q abort
    """
    curses.curs_set(0)
    curses.use_default_colors()
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_YELLOW, -1)  # header
        curses.init_pair(2, curses.COLOR_GREEN, -1)   # checked row
        curses.init_pair(3, curses.COLOR_RED, -1)     # warning label

    selected = [False] * len(hits)
    cursor = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        _safe_addstr(stdscr, 0, 0, f"Credentials found: {path}", curses.color_pair(1) | curses.A_BOLD, w)
        _safe_addstr(stdscr, 1, 0, "↑↓/jk navigate  SPACE toggle  A all  D delete selected  S skip  Q abort", 0, w)
        _safe_addstr(stdscr, 2, 0, "─" * min(w - 1, 80), 0, w)

        list_start = 3
        visible = h - list_start - 1
        scroll = max(0, cursor - visible + 1)

        for i, (line_num, label, line, _match) in enumerate(hits):
            if not scroll <= i < scroll + visible:
                continue
            y = list_start + i - scroll
            check = "[x]" if selected[i] else "[ ]"
            arrow = "▶ " if i == cursor else "  "
            text = f"{arrow}{check} :{line_num} [{label}]: {line}"
            attr = curses.A_REVERSE if i == cursor else 0
            if selected[i]:
                attr |= curses.color_pair(2)
            _safe_addstr(stdscr, y, 0, text, attr, w)

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")) and cursor > 0:
            cursor -= 1
        elif key in (curses.KEY_DOWN, ord("j")) and cursor < len(hits) - 1:
            cursor += 1
        elif key == ord(" "):
            selected[cursor] = not selected[cursor]
        elif key == ord("a"):
            val = not all(selected)
            selected = [val] * len(hits)
        elif key == ord("d"):
            # Delete selected, or current row if nothing selected
            to_delete = [hits[i][0] for i, s in enumerate(selected) if s]
            return to_delete or [hits[cursor][0]]
        elif key == ord("s"):
            return "skip"
        elif key in (ord("q"), 27):  # q or ESC
            return None


def _safe_addstr(stdscr, y: int, x: int, text: str, attr: int, width: int) -> None:
    try:
        stdscr.addstr(y, x, text[: width - 1], attr)
    except curses.error:
        pass
