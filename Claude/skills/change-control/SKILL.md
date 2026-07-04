---
name: change-control
description: Load BEFORE modifying anything production-touching (Synology NAS services, UniFi/network gear, Raspberry Pi fleet or other physical devices, deploy scripts, docker-compose.nas.yml), before any write under dotfiles/Claude (live global Claude config via symlink), when classifying a change, when deciding whether a change needs a rollback point or explicit human sign-off, or before any destructive op (delete/flash/reboot/overwrite a device).
---

## Summary
Every change in this portfolio is one of four classes — docs-only, repo code, Claude-config
(live instantly via `~/.claude` symlink), or prod-touching — each with its own gate.
Three non-negotiables (owner-stated, 2026-07-03): no prod-NAS change without a tested
rollback, no untested change against live network gear, no unattended destructive op
without explicit human go. All commits route through `/git-commit`, never around it.

## Routing

| Situation | Read |
|---|---|
| Classifying a change; unsure which gate applies; edge cases (compose split, pi scripts) | [references/taxonomy.md](references/taxonomy.md) |
| About to touch NAS, network gear, a physical device, or `dotfiles/Claude/**` | [references/gates.md](references/gates.md) |
| Committing, reviewing, or pushing any change | [references/commit-path.md](references/commit-path.md) |

## When NOT to use this skill
- Sandboxed or local-only experimentation (local docker, scratch scripts) → `validation-and-qa`.
- Day-to-day debugging of running systems → `debugging-playbook`.
- Digging into past incidents and their evidence → `failure-archaeology`.
- Understanding what the infrastructure is → `homelab-architecture`; executing routine
  operational runbooks → `homelab-operations`; Claude config file mechanics → `claude-config`.
