---
name: claude-discipline-campaign
description: Executable campaign to make cheap Claude sessions reliably follow CLAUDE.md discipline. Load when working on session-discipline, compliance, or token-efficiency improvements; when asked to "make sessions cheaper" or "more reliable"; when enforcing CLAUDE.md rules mechanically (skill size gate, memory budget, agent-token research files, heavy-skill-via-Agent); when investigating burned sessions, token blowouts, wrong-path agents, or rules being ignored; or when deciding whether a new discipline rule should be prose or a hook.
---

## Summary
Multi-phase campaign replacing prose discipline rules with mechanical enforcement, judged
only by numbers (violation counts to zero, token/tool-call deltas) — never by eye. The
evidence that prose fails is the current violation count: rules stated in CLAUDE.md, yet
6 of 11 skills over the 30-line gate and 44 forbidden YAML fields in memory files.
Baseline measured 2026-07-03. Run phases in order; every phase has a numeric gate.

## Phases

| Phase | Do | Read |
|---|---|---|
| 0 Baseline | Re-measure with exact commands; diff against recorded numbers | [references/baseline.md](references/baseline.md) |
| 1 Enforce | Pick from the ranked enforcement menu (hooks > commit gate > prose) | [references/enforcement.md](references/enforcement.md) |
| 2 Economy | Router docs, Agent-routed heavy skills, research-file handoffs | [references/context-economy.md](references/context-economy.md) |
| 3 Measure | Re-measure cadence, promotion via change-control, retirement protocol | [references/measurement.md](references/measurement.md) |

## Known-wrong paths — do not retry
- Adding more CLAUDE.md prose rules: the current violation counts ARE the disproof.
- Growing MEMORY.md into a rulebook: it is a 10-line index, nothing else.
- Per-repo copies of global rules: they drift; global truth lives in dotfiles/Claude only.

## When NOT to use
- One-off audit or a single lint run → diagnostics-toolkit.
- settings.json/hook mechanics → claude-config; classifying/gating a config change → change-control.
- General evidence and experiment methodology → workflow-research-methodology.
