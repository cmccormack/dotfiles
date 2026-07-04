# Domain Reference — As Used Here

Not a textbook. Each section documents only what the actual code touches, with pointers.

## UniFi controller API (macknet)
Controller = the UniFi Network Application running on the UDM Pro (192.168.1.1).
Client: [macknet/src/macknet/unifi/client.py](~/Projects/macknet/src/macknet/unifi/client.py).
- **Auth (as implemented):** session auth — `POST /api/auth/login` with username/password
  sets a cookie and returns an `x-csrf-token` header, echoed on all later requests.
  Self-signed cert → `verify_ssl=False` default; cookie jar `unsafe=True` (IP host).
  Docs also describe an `X-API-KEY` header method (`docs/unifi/INDEX.md` calls it
  preferred) — the client does not use it.
- **API layers:** client uses the *internal* API, base
  `/proxy/network/api/s/{site}/` (site slug `default`). The *official* v1 API
  (`/proxy/network/integration/v1/`, UUID site ids) is documented but unused.
- **Endpoints touched:** `stat/device` (infrastructure), `stat/sta` (active clients only),
  `rest/user` (all clients ever seen), `stat/sysinfo`, `cmd/stamgr` `forget-sta`,
  and non-site-scoped `/proxy/network/api/self/sites`.
- **Envelope:** `{"meta": {...}, "data": [...]}` — `_get/_post` unwrap `data`.
- **Jargon:** *site* = controller tenancy unit (here always `default`); *sta* = station,
  a connected client. Login is rate-limited (429) — see invariants.md.

## Synology DSM Web API (macknet)
DSM = DiskStation Manager, the DS918+'s OS. Client:
[macknet/src/macknet/nas/client.py](~/Projects/macknet/src/macknet/nas/client.py).
- **Auth:** no static API tokens exist in DSM. `SYNO.API.Auth` v6 login (`auth.cgi`)
  returns `sid` (session id, sent as `_sid` form field) + `synotoken` (CSRF, sent as
  `X-SYNO-TOKEN` header); `__aexit__` logs out. Optional `NAS_OTP` for 2FA accounts.
- **Transport:** everything else is `POST https://<host>:5001/webapi/entry.cgi` with
  `api`/`method`/`version` form fields; `success:false` → `NasError(code)`.
- **APIs touched:** `SYNO.API.Info` (discovery, via `query.cgi`, unauthenticated),
  `SYNO.Core.SyslogClient.Log` (Log Center entries, newest-first; `level` filter is
  unreliable — grep the description instead), `SYNO.Core.System` /
  `SYNO.Core.System.Utilization`, `SYNO.Storage.CGI.Storage`.
- CLI wrapper: `uv run python -m macknet.nas.logs` (flags in macknet CLAUDE.md).

## Kobo sync (bookshelf)
CWA (Calibre-Web Automated) speaks Kobo's *native* sync protocol, so a stock Kobo syncs
wirelessly against the NAS instead of the Kobo store.
- **Device side:** point `api_endpoint` under `[OneStoreServices]` in
  `.kobo/Kobo/Kobo eReader.conf` at `http://<ip>:8083/kobo/<token>`. Firmware 4.39+
  removed the Beta-Features server menu, so
  [bookshelf/kobo_set_server.py](~/Projects/bookshelf/kobo_set_server.py) patches the file
  over USB (writes `.conf.bak` first). Use an IP, not `hostname:port` — the Kobo appends
  the port to unrelated URLs otherwise.
- **Server side:** token is per-CWA-install (regenerate after redeploy);
  `config_kobo_proxy=1` must be set or the device shows "Retry sync" (it needs Kobo's
  servers for resource definitions). CWA converts EPUB→KEPUB (Kobo's enhanced format) on
  the fly via kepubify — the library stays EPUB.
- Verified on Kobo Libra Colour fw 4.45.23697, CWA v2.2.1 (`bookshelf/KOBO_SETUP.md`).

## PiKVM (keylimepi + macknet docs)
PiKVM = open-source KVM-over-IP: the Pi captures the target's HDMI and presents itself as
a USB keyboard/mouse (HID gadget over USB-C OTG), so the target needs no software.
- **Build:** Pi 4B + HDMI-to-CSI bridge (TC358743 chip — Waveshare or Geekworm X630; the
  X630 needs its hardware-reset jumper on pins 1–2) + USB-C power splitter (the one USB-C
  port is both OTG and power). Guide: [keylimepi/README.md](~/Projects/keylimepi/README.md).
- **First boot:** config via `keylimepi.txt` dropped on the boot partition (sourced by the
  PiKVM firstboot hook — hostname/timezone/wifi). Never use Raspberry Pi Imager's
  customization options; they corrupt PiKVM's own first-boot config. Validate the card
  with `keylimepi/setup.sh <boot-mount>`.
- **Defaults to rotate immediately:** web `admin`/`admin`, SSH `root`/`root` — use
  `macknet/scripts/pi/secure-new-ssh-host.sh` (keychain-stored random password).
- Decision record + step-by-step for the MackPi4-1 conversion:
  `macknet/docs/raspberry-pi/pikvm.md` and `pikvm-upgrade.md`. Image variant (v2 vs
  v3-hdmi-rpi4) is currently contradictory between repos — see weak-points.md.

## Provenance and maintenance
Compiled 2026-07-03 from the client code and docs cited inline. Re-verify:
- `grep -n "proxy/network/api" ~/Projects/macknet/src/macknet/unifi/client.py`
- `grep -n "SYNO\." ~/Projects/macknet/src/macknet/nas/client.py`
- `grep -n "OneStoreServices\|api_endpoint" ~/Projects/bookshelf/kobo_set_server.py`
- `grep -n "TC358743\|jumper" ~/Projects/keylimepi/README.md`
