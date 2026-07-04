# Python / uv Environment Triage

All live repos use uv + `pyproject.toml` + `uv.lock` + `.python-version` (3.13; steamdeck pins 3.14).
Verified against uv 0.9.5. Env design questions → `python-env` skill; this is triage only.

## Symptom table

| Symptom | Likely cause | Discriminating check | Fix |
|---|---|---|---|
| `ModuleNotFoundError` for a dep listed in pyproject | Ran global `python`/`pytest`, not `uv run` | `uv run python -c 'import sys; print(sys.executable)'` — must print `<repo>/.venv/bin/python`; compare `which python` | Prefix the command with `uv run` |
| Syntax/feature errors on valid code | Interpreter version mismatch | `cat .python-version && uv run python -V` | `uv python install "$(cat .python-version)" && uv sync` |
| Dep behaves stale after editing pyproject | uv.lock not regenerated | `uv lock --check` (nonzero exit = stale) | `uv lock && uv sync` |
| `import macknet` fails under `uv run` | src-layout package not installed into .venv | check `[tool.uv] package = true` in pyproject; `uv run python -c 'import macknet'` | `uv sync` |
| Everything broken after moving repo / upgrading Python | Stale .venv with baked-in paths | any `uv run` traceback pointing at old paths | `rm -rf .venv && uv sync` |
| Integration tests raise `KeyError: 'UNIFI_HOST'` etc. | `.env` missing — clients read `os.environ[...]` directly | `ls .env` (macknet conftest calls `load_dotenv()`) | copy `.env.example` → `.env`, fill values |

## Traps

- Bare `pytest` silently uses a global env and its package versions — always
  `uv run pytest tests/unit` (macknet CLAUDE.md canonical commands all use `uv run`).
- `uv sync --locked` / `--frozen` exist for CI-style "don't touch the lock" runs; plain
  `uv sync` will happily rewrite state — use `uv lock --check` first when diagnosing.
- Ad-hoc scripts (e.g. bookshelf `kobo_set_server.py`) are run `uv run python <script>`
  from the repo root; running from elsewhere loses the project env.

## Provenance and maintenance

Verified 2026-07-03 against ~/Projects/{macknet,bookshelf,steamdeck,dotfiles} pyprojects and uv 0.9.5.
Re-verify: `uv --version; uv lock --help | grep -- --check; head -12 ~/Projects/macknet/pyproject.toml`
