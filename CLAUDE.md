# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[View on GitHub](https://github.com/mccormack-christopher/dotfiles)

## What this repo is

A personal dotfiles backup covering MacOS, Linux (Debian/Raspbian), VS Code, and SecureCRT. The primary tool is the sync script in `scripts/`, which keeps home directory files backed up in this repo via symlinks.

## Layout

| Dir | Purpose |
|-----|---------|
| `scripts/` | Sync tool and credential scanner (see below) |
| `Claude/` | Claude user config synced from `~/.claude/` (skills, hooks, tools, settings) |
| `MacOS/home/` | MacOS dotfiles synced from `~/` |
| `Multi-OS/` | Cross-platform bash aliases and profile files (sourced on both Mac and Linux) |
| `Linux/` | Linux-specific bash profile; `Raspbian/setup.sh` bootstraps a fresh Raspbian host |
| `MacOS/` | Mac-specific configs (motd, nano) |
| `SecureCRT/` | Color scheme and keyword highlight configs for Cisco/Viptela sessions |
| `vscode/` | VS Code settings (Mac + Windows) and two Node.js JSON utility scripts |

## Claude tools (`Claude/tools/`)

Python tools callable by Claude Code agents via Bash. Symlinked to `~/.claude/tools/`. Dependencies managed by the project venv (`uv sync`).

| Tool | Purpose |
|------|---------|
| `web_fetch.py` | Fetch JS-rendered pages via headless Chromium (Playwright) |

**Setup:**
```sh
uv sync && uv run playwright install chromium
```

Tests live in `Claude/tools/tests/` and run with `uv run pytest Claude/tools/tests/ -m "not integration"`.

## Sync tool (`scripts/`)

Backs up home directory files into this repo by moving them in and replacing them with symlinks. On a new machine, run sync to restore symlinks pointing at repo files. Managed by Python (3.13, uv).

**Key files:**
- `scripts/sync/manifest.conf` — one `~/source:repo/dest` mapping per line; comments with `#`
- `scripts/sync/sync.py` — reads the manifest and creates/validates symlinks
- `scripts/sync/check_credentials.py` — scans files for credentials before they enter the repo; blocks the move if any are found

**Commands:**
```sh
uv run pytest scripts/sync/tests/                           # run tests
uv run python scripts/sync/sync.py --dry-run                # preview what would change
uv run python scripts/sync/sync.py                          # run sync
uv run python scripts/sync/sync.py --skip-cred-check        # bypass credential scan
uv run python scripts/sync/check_credentials.py <path>      # scan a file or directory
```

**Adding a new file to sync:** add a line to `scripts/sync/manifest.conf` in the form `~/path/to/file:repo/dest/path`, then run `sync.py`. The file is moved into the repo and replaced with a symlink automatically.

**Credential scanner** checks for: AWS keys, GitHub/Slack/Stripe tokens, Bearer tokens, credentials in URLs, PEM private keys, and generic `password=`/`token=`/`api_key=` assignments. Shell variable references like `${VAR}` are not flagged.

## VS Code JSON utilities (`vscode/`)

Two Node scripts with a `chalk` dependency — install first:

```sh
npm install          # from repo root (package-lock.json is here)
```

**`clean_configs.js`** — sort a JSON file's keys alphabetically, writing `<name>-clean.json`:
```sh
node vscode/clean_configs.js vscode/mac/settings.json
# → vscode/mac/settings-clean.json
```

**`combine_json_from_files.js`** — merge two JSON files into `combined.json`:
```sh
node vscode/combine_json_from_files.js file1.json file2.json
```

**Test the combine utility:**
```sh
node vscode/tests/test.js
```

## Raspbian bootstrap

`Linux/Raspbian/setup.sh` is a one-shot script run on a fresh host. It installs: zsh, Oh My Zsh, Antigen, pyenv, pipx, poetry, and Docker (Debian GPG key method). Run as the target user, not root — it calls `sudo` internally where needed.

## Multi-OS bash aliases

`Multi-OS/.bash_aliases` contains an extensive git alias set (mirroring Oh My Zsh's `git` plugin) plus helper functions `git_current_branch` and `git_current_repository`. Source this file from `.bashrc`/`.bash_profile`.
