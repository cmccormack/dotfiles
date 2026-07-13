---
name: chronicle-keeping
description: Capture publishable project history as you work. Load when a session does substantive project work (a feature lands, a bug is diagnosed, a decision or research finding is made, hardware behaves unexpectedly) so the moment gets appended to the repo's chronicle for later publishing via fieldnotes.
---

## Summary
Every substantive session appends notable moments to `<repo>/.claude/chronicle.md`
(loose markdown, newest at bottom). fieldnotes later turns chronicles into posts,
guides, and decision records. Capture at the moment it happens; a session that fixed
a real bug or made a real decision and appended nothing has dropped publishable history.

## What to append
One dated block per moment, a few lines each. Worth capturing: decisions (with the
rejected alternative and why), bugs (symptom, root cause, fix), research findings
(verdict + confidence + source), surprises (what was expected vs what happened),
metrics (tests, sizes, durations). Apply the selection test: a detail earns its place
only if cutting it would change the outcome, the lesson, or a laugh.

## Format
```markdown
## 2026-07-12: <one-line summary>
<2-6 lines: what happened, why it matters, key command/number if load-bearing>
```

## Rules
- Loose markdown only; do NOT invent schema keys (the fieldnotes pipeline structures later).
- Append, never rewrite history; fix errors with a dated correction block.
- No em-dashes or en-dashes (user rule).
- If the file does not exist, create it with a `# Chronicle: <repo>` title line.
- Commit it with the work it describes, not separately.
