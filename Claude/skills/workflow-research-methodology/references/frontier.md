# Research Frontier — open problems worth attacking here

All five are **open/candidate** problems, not commitments. Each has evidence the current
approach falls short, a portfolio-specific asset, three concrete first steps, and a
falsifiable result condition. Owner-confirmed context (2026-07-03): the hardest problem is
making cheap Claude sessions follow the discipline; the costliest failures are burned
sessions and network lockouts.

## 1. Session-discipline enforcement (research angle only)

Execution of the enforcement campaign belongs to `claude-discipline-campaign` — this entry
is only the research question: **which discipline rules are mechanically checkable, and does
mechanical checking beat prose rules for cheap models?**

- **Why current approach falls short:** rules are enforced verbally and violated in practice —
  every inspected memory file still carries `node_type`/`originSessionId` despite the strip
  rule, and skills exceed the 30-line gate (steamdeck `ansible-review.md` ~85 lines)
  (`~/Projects/.claude/research/2026-07-03-claude-conventions-f6c417.md` §7).
- **Asset:** a working enforcement prototype already exists —
  `~/Projects/macknet/.claude/hooks/check_skill_size.py` (blocks heavy skills, word-limits
  skill loads) — plus per-repo `session.jsonl` hook logging.
- **First three steps:**
  1. Inventory checkable rules: read `~/.claude/CLAUDE.md` and tag each rule check-by-script /
     check-by-hook / prose-only.
  2. Baseline: write a violations counter over the current tree (skill line counts, memory
     YAML fields, research-file naming regex) and record the number.
  3. Port `check_skill_size.py` into `dotfiles/Claude/hooks/` scope as the first global guard
     (via change-control — that write is live config).
- **Result when:** the violations counter shows a baseline N today and 0 one week after the
  first hook lands, with no manual cleanup commits in between.

## 2. Cross-session memory compaction under the 10/15-line budgets

- **Why current approach falls short:** the budget (MEMORY.md ≤10 lines, files ≤15, strip
  non-schema YAML) is doc-only and actively violated (f6c417 §7.2). Worse, memory doesn't
  survive repo renames: the ubiquiti→macknet rename left duplicate memory dirs
  (`~/.claude/projects/-Users-chris-Projects-ubiquiti/` and `...-macknet/` both carry
  `sdk_research.md` with the same aiounifi-rejected decision).
- **Asset:** the budgets are already specified, memory dirs are plain markdown, and the L1
  inline-decision convention gives a compaction target ("aiounifi rejected, use aiohttp").
- **First three steps:**
  1. `ls ~/.claude/projects/*/memory/` and count per-file lines + disallowed YAML fields.
  2. Write a `memory-audit` script (stdlib) reporting budget/field violations per project.
  3. Hand-compact one project (macknet) to spec; note what information had to be dropped.
- **Result when:** the audit reports 0 violations across all projects AND a later session
  demonstrably retrieves a compacted decision (cites the L1 line, doesn't re-research it).

## 3. Multi-agent orchestration cost — when does a subagent pay for itself?

- **Why current approach falls short:** proposer/critic and skeptic/promote pairs are heavy
  house practice (steamdeck `skill-proposer-a3f7c2.md`/`skill-critic-17b9c5.md`,
  `2026-06-08-skeptic-analysis-44290d.md`/`2026-06-08-promote-analysis-ef5cfd.md`) but the
  break-even point is unmeasured — delegation is chosen by taste. Burned sessions are one of
  the two costliest failure modes, so a wrong guess is expensive.
- **Asset:** `session.jsonl` in every repo records per-session, per-tool-call events
  (2139 lines in steamdeck, 1378 in macknet as of 2026-07-03), and `/token-audit` already
  analyzes it.
- **First three steps:**
  1. Extract Agent/Task-tool events from each repo's `session.jsonl` with `jq`, grouped by
     session id.
  2. For 5 delegated and 5 non-delegated sessions of similar scope, compare main-thread
     tool-call counts and `/token-audit` findings.
  3. Predict a threshold ("delegation pays when the exploration would exceed ~N tool calls
     inline") BEFORE step 2's comparison — per methodology.md §2.
- **Result when:** a measured threshold with numbers attached, stated as a one-line rule a
  cheap session can apply, and it correctly classifies the next 5 delegation decisions.

## 4. Homelab observability — the cheapest signal that isn't silence

- **Why current approach falls short:** zero CI across the portfolio despite real pytest
  suites (portfolio survey aa87cf), and no monitoring: two Pis went ~9 months unpatched
  while `apt-daily.service` reported SUCCESS — a green no-op masked the failure
  (`~/Projects/macknet/.claude/research/2026-06-28-pi-adversarial-review-a69fef.md`).
  Silence and false-green are currently indistinguishable. Network lockouts (the other
  costliest failure) are also invisible until a human notices.
- **Asset:** macknet already has async UniFi + Synology API clients and SSH access to the Pi
  fleet — the collection layer exists; only the signal is missing.
- **First three steps:**
  1. Define the 3 checks that would have caught the apt case: package-list age, last
     successful upgrade timestamp, reachability of each fleet host.
  2. Write one stdlib script in macknet emitting a single-line pass/fail per host.
  3. Schedule it on the NAS or a Pi (cron) writing to a dated log — no dashboard, a file.
- **Result when:** re-introducing the known fault (remove the APT periodic config on a test
  box) flips the signal to fail within one scheduled run.

## 5. Skill-triggering precision — do trigger-rich descriptions actually fire?

- **Why current approach falls short:** the older global skills have no frontmatter at all
  (f6c417 §2) so they never auto-trigger, and the new library's trigger-rich descriptions
  (this skill included) are written on faith — no measurement exists that a session facing a
  matching task actually loads the right skill.
- **Asset:** the PreToolUse hook already logs every Skill invocation to `session.jsonl`, so
  fire/no-fire is observable after the fact without new plumbing.
- **First three steps:**
  1. `grep '"tool":"Skill"' ~/Projects/*/.claude/logs/session.jsonl` — establish the current
     fire rate baseline (likely near zero for the new library; confirm).
  2. Write 10 one-line task prompts per skill that SHOULD trigger it and 5 that should not
     (store as a fixture file in the skill library).
  3. Run them in fresh cheap-model sessions; log which skill (if any) loaded.
- **Result when:** a precision/recall table per skill from ≥15 prompts each, and one
  description rewrite measurably moves its numbers.

## When NOT to use this file

- Executing the discipline campaign (problem 1's operational side) → `claude-discipline-campaign`.
- Day-to-day evidence for commits (tests, pre-push verification) → `validation-and-qa`.
- These are research candidates: do not present any of them as an adopted practice.

## Provenance and maintenance

Written 2026-07-03 from `~/Projects/.claude/research/2026-07-03-portfolio-survey-aa87cf.md`,
`2026-07-03-claude-conventions-f6c417.md`, and the cited macknet/steamdeck research files.
Re-verify with:

- `wc -l ~/Projects/*/.claude/logs/session.jsonl` — logging still live (was 4248 total).
- `ls ~/.claude/projects/*/memory/` — memory-violation evidence still current.
- `ls ~/Projects/*/.github/workflows 2>/dev/null` — "no CI" claim still true.
- Retire any problem here once adopted or refuted; record the verdict in a dated research file.
