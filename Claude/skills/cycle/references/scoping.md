# Scoping

A repo can have more than one tracker scope: a root-level set for the project as a
whole, and additional independent sets in subfolders that represent a genuinely
separate stream of work (a subproject, a service, a host). This mirrors how
directory-scoped skills and per-directory CLAUDE.md files already work in this
environment, nearest-ancestor wins.

1. From the invoking working directory, walk upward looking for a directory that
   contains **all three** of `TODO.md`, `ISSUES.md`, `RESUME.md` together. Require
   all three as a unit, a directory with only one or two is not a valid scope, treat
   it as not-found and keep walking (prevents half-migrated or stray files from being
   mistaken for a real scope).
2. Stop walking at the git repo root (`git rev-parse --show-toplevel`), never search
   above it.
3. If a scope is found below the repo root (e.g. `gaming/steamdeck/`), that is the
   active scope for this invocation, not the repo root, even if the repo root also
   has its own tracker set. A session invoked from `gaming/steamdeck/` works that
   scope's queue; a session invoked from `gaming/` root works the root queue. They
   are independent backlogs, on purpose.
4. If no scope is found anywhere from cwd up to repo root, this is bootstrap mode
   (bootstrap.md) at the **current working directory**, not automatically the repo
   root. Ask Chris which scope he means: "Create trackers here in
   `<cwd-relative-path>`, or at the repo root `<repo>/`?" Never assume, subfolder
   scoping only exists because Chris asked for it to be a real choice.
5. A repo may end up with a root scope plus N subfolder scopes over time (e.g. a
   `gaming/` root scope today, `gaming/steamdeck/` and `gaming/library/` later if
   Chris chooses to split them out). `/cycle` never auto-creates a subfolder scope on
   its own initiative, splitting out a new scope is always a bootstrap-mode,
   human-confirmed action.

## Provenance
Adopted 2026-08-15, `.claude/plans/if-we-dno-t-already-serialized-cupcake.md`.
