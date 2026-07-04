# Known Weak Points

Stated plainly so nobody rediscovers them. Verified 2026-07-03. Fixing docs → see
`docs-house-style`; fixing repo scaffolding → `new-project-bootstrap`.

- **Empty READMEs:** `macknet/README.md` and `steamdeck/README.md` are 0 lines. All
  knowledge lives in CLAUDE.md and docs/ — invisible on GitHub.
- **No CI anywhere.** macknet, steamdeck, and dotfiles have real pytest suites but zero
  `.github/workflows`. Tests run only when someone remembers to run them.
- **Git identity drift:** remotes are `cmccormack/*`, but dotfiles README/CLAUDE.md link
  `github.com/mccormack-christopher/dotfiles`. One of these is wrong for any given viewer.
- **Default-branch drift:** dotfiles is on `master`; every other live repo uses `main`.
- **bookshelf naming split:** repo is `bookshelf`, but CLAUDE.md is titled "cwa-library",
  the container is `cwa-library`, and CLAUDE.md still carries the placeholder
  `github.com/<your-username>/bookshelf`.
- **Uncommitted work as the norm:** as of 2026-07-03, dirty trees in macknet (8 files),
  steamdeck (3), bookshelf (1), keylimepi (1). Unfinished work is signaled by dirty trees,
  not TODOs — check `git status` before trusting that a repo matches its docs.
- **Committed agent worktree in steamdeck:** `.claude/worktrees/agent-abf29b3f8851c49dc/`
  plus a matching long-lived branch duplicate the whole tree. Should be gitignored/pruned.
- **NAS SSH docs conflict:** macknet CLAUDE.md says NAS SSH is "disabled by design"; the
  older bookshelf CLAUDE.md still documents SSH access with public-key auth, and its
  NAS commands assume a shell. Trust macknet (newer); bookshelf needs updating.
- **Snapshot staleness in UniFi facts:** `macknet/.claude/skills/unifi.md` says Network
  10.4.57 / UniFi OS 5.1.15; `inventory/network.yaml` (2026-06-22) records UDM Pro 5.1.19.
  Version claims anywhere in this doc tree are point-in-time — regenerate the inventory.
- **PiKVM image variant conflict:** keylimepi README says flash the "DIY V2 image"
  (`pikvm-v2-rpi4.img`); macknet's `pikvm-upgrade.md` checklist actually downloaded
  `v3-hdmi-rpi4-aarch64-latest.img.xz`. Unresolved — confirm which image the build uses
  before writing more docs against either.
- **docker-compose v1 (EOL) on the NAS:** DSM 7.1.1 ships v1 at
  `/usr/local/bin/docker-compose`; upgrade path is DSM 7.2 / Container Manager. Compose
  files must stay v1-compatible until then.
- **Pi fleet in transition:** both Pis are flagged for reflash (2026-07-02 decision in
  `fleet.local.md`); that file also contains impossible "last interactive use" dates
  (2026-09-xx, in the future). The fleet table may not match reality mid-migration.

## Provenance and maintenance
Compiled 2026-07-03 from portfolio survey (`~/Projects/.claude/research/2026-07-03-portfolio-survey-aa87cf.md`)
and direct repo inspection. Re-verify:
- `wc -l ~/Projects/macknet/README.md ~/Projects/steamdeck/README.md`
- `ls ~/Projects/{macknet,steamdeck,dotfiles}/.github 2>&1` (CI still absent)
- `for r in macknet bookshelf steamdeck keylimepi dotfiles; do git -C ~/Projects/$r status --short | wc -l; done`
- `grep -n "pikvm-v2\|v3-hdmi" ~/Projects/keylimepi/README.md ~/Projects/macknet/docs/raspberry-pi/pikvm-upgrade.md`
