# User Preferences — Chris McCormack

## Communication
- Terse. No trailing summaries of what was just done.
- One sentence updates while working, not running commentary.
- No emoji unless asked.
- File references as markdown links `[file.py:42](file.py#L42)`, not backticks.
- End-of-turn: one or two sentences max — what changed and what's next.
- Short, considered response to each prompt — think before answering.
- Push back when an idea is weak or a better practice exists. State the concern directly, don't just comply.

## Permissions
- Read-only bash commands (ls, find, grep, cat, head, tail, wc, stat, file, echo, pwd, git log/status/diff, etc.) are pre-approved. Run them without asking.

## Agent & Context Discipline
- Delegate broad exploration to Explore subagents, not inline grep chains.
- **Agent output is mandatory-file:** agents always write full detail to `.claude/research/YYYY-MM-DD-topic-{token}.md` where `{token}` is 6 hex chars from `os.urandom(3).hex()` — prevents collision across parallel agents. First line of the file must be `agent-token: {token}`. Main thread includes the token in its summary so the file is traceable. Caller reads the file if it needs more detail.
- Don't re-read files just written — Edit/Write track state.
- Use TodoWrite for multi-step tasks; mark done immediately when complete.
- Prefer editing existing files over creating new ones.
- **Never invoke a heavy skill directly.** Skills that load large instruction documents (update-config, code-review, etc.) must be invoked via an Agent — the docs stay in the subagent's context, only the result returns to the main thread.
- **Skill size gate:** project skills must be ≤30 lines + a `## Summary` header (≤5 lines) that works standalone. Known heavy bundled skills: `update-config`, `code-review` — always route via Agent.

## Memory Budget
- `MEMORY.md` index: 10 lines max — one line per artifact, path + one-phrase hook.
- Memory files: 15 lines max. Strip YAML fields not in the schema (`node_type`, `originSessionId`, etc.).
- L1 decisions are inline in memory files — one-sentence conclusions, not file pointers. "aiounifi rejected, use aiohttp" not "see sdk_research.md".
- Prune anything derivable from the codebase (file paths, function names, architecture). Keep only non-obvious decisions and rejected alternatives.

## Skills
- `/git-commit` — review, commit, correlate, and push session changes
- `/review-skill <name>` — audit a skill file for token efficiency and clarity
- `/token-audit` — analyze `.claude/logs/session.jsonl`
- `/web_fetch` — fetch JS-rendered pages via headless Chromium; tool at `~/.claude/tools/web_fetch.py`

## Markdown Conventions
- Human-readable markdown files (README, CLAUDE.md, docs, etc.) include a `[View on <SCM>](URL)` link under the title.

## Code Style
- No comments unless the WHY is non-obvious.
- No docstrings for obvious functions.
- No error handling for scenarios that can't happen.
- Standard library preferred; no external dependencies without approval.
