# New-machine bootstrap

## 1. Install uv
Official standalone installer (verified live at docs.astral.sh/uv, 2026-07-03):
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Installs to `~/.local/bin/uv` (current machine runs uv 0.9.5 from there). `brew install uv`
is the documented alternative.

## 2. Restore dotfiles
```sh
git clone git@github.com:cmccormack/dotfiles.git ~/Projects/dotfiles
cd ~/Projects/dotfiles
uv sync
uv run playwright install chromium          # for Claude/tools/web_fetch.py
uv run python scripts/sync/sync.py --dry-run
uv run python scripts/sync/sync.py
```
Notes: default branch is `master` (not main). `sync.py` reads `scripts/sync/manifest.conf`
(`~/src:repo/dest` per line) and symlinks home paths to repo copies — including
`~/.claude/{CLAUDE.md,settings.json,skills,hooks,scripts}`, zsh config, gitconfig, ssh config,
VS Code settings. On a fresh machine the home path is absent, so it just creates the symlink;
a manifest entry with no repo copy either is reported `skip`.

Credential scanner (`scripts/sync/check_credentials.py`): runs automatically inside `sync.py`
whenever a real home file is about to be **moved into the repo** (first-time adds), not on
already-linked or restore-only entries. Detects AWS/GitHub/Slack/Stripe keys, Bearer tokens,
credentials in URLs, PEM private keys, generic `password=`/`token=`/`api_key=`; ignores `${VAR}`.
Findings open an interactive review (delete lines / skip); otherwise the move is blocked.
Bypass: `--skip-cred-check`. Standalone scan: `uv run python scripts/sync/check_credentials.py <path>`.

## 3. Recreate any repo's environment
```sh
git clone git@github.com:cmccormack/<repo>.git ~/Projects/<repo>
cd ~/Projects/<repo>
uv sync                          # creates .venv on the pinned Python, installs dev group
cp .env.example .env             # macknet, bookshelf only — then fill in values
```
Extras per repo:
- bookshelf: `uv run playwright install chromium` (setup_cwa.py drives a browser).
- steamdeck: `uv run ansible-galaxy collection install -r requirements.yml`.
- keylimepi: no Python env — its `setup.sh` runs on the Pi itself.

uv downloads the interpreter pinned in `.python-version` automatically; to pre-install:
`uv python install 3.13` (and `3.14` for steamdeck).

## Provenance and maintenance
Verified 2026-07-03: installer command fetched live from docs.astral.sh/uv; sync tool behavior
read from `~/Projects/dotfiles/scripts/sync/{sync.py,check_credentials.py,manifest.conf}` and
dotfiles CLAUDE.md; remotes/branches via `git -C ~/Projects/dotfiles remote -v` equivalent.
Re-verify: `uv --version`, `sed -n 130,175p ~/Projects/dotfiles/scripts/sync/sync.py`,
`cat ~/Projects/dotfiles/scripts/sync/manifest.conf`.
