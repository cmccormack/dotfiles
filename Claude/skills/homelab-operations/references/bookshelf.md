# bookshelf — Calibre-Web-Automated / Kobo stack

Repo: `~/Projects/bookshelf` (internal name `cwa-library`, also the container name).
Single CWA container serving the ebook library on port 8083 plus native Kobo wireless
sync. Prod runs on the Synology DS918+ NAS; local runs are for testing before deploy.

## Compose files — how to choose

| File | When | Volumes |
|---|---|---|
| `docker-compose.yml` | Local test on the Mac, used alone | relative: `./config`, `./library`, `./ingest` |
| `docker-compose.nas.yml` | NAS deploy, **overlay on top of the base file** | `/volume1/docker/cwa-library/config`, `/volume1/calibre/{library,ingest}` |

The `.nas` overlay adds `WATCH_METHOD=polling` (inotify unavailable over Synology
network shares) and `NETWORK_SHARE_MODE=true` (disables SQLite WAL — prevents lock
errors on Btrfs). Env comes from `.env`: `PUID`/`PGID` (must match the library/ingest
owner — `id $(whoami)` on the NAS), `TZ`, `PORT` (default 8083), `ADMIN_PASSWORD`,
`ADMIN_REFRESH_PASSWORD`.

Local test (base file only):

```bash
cd ~/Projects/bookshelf && docker compose up -d
```

NAS deploy — **STOP: prod NAS. Requires human go + tested rollback (see
change-control).** Rollback baseline: `backup-config`-style copy of
`/volume1/docker/cwa-library/config` before changing anything; re-deploy is
`docker-compose ... down` + previous image. Synology only has compose **v1** at
`/usr/local/bin/docker-compose` — hyphenated form, never `docker compose`:

```bash
ssh <user>@<nas-ip>
cd /volume1/docker/cwa-library/bookshelf
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d
```

Update to latest CWA image (same STOP gate; pull then re-up):

```bash
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml pull
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d
```

## Helper scripts (run from the Mac, repo root, via uv)

`setup_cwa.py` — admin hardening + Kobo sync enable, drives the web UI via Playwright.
Exactly one of `--update-password` / `--rotate-password` is required.

| Flag | Meaning |
|---|---|
| `--host` / `--port` | CWA target (default `localhost:8083`; use `--host <nas-ip>` for prod) |
| `--env-file` | `.env` path to read/update (default `.env`) |
| `--password` | current admin password (default `admin123`; rotate falls back to `ADMIN_PASSWORD`) |
| `--update-password [PW]` | set password to PW, or to `ADMIN_PASSWORD` from `.env` if omitted |
| `--rotate-password` | new password from `ADMIN_REFRESH_PASSWORD` or generated; offers to write it back to `.env` and clear the refresh var |
| `--yes` / `-y` | skip all confirmations |

```bash
uv run python setup_cwa.py --host <nas-ip> --rotate-password
```

It also enables Kobo sync (`config_kobo_sync`) and prints the sync URL format
`http://<host>:<port>/kobo/<user-token>`.

`kobo_set_server.py` — patch a USB-mounted Kobo's `api_endpoint`
(`.kobo/Kobo/Kobo eReader.conf`, `[OneStoreServices]`). Writes a `.conf.bak` backup
first; safe to re-run. Use an IP for host — Kobo mangles `domain:port` URLs. Token:
CWA User Profile -> Kobo Sync -> Create/View token (per-install; regenerate after a
fresh deploy).

```bash
uv run python kobo_set_server.py /Volumes/KOBOeReader <nas-ip> 8083 <token>
```

`make_test_pdf.py` — writes `ingest/test_book.pdf` to exercise the ingest pipeline:

```bash
uv run python make_test_pdf.py
```

## Data conventions

- Books in: drop into the ingest folder (`./ingest` local; `/volume1/calibre/ingest`
  on NAS via File Station -> calibre -> ingest). CWA auto-imports and removes the file.
- Library (metadata.db + EPUBs): `./library` local; `/volume1/calibre/library` on NAS.
- App config + `app.db`: `./config` local; `/volume1/docker/cwa-library/config` on NAS.
- Cloned repo on NAS: `/volume1/docker/cwa-library/bookshelf`.
- The `calibre` share must be created via `synoshare`, not `mkdir` (Btrfs subvolume) —
  see `NAS_SETUP.md` Step 3.

## Health check after any change

```bash
/usr/local/bin/docker ps --filter name=cwa-library        # Up, not restarting
/usr/local/bin/docker logs cwa-library --tail 50          # no tracebacks
curl -s -o /dev/null -w '%{http_code}\n' http://<nas-ip>:8083/login   # 200
```

Then drop a test PDF in ingest and confirm it imports. After any `calibredb` run via
`docker exec` (creates root-owned files), always:

```bash
sudo chown -R <user>:users /volume1/calibre/library/
sudo chmod -R u+rwX,g+rX /volume1/calibre/library/
/usr/local/bin/docker restart cwa-library
```

Kobo "Retry sync" and other failures: [debugging-playbook]; full procedures in repo
`NAS_SETUP.md` and `KOBO_SETUP.md`.

## Provenance and maintenance

Documented 2026-07-03 from `~/Projects/bookshelf` source (compose files, helper
scripts, `CLAUDE.md`, `NAS_SETUP.md`). Commands transcribed, not executed. Re-verify:

```bash
git -C ~/Projects/bookshelf log -1 --format='%h %cs'
grep -n 'add_argument' ~/Projects/bookshelf/setup_cwa.py
head -25 ~/Projects/bookshelf/docker-compose.nas.yml
```
