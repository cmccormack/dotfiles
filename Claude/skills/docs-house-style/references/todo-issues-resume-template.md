# TODO.md / ISSUES.md / RESUME.md templates

House style for the three-file `/cycle` tracker set (see the `cycle` skill). One set
per tracker scope: a repo root, or a subfolder that represents a genuinely separate
stream of work (see `cycle/references/scoping.md`).

## TODO.md (backlog, formalizes macknet's existing style)

- H1 `# TODO`, one-line scope sentence.
- H2 per initiative (not a flat checklist); title states the thing, parenthetical
  states current phase.
- Prose status paragraph under the H2, then `- [ ]`/`- [x]` checklists for concrete
  sub-actions, inline `(YYYY-MM-DD)` dates on completed items.
- Optional `**Done when:**` line per checklist item where a task is non-trivial to
  verify, machine-checkable, not self-assessed.
- Cross-reference `docs/` and memory names as markdown links, never duplicate content.
- No "RESUME HERE" markers, that's RESUME.md's job exclusively.

## ISSUES.md (blockers/open questions, new)

```markdown
# ISSUES

Problems, blockers, and open questions discovered mid-work that need a decision or fix.
Not a backlog (TODO.md) and not narrative history (chronicle.md, where it exists).

## Open

### <Title> (opened YYYY-MM-DD)
**Status:** open | blocked-on-chris | blocked-on-external
**Description:** <what's wrong / what's undecided>
**Needs:** <what unblocks it>
**Links:** <doc paths, research tokens, related TODO.md section>

## Resolved

### <Title> (opened YYYY-MM-DD, resolved YYYY-MM-DD)
**Resolution:** <one line>
```

Resolved issues are kept one cycle after close (visible proof of what got fixed),
then pruned by the next bootstrap-mode pass at that scope. If a chronicle.md exists
at that scope, `/cycle` suggests folding the resolution in before pruning, never
automatic.

## RESUME.md (the handoff pointer, new)

```markdown
# RESUME

<!-- Rewritten every /cycle run. History = git log on this file. -->

## Claimed by
<empty, or "session <short-id>, claimed YYYY-MM-DD HH:MM">

## Next task
1. <first concrete action, imperative, pasteable>
2. <second action, if sequence matters>

## Done when
<machine-checkable completion condition>

## Preserved questions
- [ ] <question, dated when first asked>

## State
<2-5 lines: what's done, what's blocked, session date>

## Context links
<doc paths, research tokens, memory names>

## Last updated
<YYYY-MM-DD HH:MM> by /cycle session <short id>
```

Only one `## Next task` at a time, the backlog lives in TODO.md. Fully overwritten
each cycle; git history is the audit trail, not accumulated old sections.

## Provenance
Adopted 2026-08-15, `.claude/plans/if-we-dno-t-already-serialized-cupcake.md`. Prior
art: Cline Memory Bank, the `thepushkarp/handoff` plugin, `tick-md`, Ralph Wiggum
autonomous-loop pattern (see plan's Context section for details).
