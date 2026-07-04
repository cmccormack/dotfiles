# How to add a new config axis

Every path below touches `dotfiles/Claude/` — **live global config via symlink**. Load the
change-control skill first; finish every path with `/git-commit`.

## Add a hook
1. Change-control: state what fires, on which matcher, and the blast radius (hooks run on
   EVERY matched tool call, in every project).
2. Write the script in `~/Projects/dotfiles/Claude/hooks/<name>.sh`; `chmod +x`. Follow the
   house pattern: opt-in gate (`[[ -d "$PWD/.claude" ]] || exit 0`), silent failure (`|| true`).
3. Register in settings.json via the `update-config` skill **run through an Agent** (heavy
   skill — never inline): add to `hooks.PreToolUse` / `hooks.Stop` with
   `"command": "bash $HOME/.claude/hooks/<name>.sh"`, `"async": true` unless it must block.
4. Restart the session (hooks load at start), trigger the matched tool once, verify output.
5. `/git-commit`.
Verify: `jq '.hooks' ~/.claude/settings.json && bash ~/.claude/hooks/<name>.sh </dev/null`

## Add a skill
1. Change-control (global skill = instantly live everywhere; project skill = repo-scoped).
2. Global library: `~/Projects/dotfiles/Claude/skills/<name>/SKILL.md` — YAML frontmatter
   `name:` + trigger-rich `description:`, `## Summary` ≤5 lines first, body ≤30 lines,
   detail in `references/*.md` each ending with `## Provenance and maintenance`.
   Project: `<repo>/.claude/skills/<name>.md`, flat, ≤30 lines + `## Summary`.
3. If it loads big docs, add it to the heavy-skill list in `~/.claude/CLAUDE.md` (route-via-
   Agent rule) instead of inlining the docs.
4. Audit with `/review-skill <name>`; test with an explicit `/<name>` invocation.
5. `/git-commit`.
Verify: `ls ~/.claude/skills/<name>* && head -5 ~/.claude/skills/<name>/SKILL.md`

## Add a permission
1. Decide scope first: needed by **agents** or across projects → global
   `dotfiles/Claude/settings.json` (agents inherit only this file); one repo, one human →
   `<repo>/.claude/settings.local.json`; whole repo team-visible → `<repo>/.claude/settings.json`.
2. Narrowest rule that works: `Bash(cmd *)` over `Bash(*)`; `WebFetch(domain:x)` — never
   `WebFetch(*)` in project scope; agent Write paths absolute.
3. Change-control, then edit via `update-config` through an Agent (global file) or directly
   (settings.local.json). `/git-commit` for repo-tracked files.
Verify: `jq '.permissions.allow | length' ~/.claude/settings.json`

## Provenance and maintenance
Written 2026-07-03 from the verified change surfaces in this skill's other references.
Re-verify the whole axis list: `ls ~/Projects/dotfiles/Claude/`.
