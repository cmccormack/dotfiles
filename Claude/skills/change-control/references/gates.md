# Gates per Change Class

Gate = what must be true before the change is made, and what must be verified after.
Classes are defined in [taxonomy.md](taxonomy.md). Every class ends at the same exit:
commit via `/git-commit` ([commit-path.md](commit-path.md)).

## The three taboos (non-negotiable, owner-stated 2026-07-03)

1. **No prod-NAS changes without a tested rollback.** Know the undo and have exercised
   it (or an equivalent) before touching the DS918+.
2. **No untested changes against live network gear.** UniFi controller/UDM writes get
   validated somewhere safe first. The controller is the network's control plane — a bad
   change can lock you out of the very tool needed to fix it.
3. **No unattended destructive ops** (delete / flash / reboot / overwrite a device)
   **without explicit human go.** Ask, show exactly what will run, wait for yes.

The owner names network lockouts from misconfig as one of the two costliest failure modes
(the other: burned Claude sessions — see taboo rationale under Class 3). Git history shows
no committed lockout incident — these gates are preventive, codified after adversarial
review, not folklore. Documented evidence of the risk being engineered against:
- [macknet/docs/raspberry-pi/troubleshooting.md](~/Projects/macknet/docs/raspberry-pi/troubleshooting.md)
  row 1: "Locked out after SSH change" — cause (bad sshd drop-in) and recovery (console in,
  remove `/etc/ssh/sshd_config.d/99-macknet-hardening.conf`) written down in advance.
- Adversarial review `~/Projects/macknet/.claude/research/2026-06-28-pi-adversarial-review-a69fef.md`:
  "Confirm rollback path first… keep a sudo session open through every change"; fail2ban
  rejected as a net-negative lockout vector on a LAN-only key-only fleet.
- Gates codified in macknet commit `69f56ff` ("Add Raspberry Pi maintenance playbook and docs", 2026-07-02).
- [macknet/docs/synology/security.md](~/Projects/macknet/docs/synology/security.md): Auto-Block
  requires LAN allowlist "to prevent accidental lockout".

## Class 1 — Docs-only

| Gate | Rationale |
|---|---|
| Human-readable md gets `[View on <SCM>](URL)` under the title | House style, `~/.claude/CLAUDE.md` |
| Facts verified against the repo/device before written | Wrong runbooks are worse than none |
| Commit via `/git-commit` | Review gate catches stale paths/commands |

## Class 2 — Repo code

1. Run the repo's tests before committing: `uv run pytest` (macknet: unit always,
   `tests/integration/` is marked — deselect with `-m "not integration"` when offline).
2. Obey code style: stdlib preferred, **no external deps without approval**; no comments
   unless the WHY is non-obvious; prefer editing existing files (`~/.claude/CLAUDE.md`).
3. Secrets stay in `.env` (never committed); `.env.example` documents the shape.
4. Exit through `/git-commit` — its agent code-review step is the review gate.

## Class 3 — Claude-config (`dotfiles/Claude/**`)

Treat as prod-adjacent: writes are live globally the instant they land (symlink, no deploy).

1. State the blast radius before editing: which sessions/projects change behavior.
2. Skill size gate: ≤30 lines body + `## Summary` ≤5 lines that stands alone. Heavy
   instruction docs go in `references/` or `docs/`, loaded via Agent, never inline.
3. `settings.json` / hooks: validate JSON before write (`python3 -m json.tool <file>`);
   a broken hook or malformed settings degrades every session at once.
4. Rationale: the owner's hardest live problem (stated 2026-07-03) is making cheap Claude
   sessions reliably follow discipline. Bloated or broken global config burns sessions —
   the other costliest failure mode. Mechanics of these files: `claude-config` skill.
5. Exit through `/git-commit` in the dotfiles repo.

## Class 4 — Prod-touching

Never unattended. Sequence for any live host or device:

1. **Recon (read-only).** Pi fleet: `~/Projects/macknet/scripts/pi/recon.sh chris@HOST`.
2. **Rollback point, tested (taboo 1).** Pi: `scripts/pi/backup-config.sh chris@HOST`
   (captures `/etc` + manifests into gitignored `backups/`). NAS: Btrfs snapshot of the
   affected share (Snapshot Replication; snapshots at `/volume1/@sharesnap/<Share>/`,
   see [macknet/docs/synology/backup-snapshots.md](~/Projects/macknet/docs/synology/backup-snapshots.md))
   plus knowing the container-level undo (previous compose file + config dir).
3. **Test off-prod first (taboo 2).** bookshelf pattern: `docker-compose.yml` locally on
   the `local-test` flow before `docker-compose.nas.yml` on the NAS. Network gear: dry-run
   or read-back verification; no speculative controller writes.
4. **Explicit human go for anything destructive (taboo 3).** Show the exact command,
   target host/IP (Pi fleet: **wired IP only** — wifi addresses can renumber on reboot),
   and the undo. Wait.
5. **Keep a second session open** (SSH/sudo or console) through the change — never cut
   off the branch you are standing on (a69fef review, above).
6. **Verify, then log.** Pi SSH changes gate on `sshd -t` + a fresh key-only login before
   trusting them. Record what/why/undo in the maintenance log
   ([macknet/docs/raspberry-pi/maintenance-log.md](~/Projects/macknet/docs/raspberry-pi/maintenance-log.md)
   format; real entries in gitignored `fleet.local.md`).
7. Commit the repo-side artifacts via `/git-commit`.

## Other written non-negotiables (pointers, not copies)

All in `~/.claude/CLAUDE.md` — read it; do not contradict it:
no `Co-Authored-By` trailers; agent output to `.claude/research/YYYY-MM-DD-topic-{token}.md`
with `agent-token:` first line; heavy skills (update-config, code-review) only via Agent;
memory budget limits; read-only bash pre-approved, everything else asks.

## Provenance and maintenance
Date-stamped 2026-07-03; taboos owner-stated 2026-07-03. Re-verify:
`git -C ~/Projects/macknet log --oneline -3` (69f56ff still the playbook commit);
`ls ~/Projects/macknet/scripts/pi/` (recon/backup/harden scripts exist);
`sed -n '1,15p' ~/Projects/macknet/docs/raspberry-pi/troubleshooting.md` (lockout row intact);
`grep -n "local-test" ~/Projects/bookshelf/CLAUDE.md` (test-before-NAS branch flow current).
