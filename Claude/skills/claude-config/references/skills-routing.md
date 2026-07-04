# Skills: formats, triggering, size gate

## Two formats coexist in ~/.claude/skills (= dotfiles/Claude/skills, live symlink)

1. **Legacy flat `<name>.md`** — no YAML frontmatter; plain purpose line first, optional
   `Usage: /name <args>`, numbered `## Step N` sections or When/Invocation/Output/Notes.
   Current files: `git-commit.md` (67 lines), `review-skill.md` (14), `token-audit.md` (14),
   `web_fetch.md` (41). Status: production.
2. **SKILL.md directory format** (this library): `<name>/SKILL.md` with YAML frontmatter
   (`name:`, `description:`) + `references/*.md` for detail. The `description` is what the
   harness matches against the conversation to auto-load the skill — make it trigger-rich
   (verbs + situations), because a vague description means the skill silently never fires.
   Status: new, in migration; claude-config is one of the first.

Per-project skills live in `<repo>/.claude/skills/*.md` (macknet: `unifi.md`, `synology.md`;
steamdeck: `steam-input.md`, `ansible-review.md`, `ansible-run.md`) — flat format, opening
with a standalone `## Summary`.

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
1. Is it listed? Flat: `ls ~/.claude/skills/*.md`. Directory: `ls ~/.claude/skills/*/SKILL.md`.
2. Directory format: frontmatter must parse — `name:` matches dir name, `description:` present.
3. Description too vague → rewrite with concrete trigger phrases; new sessions pick it up.
4. Explicit `/name` invocation bypasses description matching — use it to isolate the problem.

## Provenance and maintenance
Verified 2026-07-03 against ~/.claude/skills, macknet and steamdeck skill dirs, and CLAUDE.md.
Re-verify: `ls ~/.claude/skills && wc -l ~/.claude/skills/*.md`.
