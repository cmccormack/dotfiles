# Phase 0 — Baseline measurement

Measure BEFORE changing anything. Every later claim ("hooks reduced violations") is a diff
against these numbers. If your measurements differ wildly from the recorded baseline,
STOP: someone or something changed the environment — re-survey (portfolio + conventions)
before acting, and record the new baseline in a research file first.

## Instruments

Primary (on disk and tested 2026-07-03; all four exit 0/1/2, stdlib-only, `--help` works):

```
python3 ~/.claude/skills/diagnostics-toolkit/scripts/skill_lint.py
python3 ~/.claude/skills/diagnostics-toolkit/scripts/memory_audit.py
python3 ~/.claude/skills/diagnostics-toolkit/scripts/research_scaffold.py
python3 ~/.claude/skills/diagnostics-toolkit/scripts/session_stats.py
```

Fallbacks (verified working 2026-07-03 — use these when scripts are absent, and to
cross-check script output the first time you trust it):

```
# Skill size gate (CLAUDE.md: body <=30 lines). Lists offenders.
for f in ~/.claude/skills/*.md ~/.claude/skills/*/SKILL.md \
         ~/Projects/*/.claude/skills/*.md; do
  [ -f "$f" ] && echo "$(wc -l < "$f") $f"; done | awk '$1>30'

# Memory: forbidden YAML fields (node_type, originSessionId). Files, then total count.
grep -rlc 'node_type\|originSessionId' ~/.claude/projects/*/memory/*.md
grep -rc  'node_type\|originSessionId' ~/.claude/projects/*/memory/*.md \
  | awk -F: '{s+=$NF} END {print s}'

# Memory: files over 15-line budget; MEMORY.md indexes over 10.
for f in ~/.claude/projects/*/memory/*.md; do n=$(wc -l < "$f"); \
  [ "$n" -gt 15 ] && echo "$n $f"; done
wc -l ~/.claude/projects/*/memory/MEMORY.md

# Research files: bad names, then missing agent-token first line.
ls ~/Projects/*/.claude/research/*.md \
  | grep -Ev '/[0-9]{4}-[0-9]{2}-[0-9]{2}-.*-[0-9a-f]{6}\.md$'
for f in ~/Projects/*/.claude/research/*.md; do \
  head -1 "$f" | grep -q '^agent-token: ' || echo "missing: $f"; done

# [View on <SCM>] link presence in human-readable md (0 = missing).
grep -c 'View on' ~/Projects/{dotfiles,macknet,steamdeck,bookshelf,keylimepi}/{CLAUDE,README}.md
```

## Recorded baseline — 2026-07-03

| Metric | Baseline | Target |
|---|---|---|
| Skill files over 30-line gate | 6 of 11 (git-commit 67, ansible-review 84, ansible-run 56, synology 52, web_fetch 41, unifi 38) | 0 |
| Memory files with forbidden YAML fields | 22 of 26 files | 0 |
| Forbidden-field occurrences total | 44 | 0 |
| Memory files over 15-line budget | 10 | 0 |
| MEMORY.md indexes over 10 lines | 1 (steamdeck, 13) | 0 |
| Research files with non-conforming names | 7 of 28 (all steamdeck, old undated pattern) | 0 (rename or grandfather — decide, record) |
| Research files missing `agent-token:` first line | 0 | 0 (hold) |
| Docs missing `[View on <SCM>]` link | 4 of 8 checked (macknet CLAUDE+README, steamdeck CLAUDE, dotfiles README) | 0 |
| Heavy-skill guard hook scope | macknet only (`.claude/hooks/check_skill_size.py`) | global |
| session.jsonl (~/Projects/.claude/logs/) | 315 lines | n/a — trend input for Phase 2/3 |

## Gate

- Expect numbers at or below baseline. Below → prior enforcement is working; proceed.
- Numbers ABOVE baseline in one metric → new violations since 2026-07-03; find what wrote
  them (git log / session.jsonl) before enforcing, or the hook will fight an active writer.
- Numbers wildly different everywhere (paths missing, counts halved) → environment changed;
  re-survey, do not act on stale assumptions.

## Provenance and maintenance
Measured 2026-07-03 by running every fallback command above against the live filesystem.
Re-verify: rerun the fallback block; diff against the table. diagnostics-toolkit
instruments verified on disk and tested 2026-07-03 (this review).
