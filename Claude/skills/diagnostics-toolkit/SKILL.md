---
name: diagnostics-toolkit
description: "Executable measurement scripts for Claude-harness hygiene. Use when auditing skill or memory or session hygiene, measuring token usage from session.jsonl, checking CLAUDE.md convention compliance (skill size gate, memory budget, research naming), scaffolding a research file with an agent token, or whenever you need numbers instead of impressions. MEASURE, don't eyeball."
---

## Summary
Stdlib-only Python scripts that turn CLAUDE.md's verbal gates into measured numbers:
skill size lint, memory budget audit, research-file scaffold/validator, session-log stats.
Run a script (each has `--help`), read exit code (0 clean, 1 violations, 2 bad input),
consult the interpretation guide for thresholds and which sibling skill fixes what.

## Routing

| Need | Run / read |
|---|---|
| Audit skills vs 30-line gate + Summary + description triggers | `scripts/skill_lint.py [--root DIR]` |
| Audit memory budget, forbidden YAML, dangling links | `scripts/memory_audit.py [--root DIR]` |
| Mint a research file (token + first line) | `scripts/research_scaffold.py <topic> [--dir DIR]` |
| Validate existing research filenames/tokens | `scripts/research_scaffold.py --check [--dir DIR]` |
| Session.jsonl tool counts, re-reads, size | `scripts/session_stats.py [--file PATH]` |
| What columns mean, 2026-07-03 baselines, action thresholds | [references/interpretation-guide.md](references/interpretation-guide.md) |

## When NOT to use
- Interactive prose analysis of the current session's log → legacy `/token-audit` skill (these scripts give it raw numbers; don't duplicate its recommendations step).
- Fixing what you measured → claude-config (config/skill edits), claude-discipline-campaign (systematic enforcement), docs-house-style (doc fixes).
