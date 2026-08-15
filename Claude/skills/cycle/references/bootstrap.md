# Bootstrap Mode

Trigger: no scope found from cwd up to repo root (scoping.md).

1. Concurrency check first (concurrency.md), another session could be mid-bootstrap.
2. Resolve scope per scoping.md; if ambiguous (cwd is not the repo root and has no
   existing scope above or below it), ask which directory the new trackers belong to.
3. AskUserQuestion: "No tracker files at `<resolved path>`, create TODO.md/ISSUES.md/
   RESUME.md from the house templates?" No, stop, do nothing.
4. Search for existing ad hoc tracker-like content to migrate, scoped to the resolved
   directory and its own CLAUDE.md if present, in order:
   - CLAUDE.md `## Status` / "Open items:" section.
   - Any "RESUME HERE" / "session handoff" marker in existing docs.
   - README.md "Status" column entries marked anything other than "Implemented"/"Active".
5. Show what was found and where each piece would land (TODO.md vs ISSUES.md vs
   RESUME.md) per the split rules in
   `docs-house-style/references/todo-issues-resume-template.md`; ask for
   confirmation before writing, migration looks lossy even when it isn't, get
   explicit sign-off.
6. Write the three files from templates, with migrated content merged in. Never
   duplicate: content that moves out of CLAUDE.md's Status section must be removed
   from there in the same commit, not left in both places.
7. Commit via `/git-commit` (Class 1, docs-only, see change-control gates.md).
8. Hand off to normal-mode.md using the freshly written RESUME.md, or if bootstrap
   itself was the whole session, close per session-end.md.
