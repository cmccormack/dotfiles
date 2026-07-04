# docker-compose Triage (macknet, bookshelf)

Two compose stacks exist. macknet has a single `docker-compose.yml` (one service,
`unifi`, `build: .`, `env_file: .env`) — local only, no NAS variant. bookshelf has the
local vs NAS split: base `docker-compose.yml` (container `cwa-library`) plus overlay
`docker-compose.nas.yml`. Deploy/update procedure → `homelab-operations`;
prod-NAS changes → `change-control` first.

## The variant split (bookshelf)

- Local test: `docker-compose.yml` alone — relative binds `./config ./library ./ingest`,
  inotify ingest watcher, PUID/PGID default 1000.
- NAS: `docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d` —
  `/volume1/...` binds, `WATCH_METHOD=polling`, `NETWORK_SHARE_MODE=true`.
- Synology ships docker-compose **v1** at `/usr/local/bin/docker-compose`; the v2
  `docker compose` plugin does not exist there. Neither binary is in the default SSH PATH.

Which variant is a running container using?

```bash
docker inspect cwa-library --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'
docker inspect cwa-library --format '{{json .Config.Env}}' | tr ',' '\n' | grep -E 'WATCH_METHOD|NETWORK_SHARE_MODE|PUID|PGID'
```

Mount sources under `/volume1/` = NAS deploy; under the repo dir = local. No
`WATCH_METHOD`/`NETWORK_SHARE_MODE` hits on the NAS = the overlay was NOT applied.

## Symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| Books dropped in ingest never processed (NAS) | Overlay missing → inotify watcher, which never fires over network shares | env grep above shows no `WATCH_METHOD=polling` | Re-up with both `-f` files — prod NAS change, gate via change-control |
| SQLite `database is locked` errors (NAS/Btrfs) | `NETWORK_SHARE_MODE=true` missing (WAL mode on Btrfs share) | env grep above | Same re-up with overlay |
| Permission denied on `/config` or library writes | PUID/PGID mismatch — NAS user chris is 1026/100, compose default 1000 | `docker exec cwa-library id` vs `id` over NAS SSH | Set `PUID`/`PGID` in `.env`, recreate container |
| `docker compose: command not found` on NAS | v2 syntax on a v1-only box | `/usr/local/bin/docker-compose version` | Use the hyphenated full path |
| `docker: command not found` over NAS SSH | Binary not in default PATH | `ls -l /usr/local/bin/docker` | Use full path |
| Container restart-looping | App-level crash | `docker logs cwa-library --tail 50` | Follow the log; see bookshelf.md for CWA modes |
| macknet `unifi` service exits immediately | `.env` absent (`env_file: .env`) → client raises `KeyError: 'UNIFI_HOST'` | `docker logs` shows the KeyError | Copy `.env.example` → `.env` |
| Workload gone after a Pi/NAS reboot | Containers `Exited` with `RestartPolicy=no` — by design on the Pi fleet | `docker inspect <c> --format '{{.HostConfig.RestartPolicy.Name}}'` | Bring stack up manually, or set `restart: unless-stopped` deliberately |

## Traps

- Bringing the NAS stack up with only the base file "works" — it starts, then ingest and
  SQLite silently degrade. Always both `-f` flags on NAS (header comment in
  docker-compose.nas.yml documents this).
- `docker exec` runs as root; `calibredb` edits inside the container leave root-owned
  files → `sudo chown -R <user>:users /volume1/calibre/library/` then restart.
- Rollback point before any NAS `pull`/`up`: config lives under
  `/volume1/docker/cwa-library/`; note the previous image digest before pulling.

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/bookshelf/{docker-compose.yml,docker-compose.nas.yml,NAS_SETUP.md,CLAUDE.md} and ~/Projects/macknet/docker-compose.yml.
Re-verify: `cat ~/Projects/bookshelf/docker-compose.nas.yml ~/Projects/macknet/docker-compose.yml`
