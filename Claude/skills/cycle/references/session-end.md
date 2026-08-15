# Session End

Every `/cycle` session, whether it finishes the queue or hits a blocker, ends the
same way:

1. RESUME.md is rewritten in full (never left half-updated), `## Claimed by` cleared,
   no leftover template placeholders (`<...>`) anywhere in it.
2. ISSUES.md updated if a new blocker was found or an existing one resolved.
3. Everything committed via `/git-commit` (tracker files plus any completed work not
   yet landed), this is the actual handoff, not a description of one.
4. The session's final chat message ends with exactly this line, on its own:

   ```
   🔄 Ready to /clear and run /cycle.
   ```

   Verbatim, so both a human skimming the transcript and the Stop hook (which checks
   the last assistant message for this exact string) recognize a clean stop.

A session is never "done for now, I'll finish the handoff later." If it cannot fully
finish RESUME.md for a genuine reason (needs a human decision), that decision becomes
a `## Preserved questions` entry and the handoff still gets finalized around it, the
handoff is the thing that's always complete, not the underlying task.

The `cycle-stop-check.sh` Stop hook (`~/Projects/dotfiles/Claude/hooks/`) enforces
this mechanically: it blocks session end at any resolved `/cycle` scope where
RESUME.md still has an unfilled placeholder or a non-empty `## Claimed by`. This
replaces relying on the model to remember, an unenforced version of this pattern
previously let sessions go lazy and leave handoffs unfinished, costing a full
cache-miss on the next session.

## Provenance
Closing-line convention and Stop-hook enforcement adopted 2026-08-15 after Chris's
prior experience with an unenforced version of this pattern; see
`.claude/plans/if-we-dno-t-already-serialized-cupcake.md`.
