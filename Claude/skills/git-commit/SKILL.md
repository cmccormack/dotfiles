---
name: git-commit
description: Review, commit, correlate, and push the current session's changes. Use when asked to commit, /git-commit, or at session end with uncommitted work. Stages session-changed files, agent-reviews the diff, conventional commit, git-notes correlation, push.
---

# Git Commit Skill

## Summary
Stage the files changed this Claude session, agent-review the staged diff, commit with a
generated conventional message, correlate the commit to the session via git notes, push.
Every shell/git step runs via Agent to keep command output out of the main context.

## Steps
1. **Discover session files.** Via Agent: `bash ~/.claude/scripts/git-session-files.sh
   .claude/logs/session.jsonl`; return the raw file list (or the error). Show the list; ask
   **"Stage all of these files? (yes / list files to exclude / cancel)"**. Empty → stop.
2. **Stage.** Via Agent: `git add <file1> <file2> ...` then `git diff --staged`; return the
   full untruncated diff. Empty diff → nothing to commit, stop.
3. **Code review.** Via Agent, pass the staged diff: review for bugs, security issues,
   obvious errors, unfinished/debug code; flag only real problems (file:line, brief), else
   exactly `LGTM`. Not LGTM → show issues, ask **"Fix first, or commit anyway?"**; stop on fix.
4. **Draft message.** Via Agent, pass the staged diff: conventional commits (type: summary
   first line, 72 char max), optional 2–3 bullet body only if non-obvious, no Claude/AI
   mention, no trailing newline; raw text only. Show the draft, then proceed immediately.
5. **Commit.** Via Agent: `git commit -m '<message>'`; return full output incl. hash. On
   failure (pre-commit hook, etc.) surface the full error and stop; do not retry.
6. **Correlate.** Via Agent: `bash ~/.claude/scripts/git-correlate.sh
   .claude/logs/session.jsonl` — silently attaches the session ID via git notes.
7. **Push.** Via Agent: `bash ~/.claude/scripts/git-push-notes.sh`; return full output
   incl. warnings. On failure report the full error; do not retry automatically.

## Notes
Notes live in `refs/notes/claude` as JSON `{session, ts, tool_calls}`; view with `git notes
--ref=claude show <sha>`; auto-push: `git config --add remote.origin.push refs/notes/claude`.
`CLAUDE_CODE_SESSION_ID` is process-scoped — stable across agents and compaction.
