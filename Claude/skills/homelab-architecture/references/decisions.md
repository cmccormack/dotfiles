# Load-Bearing Design Decisions

Each entry: decision → why → evidence. Do not reverse one without reading its evidence.

## macknet is the automation hub
One repo owns network/NAS/Pi automation *and* the reference docs of record; integrations
live as sibling subpackages (`macknet.unifi`, `macknet.nas`), and other repos link to
macknet's docs instead of duplicating them.
**Why:** one client codebase, one doc tree, no drift between per-service repos.
**Evidence:** git `69ced93` "Restructure as macknet.unifi; rename repo to MackNet",
`44b5ad4` "Add macknet.nas Synology DSM integration"; macknet CLAUDE.md "Future
integrations live as sibling subpackages"; bookshelf CLAUDE.md links to macknet synology docs.

## Hand-rolled aiohttp clients as async context managers, no vendor SDKs
`UnifiClient` and `NasClient` are deliberately identical in shape: session created and
login performed in `__aenter__` (close-on-login-failure), logout/close in `__aexit__`,
private `_get/_post`/`_api` helpers that unwrap the response envelope so callers get bare
payloads.
**Why:** house style is stdlib-plus-approved-deps; both vendor APIs are thin HTTP and an
SDK adds a dependency without covering the internal endpoints actually used.
**Evidence:** [macknet/src/macknet/unifi/client.py](~/Projects/macknet/src/macknet/unifi/client.py),
[macknet/src/macknet/nas/client.py](~/Projects/macknet/src/macknet/nas/client.py); code-style
rules in `~/.claude/CLAUDE.md`.

## Local vs `.nas` docker-compose split (bookshelf)
Base `docker-compose.yml` uses relative paths (`./config`, `./library`, `./ingest`) for
local testing; `docker-compose.nas.yml` is an *override* file (`-f base -f nas`) that swaps
volumes to `/volume1/...` and adds `WATCH_METHOD=polling` + `NETWORK_SHARE_MODE=true`.
**Why:** test the exact container locally before touching the NAS; the NAS needs polling
(no inotify on network shares) and WAL-off (SQLite lock errors on Btrfs).
**Evidence:** comments in [bookshelf/docker-compose.nas.yml](~/Projects/bookshelf/docker-compose.nas.yml);
branch strategy `main` / `local-test` in bookshelf CLAUDE.md.

## NAS share conventions
App data bind-mounts under `/volume1/docker/<appname>/`; bulk data gets its own share
(`/volume1/calibre/`). Shares are created with `synoshare`, never `mkdir`.
**Why:** Synology Btrfs shares are subvolumes registered with DSM — `mkdir` produces a
plain directory DSM won't manage and that can't be promoted later.
**Evidence:** "Btrfs Gotcha" in bookshelf CLAUDE.md; macknet `.claude/skills/synology.md`
key-paths table; `macknet/docs/synology/storage.md`.

## INDEX/router doc economy
Every doc tree starts at an INDEX (`macknet/docs/INDEX.md` → per-domain INDEX with
"quick facts") and skills are thin routers pointing at docs to be loaded via subagent.
**Why:** context economy — load the map, then only the file the task needs; quick-facts
sections answer most questions without loading anything else.
**Evidence:** `macknet/docs/INDEX.md` ("Load this index first"), `docs/unifi/INDEX.md`
quick facts, macknet skills `unifi.md`/`synology.md`; steamdeck CLAUDE.md cache pattern.

## uv everywhere (Python 3.13; steamdeck pins 3.14)
Every live Python repo (macknet, bookshelf, steamdeck, dotfiles) uses uv + `pyproject.toml`
+ `uv.lock`; no requirements.txt/poetry anywhere in the active set.
**Why:** one toolchain, `uv run` as the universal invoker in docs and skills.
**Evidence:** `ls ~/Projects/{macknet,bookshelf,steamdeck,dotfiles}/uv.lock`.

## dotfiles symlink-sync is the global-config mechanism
`scripts/sync/sync.py` reads `manifest.conf` (`~/src:repo/dest`), moves the real file into
the repo, and symlinks it back — so `~/.claude/{CLAUDE.md,settings.json,skills,hooks,scripts}`
ARE the repo working tree. A credential scanner gates every move.
**Why:** global Claude config is versioned, reviewable, and restorable on a new machine;
the scanner keeps secrets out of git.
**Evidence:** [dotfiles/scripts/sync/manifest.conf](~/Projects/dotfiles/scripts/sync/manifest.conf)
"Claude config" block; `ls -la ~/.claude/skills` shows the symlink.

## Pi fleet conventions: wired IP, key-only SSH, gitignored real inventory
Maintenance always targets the wired IP (wifi renumbers on reboot; eth0 holds the default
route); SSH is key-only with passwordless sudo; real host details live only in gitignored
`fleet.local.md`. Fresh appliances get default creds rotated into the macOS keychain via
`scripts/pi/secure-new-ssh-host.sh` before anything else.
**Evidence:** `macknet/docs/raspberry-pi/INDEX.md`, `macknet/scripts/pi/README.md`.

## NAS SSH is disabled by design — automation goes through the DSM Web API (port 5001)
**Why:** smaller attack surface after the 2026-06-27 hardening pass; DSM has no static API
tokens, so the API client does session login per run instead.
**Evidence:** macknet CLAUDE.md Architecture section; `bookshelf/NAS_SECURITY.md` commit
`3a16199`. Note: bookshelf CLAUDE.md still documents SSH access — see weak-points.md.

## Provenance and maintenance
Compiled 2026-07-03 from the files and commits cited inline. Re-verify:
- `git -C ~/Projects/macknet log --oneline` (commit hashes still present)
- `grep -n "disabled by design" ~/Projects/macknet/CLAUDE.md`
- `grep -n "NETWORK_SHARE_MODE" ~/Projects/bookshelf/docker-compose.nas.yml`
- `readlink ~/.claude/skills` (symlink-sync still live)
