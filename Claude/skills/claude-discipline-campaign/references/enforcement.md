# Phase 1 — Mechanical enforcement, ranked menu

Enter only after Phase 0 numbers are recorded. One enforcement change at a time; predict
the number it moves before enabling it (workflow-research-methodology: predict, then run).
Every option below that touches settings.json or hooks is a Claude-config-class change —
route through change-control, commit via /git-commit, and remember hooks are read at
session start (restart to activate).

## Option A — Hooks running the lint scripts (strongest; pick first)

Working precedent already in the portfolio: macknet registers a PreToolUse hook with
matcher `Skill` running `.claude/hooks/check_skill_size.py`, which blocks the known-heavy
bundled skills (update-config, code-review) and any project skill over 500 words with
`{"continue": false, "stopReason": ...}`. That is the pattern to promote globally.

1. Promote the heavy-skill guard: copy check_skill_size.py into `dotfiles/Claude/hooks/`,
   register PreToolUse matcher `Skill` in `dotfiles/Claude/settings.json` (lands live via
   the ~/.claude symlink). Expected effect: heavy-skill-inline violations become impossible,
   not remembered. Cost: one subprocess per Skill call (milliseconds).
2. Lint on write (candidate — not implemented): must be PreToolUse matcher `Write|Edit`,
   NOT PostToolUse — verified 2026-07-04 against https://code.claude.com/docs/en/hooks.md:
   PostToolUse fires after success and CANNOT block; only PreToolUse can prevent the
   write. Scope by `tool_input.file_path` under `~/.claude/skills/` and
   `projects/*/memory/`, exit fast otherwise. Cost: one subprocess per Write/Edit
   portfolio-wide — measure before adopting (predict the token/latency delta first).
3. Stop-hook sweep: append a one-line violation summary to session.jsonl at session end.
   Weakest hook variant (reports, does not prevent) but feeds Phase 3 trend data.

Status 2026-07-04: A1 (heavy-skill guard) is LIVE globally (dotfiles aaa7809); macknet's
local copy retired (macknet 3b6ccb9). Hook events verified via claude-code-guide.

Verification: trigger the matched tool once with a deliberate violation (e.g. invoke
update-config inline; write a 40-line skill to a scratch path) — expect the block message.
Then `tail -1 ~/Projects/.claude/logs/session.jsonl` to confirm logging still works.

## Option B — /git-commit gate (medium; complements A)

Add a lint step to the /git-commit flow: before staging, run skill_lint.py + memory_audit.py
via Agent; a finding blocks the commit like the existing LGTM code-review gate.
Expected effect: nothing non-compliant reaches the dotfiles repo — catches what hooks miss
(files edited while hooks were off, hand edits outside Claude).
Cost: only fires at commit time; `~/.claude` is live via symlink, so a bad skill still runs
all session until commit. Also: edits git-commit.md itself (a 67-line gate violator —
fix its length in the same change or accept the irony deliberately, and say so).
Verification: stage a deliberately oversized skill, run /git-commit, expect the block;
revert the bait file.

## Option C — CLAUDE.md prose pointer (FENCED OFF — known-wrong path)

Adding "remember to run the lint" prose to CLAUDE.md is the already-falsified approach:
the size gate, the YAML-strip rule, and the heavy-skill rule are all IN CLAUDE.md today,
and the baseline still shows 6 oversized skills, 44 forbidden fields, and a guard hook in
only one repo. More prose does not change model behavior at Sonnet effort; the violation
count is the evidence. Only acceptable prose change: replace rule text with a one-line
pointer to this skill AFTER a mechanical gate exists, shrinking CLAUDE.md.

## Cleanup pass (do once, after A or B is live)

The baseline debt itself: strip the 44 forbidden fields, trim the 10 over-budget memory
files and steamdeck MEMORY.md, shorten/split the 6 oversized skills, add the 4 missing
[View on] links, decide rename-vs-grandfather for the 7 old research filenames (record the
decision in a research file). Gate: rerun Phase 0 — expect every count at 0 except any
explicitly grandfathered; a nonzero you cannot name means the enforcement leaks.

## Provenance and maintenance
Written 2026-07-03. Precedent verified by reading /Users/chris/Projects/macknet/.claude/
settings.json and hooks/check_skill_size.py; global hook state verified in
dotfiles/Claude/settings.json (logging hooks only — no guard). Re-verify:
`jq .hooks ~/.claude/settings.json && cat ~/Projects/macknet/.claude/settings.json`.
