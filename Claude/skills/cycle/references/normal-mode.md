# Normal Mode

Trigger: RESUME.md exists at the resolved scope.

1. Resolve scope (scoping.md), then concurrency check (concurrency.md).
2. Read RESUME.md/TODO.md/ISSUES.md at the resolved scope; correlate `## Next task`
   against the matching heading/entry. Stale reference (renamed/removed/already
   resolved), say so, pick the next reasonable item from ISSUES.md Open or TODO.md's
   first unchecked item; never silently guess.
3. Set `## Claimed by`, commit that alone first (cheap, makes the claim visible to
   any concurrent session fast). Announce the task in one line. Surface
   `## Preserved questions` via AskUserQuestion **before** starting work, this is the
   mechanism that satisfies "questions preserved for a fresh session, not asked only
   at the end."
4. Classify the work via `change-control` taxonomy before touching anything. Class 4
   discovered mid-task, stop immediately, never execute destructively; write the
   blocker to ISSUES.md and state to RESUME.md, end cleanly per session-end.md.
5. Work the task against its `## Done when` criterion. New clarifying questions
   mid-work get appended to RESUME.md `## Preserved questions` immediately, not held
   only in context (a session that dies before finishing loses anything held only in
   context, never anything already written to disk).
6. On a checkpoint-worthy completion: verify against `## Done when`, commit via
   `/git-commit` (its review gate applies unchanged), clear `## Claimed by`, loop to
   step 2 if more queued work exists at this scope.
7. On blocker or empty queue: rewrite RESUME.md fully (`## Next task` = the next
   thing, or "queue empty, see TODO.md"), update ISSUES.md if a new blocker was
   found, clear `## Claimed by`, commit the tracker updates via `/git-commit`. Then
   follow session-end.md exactly, ending the final message with the required
   closing line; the Stop hook enforces this, don't rely on remembering it.
