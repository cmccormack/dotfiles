Review a skill or custom slash command for token efficiency, clarity, and correctness.

Usage: /review-skill <skill-name>

Steps:
1. Find the skill file in `.claude/skills/<name>.md` or `~/.claude/skills/<name>.md`
2. Read it and evaluate:
   - Description line: is it ≤ 150 chars and specific enough to trigger correctly?
   - Instructions: are they clear without excess prose? Could any paragraph be cut?
   - Agent delegation: does it spawn agents with minimal-summary instructions?
   - Output: does it specify a word/line cap on responses?
   - Token traps: verbose preamble, redundant steps, re-reading already-known state?
3. Output a punch list (what works / what to tighten) with concrete rewrites for anything bloated.
4. Keep your response under 250 words.
