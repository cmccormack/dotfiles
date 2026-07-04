# README Standard

Skeleton extracted from the two strongest live examples: `~/Projects/keylimepi/README.md`
(hardware build guide: parts table, `## Step N — verb` sections, troubleshooting) and
`~/Projects/bookshelf/README.md` (service: flow diagram, quick start, files/ports tables).

## Known debt this template exists to fix
`macknet/README.md` (0 lines), `steamdeck/README.md` (0 lines), `dotfiles/README.md`
(1 stale line). Their knowledge lives only in CLAUDE.md/docs — invisible on GitHub.
When touching one of these repos, offer to fill the README from this template.

## Template (copy-paste; delete sections that don't apply)

```markdown
# <Project Name>

[View on GitHub](https://github.com/cmccormack/<repo>)

<1–2 sentences: what it is and the problem it solves. Link upstream projects
(bookshelf links Calibre-Web Automated). If repo name ≠ project name, title is the
project name (bookshelf repo → "# cwa-library").>

## Flow                    <!-- services: one ascii pipeline, like bookshelf -->
## Parts List              <!-- hardware: table of Component | Notes, like keylimepi -->

## Quick Start
<copy-paste commands that work from a fresh clone: cp .env.example .env,
docker compose up -d, uv run ... End with the URL/result the user should see.>

## Step 1 — <verb>         <!-- builds/guides: numbered verb-titled steps (keylimepi);
                                blockquote warnings before the step they protect -->

## <Deployment / Advanced>
See **[DEEPER_DOC.md](DEEPER_DOC.md)**. <Then only the key-differences bullets,
like bookshelf's NAS section. Cross-repo docs get full GitHub URLs.>

## Files
| File | Purpose |
|------|---------|

## Ports                   <!-- services: | Service | Port | -->

## Troubleshooting
**<Symptom>**
- <check / fix, one line each — keylimepi format>
```

Rules: every command block must be runnable as-is; defer depth to linked docs
(NAS_SETUP.md, docs/); no roadmap prose — point at CLAUDE.md for future phases
(bookshelf's "Phase 2" section does exactly this).

## Provenance and maintenance
Derived 2026-07-03 from `~/Projects/keylimepi/README.md` and `~/Projects/bookshelf/README.md`;
debt list from the 2026-07-03 portfolio survey (`aa87cf`). Re-verify:
`wc -l ~/Projects/{macknet,bookshelf,keylimepi,steamdeck,dotfiles}/README.md` — nonzero
counts mean debt items are fixed; re-read the two exemplars if their structure changed.
