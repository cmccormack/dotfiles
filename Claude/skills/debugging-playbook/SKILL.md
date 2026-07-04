---
name: debugging-playbook
description: >-
  Symptom-to-triage runbook for the homelab portfolio. Load when something is
  broken, failing, or erroring in any repo (macknet, bookshelf, keylimepi,
  steamdeck, dotfiles) or homelab service; a container won't start or ingest
  stalls; a UniFi/Synology API client fails, 401s/429s, or times out; a
  Raspberry Pi is unreachable or SSH is refused; PiKVM has no video; Kobo sync
  fails; an ansible-playbook run errors; a Python/uv env misbehaves
  (ModuleNotFoundError, wrong interpreter, stale uv.lock); or a Claude session
  is misbehaving, burning tokens, went down a wrong path, or lost work.
---

# Debugging Playbook

## Summary
Symptom → likely cause → one discriminating check → fix, per homelab layer.
Diagnose read-only first; the fix step comes last. Any fix touching live network
gear or the prod NAS routes through `change-control` before execution — no
untested live network changes, no prod-NAS change without a rollback point,
no unattended destructive ops. Load only the reference for your layer.

## Routing

| Symptom area | Reference |
|---|---|
| Wrong python, ModuleNotFoundError, stale uv.lock | [references/python-uv.md](references/python-uv.md) |
| Container won't start, ingest stalls, local vs .nas variant | [references/docker-compose.md](references/docker-compose.md) |
| ansible-playbook fails, Steam Deck unreachable | [references/ansible.md](references/ansible.md) |
| UniFi/Synology client errors (KeyError, 429, NasError) | [references/api-clients.md](references/api-clients.md) |
| Calibre-Web / Kobo sync failures | [references/bookshelf.md](references/bookshelf.md) |
| Pi unreachable, SSH lockout, PiKVM, SD-card suspicion | [references/pi-fleet.md](references/pi-fleet.md) |
| Token burn, wrong-path agent, lost session work | [references/claude-sessions.md](references/claude-sessions.md) |

## When NOT to use
- Designing or approving a fix for prod gear/NAS → `change-control`.
- Understanding how the system fits together → `homelab-architecture`.
- Re-opening a settled past investigation → `failure-archaeology`.
