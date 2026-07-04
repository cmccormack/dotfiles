# Invariants

Things that must stay true. Breaking one breaks a running system or a live session.
Any change touching these routes through `change-control` first.

## Live global config
- `~/.claude/{CLAUDE.md,settings.json,skills,hooks,scripts,history.jsonl}` are symlinks
  into `~/Projects/dotfiles/Claude/`. **Edits to that repo subtree take effect in every
  Claude session immediately, mid-write included.** There is no staging copy.
- Subagents inherit ONLY the global dotfiles settings.json, not project settings
  (steamdeck CLAUDE.md). Removing a global permission silently breaks agents in every repo.

## NAS paths services depend on
The running CWA container ("cwa-library") bind-mounts these exact paths
(`bookshelf/docker-compose.nas.yml`); renaming or moving them breaks ingest and Kobo sync:
- `/volume1/docker/cwa-library/config` — CWA config + `app.db`
- `/volume1/calibre/library` — Calibre library (metadata.db + EPUBs)
- `/volume1/calibre/ingest` — watched ingest folder
- `/volume1/docker/cwa-library/bookshelf` — cloned repo on the NAS (compose files)
Also: `/etc/ssh/sshd_config` on the NAS is overwritten by every DSM update — any
hardening must be persisted via a Task Scheduler boot script, not edited in place.

## API client contracts (macknet)
- Both clients are async context managers; the aiohttp session exists only inside
  `async with`. Never call methods on an unentered client.
- UniFi: login (`POST /api/auth/login`) sets a cookie and returns `x-csrf-token`, which
  every later request must echo; `_get/_post` unwrap `body["data"]`. The cookie jar uses
  `unsafe=True` because the controller is addressed by IP.
- DSM: no static tokens exist — every run logs in via `SYNO.API.Auth` v6 and must echo
  `_sid` (form field) + `X-SYNO-TOKEN` (header) on each `entry.cgi` call; `success:false`
  raises `NasError` with the DSM error code.
- Integration tests share ONE client session via a session-scoped fixture — the controller
  rate-limits logins (HTTP 429). Don't "fix" tests by giving each its own client.

## Secrets and real-world data
- `.env` is never committed; `.env.example` is the template (every deployable repo).
- `macknet/docs/raspberry-pi/fleet.local.md` is gitignored real inventory (IPs, MACs,
  history). `inventory/network.yaml` also contains real MACs/hostnames — treat as sensitive.
- Kobo sync URLs embed the per-install token (`/kobo/<token>`); the token is invalidated
  by a fresh CWA deploy and must be regenerated, then re-written to the device.

## Operational taboos (user-confirmed 2026-07-03)
- No production-NAS changes without a rollback point.
- No untested changes to the live network (UniFi config).
- No unattended destructive device operations (flash/wipe/reboot without a human watching).

## Provenance and maintenance
Compiled 2026-07-03 from macknet CLAUDE.md + client code, bookshelf compose/CLAUDE.md,
steamdeck CLAUDE.md, dotfiles manifest. Re-verify:
- `readlink ~/.claude/skills ~/.claude/settings.json`
- `grep -n "volume1" ~/Projects/bookshelf/docker-compose.nas.yml`
- `grep -n "x-csrf-token" ~/Projects/macknet/src/macknet/unifi/client.py`
- `grep -n "session-scoped\|429" ~/Projects/macknet/CLAUDE.md ~/Projects/macknet/tests/integration/conftest.py`
