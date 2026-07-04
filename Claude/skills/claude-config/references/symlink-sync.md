# The ~/.claude ↔ dotfiles symlink sync

Global Claude config lives in the dotfiles repo at `~/Projects/dotfiles/Claude/` and is
symlinked into `~/.claude`. The sync tool is `dotfiles/scripts/sync/sync.py`, driven by
`dotfiles/scripts/sync/manifest.conf` (format: `~/src:repo/dest`; it moves the file into
the repo and symlinks back).

## Current symlinks (verified)

| ~/.claude entry | Target in dotfiles/Claude/ | In manifest.conf? |
|---|---|---|
| `CLAUDE.md` | `Claude/CLAUDE.md` | yes |
| `settings.json` | `Claude/settings.json` | yes |
| `hooks/` | `Claude/hooks` | yes |
| `skills/` | `Claude/skills` | yes |
| `scripts/` | `Claude/scripts` | yes |
| `history.jsonl` | `Claude/history.jsonl` | yes |
| `tools/` | `Claude/tools` | **no — manual symlink, manifest drift** |

Everything else in `~/.claude` (`projects/`, `statusline/`, `logs/`, `plugins/`, caches,
session state) is machine-local and NOT in the repo. Note `statusline/statusline.sh` is
referenced by settings.json but not synced — a fresh machine needs it created separately.

## The consequence

Edits under `dotfiles/Claude/` are **live globally, instantly** — every running and future
Claude session on this machine sees them the moment the file is saved. There is no staging
step; git history is the only rollback. Therefore:

1. Route every change through the change-control skill (state intent, get approval).
2. Edit the `dotfiles/Claude/` path, not the `~/.claude` path — same inode, but keeps you
   aware you are editing a repo.
3. Commit promptly via `/git-commit` so the live state and repo HEAD do not diverge.
4. Adding a NEW file under a symlinked dir (e.g. a new skill) is also instantly live.

Status: production. The unmanaged `tools` symlink and unsynced `statusline/` are known drift.

## Provenance and maintenance
Verified 2026-07-03 against live filesystem. Re-verify: `ls -la ~/.claude | grep -- '->'`
and `grep claude ~/Projects/dotfiles/scripts/sync/manifest.conf`.
