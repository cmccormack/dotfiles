# Git Commit Skill

Stage files changed this Claude session, run a code review, commit with a generated message, correlate the commit to this session, and push.

## Step 1 — Discover session files

Run via Agent:
> "Run this command and return the raw output as a list of file paths, one per line: `bash ~/.claude/scripts/git-session-files.sh .claude/logs/session.jsonl`. If the command errors, report the error."

Show the user the file list. Ask: **"Stage all of these files? (yes / list specific files to exclude / cancel)"**

If the list is empty, tell the user no session files were found and stop.

## Step 2 — Stage files

Run via Agent:
> "Stage these files in git and return the full staged diff. Commands: `git add <file1> <file2> ...` then `git diff --staged`. Return the full diff output — do not truncate it."

If the diff is empty after staging, tell the user there is nothing to commit and stop.

## Step 3 — Code review

Spawn an Agent with the staged diff from Step 2:
> "Review this git diff for bugs, security issues, obvious errors, or unfinished/debug code. Flag only real problems (file:line, brief description). If nothing is wrong, respond with exactly: LGTM
>
> Diff:
> <paste diff here>"

If the review returns anything other than LGTM, show the issues to the user and ask: **"Fix these issues first, or commit anyway?"** Stop if they choose to fix.

## Step 4 — Draft commit message

Spawn an Agent with the staged diff from Step 2:
> "Write a git commit message for this diff. Rules: conventional commits format (type: summary on first line, 72 char max), optional body with 2–3 bullet points explaining what changed and why (only if non-obvious), no mention of Claude or AI assistance, no trailing newline. Return the raw message text only.
>
> Diff:
> <paste diff here>"

Show the draft to the user. Proceed to Step 5 immediately — do not wait for approval.

## Step 5 — Commit

Run via Agent:
> "Run: `git commit -m '<approved message>'` and return the full output including the commit hash."

If commit fails (pre-commit hook rejection, etc.), surface the full error to the user and stop. Do not retry.

## Step 6 — Correlate session

Run via Agent:
> "Run: `bash ~/.claude/scripts/git-correlate.sh .claude/logs/session.jsonl` and return the output."

This silently attaches the Claude session ID to the commit via git notes — not in the commit message.

## Step 7 — Push

Run via Agent:
> "Run: `bash ~/.claude/scripts/git-push-notes.sh` and return the full output including any warnings."

If push fails, report the full error. Do not retry automatically.

## Notes

- Session correlation is stored in `refs/notes/claude` as JSON: `{session, ts, tool_calls}`.
- To view: `git notes --ref=claude show <sha>`
- To always push notes automatically: `git config --add remote.origin.push refs/notes/claude`
- `CLAUDE_CODE_SESSION_ID` is a process-scoped env var — stable across agents and compaction within the same Claude process.
