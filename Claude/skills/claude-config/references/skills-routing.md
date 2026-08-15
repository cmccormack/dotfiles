# Skills: formats, triggering, size gate

## One working format: SKILL.md directories (~/.claude/skills = dotfiles/Claude/skills, live symlink)

**Flat `<name>.md` skills are dead** (found 2026-08-15): the harness stopped loading them,
silently. Symptom: the skill vanishes from the slash-command list and the session skill
inventory; typing its /name autocompletes to something else. The four legacy flat files
(git-commit, review-skill, token-audit, web_fetch) were converted that day to
`<name>/SKILL.md` with frontmatter, bodies unchanged; pickup was immediate, no restart.

**SKILL.md directory format**: `<name>/SKILL.md` with YAML frontmatter (`name:`,
`description:`) + `references/*.md` for detail. The `description` is what the harness
matches against the conversation to auto-load the skill: make it trigger-rich
(verbs + situations), because a vague description means the skill silently never fires.

Per-project skills: same rule, `<repo>/.claude/skills/<name>/SKILL.md`. Repos still
carrying flat files (macknet: `unifi.md`, `synology.md`; steamdeck: `steam-input.md`,
`ansible-review.md`, `ansible-run.md`) have invisible skills until converted.

## Rules (from ~/.claude/CLAUDE.md)
- **Size gate:** project skills ≤30 lines + `## Summary` header ≤5 lines that works standalone.
  Enforcement is mostly verbal; macknet has the only mechanical check — a `PreToolUse`
  hook on matcher `Skill` running `.claude/hooks/check_skill_size.py` (repo-local, not global).
- **Heavy-skill rule:** never invoke a heavy skill inline — route via an Agent so its docs
  stay in the subagent's context. Known heavy: `update-config`, `code-review`.
- Authoring a new skill (body structure, voice, references layout)? Single home:
  `docs-house-style/references/skill-authoring.md` — this file covers routing mechanics only.
  Lint with `diagnostics-toolkit/scripts/skill_lint.py`.

## Debugging "my skill didn't fire"
0. Is it a flat `.md` file? Dead format; convert to `<name>/SKILL.md` first (see above).
1. Is it listed? `ls ~/.claude/skills/*/SKILL.md`.
2. Directory format: frontmatter must parse — `name:` matches dir name, `description:` present.
3. Description too vague → rewrite with concrete trigger phrases; new sessions pick it up.
4. Explicit `/name` invocation bypasses description matching — use it to isolate the problem.

## Provenance and maintenance
Verified 2026-07-03 against ~/.claude/skills, macknet and steamdeck skill dirs, and CLAUDE.md.
Re-verify: `ls ~/.claude/skills && wc -l ~/.claude/skills/*.md`.
