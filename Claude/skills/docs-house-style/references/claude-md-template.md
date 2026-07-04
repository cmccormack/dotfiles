# Per-Repo CLAUDE.md Template

Mined from the four live examples: macknet (commands/architecture/env/testing), bookshelf
(infra, branch strategy, gotchas), steamdeck (stack/status, Claude patterns, skills list),
dotfiles (layout table, tool commands).

## What goes where

| Content | Home |
|---|---|
| Setup, usage, troubleshooting for humans | README |
| Context rules for Claude: commands, architecture invariants, gotchas, agent permissions, testing patterns | CLAUDE.md |
| Invocable procedures and doc routing | Skill (`.claude/skills/` or this library) |
| Non-obvious decisions, rejected alternatives (budgeted) | Memory files |
| Full findings from agent investigations | `.claude/research/` |

Link, never repeat: bookshelf README points at NAS_SETUP.md and CLAUDE.md rather than
duplicating either. CLAUDE.md is not a tutorial — no screenshots, no step-by-step builds.

## Template (copy-paste; delete sections that don't apply)

```markdown
# <Project Name>

[View on GitHub](https://github.com/cmccormack/<repo>)

<1–3 sentences: what this repo is. Early projects state maturity, like steamdeck's
"## Status — Early/exploratory, no fixed architecture yet.">

## Stack
- <language/runtime, key deps, target platform — bullet list (steamdeck)>

## Docs
Load [docs/INDEX.md](docs/INDEX.md) first; read individual files only as needed. <!-- if docs/ exists -->

## Commands
```sh
uv run pytest tests/ -m "not integration"
uv run python <entrypoint> --dry-run
```

## Architecture
<Only the non-obvious: package layout, signature patterns (macknet's async aiohttp
context-manager clients), where scripts vs modules live (steamdeck's Conventions).>

## Environment
- `.env` from `.env.example`; never commit `.env`.

## Testing pattern
<How tests are structured and any fixture gotchas — macknet's integration-marked,
session-scoped login fixture to dodge rate limits.>

## Claude Patterns            <!-- only if repo-specific: steamdeck's cache schema,
                                   agent-permission notes -->

## Skills
- `/name` — one-line purpose (steamdeck lists its three)

## Gotchas
<Platform landmines, one bullet each — bookshelf's docker-compose v1 / Btrfs /
synoshare notes.>
```

## Provenance and maintenance
Derived 2026-07-03 from CLAUDE.md in macknet, bookshelf, steamdeck, dotfiles and
`~/.claude/CLAUDE.md`. Re-verify: `head -20 ~/Projects/{macknet,bookshelf,steamdeck,dotfiles}/CLAUDE.md`.
