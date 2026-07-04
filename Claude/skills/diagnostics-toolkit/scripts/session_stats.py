#!/usr/bin/env python3
"""Summarize a .claude/logs/session.jsonl hook log with counts and size metrics.

Known line shapes (from log-tool-use.sh / log-session-stop.sh hooks):
  {"ts", "event"}                       — session lifecycle (session_stop)
  {"ts", "session", "tool", "detail"}   — tool call; detail is {"cmd"}, {"file"},
                                          {"prompt"}, or null depending on tool
Unknown shapes are counted, never fatal.
"""

import argparse
import collections
import json
import sys
from pathlib import Path

TOP_N = 5


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--file",
        default="./.claude/logs/session.jsonl",
        help="session log path (default: ./.claude/logs/session.jsonl)",
    )
    args = ap.parse_args()

    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 2

    total = parsed = unparseable = unknown = 0
    events = collections.Counter()
    tools = collections.Counter()
    cmds = collections.Counter()
    reads = collections.Counter()
    writes = collections.Counter()
    sessions = set()
    first_ts = last_ts = None

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                unparseable += 1
                continue
            parsed += 1
            ts = o.get("ts")
            if ts:
                first_ts = first_ts or ts
                last_ts = ts
            if "event" in o:
                events[o["event"]] += 1
            elif "tool" in o:
                tools[o["tool"]] += 1
                sessions.add(o.get("session"))
                d = o.get("detail") or {}
                if "cmd" in d:
                    cmds[d["cmd"]] += 1
                elif "file" in d:
                    (reads if o["tool"] == "Read" else writes)[d["file"]] += 1
            else:
                unknown += 1

    size = path.stat().st_size
    print(f"Log: {path}")
    print(f"Size: {size:,} bytes (~{size // 4:,} tokens if read whole)")
    print(f"Lines: {total} total, {parsed} parsed, {unparseable} unparseable, {unknown} unknown shape")
    if first_ts:
        print(f"Span: {first_ts} .. {last_ts}")
    print(f"Sessions: {len(sessions)} unique ids, events: {dict(events) or 'none'}")

    n_tool = sum(tools.values())
    print(f"\nTool calls ({n_tool} total):")
    for tool, n in tools.most_common():
        print(f"  {tool:<10} {n:>5}  {n / n_tool:5.1%}")

    if cmds:
        print(f"\nTop {TOP_N} Bash commands:")
        for cmd, n in cmds.most_common(TOP_N):
            print(f"  {n:>4}x  {cmd[:90]}")

    rereads = [(f_, n) for f_, n in reads.most_common() if n > 1]
    if reads:
        print(f"\nReads: {sum(reads.values())} across {len(reads)} files; "
              f"{len(rereads)} files read more than once")
        for f_, n in rereads[:TOP_N]:
            print(f"  {n:>4}x  {f_}")
    if writes:
        print(f"Writes/Edits: {sum(writes.values())} across {len(writes)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
