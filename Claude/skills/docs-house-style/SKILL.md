---
name: docs-house-style
description: Docs of record, templates, and house markdown style for this portfolio. Load when: writing or updating any README, CLAUDE.md, docs/ page, memory file, or research file; creating an INDEX/router doc; authoring or restyling a skill for this library; filling an empty/stub README (macknet, steamdeck, dotfiles); unsure of markdown conventions here (View-on-GitHub link, file refs as links, no emoji, table-heavy); or deciding whether content belongs in README vs CLAUDE.md vs a skill vs memory.
---

## Summary
One authoritative copy of every doc convention: house markdown rules (source of authority
is `~/.claude/CLAUDE.md` — this skill summarizes, never forks it), copy-paste templates for
README / per-repo CLAUDE.md / INDEX router docs, the exact memory-file schema and budgets,
the research-file naming contract, and the SKILL.md format this library uses. Empty READMEs
in macknet and steamdeck are known debt the README template exists to fix.

## Routing

| Task | Read |
|---|---|
| Markdown rules: View-on-SCM link, file-ref links, emoji, tables, voice | [references/markdown-style.md](references/markdown-style.md) |
| Write or fix a README (template + the empty-README debt list) | [references/readme-template.md](references/readme-template.md) |
| Write a per-repo CLAUDE.md; decide README vs CLAUDE.md vs skill vs memory | [references/claude-md-template.md](references/claude-md-template.md) |
| Create an INDEX/router doc; doc-economy pattern and when it pays | [references/index-pattern.md](references/index-pattern.md) |
| Memory files: exact frontmatter, 15-line budget, MEMORY.md index, [[links]] | [references/memory-schema.md](references/memory-schema.md) |
| Research files: naming, agent-token line, what belongs in one | [references/research-files.md](references/research-files.md) |
| Author a skill for this library (SKILL.md + references/ + provenance) | [references/skill-authoring.md](references/skill-authoring.md) |

## When NOT to use
- settings.json, hooks, permissions, symlink mechanics → claude-config
- Measuring doc/convention compliance across sessions → diagnostics-toolkit
- The change/approval procedure for edits under `dotfiles/Claude/**` (live config) → change-control
