# New repo runbook

Numbered, copy-pasteable. Run from `~/Projects`. Replace `NAME` throughout.

## 1. Pre-flight decisions

Answer before typing any command:

- [ ] **Name.** Repo name = project name = pyproject `name` = README H1. Decide once.
  Cautionary example: repo `bookshelf` is internally "cwa-library" — README title, docs,
  and repo name drifted apart and its CLAUDE.md still says `github.com/<your-username>`.
- [ ] **Python or not?** Docs/ops-only repos (keylimepi) skip uv entirely — steps 3 is
  Python-only. Everything else in the portfolio is Python + uv.
- [ ] **Layout.** Real package → `src/NAME/` + tests (macknet, steamdeck). One-off
  tool/ops repo → scripts at root (bookshelf, route53_mermaid).
- [ ] **Will it touch prod systems** (NAS, UniFi gear, Pi fleet, live deploys)?
  If yes → `change-control` gates apply from day one; plan rollback before first deploy.

## 2. Git init to standard

Default branch is `main`. `init.defaultBranch` is NOT set globally and dotfiles is legacy
`master` — always pass `-b main` explicitly:

```bash
mkdir NAME && cd NAME && git init -b main
```

Identity: global config is already correct — `Chris McCormack <mack.developer@gmail.com>`,
used by every recent commit in all five active repos. GitHub account is **cmccormack**
(remotes are all `git@github.com:cmccormack/*`). Do not use `mccormack-christopher` —
that appears only in a stale dotfiles README badge and is the known drift to avoid.
Never add `Co-Authored-By:` trailers.

## 3. Python scaffold (skip for docs-only repos)

```bash
uv init            # in existing dir; or `uv init NAME` to create dir + git in one step
```

`uv init` (0.9.x) generates: `pyproject.toml`, `.python-version`, `README.md` (empty),
`main.py` (hello stub — delete or replace), `.gitignore`, and runs `git init` on `main`
if no repo exists.

Pin: keep what uv writes — latest stable, currently `requires-python = ">=3.14"` with
`.python-version` `3.14` (matches steamdeck and route53_mermaid, the newest scaffolds;
older repos are `>=3.13` — do not copy those pins forward).

pyproject conventions (mirror macknet for a full package):
- `description` — replace uv's "Add your description here" placeholder.
- dev deps in `[dependency-groups] dev = [...]` (pytest, ruff) — not optional-dependencies.
- src-layout package: add `[tool.uv] package = true` and `[project.scripts]` entries.
- pytest config in `[tool.pytest.ini_options]` with `testpaths = ["tests"]`.

.gitignore: uv's template covers only `__pycache__/ *.py[oc] build/ dist/ wheels/
*.egg-info .venv`. Append the house entries every active repo carries:

```gitignore
.env
.DS_Store
.pytest_cache/
.ruff_cache/

# Claude Code — session artifacts, never committed
.claude/logs/
.claude/research/
.claude/cache/
.claude/worktrees/
.claude/settings.local.json
```

`.claude/worktrees/` matters: steamdeck committed a full agent-worktree tree plus its
branch — permanent clutter. Secrets pattern: `.env` ignored, `.env.example` committed.

## 4. Docs scaffold

Create `README.md` (non-empty — macknet and steamdeck shipped 0-line READMEs, don't
repeat that) and `CLAUDE.md`. Both open with the title then a `[View on GitHub](URL)`
link. Templates and section order → `docs-house-style` skill; do not improvise structure.

## 5. .claude scaffold

```bash
mkdir -p .claude/research .claude/logs
```

That's all. Global hooks (session.jsonl logging), skills, and tools apply automatically
via the `~/.claude` symlinks into dotfiles/Claude — nothing to install per-repo.
`.claude/settings.local.json` accumulates on its own as permissions are approved (see
`~/Projects/.claude/settings.local.json` for what one looks like: a `permissions.allow`
list) — don't hand-author it. Project-scoped skills/settings only when the repo needs
its own (macknet, steamdeck pattern); route via `claude-config`.

## 6. First commit

Use the `/git-commit` skill flow: session-file discovery → stage → agent code review
(LGTM gate) → conventional-commit message (`type: summary`, ≤72 chars, no AI mention) →
commit → session-id correlation via git notes → push. Example subject:
`feat: initial project scaffold`. Never commit around the skill; never `Co-Authored-By`.

## 7. Optional: publish to GitHub

```bash
gh repo create cmccormack/NAME --private --source . --push
```

(`--public` only for portfolio-worthy repos.) Then fill in the real
`[View on GitHub](https://github.com/cmccormack/NAME)` links in README.md and CLAUDE.md
per `docs-house-style`, and commit that via `/git-commit`.

Finish with [definition-of-done.md](definition-of-done.md).

## Provenance and maintenance

Written 2026-07-03 from live repos (macknet, bookshelf, keylimepi, steamdeck, dotfiles,
route53_mermaid), global git config, and gh auth. Re-verify before trusting:

```bash
git config --global user.name && git config --global user.email
git config --global --get init.defaultBranch   # rc=1 (unset) as of 2026-07-03
gh auth status                                  # account cmccormack
uv --version                                    # 0.9.5 at writing
grep requires-python ~/Projects/{macknet,steamdeck,route53_mermaid}/pyproject.toml
cat ~/Projects/route53_mermaid/.gitignore       # current uv init template output
```
