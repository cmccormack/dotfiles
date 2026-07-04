# steamdeck — Deck toolkit: deck-query, helper scripts, Ansible

Repo: `~/Projects/steamdeck`. Python (uv) + bash + Ansible tooling for the Steam
Deck at `deck@192.168.1.30` (key-based SSH). Focus: GOG Galaxy diagnostics and
Deck maintenance. Config first: copy `config.ini.example` -> `config.ini` (keys:
`host`, `galaxy_log_dir`, `galaxy_db_path`, `local_cache_dir`, `ssh_timeout`).

## deck-query CLI (read-only diagnostics)

```bash
uv run python deck-query.py [--host deck@IP] [--json] <command>
```

| Command | Anatomy |
|---|---|
| `logs list [--cache]` | Galaxy log files with size/mtime |
| `logs grep PATTERN [--files F...] [--level L] [--since ISO] [--until ISO] [--cache]` | search log entries |
| `logs tail FILE [N] [--raw] [--cache]` | last N (default 100) entries of one log |
| `logs sessions [--cache]` | GalaxyClientService session analysis (ms-to-listen/client, stop reason) |
| `sync` | pull all logs + DB into the local cache for offline work |
| `db fetch` | scp `galaxy-2.0.db` locally, prints path |
| `db tables/query SQL/install-state [PID]/game-times [PID]/cloud-saves [PID] --db PATH` | SQLite queries (`--db` required except `tables`) |

`--cache` reads from `local_cache_dir` (`.cache/host/`, gitignored) instead of SSHing
to the Deck — run `sync` first, then work offline.

## Helper scripts (`scripts/`)

- `fetch-remote.sh <profile> [host]` — targeted pulls into `.cache/host/` with a
  sync manifest. Profiles: `galaxy-logs`, `galaxy-db`, `galaxy-crashes` (.dmp files
  <1 h old), `galaxy-all`, `steam-config` (shortcuts.vdf, localconfig.vdf). Host
  defaults to `deck@192.168.1.30`; override via 2nd arg or `REMOTE_HOST`.
- `launch-game.sh <exe-path> [exe-args...]` — runs a Windows exe on the Deck via
  Proton. Env knobs: `REMOTE_HOST`, `COMPAT_PREFIX` (derived from the exe path if it
  contains `compatdata/`), `PROTON_VERSION` (default `GE-Proton9-14`), `STEAM_ROOT`,
  `POLL_SECS` (process-confirmation poll, default 30). Starts processes on the live
  Deck — run attended.
- `install-nwjs-runner.sh [--nwjs-version X.Y.Z] [--game-dir PATH] [--variant NAME]
  [--extra-flags "..."]` — installs a versioned NW.js Steam compatibility tool into
  `compatibilitytools.d` (versions/variants coexist). Afterwards restart Steam, then
  game Properties -> Compatibility -> "NW.js Linux Runner vX.Y.Z". Version pinning
  rationale: failure-archaeology.
- `pre-launch-galaxy-service.sh` — not run from the Mac: `scp` to
  `/home/deck/pre-launch-galaxy-service.sh`, `chmod +x`, then set the GOG Galaxy
  non-Steam shortcut Launch Options to `/home/deck/pre-launch-galaxy-service.sh %command%`.
  Starts GalaxyClientService outside Wine's SCM to avoid the elevation-mismatch stop.

## Ansible playbooks (`playbooks/`, inventory `inventory/hosts.ini`)

Inventory: group `[steamdeck]` -> `192.168.1.30 ansible_user=deck`. Ansible is a uv
dependency; collections from `requirements.yml` (`community.general`):

```bash
uv run ansible-galaxy collection install -r requirements.yml   # once
uv run ansible-playbook -i inventory/hosts.ini playbooks/flatpak.yml \
  -e "flatpak_app_id=org.example.AppName flatpak_state=latest"
```

Every playbook var is also settable by env var (shown in each playbook header).
The in-repo `/ansible-run <name>` skill wraps resolution + run (uses brew ansible).

- `flatpak.yml` — install/remove/update Flatpaks (user scope). Vars: `flatpak_app_id`
  [`FLATPAK_APP_ID`] required (ID or comma-list); `flatpak_state` present|absent|latest
  (default present); `flatpak_remote` (default flathub) + `flatpak_remote_url`;
  `target_host` [`DECK_HOST`] (default `steamdeck` group).
- `remove-launchers.yml` — **DESTRUCTIVE. STOP: deletes the Wine/Proton prefix —
  game files inside it are lost. Human go required; confirm the saves backup vars
  are set and verify the backup landed before proceeding (change-control).**
  Kills launcher processes (`launcher_process_pattern`), backs up
  `saves_src_path` [`DECK_SAVES_SRC`] to `saves_backup_path` [`DECK_SAVES_BACKUP`,
  default `/home/deck/Backups/launcher-saves`], removes `nsl_dir_path`
  [`DECK_NSL_DIR`] (NonSteamLaunchers), then deletes `launcher_prefix_path`
  [`DECK_LAUNCHER_PREFIX`] (required).

## Data conventions

- `.cache/host/` — synced Deck logs/DB/config (gitignored working set).
- `.claude/cache/<slug>.json` — research lookup cache; check before re-deriving.
- `config.ini` — local, from `config.ini.example`; not committed.
- Tests: `uv run --with pytest pytest tests/` — pytest is not a declared dep here (see python-env traps).

## Provenance and maintenance

Documented 2026-07-03 from `~/Projects/steamdeck` source (deck_query argparse, all
four scripts' headers, both playbooks, inventory, pyproject). Nothing executed
against the Deck. Re-verify:

```bash
git -C ~/Projects/steamdeck log -1 --format='%h %cs'
grep -n 'add_parser\|add_argument' ~/Projects/steamdeck/src/deck_query.py | head -30
head -35 ~/Projects/steamdeck/playbooks/remove-launchers.yml
```
