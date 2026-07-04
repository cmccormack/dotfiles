# Per-repo .claude/ conventions

Presence of `<repo>/.claude/` is the opt-in switch for session logging (see
session-logging.md). Observed layout across macknet, bookshelf, keylimepi, steamdeck:

| Entry | Convention | Status |
|---|---|---|
| `logs/session.jsonl` | Written by global hooks; present in all four repos | production |
| `research/` | Agent output files (naming below); macknet 7, steamdeck ~18, bookshelf 3 | production |
| `settings.local.json` | Machine/user-local permission grants, gitignored by Claude Code; narrow rules only (e.g. keylimepi allows exactly `Bash(chmod +x /Users/chris/Projects/keylimepi/setup.sh)`) | production |
| `settings.json` | Checked-in project settings — macknet (permissions + skill-size hook), steamdeck. Remember: **agents inherit only global settings**, so agent-facing permissions go in dotfiles/Claude/settings.json, not here | production |
| `skills/`, `commands/`, `hooks/` | Project skills (≤30-line gate), slash commands (macknet `/devices`), project hooks (macknet `check_skill_size.py`) | production |
| `cache/` | steamdeck only: `<slug>.json` structured lookup cache, checked before re-running expensive research | experimental (one repo) |
| `docs/` | steamdeck only: `.claude/docs/ansible-standards.md` | experimental (one repo) |
| `worktrees/` | steamdeck has a stale committed agent worktree — anti-pattern, should be gitignored | drift |

## research/ naming
Full contract (name format, token mint, first-line rule, what belongs in a research
file) lives in ONE place: `docs-house-style/references/research-files.md`. Scaffold
compliant files with `diagnostics-toolkit/scripts/research_scaffold.py`.

## Setting up a new repo
```bash
mkdir -p .claude/logs .claude/research
```
That alone enables logging and gives agents a research target. Add `settings.local.json`
only when a permission prompt actually recurs; add `settings.json` only for conventions the
whole repo should share.

## Provenance and maintenance
Verified 2026-07-03 by listing `.claude/` in macknet, bookshelf, keylimepi, steamdeck and
reading macknet/.claude/settings.json + keylimepi/.claude/settings.local.json. Re-verify:
`ls /Users/chris/Projects/{macknet,bookshelf,keylimepi,steamdeck}/.claude/`.
