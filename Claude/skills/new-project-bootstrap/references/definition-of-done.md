# Definition of done — bootstrap complete

All measurable; run from the repo root.

- [ ] On `main` with ≥1 commit: `git branch --show-current` = `main`; `git log --oneline | head -1` non-empty.
- [ ] Author on every commit is `Chris McCormack <mack.developer@gmail.com>`; no `Co-Authored-By` trailers: `git log --format='%an <%ae>%n%(trailers)'`.
- [ ] Clean tree — no stray uncommitted work: `git status --short` empty (or only deliberate WIP).
- [ ] No tracked junk: `git ls-files | grep -E '__pycache__|\.pyc$|^\.env$|\.venv/|\.claude/(logs|research|cache|worktrees)'` empty.
- [ ] `.gitignore` contains the house block (`.env`, `.DS_Store`, `.claude/logs/`, `.claude/research/`, `.claude/settings.local.json`).
- [ ] `README.md` non-empty (`wc -c` > 0) with H1 + `[View on GitHub]` link; `CLAUDE.md` exists — structure per `docs-house-style`.
- [ ] Python repos: `pyproject.toml` has real `description`, `requires-python` pin, dev deps in `[dependency-groups]`; `uv.lock` + `.python-version` committed; `uv run python -c 'import sys; print(sys.version)'` matches the pin.
- [ ] Package repos: `tests/` exists and `uv run pytest` passes. If the repo ships skills, run the lint gate: `python3 ~/.claude/skills/diagnostics-toolkit/scripts/skill_lint.py` (on disk and tested 2026-07-03).
- [ ] `.claude/research/` and `.claude/logs/` dirs exist.
- [ ] If published: `git remote get-url origin` = `git@github.com:cmccormack/NAME.git` and README link matches.
- [ ] If prod-touching: `change-control` classification done before any deploy.

## Provenance and maintenance

Written 2026-07-03 from the same repo audit as the runbooks. Re-verify the identity and
remote conventions:

```bash
git config --global user.email          # mack.developer@gmail.com
for r in ~/Projects/{macknet,bookshelf,keylimepi,steamdeck}; do git -C $r remote get-url origin; done
```
