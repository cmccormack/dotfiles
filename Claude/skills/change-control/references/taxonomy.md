# Change Taxonomy

Classify BEFORE editing. When a change spans classes, apply the strictest gate that
matches any part of it.

## The four classes

| Class | Definition | Examples from this portfolio | Blast radius |
|---|---|---|---|
| 1. Docs-only | Markdown/text with no runtime effect | `README.md`, `CLAUDE.md`, `docs/**`, `.claude/research/*.md` | None until someone reads it wrong |
| 2. Repo code | Source, tests, scripts in a repo — inert until run/deployed | `~/Projects/macknet/src/**`, `~/Projects/bookshelf/setup_cwa.py`, `~/Projects/macknet/scripts/pi/*.sh` (editing, not running) | One repo, one machine |
| 3. Claude-config | Anything under `~/Projects/dotfiles/Claude/**` | `Claude/skills/*`, `Claude/settings.json`, `Claude/hooks/*`, `Claude/scripts/*`, `Claude/CLAUDE.md` | **Global, instant.** `~/.claude/skills` is a symlink to `dotfiles/Claude/skills` — a Write lands in every current and future Claude session with no deploy step |
| 4. Prod-touching | Executes against live infrastructure or hardware | Synology DS918+ (DSM, `docker-compose.nas.yml` deploys), UniFi controller/UDM writes, Pi fleet (`scripts/pi/*.sh chris@HOST`), PiKVM, Kobo (`kobo_set_server.py`), Steam Deck (`/ansible-run`), anything that deletes/flashes/reboots/overwrites a device | The home network, the family's data, or physical hardware |

Verify the symlink claim yourself: `ls -la ~/.claude/skills` → `-> /Users/chris/Projects/dotfiles/Claude/skills`.

## Classification procedure

1. Does the change execute against, or deploy to, a live host or device (NAS, UniFi gear,
   any Pi, Kobo, Deck)? → **Class 4**, even if the edit itself is one line of YAML.
2. Is any written path under `~/Projects/dotfiles/Claude/`? → **Class 3**.
3. Does it change behavior of code or scripts when they next run? → **Class 2**.
4. Otherwise → **Class 1**.

## Edge cases that get misclassified

| Change | Looks like | Actually is | Why |
|---|---|---|---|
| Edit `~/Projects/bookshelf/docker-compose.nas.yml` | Class 2 | Class 2 to edit, **Class 4 the moment it is deployed to the NAS** | The `.nas` compose split exists so testing happens locally first ([bookshelf/CLAUDE.md](~/Projects/bookshelf/CLAUDE.md): `main` = NAS-ready, `local-test` = local Docker first) |
| Edit `~/Projects/macknet/scripts/pi/harden-ssh.sh` | Class 2 | Class 2 — but **running** it against `chris@HOST` is Class 4 | A read-only-looking maintenance script still rewrites `sshd_config.d` on a live box |
| Write a new skill file in `dotfiles/Claude/skills/` | Class 1 (it's markdown) | **Class 3** | It is live in `~/.claude/skills` the instant the Write returns |
| API **reads** via macknet clients (`client.devices()`, DSM info calls) | Class 4 | Not a change at all — read-only queries are fine | Only writes/config pushes to the controller or DSM gate as Class 4 |
| `.claude/research/*.md`, `.claude/logs/` in any repo | Class 3 | Class 1 | Project-local artifacts, not the live global config |
| Reboot, reflash, factory-reset, `rm` on a device | Class 4 routine | Class 4 **destructive** | Requires explicit human go — see [gates.md](gates.md), taboo 3 |

## Provenance and maintenance
Date-stamped 2026-07-03 from live repo state. Re-verify: `ls -la ~/.claude/skills` (symlink);
`ls ~/Projects/macknet/scripts/pi/ ~/Projects/bookshelf/docker-compose.nas.yml` (paths still exist);
`grep -n "Branch Strategy" -A3 ~/Projects/bookshelf/CLAUDE.md` (compose/branch split still current).
