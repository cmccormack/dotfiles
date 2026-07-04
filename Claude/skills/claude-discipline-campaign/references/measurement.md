# Phase 3 — Measurement loop, promotion, retirement

Success is numbers, never eyeballed. The campaign metrics:

| Metric | Source | Target |
|---|---|---|
| Skill-gate violations | skill_lint.py (tested 2026-07-03) / baseline.md fallback | 0 |
| Memory forbidden fields + over-budget files | memory_audit.py (tested 2026-07-03) / fallback | 0 |
| Research naming + agent-token compliance | research_scaffold.py check (tested 2026-07-03) / fallback | 0 non-grandfathered |
| Missing [View on] links | fallback grep | 0 |
| Tokens / tool-calls per task class | session_stats.py (tested 2026-07-03) / session.jsonl counts | trending down vs 2026-07-03 baseline |

## Cadence

Re-measure (full Phase 0 block): immediately after enabling any enforcement change, then
at the start of any session that loads this skill. A measurement takes seconds; drift
discovered late costs a burned session.

## Promotion protocol (experiment → adopted)

An enforcement mechanism is promoted only when: (1) its metric hit target, (2) it survived
one deliberate-violation test (expect block), and (3) one normal working session ran with
no false positives. Then: route the config through change-control (Claude-config class —
live via symlink), commit via /git-commit, and add a one-line L1 decision to the relevant
memory file ("skill gate enforced by PostToolUse hook, prose rule retired"). Never promote
on "seems fine".

## Retirement protocol (experiment → rejected)

If a mechanism misses target, false-positives on normal work, or costs more than it saves
(Phase 2 gate): revert the settings/hook change (change-control + /git-commit), write the
evidence to `.claude/research/YYYY-MM-DD-topic-{token}.md` per workflow-research-methodology
— what was predicted, what was observed, why rejected — and record the one-line rejection
in memory so no future session retries it. A fenced-off path with numbers attached stays
fenced; one without gets retried and burns a session.

## Gate

Expect all violation metrics at 0 within two working sessions of Phase 1 completion.
- Still nonzero and the offending files are NEW → the hook has a scope hole; fix matcher/paths.
- Still nonzero and files are OLD → cleanup pass incomplete; finish it, this is debt not drift.
- Metrics at 0 but token trends flat → discipline was not the token sink; the blowouts come
  from elsewhere (investigate with session_stats.py / token-audit before inventing fixes).

## Provenance and maintenance
Written 2026-07-03 against the baseline in references/baseline.md. Re-verify: rerun the
Phase 0 fallback block and `jq .hooks ~/.claude/settings.json`; diagnostics-toolkit
scripts verified on disk and tested 2026-07-03 (this review); fallbacks remain for cross-checks.
