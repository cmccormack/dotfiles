# The Commit Path — /git-commit

Every class of change exits through the `/git-commit` skill
([~/.claude/skills/git-commit.md](~/.claude/skills/git-commit.md)). Do not commit around
it with raw `git commit`: the skill carries the review gate, the message rules, and the
session-to-commit correlation that raw git skips. This file summarizes the flow so other
skills can route to it — the skill file itself is the executable source of truth.

## The seven steps (as implemented in git-commit.md)

| # | Step | Mechanism | Stop condition |
|---|---|---|---|
| 1 | Discover session files | Agent runs `bash ~/.claude/scripts/git-session-files.sh .claude/logs/session.jsonl` | Empty list → stop; user confirms staging set |
| 2 | Stage + full diff | `git add …` then `git diff --staged` via Agent | Empty diff → stop |
| 3 | Code review gate | Agent reviews the staged diff; clean pass = exactly `LGTM` | Anything else → user chooses fix or commit-anyway |
| 4 | Draft message | Agent writes conventional-commit message: `type: summary` ≤72 chars, optional 2–3 bullet body, **no mention of Claude/AI** | Shown to user; proceeds without waiting |
| 5 | Commit | `git commit -m '<message>'` via Agent | Hook rejection → surface error, stop, no retry |
| 6 | Correlate session | `bash ~/.claude/scripts/git-correlate.sh .claude/logs/session.jsonl` — writes `{session, ts, tool_calls}` JSON to git notes `refs/notes/claude`, NOT the message | — |
| 7 | Push | `bash ~/.claude/scripts/git-push-notes.sh` | Push failure → report, no auto-retry |

## Hard rules baked into the path

- **Never `Co-Authored-By:` trailers** (`~/.claude/CLAUDE.md`, Git section; also encoded in
  dotfiles commit `b086304`). This overrides any harness default that appends one.
- Conventional commits format; subject ≤72 chars.
- Each shell/git step runs via Agent so command output stays out of main-thread context.
- Session traceability lives in git notes, keeping commit messages clean:
  `git notes --ref=claude show <sha>` to inspect;
  `git config --add remote.origin.push refs/notes/claude` to push notes automatically.

## What "route through /git-commit, never around it" means for skill authors

- A skill that produces file changes ends with "commit via `/git-commit`" — it does not
  embed its own `git commit` command.
- Exception: none for commits. Read-only git (`log`, `status`, `diff`) is pre-approved
  and fine anywhere.
- If a change must NOT be committed yet (half-finished prod work), say so explicitly and
  leave the tree dirty — dirty-but-honest beats a commit that dodged review.

## Provenance and maintenance
Date-stamped 2026-07-03 from `~/.claude/skills/git-commit.md` and
`~/.claude/scripts/{git-session-files,git-correlate,git-push-notes}.sh` (all present).
Re-verify: `ls ~/.claude/scripts/` and `head -5 ~/.claude/skills/git-commit.md`;
`git -C ~/Projects/dotfiles log --oneline | grep b086304` (no-trailer rule commit).
