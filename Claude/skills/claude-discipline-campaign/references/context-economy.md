# Phase 2 — Context economy

Goal: fewer tokens per task class in cheap sessions, verified by session_stats.py deltas
(on disk and tested 2026-07-03), fallback: tool-call counts per session id from
`~/Projects/*/.claude/logs/session.jsonl` (events are `{ts,event}` or
`{ts,session,tool,detail:{cmd|prompt|file}}`; verified 2026-07-03, 315 lines in the
Projects log).

## Patterns to apply (all already proven in-portfolio — extend, do not invent)

1. Router-doc skills: SKILL.md = standalone `## Summary` (<=5 lines) + routing table;
   heavy content lives in references/* loaded only when routed. Precedent: change-control,
   claude-config, this skill. Converting the 6 oversized skills to this shape IS the
   Phase 1 cleanup — do it there, measure here.
2. Heavy skills via Agent, mechanically: Option A hook makes inline invocation impossible.
   The docs load in the subagent; only the result returns.
3. Research-file handoffs: agents write full detail to
   `.claude/research/YYYY-MM-DD-topic-{token}.md` (token = 6 hex, first line
   `agent-token: {token}`) and return only a summary + token. Scaffold with
   research_scaffold.py (on disk and tested 2026-07-03); fallback mint:
   `python3 -c "import os; print(os.urandom(3).hex())"`.
4. Index-first docs: load `docs/INDEX.md`, then only the file needed (macknet/bookshelf
   pattern); steamdeck's `.claude/cache/<slug>.json` lookup-before-research for repeat
   questions.

## Gate

Pick 2-3 recurring task classes (e.g. git-commit runs, research dispatches, config edits).
Expect: tool-call count and Read-volume per class trends DOWN after Phase 1+2 versus the
same class pre-campaign. If a class trends UP → the router indirection costs more than it
saves for that class; record the finding and exempt that class rather than forcing it.
If session.jsonl shows repeated Reads of the same large file in one session → a missing
router or cache entry; fix the doc, not the model.

## Provenance and maintenance
Written 2026-07-03. Log schema verified against ~/Projects/.claude/logs/session.jsonl;
patterns verified in change-control/claude-config skills and macknet/steamdeck CLAUDE.md.
Re-verify: `tail -3 ~/Projects/.claude/logs/session.jsonl | jq .` and
`ls ~/.claude/skills/*/references/`.
