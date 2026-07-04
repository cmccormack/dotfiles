# Skill Authoring — This Library

Format for skills in `~/Projects/dotfiles/Claude/skills/` (symlinked LIVE to
`~/.claude/skills` — edits are global and instant; route changes through change-control).
The docs-house-style skill itself is the template: copy its structure for new skills.

## Layout

```
skills/<name>/
  SKILL.md
  references/*.md
```

Legacy flat skills (`git-commit.md`, `token-audit.md`, no frontmatter) exist; new skills
use the directory format above.

## SKILL.md
- YAML frontmatter: `name:` matching the directory; `description:` trigger-rich —
  enumerate concrete load-when situations ("Load when: writing any README...; creating an
  INDEX doc; unsure of markdown conventions") so routing works without opening the body.
- Body ≤30 lines (`~/.claude/CLAUDE.md` skill size gate):
  1. `## Summary` first, ≤5 lines, standalone — states scope + source of authority.
  2. `## Routing` table: `| Task | Read |` rows pointing at `references/*.md`.
  3. `## When NOT to use` — route adjacent tasks to sibling skills by name.

## references/*.md
- Imperative voice, terse, `~` for user paths, tables over prose.
- Heavy detail lives here, loaded on demand — never in SKILL.md.
- **Ground truth only:** every rule/template element traceable to a real file or a dated
  owner statement. No invented conventions.
- Cross-reference sibling skills instead of duplicating their content.
- Every reference ends with `## Provenance and maintenance`: verification date, sources,
  and runnable re-verification commands.

## Voice
Matches procedural skills (git-commit, ansible-review): imperative, numbered steps for
procedures, explicit output caps and stop conditions in bold, shell/git work delegated
"Run via Agent" to keep command output out of the main context.

## Provenance and maintenance
Derived 2026-07-03 from `~/.claude/CLAUDE.md` (Skill size gate), sibling skills
change-control and claude-config, and legacy `~/.claude/skills/*.md`. Re-verify:
`ls ~/.claude/skills` (symlink target) and
`head -12 ~/Projects/dotfiles/Claude/skills/change-control/SKILL.md`.
