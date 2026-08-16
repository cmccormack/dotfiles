---
name: cycle
description: Resume cross-session work in the current repo or subfolder scope via RESUME.md/TODO.md/ISSUES.md. Use for /cycle, "resume where I left off", starting a fresh session with no context, or when asked what to work on next.
---

# Cycle

## Summary
Resolves the nearest tracker scope (references/scoping.md), reads RESUME.md if
present to find the next task, correlates against TODO.md/ISSUES.md, surfaces a
ranked top-3 "Next up" list and preserved questions before starting work, works the
task to a checkpoint or blocker, commits via `/git-commit`, writes a fresh
RESUME.md/ISSUES.md before stopping. First run in an unscoped location offers to
bootstrap.

## Routing
| Situation | Read |
|---|---|
| Where do the tracker files for this invocation live | [references/scoping.md](references/scoping.md) |
| No TODO.md/ISSUES.md/RESUME.md found at the resolved scope | [references/bootstrap.md](references/bootstrap.md) |
| RESUME.md exists at the resolved scope, normal resume flow | [references/normal-mode.md](references/normal-mode.md) |
| Any git read/write this skill does (staging, commit, other-session detection) | [references/concurrency.md](references/concurrency.md) |
| Ending a session: what must be true before stopping, closing-line format | [references/session-end.md](references/session-end.md) |

## When NOT to use this skill
- Committing already-finished work with no resume framing, use `/git-commit` directly.
- Classifying whether a change is safe, use `change-control` (this skill defers to it).
- Publishing chronicle/blog content, use `fieldnotes`, `chronicle-keeping`.
