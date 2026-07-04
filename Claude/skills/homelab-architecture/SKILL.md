---
name: homelab-architecture
description: >
  Architecture contract and domain reference for Chris's homelab. Load when: needing to
  understand how the homelab fits together; which repo owns what (macknet, bookshelf,
  keylimepi, steamdeck, dotfiles); device, network, or NAS topology; why a design decision
  was made; how the UniFi/Synology/Kobo/PiKVM integrations actually work; or before
  proposing a structural change.
---

# Homelab Architecture

## Summary
UniFi network (UDM Pro + 16-port PoE switch + 4 U6-Lite APs), Synology DS918+ NAS, and a
small Raspberry Pi fleet, automated from [macknet](~/Projects/macknet) (async Python API
clients, hub repo). bookshelf runs the ebook stack on the NAS; keylimepi is a PiKVM build;
dotfiles/Claude is the LIVE global Claude config via symlink. All Python is uv (3.13; steamdeck 3.14).
This skill is the map and the "why" — not an operations runbook.

## Routing

| Need | Read |
|---|---|
| Devices, IPs, repo ownership, cross-links | [references/topology.md](references/topology.md) |
| Design decisions with rationale + evidence | [references/decisions.md](references/decisions.md) |
| Invariants that must not break | [references/invariants.md](references/invariants.md) |
| Known weak points, plainly stated | [references/weak-points.md](references/weak-points.md) |
| UniFi / Synology DSM / Kobo sync / PiKVM as used here | [references/domain-apis.md](references/domain-apis.md) |

Load one reference file, not all five. Deeper detail lives in `macknet/docs/INDEX.md`
(load that index first, then only the file needed).

## When NOT to use
Operating or deploying services → `homelab-operations`. Fixing breakage → `debugging-playbook`.
Changing anything production-touching (NAS, network, devices, dotfiles/Claude) → `change-control` first.
