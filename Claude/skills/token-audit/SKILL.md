---
name: token-audit
description: Analyze .claude/logs/session.jsonl for tool usage patterns and token costs. Use for /token-audit or when asked where session tokens went.
---

# Token Audit

## Summary
Analyze `.claude/logs/session.jsonl` (one JSON event per line) for tool usage patterns
and context bloat. Output: a short table + 1-3 bullet recommendations, under 200 words.

## Steps
1. Read `.claude/logs/session.jsonl`.
2. Count calls by tool name; list the top 5 most-called tools with counts.
3. For Bash events, list the 5 most-repeated commands (exact or near-duplicate).
4. Flag context-bloat patterns: same file read multiple times; Bash commands run
   more than 3 times in a session; large numbers of Read calls on the same path.
5. Recommend 1-3 specific changes to reduce token waste next session.
