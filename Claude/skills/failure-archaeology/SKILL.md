---
name: failure-archaeology
description: Chronicle of settled battles across the portfolio (macknet, bookshelf, keylimepi, steamdeck, dotfiles) so nobody re-fights them. Load when about to re-investigate an old problem (Kobo sync reverting, GOG Galaxy failures, NW.js/overlay issues, Pi patching surprises); wondering why something was done a weird way (macknet.unifi namespace, NW.js pinned to v0.76.1, no fail2ban); considering reverting or redoing an approach; or when you find a dead branch, stale worktree, or stalled/abandoned work.
---

## Summary
Settled failures, rejected alternatives, and their evidence for all 5 live repos, plus a durable recipe for excavating git/research history yourself. Check the chronicle BEFORE re-investigating anything that smells historical — steamdeck's investigation log even keeps an explicit "DO NOT REPEAT" list. Never fabricate a root cause; cite hashes only after `git show`.

## Routing

| Need | Read |
|---|---|
| Did we already fight this? Per-repo findings + cross-portfolio patterns | [references/chronicle.md](references/chronicle.md) |
| Excavate history yourself (chronicle may be stale) | [references/excavation-recipe.md](references/excavation-recipe.md) |
| Deepest single record: GOG Galaxy / EnableLUA saga | [~/Projects/steamdeck/docs/games/demons-roots/investigation.md](~/Projects/steamdeck/docs/games/demons-roots/investigation.md) |

Key settled calls: NW.js v0.76.1 active (overlay), v0.88+ regression; Kobo `api_endpoint` never `domain:port`; fail2ban rejected on LAN Pis; macknet critic overruled on restructure; no revert commits anywhere — mine removals and `.claude/research/`.

## When NOT to use
- Something is broken right now → debugging-playbook.
- How the system is built today → homelab-architecture.
- Changing/reverting code going forward → change-control.
