---
name: git-commit
description: Review, commit, correlate, and push the current session's changes. Use when asked to commit, /git-commit, or at session end with uncommitted work. Stages session-changed files, agent-reviews the diff, conventional commit, git-notes correlation, push.
---

# Git Commit Skill

## Summary
Stage this session's changed files, agent-review the staged diff, commit with a generated
conventional message, correlate the commit to the session via git notes, push. One Agent
reads the big diff in its own context; every other step runs inline (small outputs only).

## Steps
1. **Discover.** Inline: `bash ~/.claude/scripts/git-session-files.sh .claude/logs/session.jsonl`.
   Output is git-dirty files split into `## session` (changed this session) and `## other`
   (leftovers from earlier sessions). Both empty → nothing to commit, stop. Show both lists;
   ask **"Stage session files? (yes / also include others / list exclusions / cancel)"**,
   recommending session-only.
2. **Stage.** Inline: `git add <files>`, then `git diff --staged --stat`. Empty → stop.
3. **Review + draft message.** ONE Agent, which runs `git diff --staged` itself (never
   paste the diff into the prompt or have it returned). It reviews for bugs, security issues,
   obvious errors, unfinished/debug code, flagging only real problems (file:line, brief).
   If clean it replies `LGTM` followed by a conventional commit message (type: summary,
   72 chars max; optional 2-3 bullet body only if non-obvious; no Claude/AI mention; raw
   text). Not LGTM → show the issues, ask **"Fix first, or commit anyway?"**; stop on fix.
4. **Commit.** Inline: `git commit -m '<message>'`. Show the draft, commit immediately (no
   approval pause). On failure (pre-commit hook, etc.) surface the full error, stop, no retry.
5. **Correlate + push.** Inline: `bash ~/.claude/scripts/git-correlate.sh
   .claude/logs/session.jsonl` then `bash ~/.claude/scripts/git-push-notes.sh`. Report the
   push output including warnings; on failure report fully, no automatic retry.

## Notes
Notes live in `refs/notes/claude` as JSON `{session, ts, tool_calls}`; view with `git notes
--ref=claude show <sha>`; auto-push: `git config --add remote.origin.push refs/notes/claude`.
`CLAUDE_CODE_SESSION_ID` scopes both discovery and the tool_calls count; without it (or the
log), every dirty file lands under `## other` and the count falls back to whole-log.
