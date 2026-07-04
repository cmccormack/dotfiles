# House Markdown Rules

Source of authority: `~/.claude/CLAUDE.md` (sections: Communication, Markdown Conventions).
This file summarizes it for doc-writing; if the two ever disagree, `~/.claude/CLAUDE.md` wins.

## Rules

- **Terse.** No filler intros, no trailing recaps of what the doc just said. Task-focused.
- **No emoji.** (`~/.claude/CLAUDE.md`: "No emoji unless asked".) Observed exception:
  keylimepi's README uses `⚠️` blockquote callouts for hardware-damage warnings — acceptable
  only for physical-risk warnings, nothing else.
- **File references are markdown links, not backticks:** `[client.py:42](src/macknet/unifi/client.py#L42)`.
  Applies inside docs the same as in chat (see macknet CLAUDE.md's Architecture section).
- **`[View on <SCM>](URL)` link under the title** of every human-readable markdown file —
  README, CLAUDE.md, docs pages. Live examples: `~/Projects/keylimepi/README.md`,
  bookshelf README + CLAUDE.md, dotfiles CLAUDE.md. macknet and steamdeck CLAUDE.md lack it — known drift; add when touching those files.
- **Tables over prose lists** for files, commands, parts, ports, shortcuts, routing
  (every surveyed repo does this: bookshelf `## Files`, dotfiles `## Layout`, keylimepi parts list).
- **Imperative voice** for procedures ("Flash with `dd`", "Copy `.env.example` → `.env`").
- **`~` for user paths** in docs; absolute paths only where a command requires them.
- **Deep detail goes in a linked doc, not inline** — README links NAS_SETUP.md, CLAUDE.md
  links docs/INDEX.md. Keep each file at one altitude.

## Provenance and maintenance
Derived 2026-07-03 from `~/.claude/CLAUDE.md` and the READMEs/CLAUDE.md of keylimepi,
bookshelf, macknet, steamdeck, dotfiles. Re-verify:
`grep -A3 "Markdown Conventions" ~/.claude/CLAUDE.md` and
`head -5 ~/Projects/{keylimepi,bookshelf}/README.md`.
