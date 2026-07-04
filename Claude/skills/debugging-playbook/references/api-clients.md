# macknet API Client Triage (UniFi, Synology)

Both clients are aiohttp async context managers in ~/Projects/macknet:
`src/macknet/unifi/client.py` (`UnifiClient`) and `src/macknet/nas/client.py`
(`NasClient`). Both read `os.environ[...]` directly — a missing `.env` raises
`KeyError` before any network I/O.

## The exception type IS the diagnosis

| Exception | Layer at fault |
|---|---|
| `KeyError: 'UNIFI_HOST'` / `'NAS_HOST'` etc. | Environment — `.env` not loaded. Scripts must call `load_dotenv()` (as `macknet/__main__.py` and test conftest do) or export vars |
| `aiohttp.ClientConnectorError` | Network/host — wrong IP, device down, wrong port |
| `aiohttp.ClientResponseError` | HTTP layer — controller/DSM rejected the request; check `.status` |
| `NasError` (`{api}.{method} failed: error code N`) | DSM application layer — HTTP 200 but `success: false` |

## Smoke checks (run from ~/Projects/macknet)

```bash
uv run python -m macknet                    # UniFi: prints version + device/client counts
uv run python -m macknet.nas.logs --limit 5 # Synology: pulls 5 DSM log entries
```

## UniFi (`UnifiClient`)

- Auth: `POST https://$UNIFI_HOST/api/auth/login`; the returned `x-csrf-token` header is
  echoed on every later request; all site-scoped calls go via `/proxy/network/api/s/{site}/`.
- **429 on login = the controller's login rate limit.** Hit by scripts that construct a
  new `UnifiClient` per request or by back-to-back test runs. Fix: one `async with`
  session per run — the integration suite shares a session-scoped fixture for exactly
  this (commit fdb4a9a). Then wait out the limit; duration unverified.
- 401/403 on login = credentials rejected (status meaning standard, not repo-verified).
- Cert errors only if you passed `verify_ssl=True` — default is False (self-signed
  controller cert); cookie jar is `unsafe=True` because the host is an IP.
- 404s on otherwise-valid endpoints → wrong `UNIFI_SITE`; enumerate with `client.sites()`.
- Device/client lookup CLI: `uv run python -m macknet.unifi.query`.

## Synology (`NasClient`)

- Auth: `SYNO.API.Auth` login on port 5001 returns `sid` + `synotoken`; both echoed to
  `/webapi/entry.cgi`. No static API tokens exist in DSM. 2FA account → set `NAS_OTP`.
- SSH on the NAS is disabled by design — do not "fall back to SSH"; everything goes
  through the Web API.
- `NasError` codes (from macknet docs/synology/api.md): 101 invalid parameter,
  102 API doesn't exist, 103 method doesn't exist, 104 version unsupported,
  105 insufficient privileges, 119 SID expired, 120 account disabled.
  Login failures raise `NasError("SYNO.API.Auth", "login", <code>)`.
- The DSM `level` filter on `system_log` is unreliable — use `--grep REGEX` instead;
  DSM returns newest-first, so widen `--limit` to reach further back (macknet CLAUDE.md).

## Gate

If the client works but device behavior is the suspect (clients being kicked by
min-RSSI, DHCP oddities), do not change controller or DSM settings from a debugging
session — route to `change-control`. `inventory/network.yaml` is the known-good record
of AP/radio config for diffing.

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/macknet/src/macknet/{unifi,nas}/client.py, CLAUDE.md, docs/synology/api.md, pyproject.toml.
Re-verify: `cd ~/Projects/macknet && uv run python -m macknet && sed -n '126,140p' docs/synology/api.md`
