# bookshelf / Calibre-Web-Automated / Kobo Sync Triage

Stack: single CWA container `cwa-library` (compose triage → docker-compose.md), Calibre
library on the NAS, Kobo syncing over `http://<host-ip>:8083/kobo/<token>`. Helper
scripts run from ~/Projects/bookshelf with `uv run python <script>`.

First look, always:

```bash
docker logs cwa-library --tail 100 -f
```

## Kobo sync symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| Kobo shows "Retry sync" though the request reaches CWA | Kobo proxy disabled — device can't fetch resource definitions | `docker logs cwa-library -f` during a sync shows the library request arriving, then nothing useful on-device | Enable Kobo proxy in CWA admin (`config_kobo_proxy=1`) |
| Kobo can't reach server at all | Sync URL uses `hostname:port` — Kobo appends the port to unrelated URLs — or firewall/VLAN | Re-check what was written: it must be a bare LAN IP | Re-run `uv run python kobo_set_server.py /Volumes/KOBOeReader <ip> 8083 <token>` (writes `.conf.bak`, safe to repeat) |
| Sync worked at home, fails on travel router | Kobo and CWA on different VLAN/subnet | Compare subnets of both clients | Put both on the same network; UniFi config changes gate via `change-control` |
| Sync broken after a fresh NAS redeploy | Kobo sync token is per-CWA-install | Token in CWA (User Profile → Kobo Sync) vs what the device has | Generate new token, re-run `kobo_set_server.py` |
| No sync-server option in Kobo Beta Features menu | Firmware 4.39+ removed it | — | USB-patch route above is the supported path |
| Books convert to KEPUB during sync | Not a bug — CWA converts EPUB→KEPUB on the fly; library stays EPUB | — | None |

## Library / ingest symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| Ingest file sits unprocessed | NAS: polling overlay missing; local: watcher/container down | See docker-compose.md variant check | Apply overlay / restart stack |
| Can't log in to CWA web UI | Fresh install ships admin / admin123; `setup_cwa.py` rotates it | — | `uv run python setup_cwa.py --rotate-password --host <nas-ip>` (also `--update-password`) |
| Permission errors after metadata edits | `calibredb` via `docker exec` created root-owned files | `ls -ln /volume1/calibre/library \| head` over NAS SSH | `sudo chown -R <user>:users /volume1/calibre/library/` then restart the container |
| Creating the calibre share fails / share invisible | Btrfs: a plain `mkdir /volume1/calibre` cannot become a shared folder | Does the dir predate the share? | Delete it, then `sudo /usr/syno/sbin/synoshare --add calibre 'Calibre ebook library' /volume1/calibre '' '' '' 1 0` — prod NAS, gate via change-control |

## Traps

- CWA auto-detects the library from the `/calibre-library` mount — do not hand-configure
  a library path; if the mount is wrong, fix the compose file instead.
- After any redeploy, assume the Kobo token AND the server IP both changed; re-run the
  USB patch once rather than debugging the device.
- Test PDF for ingest checks: `uv run python make_test_pdf.py`.

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/bookshelf/{CLAUDE.md,KOBO_SETUP.md,NAS_SETUP.md,docker-compose*.yml,kobo_set_server.py,setup_cwa.py}.
Re-verify: `head -60 ~/Projects/bookshelf/KOBO_SETUP.md; grep -n rotate-password ~/Projects/bookshelf/setup_cwa.py`
