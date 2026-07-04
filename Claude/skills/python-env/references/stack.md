# Standard stack per repo

uv is the only package manager in the live set (no requirements.txt/poetry/pipenv).
`uv.lock` is committed in all four Python repos; `.venv/` and `__pycache__/` gitignored.
uv on this machine: 0.9.5 at `~/.local/bin/uv`. uv-managed interpreters installed: 3.13.9, 3.14.0.

| Repo | requires-python | .python-version | Runtime deps | Dev deps | Compose |
|------|-----------------|-----------------|--------------|----------|---------|
| macknet | >=3.13 | 3.13 | aiohttp>=3.9, pyyaml>=6.0 | `[dependency-groups] dev`: pytest, pytest-asyncio, python-dotenv, pytest-mock | `docker-compose.yml` — service `unifi`, `build: .` (local Dockerfile), `env_file: .env` |
| bookshelf | >=3.13 | 3.13 | fpdf2, playwright, python-dotenv | none | `docker-compose.yml` (service `calibre-web-automated`, container `cwa-library`, port 8083) + `docker-compose.nas.yml` NAS override |
| steamdeck | >=3.14 | 3.14 | ansible>=14.0.0 | **none — pytest not declared despite tests/** (see traps) | none |
| dotfiles | >=3.13 | 3.13 | pytest, playwright, html2text (declared as runtime deps) | none | none |
| keylimepi | — | — | no Python: bash `setup.sh` + static HTML only | — | none |

## Conventions
- Create/refresh env: `uv sync` (installs the `dev` dependency-group by default where one exists;
  auto-installs the pinned interpreter from `.python-version` if missing).
- Execute anything: `uv run <cmd>` — e.g. `uv run pytest tests/unit`, `uv run python -m macknet`.
- macknet is a packaged project (`[tool.uv] package = true`) with console scripts:
  `uv run macknet`, `uv run macknet-query`, `uv run macknet-inventory`.
- macknet quirk: `[project.optional-dependencies] dev = []` is an empty leftover — real dev deps
  live in `[dependency-groups]`. Add dev deps there, not to the optional-dependencies table.
- Secrets: `.env` + `.env.example` in macknet and bookshelf; never committed (gitignored).
  macknet conftest calls `load_dotenv()` so integration tests pick up `.env` automatically.
- steamdeck Ansible: collections in `requirements.yml` (community.general) —
  `uv run ansible-galaxy collection install -r requirements.yml`. ansible binaries live in the venv.
- Bookshelf NAS compose usage (deploy detail → homelab-operations):
  `docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d` — Synology has compose v1
  (hyphenated) only.

## Provenance and maintenance
Verified 2026-07-03 against each repo's pyproject.toml, .python-version, uv.lock, .gitignore,
compose files, and `.venv/bin` contents. Re-verify:
`for r in macknet bookshelf steamdeck dotfiles; do cat ~/Projects/$r/pyproject.toml ~/Projects/$r/.python-version; done`,
`uv --version`, `ls ~/Projects/*/docker-compose*.yml`.
