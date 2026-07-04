# Research File Convention

Source rules: `~/.claude/CLAUDE.md` "Agent & Context Discipline". Practiced in
`.claude/research/` of macknet, bookshelf, steamdeck (and `~/Projects/.claude/research/`).

## Contract

- Path: `<project>/.claude/research/YYYY-MM-DD-topic-{token}.md`
- `{token}` = 6 hex chars: `python3 -c "import os; print(os.urandom(3).hex())"` —
  prevents collisions across parallel agents.
- First line of the file, exactly: `agent-token: {token}`
- The main thread includes the token in its summary so the file is traceable; the caller
  reads the file only if it needs more detail than the summary.
- Agent write permissions must use absolute paths:
  `Write(/Users/chris/Projects/<proj>/.claude/research/*)` (steamdeck CLAUDE.md rule).

## What belongs in one
Full agent findings that would bloat the main context: sources examined, evidence,
decisions with reasoning, uncertainties/open questions, rejected options. Multi-agent
patterns (architect/critic, proposer/critic) write one file per agent, separate tokens.

## What does NOT belong
- Structured lookup data an agent will re-query → `.claude/cache/<slug>.json`
  (steamdeck pattern: `{"created","query","summary","data"}`).
- Durable one-line decisions → promote to a memory file ([memory-schema.md](memory-schema.md)).
- Procedures worth repeating → a skill.

Older `topic-{hex}.md` files (no date prefix) predate this convention — do not imitate.

## Provenance and maintenance
Derived 2026-07-03 from `~/.claude/CLAUDE.md` (Agent & Context Discipline),
steamdeck CLAUDE.md, and live files in `~/Projects/{macknet,bookshelf,steamdeck}/.claude/research/`.
Re-verify: `ls ~/Projects/macknet/.claude/research/ | head` (date-topic-6hex names) and
`head -1 ~/Projects/.claude/research/2026-07-03-portfolio-survey-aa87cf.md`.
