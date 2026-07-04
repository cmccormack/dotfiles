# INDEX / Router Doc Pattern (doc economy)

A routing table loaded first so readers (Claude or human) open only the one file a task
needs. Practiced in macknet: `docs/INDEX.md` is the top hub routing to per-domain hubs
(`unifi/INDEX.md`, `synology/INDEX.md`, `raspberry-pi/INDEX.md`), each of which routes to
detail files. Bookshelf uses the lighter variant — README `## Files` table plus a
cross-repo link to macknet's Synology docs instead of duplicating them.

## When to create one
- A docs topic grows past ~3 files, or agents keep loading a whole directory for one fact.
- Cross-repo: if another repo already documents the topic, link its INDEX (bookshelf →
  macknet), don't fork the docs.
- CLAUDE.md points at the top INDEX ("Load this index first") — never at individual files.

## Template (from macknet docs/INDEX.md + unifi/INDEX.md)

```markdown
# <Topic> Index

<one line of scope/version facts, e.g. "Controller: UCG/UDM running UniFi OS 5.x">

Load this index first. Read individual files only when the task requires their detail.

| File | When to load it |
|---|---|
| [`quick-reference.md`](quick-reference.md) | <task phrase — "start here for most tasks"> |
| [`api.md`](api.md) | <what question this file answers> |

## Quick facts (load this index only)
- <8–10 bullets answering the most common lookups without opening any file:
  auth headers, base URLs, envelope shapes, legacy-vs-current model names>
```

Rules: the "When to load it" column is a trigger phrase, not a summary; `## Quick facts`
absorbs the 80% lookups so the index alone often suffices; sub-INDEXes carry the same
"Load this index first" line so the routing is recursive.

## Provenance and maintenance
Derived 2026-07-03 from `~/Projects/macknet/docs/INDEX.md`, `~/Projects/macknet/docs/unifi/INDEX.md`,
and `~/Projects/bookshelf/README.md`. Re-verify: `head -10 ~/Projects/macknet/docs/INDEX.md`
and `ls ~/Projects/macknet/docs/*/INDEX.md`.
