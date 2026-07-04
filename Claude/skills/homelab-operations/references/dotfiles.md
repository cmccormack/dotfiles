# dotfiles — day-to-day sync operations

Repo: `~/Projects/dotfiles`. Manifest-driven symlink sync: first run **moves** each
listed home file into the repo and symlinks it back; later runs verify links and
no-op. Bootstrap (uv sync, playwright, Raspbian setup.sh): python-env skill.

## Running a sync

```bash
cd ~/Projects/dotfiles
uv run python scripts/sync/sync.py --dry-run   # ALWAYS preview first — real run moves files
uv run python scripts/sync/sync.py             # sync
uv run python scripts/sync/sync.py --skip-cred-check   # bypass scanner (see gate below)
```

Per-entry outcomes: `ok` (already linked), `move`/`link` (synced this run),
`skip` (source missing), `warn` (source is a foreign symlink — left alone),
`blocked` (credentials found).

Manifest: `scripts/sync/manifest.conf`, one `~/source:repo/dest` per line, `#`
comments. Add a file = add a line, run `sync.py`. Directories sync as a whole
(e.g. `~/.claude/skills:Claude/skills`).

## What the credential scanner blocks

`check_credentials.py` scans every file before it enters the repo. On findings it
opens a review TUI (`credential_review.py`): delete the flagged lines, skip (sync
anyway), or abort (blocked). Patterns: `password/secret/api_key/token=` assignments
(6+ chars), AWS key IDs + secrets, GitHub `ghp_/gho_/ghs_/ghr_/github_pat_` tokens,
Bearer tokens, `user:pass@` URLs, PEM private keys, Slack `xox*`, Stripe
`sk_/pk_live|test`, 32+ hex-char assignments. `${VAR}` references are not flagged.
One report per line; deletion removes whole lines, then rescans.

Standalone scan / scrub:

```bash
uv run python scripts/sync/check_credentials.py <path>          # report, exit 1 on hits
uv run python scripts/sync/check_credentials.py --filter <path> # remove flagged lines in-place
```

**STOP — `--skip-cred-check` and `--filter` are override paths: skip means a
secret may be committed, filter rewrites the file. Eyeball the findings and get
human go before either (change-control).**

## Live-config warning

`~/.claude/{CLAUDE.md,settings.json,hooks,skills,scripts}` are symlinks into this
repo (see manifest) — editing `~/Projects/dotfiles/Claude/...` changes the live
global Claude config for every session immediately. Skill/settings editing
conventions: claude-config skill.

Tests: `uv run pytest scripts/sync/tests/`.

## Provenance and maintenance

Documented 2026-07-03 from `~/Projects/dotfiles` source (`sync.py`,
`check_credentials.py`, `manifest.conf`, CLAUDE.md). Re-verify:

```bash
git -C ~/Projects/dotfiles log -1 --format='%h %cs'
grep -vE '^#|^$' ~/Projects/dotfiles/scripts/sync/manifest.conf
grep -n 'add_argument' ~/Projects/dotfiles/scripts/sync/sync.py
```
