---
name: review-skill
description: Audit a skill file or custom slash command for token efficiency, clarity, and correctness. Use for /review-skill <name> or when asked to review or tighten a skill.
---

# Review Skill

## Summary
Audit a skill or custom slash command for token efficiency, clarity, and correctness.
Usage: `/review-skill <skill-name>`. Output a punch list, under 250 words.

## Steps
1. Find the skill file in `.claude/skills/<name>.md` or `~/.claude/skills/<name>.md`.
2. Read it and evaluate:
   - Description line: ≤150 chars and specific enough to trigger correctly?
   - Instructions: clear without excess prose? Could any paragraph be cut?
   - Agent delegation: does it spawn agents with minimal-summary instructions?
   - Output: does it specify a word/line cap on responses?
   - Token traps: verbose preamble, redundant steps, re-reading already-known state?
3. Output a punch list (what works / what to tighten) with concrete rewrites for
   anything bloated.
4. Keep your response under 250 words.
