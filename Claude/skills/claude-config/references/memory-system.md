# Memory system (config mechanics)

Schema, budgets, and body rules live in ONE place:
`docs-house-style/references/memory-schema.md`. This file covers only where memory
lives and how to change it safely.

## Layout (machine-local, NOT synced to dotfiles)
`~/.claude/projects/<flattened-cwd>/memory/` — e.g.
`~/.claude/projects/-Users-chris-Projects-macknet/memory/`. Verified present for:
macknet, steamdeck, bookshelf, keylimepi, dotfiles, ubiquiti, Projects, and `~/.claude` itself.

Contents: `MEMORY.md` (index) + topic files. Observed naming families: `project_*.md`
(repo context), `feedback_*.md` (user corrections, e.g. `feedback_git_commit_no_approval.md`),
`reference_*.md` (lookups), plus ad-hoc (`sdk_research.md`, `pi_fleet.md`).

## Current compliance (verified 2026-07-03)
Indexes respect the 10-line budget. But every inspected memory file still carries
`metadata.node_type: memory` and `originSessionId` — the exact forbidden fields.
Status: convention production, enforcement absent (no lint/skill strips them). When you
touch a memory file for any reason, strip the forbidden fields in the same edit —
per the schema in docs-house-style.

## Changing safely
1. Editing memory is low-risk (machine-local, no symlink blast radius) but budget-check
   before saving per the memory-schema budgets (`wc -l`).
2. Update the MEMORY.md index line whenever a file is added/renamed/deleted.
3. Audit mechanically: `python3 ~/.claude/skills/diagnostics-toolkit/scripts/memory_audit.py`.

## Provenance and maintenance
Verified 2026-07-03 by listing `~/.claude/projects/*/memory/` and reading macknet's
MEMORY.md and sdk_research.md. Re-verify:
`wc -l ~/.claude/projects/*/memory/MEMORY.md && grep -l originSessionId ~/.claude/projects/*/memory/*.md`.
