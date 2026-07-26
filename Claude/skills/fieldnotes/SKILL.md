---
name: fieldnotes
description: Private publishing platform. Load before publishing any dev blog post, guide, or other publication from chronicles or session work, in any repo.
---

## Summary
All real publishing goes through `~/Projects/fieldnotes`: gated, private, static
publications (dev blog today; guides next; QRG/runbook/decision-record backlog).
Chronicles are the raw feed (see `chronicle-keeping`). Claude Artifacts are fine as
a quick private preview, but they host on claude.ai; anything meant to live goes
through fieldnotes. Load `fieldnotes/CLAUDE.md` before working there.

## Routing

| Need | Read |
|---|---|
| Anything in the platform: status, plans, invariants | `~/Projects/fieldnotes/CLAUDE.md` |
| Which publication type fits this material | `fieldnotes/docs/publication-types.md` |
| Prose rules (Chris-seeded, governs ALL published prose) | `fieldnotes/docs/style-guide.md` |
| Post pipeline: chronicle schema, engine, gates | `fieldnotes/docs/plans/fable-plan-devblog.md` |

## Rules that reach outside the repo
- Draft posts written elsewhere (e.g. a repo's docs/blog/) are source material;
  fieldnotes is the publication of record.
- Style guide governs prose; Chris iterates it, agents obey it. No em/en dashes.
- Zero JS on published pages; theme.css is approved, never restyle it.

## When NOT to use
- Capturing moments as they happen -> chronicle-keeping (fieldnotes consumes those).
- Repo-internal docs (README, runbooks in their own repo) -> docs-house-style.
