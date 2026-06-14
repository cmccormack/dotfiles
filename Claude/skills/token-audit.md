Analyze `.claude/logs/session.jsonl` and report on tool usage patterns.

Steps:
1. Read `.claude/logs/session.jsonl` (each line is a JSON event)
2. Count calls by tool name
3. List the top 5 most-called tools with counts
4. For Bash events, list the 5 most-repeated commands (exact or near-duplicate)
5. Flag any patterns that suggest context bloat:
   - Same file read multiple times
   - Bash commands run > 3 times in a session
   - Large numbers of Read calls on the same path
6. Recommend 1-3 specific changes to reduce token waste next session.

Output: a short table + 1-3 bullet recommendations. Under 200 words total.
