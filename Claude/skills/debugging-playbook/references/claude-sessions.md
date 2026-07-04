# Claude Session Triage

The costliest recurring failure in this portfolio is a burned session: token blowout,
an agent down the wrong path, rules dropped mid-session, or work lost between sessions.
Core doctrine: **durable state lives on disk, not in context** — research files
(`.claude/research/YYYY-MM-DD-topic-{token}.md`, first line `agent-token: {token}`),
`.claude/logs/session.jsonl` (written by the global PreToolUse hook in any repo with a
`.claude/` dir), git-notes session correlation (`refs/notes/claude`), and steamdeck-style
`.claude/cache/*.json`. Recover from those before re-deriving anything.
Config mechanics → `claude-config`; measurement scripts → `diagnostics-toolkit`.

## Symptom table

| Symptom | Likely cause | Discriminating check | Recovery |
|---|---|---|---|
| Session slow/expensive, context blowing up | Repeated reads, exploration done inline, heavy skill loaded in main thread | `jq -r '.tool' .claude/logs/session.jsonl \| sort \| uniq -c \| sort -rn \| head` and for hot files `jq -r '.detail.file // empty' .claude/logs/session.jsonl \| sort \| uniq -c \| sort -rn \| head` | Run `/token-audit` (reads the same log, gives specific fixes). Delegate exploration to Explore agents; route heavy skills (update-config, code-review) via Agent; load docs via the INDEX-first pattern |
| Agent came back with the wrong thing | Vague prompt, or it hit a permission wall silently | Read its mandatory research file: `ls .claude/research/ \| grep <token>` — **no file at all means the dispatch was malformed** (missing token/absolute-path instructions) | Re-dispatch with a corrected prompt, the token convention, and an absolute `Write(...)` path — never just re-run the same prompt |
| Agent reports WebFetch blocked | Agents inherit only the GLOBAL settings (`~/.claude/settings.json` ← dotfiles), never project settings | Error names the domain | Add `WebFetch(domain:<d>)` to dotfiles `Claude/settings.json` immediately and re-run (steamdeck CLAUDE.md rule). Never `WebFetch(*)` |
| Rules ignored mid-session | Compaction dropped the emphasis; CLAUDE.md alone can't enforce automation | Did the session compact recently? | Re-state the rule inline. If it's a "whenever X do Y" behavior, it needs a hook — route `update-config` via Agent |
| Work lost between sessions | Session ended before commit; findings were only in context | `git status --short` for dirty files; `jq -r '.detail.file // empty' .claude/logs/session.jsonl \| sort -u` lists every file the tools touched; grep `.claude/research/` for the findings | Run `/git-commit` (stages session files, reviews, commits, correlates). Findings not in a research file are gone — that's why the file is mandatory |
| "Which session made this commit?" | — | `git notes --ref=claude show <sha>` → `{session, ts, tool_calls}` | Cross-reference with session.jsonl timestamps |
| Stray agent branches/worktrees cluttering a repo | Background agent worktree never cleaned | `git branch --list '*agent*'; ls .claude/worktrees 2>/dev/null` | Confirm merged/abandoned, then delete branch + worktree dir; gitignore `.claude/worktrees/` |
| No session.jsonl to analyze | Repo lacks a `.claude/` dir — the log hook exits unless one exists | `ls -d .claude` | `mkdir -p .claude` to opt in for next session |

## Documented burns (evidence, not folklore)

- steamdeck committed a full agent worktree (`.claude/worktrees/agent-abf29b3f8851c49dc/`)
  plus a matching long-lived branch — repo bloat found in the 2026-07-03 portfolio survey.
- macknet 43498f7 "Fix stale unifi.md references after macknet restructure" — skills/docs
  went stale after a rename; when a refactor lands, grep skills and CLAUDE.md for old paths.
- Older steamdeck research files (`vdf-format-93bb56.md` etc.) predate the dated naming
  convention and are effectively invisible to date-based recovery greps — search by topic too.

## Provenance and maintenance

Verified 2026-07-03 against ~/.claude/CLAUDE.md, ~/Projects/dotfiles/Claude/{hooks/log-tool-use.sh,skills/token-audit.md,skills/git-commit.md,scripts/}, ~/Projects/steamdeck/CLAUDE.md, and macknet/steamdeck git logs.
Re-verify: `cat ~/Projects/dotfiles/Claude/hooks/log-tool-use.sh; git -C ~/Projects/steamdeck branch -a`
