---
name: homelab-operations
description: >
  Operational runbooks for Chris's homelab. Load when starting, stopping, deploying,
  or updating a homelab service (Calibre-Web/bookshelf on the NAS, macknet
  UniFi/Synology/Pi tooling, keylimepi PiKVM, Steam Deck toolkit, dotfiles sync);
  when running a playbook or helper script; when asking where data, backups, or
  artifacts live; or when working with the Synology NAS or a Raspberry Pi.
---

## Summary
Runbooks for operating each live homelab system: exact commands, flag anatomy,
where data and artifacts land, and post-change health checks. Every
prod-touching or destructive step carries an inline STOP gate (full policy:
change-control skill). Pick the system below and load only its reference file.

## Routing

| System | Task | Load |
|---|---|---|
| bookshelf | Run/deploy Calibre-Web (CWA), Kobo sync, book ingest | [references/bookshelf.md](references/bookshelf.md) |
| macknet | UniFi/Synology CLIs, Pi fleet maintenance scripts | [references/macknet.md](references/macknet.md) |
| keylimepi | Flash, validate, and operate the PiKVM | [references/keylimepi.md](references/keylimepi.md) |
| steamdeck | deck-query CLI, helper scripts, Ansible playbooks | [references/steamdeck.md](references/steamdeck.md) |
| dotfiles | Run a dotfiles sync, credential scanner behavior | [references/dotfiles.md](references/dotfiles.md) |

## Safety gates (apply everywhere)
No prod-NAS changes without a tested rollback. No untested changes against live
network gear. No unattended destructive device ops without explicit human go.

## When NOT to use
- Service broken / diagnosing a failure — debugging-playbook
- Understanding design or topology — homelab-architecture
- Python/uv environment setup — python-env
