# Known traps

## Running system python instead of uv run
- Symptom: `ModuleNotFoundError`, or code behaving as if on the wrong Python version.
- Cause: PATH `python3` on this machine is a pyenv shim at **3.12.8**; repos pin 3.13/3.14.
  Homebrew also ships 3.14.5 — none of these are the project venv.
- Fix: always `uv run <cmd>` (or `uv run python ...`) from the repo root. Never bare `python3`.

## steamdeck: pytest not declared
- Symptom: `uv run pytest` in steamdeck fails — pytest is not in pyproject or uv.lock,
  and `.venv/bin` has no pytest (verified 2026-07-03), yet `tests/` contains real tests.
- Cause: dev dependency-group was never added.
- Fix (one-off): `uv run --with pytest pytest tests/`. Permanent fix is adding a
  `[dependency-groups] dev` like macknet's — a dependency addition, so get approval
  (see SKILL.md Policy) and route through change-control.

## uv.lock drift
- Symptom: `uv lock --check` fails; `uv sync`/`uv run` re-resolves unexpectedly; teammates
  (or agents) get different versions.
- Cause: pyproject.toml edited without regenerating the lock.
- Fix: `uv lock && git add uv.lock` (lock is committed in all four repos). Both macknet and
  steamdeck locks verified fresh 2026-07-03.

## Per-repo Python-pin mismatch
- Symptom: syntax/feature errors when copying code or agents between repos.
- Cause: steamdeck pins **3.14** (`requires-python >=3.14`); macknet/bookshelf/dotfiles pin 3.13.
- Fix: check `.python-version` before assuming 3.13; `uv sync` per repo handles the rest.

## Playwright browser missing
- Symptom: playwright error "Executable doesn't exist" from bookshelf `setup_cwa.py` or
  dotfiles `Claude/tools/web_fetch.py`.
- Cause: playwright the package is installed by `uv sync`, but browsers are a separate download.
- Fix: `uv run playwright install chromium` in that repo.

## macknet integration tests fail without .env
- Symptom: auth failures/429s running `uv run pytest tests/integration`.
- Cause: needs a live controller plus `.env` (copied from `.env.example`); conftest loads it
  via `load_dotenv()`.
- Fix: create `.env`; run unit tests (`tests/unit`) when no controller is reachable.

## __pycache__ in git — currently a non-issue
- Claim circulating that dotfiles committed a `__pycache__`; checked 2026-07-03: **no repo has
  one committed** (`git ls-files | grep pycache` empty everywhere; all gitignore `__pycache__/`).
  Dirs exist on disk only. If suspected later, re-run that check before "fixing".

## Editing ~/.claude/skills is editing dotfiles
- Symptom: uncommitted changes appearing in dotfiles after "just tweaking a skill".
- Cause: `~/.claude/skills` (and settings/hooks/scripts) are symlinks into
  `~/Projects/dotfiles/Claude/` — edits are live globally and dirty the repo.
- Fix: treat them as dotfiles changes; commit via change-control conventions.

## Provenance and maintenance
Verified 2026-07-03 from repo pyprojects/locks/venvs, `.gitignore` + `git ls-files` per repo,
`python3 --version` vs `uv python list`, and macknet CLAUDE.md. Re-verify:
`python3 --version`, `for r in macknet bookshelf steamdeck dotfiles; do git -C ~/Projects/$r ls-files | grep pycache; (cd ~/Projects/$r && uv lock --check); done`,
`ls ~/Projects/steamdeck/.venv/bin | grep pytest`.
