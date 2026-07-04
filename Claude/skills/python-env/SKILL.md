---
name: python-env
description: Recreate any portfolio repo's Python environment from scratch, plus known traps. Load when setting up a repo's environment, hitting dependency errors or "module not found", uv/pyproject/uv.lock questions, wrong Python version, pytest or playwright missing, or bootstrapping a new machine (uv install + dotfiles restore).
---

## Summary
Every live Python repo (macknet, bookshelf, steamdeck, dotfiles) uses uv as the only
package manager: `uv sync` to create the env, `uv run <cmd>` to execute — never PATH
python (it is pyenv 3.12, repos pin 3.13/3.14). New machine: install uv, clone dotfiles,
`uv sync`, run `scripts/sync/sync.py` to restore symlinks. keylimepi has no Python env.

## Routing

| Need | Read |
|------|------|
| Per-repo pins, deps, dev groups, compose files | [references/stack.md](references/stack.md) |
| New-machine bootstrap, dotfiles sync + credential scanner | [references/bootstrap.md](references/bootstrap.md) |
| Symptom → cause → fix (lock drift, wrong python, missing pytest/chromium) | [references/traps.md](references/traps.md) |

## Policy
New external dependencies need Chris's approval; stdlib preferred. Rule lives in
`~/.claude/CLAUDE.md` (Code Style), echoed in macknet/steamdeck CLAUDE.md.

## When NOT to use
- Running or deploying services (compose up, NAS deploys, ansible-run) → homelab-operations
- Running or writing tests → validation-and-qa
- Edits under dotfiles/Claude (live global Claude config) → change-control first
- Scaffolding a brand-new repo → new-project-bootstrap
