# Concurrency Safety

Every `/cycle` session may be running alongside another Claude session in the same
repo (not an isolated worktree). Before ANY read that decides "what's next" and
before ANY write:

1. `git status` plus `git log --oneline -10`, never assume the working tree matches
   what this session last saw.
2. **Re-read RESUME.md/TODO.md/ISSUES.md immediately before writing**, not just at
   session start, the gap between read and write is exactly where two sessions
   collide. `git diff HEAD -- RESUME.md TODO.md ISSUES.md` at the resolved scope
   path; if another session wrote a newer RESUME.md since this session started,
   re-read and re-plan rather than clobber.
3. Never `git add -A`. Stage only the specific tracker files this session wrote, plus
   whatever `git-session-files.sh` reports; same discipline `/git-commit` already
   enforces (this skill calls it, never reimplements staging).
4. If `## Claimed by` in RESUME.md is already set and not stale (recent, no commit
   gap suggesting abandonment), ask Chris before taking over rather than assuming the
   claim is dead.
5. If `git status` shows uncommitted changes NOT made by this session (e.g. another
   session's in-flight work), do not touch or stage them; note their presence in this
   session's RESUME.md `## State` so the next session knows the repo was busy.
6. Commit at natural checkpoints (after each completed task, not just at session end),
   smaller windows for two sessions to collide on the same tracker file.

## Provenance and maintenance
Derived from `feedback_parallel_sessions.md` (documented habit, real incident: a
parallel session had already committed near-identical docs before this session tried
to commit its own) and `/git-commit`'s existing never-`-A` staging. The `## Claimed
by` marker and re-read-before-write discipline were added after researching prior art
(`tick-md`'s task-claim step, the Zep "markdown is not agent memory" critique on
read/write race windows). Re-verify: `grep -n "git add -A"
~/Projects/dotfiles/Claude/skills/git-commit/SKILL.md` (must return nothing).
