# macknet — UniFi/Synology clients and Pi fleet maintenance

Repo: `~/Projects/macknet`. Python (uv) async clients for the UniFi controller and
Synology DSM, plus shell scripts that maintain the Raspberry Pi fleet over SSH.
Env: copy `.env.example` -> `.env` — `UNIFI_HOST/USER/PASSWORD/SITE` and
`NAS_HOST/USER/PASSWORD` (+ optional `NAS_PORT`, `NAS_OTP`). NAS SSH is disabled by
design; all NAS access goes through the DSM Web API on 5001.

## CLIs (read-only unless noted)

```bash
uv run python -m macknet                  # smoke check: version, device/client counts
uv run python -m macknet.unifi.query     # device/client search
uv run python -m macknet.nas.logs        # Synology DSM system-log query
uv run python -m macknet.unifi.inventory # write inventory/network.yaml snapshot
```

`unifi.query` flags: positional `term` (searches name/hostname/MAC/IP/OUI), `--mac`,
`--oui`, `--ip` (prefix matches), `--online`, `--infrastructure` (APs/switches/gateways
instead of clients), `--unknown`, `--stale DAYS`, `--show-mac`, `--json`, and
`--forget` (+`--yes` to skip its confirmation).
**STOP — `--forget` deletes matched clients from the live UniFi controller. Never run
`--forget --yes` unattended; requires explicit human go (change-control).**

`nas.logs` flags: `--since/--until YYYY-MM-DD[THH:MM]`, `--grep REGEX` (matches
description), `--level info|warning|error`, `--limit N` (fetched before filtering —
DSM returns newest-first, widen to reach further back), `--json`. The DSM level
filter is unreliable — prefer `--grep`.

`unifi.inventory --output PATH` defaults to `inventory/network.yaml` (committed
snapshot of infrastructure + known clients).

Docker: `docker compose up` builds the image and runs the smoke check
(`CMD uv run python -m macknet`), env from `.env`.

## Pi maintenance playbook (`scripts/pi/`)

All scripts take `user@host`, use key-only `BatchMode` SSH, and expect passwordless
sudo. **Always target the wired IP** — wifi addresses can renumber on reboot. Record
outcomes in `docs/raspberry-pi/maintenance-log.md`.

Order of operations:

```bash
scripts/pi/recon.sh          chris@HOST   # 1. read-only survey — makes no changes
scripts/pi/backup-config.sh  chris@HOST   # 2. rollback point (REQUIRED before 3-5)
scripts/pi/update.sh         chris@HOST   # 3. apt full-upgrade within current release
scripts/pi/harden-ssh.sh     chris@HOST   # 4. key-only SSH drop-in
scripts/pi/enable-auto-security-updates.sh chris@HOST   # 5. unattended security upgrades
```

**STOP — steps 3-5 change a live device. Run recon + backup-config first (that
tarball is the tested-rollback gate) and get human go before proceeding
(change-control).**

- `backup-config.sh user@host [dest_root]` — pulls `/etc` + dpkg/apt manifests +
  crontabs into `backups/pi/<host>/<timestamp>/etc-and-manifests.tar.gz` with
  `SHA256SUMS`. Output is gitignored (contains host keys/shadow).
- `update.sh user@host [--reboot]` — `apt-get full-upgrade` with `--force-confold`
  (keeps existing conffiles), `autoremove --purge`, then `rpi-eeprom-update -a`
  (firmware staged for next boot). Prints `REBOOT_REQUIRED=yes|no`; never reboots
  without `--reboot`. **STOP — rebooting is a human-go step:**
  `ssh chris@HOST sudo systemctl reboot`, then confirm SSH returns on the wired IP.
- `harden-ssh.sh user@host` — installs
  `/etc/ssh/sshd_config.d/99-macknet-hardening.conf` (no password auth, no root
  password login, no X11). Self-gating: aborts if no `authorized_keys`, validates
  with `sshd -t`, reloads (not restarts) sshd, then verifies a fresh key-only login.
  Undo = delete the drop-in and reload sshd.
- `enable-auto-security-updates.sh user@host` — installs unattended-upgrades and
  writes `/etc/apt/apt.conf.d/20auto-upgrades` (security only; no auto-reboot).

## Securing a freshly-flashed host (`scripts/ssh/`)

`scripts/ssh/secure-new-ssh-host.sh` (moved from `scripts/pi/` on 2026-07-03; the
`scripts/pi/README.md` example still shows the old path — uncommitted WIP):

```bash
scripts/ssh/secure-new-ssh-host.sh root@192.168.1.15 root --pubkey ~/.ssh/id_ed25519.pub
security find-generic-password -a root -s macknet-ssh-root@192.168.1.15 -w   # retrieve later
```

Args: `<user>@<host> <default-password> [--pubkey <path>] [--service <name>]`.
Rotates vendor default creds (root/root, pi/raspberry, ...) to a random password
stored only in the macOS login keychain (service `macknet-ssh-<user>@<host>` unless
`--service` given), pins the host key, optionally installs a pubkey. Refuses to
overwrite an existing keychain entry. Requires `sshpass` (`brew install sshpass`).
**STOP — changes a live device's credentials; run attended with the console
reachable as fallback.**

## Data conventions

- `backups/pi/<host>/<timestamp>/` — config backups (gitignored).
- `inventory/network.yaml` — UniFi inventory snapshot (committed).
- `docs/INDEX.md` — reference-doc router (UniFi / Synology / Pi); load the index
  first, then only the file you need. Per-device notes: `docs/raspberry-pi/`.
- Tests: `uv run pytest tests/unit`; `tests/integration` needs a live controller +
  `.env` (login rate-limited — the session-scoped fixture handles it).

## Provenance and maintenance

Documented 2026-07-03 from `~/Projects/macknet` source (all six scripts read in
full, CLAUDE.md, CLI argparse definitions). Nothing executed against devices.
Re-verify:

```bash
git -C ~/Projects/macknet log -1 --format='%h %cs'; git -C ~/Projects/macknet status --short
ls ~/Projects/macknet/scripts/pi ~/Projects/macknet/scripts/ssh
grep -n 'add_argument' ~/Projects/macknet/src/macknet/unifi/query.py ~/Projects/macknet/src/macknet/nas/logs.py
```
