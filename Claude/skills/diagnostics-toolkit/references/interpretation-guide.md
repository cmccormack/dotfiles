# Diagnostics Toolkit — Interpretation Guide

Thresholds come from `~/.claude/CLAUDE.md` (Agent & Context Discipline, Memory Budget).
Baselines below were measured 2026-07-03 against the live filesystem. Exit codes for all
audit modes: 0 clean, 1 violations found, 2 bad input path.

## skill_lint.py

Scans both flat `<root>/*.md` and `<root>/*/SKILL.md` (default root `~/.claude/skills`).

| Column | Meaning |
|---|---|
| BODY | Line count after YAML frontmatter, leading/trailing blanks stripped. Gate: <=30 |
| SUMMARY | Content (non-blank) lines in the `## Summary` section, or `missing`. Gate: <=5 |
| DESC | Frontmatter description trigger quality: `ok`, `weak` (no "when"/"use"), `-` (none) |
| ISSUES | All violations; SKILL.md-style files additionally require frontmatter name + description |

Baseline 2026-07-03: 13 skills, 6 with violations. The four legacy flat skills all fail —
git-commit.md (67 lines, no Summary), web_fetch.md (41 lines), review-skill.md and
token-audit.md (no Summary). Two directory skills had weak descriptions. New skills in the
library should score `ok` across the board; a regression here is a real regression.

Action: any violation in a skill you are authoring — fix before finishing. Violations in
legacy flat skills — rewrite via **claude-config**; a library-wide sweep is
**claude-discipline-campaign** territory. Prose/tone fixes: **docs-house-style**.

## memory_audit.py

Scans `<root>/*/memory/` (default root `~/.claude/projects`).

| Column | Meaning |
|---|---|
| LINES | MEMORY.md: total lines (gate <=10). Other files: body lines after frontmatter (gate <=15) |
| ISSUES | `forbidden:` = YAML keys outside name/description/metadata.type (e.g. node_type, originSessionId); `dangling:` = `[[link]]` or `(file.md)` target missing in the memory dir |

Baseline 2026-07-03: 26 files across 4 projects, 23 with violations — every non-index file
still carries `metadata.node_type` + `metadata.originSessionId`; steamdeck MEMORY.md is 13>10;
bookshelf project_kobo_setup.md body 16>15; one dangling `[[project-context]]` in macknet
nas_access.md (file is `project_context.md` — underscore vs hyphen).

Action: forbidden fields are mechanical strips — safe to fix on sight when touching a memory
file. The near-universal violation rate makes this a **claude-discipline-campaign** job, not
piecemeal edits.

## research_scaffold.py

Create mode prints `path:` and `token:` — put the token in your summary so the file is
traceable. Check mode validates `YYYY-MM-DD-<topic>-<6hex>.md` naming and that line 1 is
`agent-token: <token>` matching the filename.

Baseline 2026-07-03: macknet 7/7 ok; bookshelf 3/3 ok; steamdeck 18 files, 7 violations —
all pre-convention `topic-<hex>.md` names (tokens/first lines are fine). Legacy names are
reported as violations; renaming them is optional migration, not urgent.

Action: always use create mode instead of hand-naming research files. A `bad first line` or
`token mismatch` on a *new* file means the authoring agent ignored the convention — flag it.

## session_stats.py

Parses hook-format lines: `{ts,event}` (session_stop) and `{ts,session,tool,detail}` where
detail is `{cmd}` (Bash), `{file}` (Read/Edit/Write), `{prompt}` (WebFetch/Agent), or null
(WebSearch). Unknown shapes and unparseable lines are counted, never fatal.

| Metric | Meaning / threshold |
|---|---|
| Size / ~tokens | bytes/4 rough token cost of reading the whole log |
| Tool calls % | Bash 28-49% and Read 19-35% are normal here (baselines below) |
| Top Bash commands | Same command >3x in one session = cache or skill candidate |
| Files read more than once | The context-bloat signal; >5 reads of one file = routing failure |

Baselines 2026-07-03: macknet log 1,378 lines / ~53k tokens / 6 sessions; worst re-read
13x `ubiquiti/docs/reference/api.md`, 50 files read >1x. Projects log 430 lines / ~21k tokens.
All lines parsed clean (0 unparseable) in both.

Action: heavy re-reads → tighten the doc-routing skill for that area (INDEX-first pattern);
repeated identical Bash → add a `.claude/cache/` lookup (steamdeck pattern). For a prose
recommendation pass on the current session, hand these numbers to legacy `/token-audit`.

## Provenance and maintenance

Written 2026-07-03 from live measurements of `~/.claude/skills`, `~/.claude/projects/*/memory`,
and `.claude/logs/session.jsonl` in Projects/macknet/steamdeck/bookshelf. Thresholds mirror
`~/.claude/CLAUDE.md`. Re-verify baselines with:

    scripts/skill_lint.py
    scripts/memory_audit.py
    scripts/research_scaffold.py --check --dir <repo>/.claude/research
    scripts/session_stats.py --file <repo>/.claude/logs/session.jsonl

If CLAUDE.md budgets change, update the constants at the top of skill_lint.py
(BODY_MAX/SUMMARY_MAX) and memory_audit.py (INDEX_MAX/BODY_MAX/ALLOWED_*) and this guide.
