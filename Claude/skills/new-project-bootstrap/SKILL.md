---
name: new-project-bootstrap
description: Runbook for starting any new project or repo to house standard. Load when: starting a new project, "set up a new repo", "new tool/script/package", scaffolding a Python project with uv, initializing git for a fresh directory, or bringing an existing untracked/uncommitted directory (e.g. route53_mermaid) up to standard. Covers git init on main, uv scaffold, .gitignore, README/CLAUDE.md, .claude/ dirs, first commit, GitHub publish.
---

## Summary
Two numbered runbooks that produce a repo meeting house standard: git on `main` as
`Chris McCormack <mack.developer@gmail.com>` (GitHub: cmccormack), Python via uv with
`requires-python` pinned, .gitignore covering env/cache/.claude noise, non-empty README +
CLAUDE.md each with a `[View on GitHub]` link, `.claude/{research,logs}/` dirs, a
`.claude/chronicle.md` stub (see `chronicle-keeping` skill; feeds fieldnotes publishing),
first commit via `/git-commit`. Retrofit variant reorders the same steps for existing dirs.

## Routing

| Situation | Read |
|---|---|
| Brand-new project from an empty directory | [references/new-repo-runbook.md](references/new-repo-runbook.md) |
| Existing uncommitted/untracked dir to bring up to standard | [references/retrofit-runbook.md](references/retrofit-runbook.md) |
| Checking whether a repo is "done" bootstrapping | [references/definition-of-done.md](references/definition-of-done.md) |

## When NOT to use this skill
- Configuring Claude Code itself (settings, hooks, skills, permissions) → `claude-config`.
- README/CLAUDE.md content and templates → `docs-house-style` (this skill only says when to create them).
- Python env mechanics beyond scaffolding (uv troubleshooting, deps) → `python-env`.
- The project will touch prod systems (NAS, network gear, Pi fleet) → also load `change-control` before any prod-facing work; bootstrap itself is repo-local and safe.
