---
name: claude-config
description: Catalog of every configuration axis of this Claude Code setup. Load when changing settings.json, hooks, or permissions; adding a skill or tool; debugging why a hook or skill didn't fire; setting up Claude on a new machine or repo; or auditing session logs. Covers the ~/.claude symlink sync, session.jsonl logging, skill routing, git-commit scripts, web_fetch tool, memory system, and per-repo .claude/ conventions.
---

## Summary
Every config axis of this setup, with current values, status, safe-change checklists, and
re-verification commands. WARNING: this directory is symlinked live into `~/.claude/skills`
(via `dotfiles/Claude/skills`) — a config skill living inside the config it documents.
Edits here are global and instant; route all changes through the change-control skill.

## Routing

| Task | Read |
|---|---|
| Which ~/.claude entries are live symlinks; edit blast radius | [references/symlink-sync.md](references/symlink-sync.md) |
| settings.json keys: hooks, permissions, statusLine, model | [references/settings.md](references/settings.md) |
| session.jsonl format, where it lands, what consumes it | [references/session-logging.md](references/session-logging.md) |
| Add/fix a skill; flat vs SKILL.md format; size gate; heavy-skill rule | [references/skills-routing.md](references/skills-routing.md) |
| /git-commit helper scripts; web_fetch tool + tests | [references/scripts-and-tools.md](references/scripts-and-tools.md) |
| Memory: where it lives, compliance state, safe changes (schema → docs-house-style) | [references/memory-system.md](references/memory-system.md) |
| Per-repo .claude/ layout: research/ naming, logs/, settings.local.json | [references/per-repo-conventions.md](references/per-repo-conventions.md) |
| Add a new hook / skill / permission (checklists) | [references/add-axis-checklists.md](references/add-axis-checklists.md) |

## When NOT to use
- Campaigning to improve convention compliance → claude-discipline-campaign
- Measuring current state (log/token analysis) → diagnostics-toolkit
- The change procedure itself (approval, rollback) → change-control
