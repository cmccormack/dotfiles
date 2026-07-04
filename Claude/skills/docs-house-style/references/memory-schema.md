# Memory File Schema

Authoritative copy. Source rules: `~/.claude/CLAUDE.md` "Memory Budget"; formats observed
in `~/.claude/projects/*/memory/` (macknet, steamdeck, bookshelf, ubiquiti).

## File format

```markdown
---
name: <file stem, e.g. pi_fleet or feedback-heavy-skills>
description: "<one-line hook, quoted>"
metadata:
  type: project|feedback|reference|user
---

<body — max 15 lines total file budget>
```

- `metadata.type` is the ONLY metadata field. Strip `node_type` and `originSessionId`
  (auto-added by the memory system; `~/.claude/CLAUDE.md` orders their removal — legacy
  files still carry them, remove when touching a file).
- Filename prefix matches type: `project_*`, `feedback_*`, `reference_*`, `user_*`.
- **15-line budget** for the whole file, frontmatter included in practice — be brutal.

## Body rules
- **L1 decisions inline, one sentence:** "aiounifi rejected, use aiohttp" — never
  "see sdk_research.md". Supersede in place: "Decision 2026-07-02 (superseded 2026-07-03): ..."
  (live example: macknet `pi_fleet.md`).
- **`[[link]]`** wiki-links reference sibling memory files: `see [[project_context]]`.
- Prune anything derivable from the codebase (paths, function names, architecture).
  Keep only non-obvious decisions, rejected alternatives, and owner feedback.

## MEMORY.md index — 10 lines max

```markdown
# Memory Index

- [Pi Fleet](pi_fleet.md) — two Pis (.15 pi4, .145 pi5), patched+hardened, decommission decision open
- [SDK Research](sdk_research.md) — custom aiohttp client chosen; aiounifi and pyunifi rejected
```

One line per artifact: `- [Title](file.md) — one-phrase hook`. The hook must carry the
conclusion, not just the topic.

## Provenance and maintenance
Derived 2026-07-03 from `~/.claude/CLAUDE.md` (Memory Budget) and live files in
`~/.claude/projects/-Users-chris-Projects-{macknet,steamdeck}/memory/`. Re-verify:
`head -8 ~/.claude/projects/-Users-chris-Projects-macknet/memory/pi_fleet.md` and
`grep -A5 "Memory Budget" ~/.claude/CLAUDE.md`.
