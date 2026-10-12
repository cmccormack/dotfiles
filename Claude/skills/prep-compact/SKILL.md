---
name: prep-compact
description: Prepare a session for /compact. Back up session state compaction would lose, then print a /compact prompt and a post-compact resume prompt. Use for /prep-compact.
---

# Prep Compact

## Summary
Before /compact: promote durable facts to their real homes, write the rest to a handoff
file, then print two copy-ready blocks: the `/compact` command and the post-compact prompt.
Handoff: `<repo>/.claude/handoff/YYYY-MM-DD-<topic>-{token}.md`, token = `os.urandom(3).hex()`.

## Steps
1. Promote first. Durable conclusions go to the project's docs/TODO/memory per house rules,
   not the handoff. Note anything you couldn't place.
2. Collect what compaction flattens, from the transcript and live state:
   - `git status --short` per touched repo; uncommitted files and whether they are intended.
   - Running background tasks: ID, command, output file, what finishing means.
   - Exact values: IDs, paths, IPs, versions, measurements with units, commands that worked.
   - Decisions made and alternatives rejected, one line each with the reason.
   - User preferences or corrections stated this session; open questions awaiting the user.
   - Backups/rollback points created; in-progress step and the next 3 steps.
   Never copy secrets; name where they live instead.
3. Write the handoff (first line `agent-token: {token}`, ≤60 lines, terse bullets,
   links not pastes for anything already in a file).
4. Print, each framed as a code block:
   - `/compact Keep: <current goal>; <next step>; handoff <path>; <2-4 must-keep facts>. Drop: tool output, file dumps, superseded plans.`
   - Post-compact: `Read <handoff path>, confirm the git and background-task state still match it, then continue with <next step>. Don't re-derive what the handoff records.`
5. Reply ≤5 lines besides the blocks: handoff path + token, anything not promoted.
