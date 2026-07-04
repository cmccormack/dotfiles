# Retrofit runbook — existing uncommitted dir to standard

Same steps as [new-repo-runbook.md](new-repo-runbook.md), reordered: audit first, decide
name, then fix in place. Live example: `~/Projects/route53_mermaid` as of 2026-07-03 —
git init'd on `main` but **0 commits**, 9 untracked files, working `uv` scaffold
(`>=3.14`), stock uv .gitignore, **0-byte README.md**, leftover `main.py` hello stub,
placeholder pyproject `description = "Add your description here"`.

## 1. Audit current state

```bash
cd DIR
git status --short --branch     # repo? branch? commits?
ls -a                           # scaffold files present?
wc -c README.md CLAUDE.md 2>/dev/null
cat pyproject.toml .gitignore .python-version 2>/dev/null
git ls-files | grep -E '__pycache__|\.pyc|\.env$|worktrees'   # tracked junk?
```

## 2. Pre-flight decisions
Same checklist as new-repo step 1: confirm name (dir = repo = pyproject `name` = README
H1), prod-touching or not. Renaming is cheapest now, before the first commit.

## 3. Git to standard
- No repo → `git init -b main`. Repo on `master` with no commits → `git branch -m main`.
- Already-tracked junk (`.venv`, `__pycache__`, `.env`, `.claude/worktrees/`) →
  `git rm -r --cached PATH`, then ignore it. Steamdeck's committed agent worktree is the
  cautionary example.

## 4. Fix the scaffold
- Append the house .gitignore block from new-repo step 3 (uv's template lacks `.env`,
  `.DS_Store`, `.pytest_cache/`, all `.claude/` entries).
- Replace pyproject placeholder `description`; move dev deps to `[dependency-groups]`.
- Delete or repurpose the `uv init` `main.py` hello stub if real code lives elsewhere
  (route53_mermaid's real tool is `route53_delegation_mermaid.py`).
- Leave existing `requires-python` alone unless it blocks something — don't churn pins.

## 5. Docs + .claude
Write the 0-byte/stub README and a CLAUDE.md per `docs-house-style`;
`mkdir -p .claude/research .claude/logs`.

## 6. Commit + publish
First commit via `/git-commit` (review everything — this commit captures accumulated
uncommitted work, not a clean scaffold). Optional `gh repo create cmccormack/NAME
--private --source . --push`, then real `[View on GitHub]` links.

Finish with [definition-of-done.md](definition-of-done.md).

## Provenance and maintenance

Written 2026-07-03 from route53_mermaid's live state and the repo audit in
`~/Projects/.claude/research/2026-07-03-portfolio-survey-aa87cf.md`. Re-verify:

```bash
git -C ~/Projects/route53_mermaid status --short --branch   # still 0 commits?
git -C ~/Projects/steamdeck ls-files .claude/worktrees | head -3
```
