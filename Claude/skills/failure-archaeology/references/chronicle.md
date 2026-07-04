# Chronicle of Settled Battles

Format: **Symptom → Root cause → Evidence → Status**. Every hash verified against the live repo on 2026-07-03. Do not re-fight anything marked fixed/superseded without new evidence.

## macknet

### Restructure to `macknet.unifi` — critic overruled
- Symptom: repo named `ubiquiti`, single `unifi` package; wanted room for NAS/Pi integrations.
- Root cause of debate: architect ([2026-06-21-macknet-architect-7432c1.md](~/Projects/macknet/.claude/research/2026-06-21-macknet-architect-7432c1.md)) proposed `macknet.unifi` namespace; critic (`...-macknet-critic-78f16f.md`) said "Don't do it" — premature, namespace adds import overhead for zero PyPI benefit.
- Evidence: restructure done anyway in `69ced93` (renamed repo, `src/macknet/unifi/`, `UI_*` → `UNIFI_*` env vars). Rename fallout: stale skill refs fixed same day in `43498f7`.
- Status: superseded (critic lost). Partially vindicated — the second integration the critic doubted did land (`44b5ad4` Synology DSM, `69f56ff` Pi maintenance). Lesson: rename fallout hides in `.claude/skills/` and docs, not just imports.

### Pi fleet adversarial review (2026-06-28)
- Symptom: fleet "looked patched" — `apt list --upgradable` showed 0.
- Root cause: `APT::Periodic` disabled, apt lists frozen at Sep 2024; both Pis ~9 months unpatched. Also: password auth on + NOPASSWD sudo = guessable password is remote root; pi5 admin path was over wifi (NM upgrade/reboot can drop wlan0).
- Evidence: [2026-06-28-pi-adversarial-review-a69fef.md](~/Projects/macknet/.claude/research/2026-06-28-pi-adversarial-review-a69fef.md); synthesized into [docs/raspberry-pi/troubleshooting.md](~/Projects/macknet/docs/raspberry-pi/troubleshooting.md).
- Status: fixed/documented, two open items — pi4 Bullseye hits LTS EOL 2026-08-31 (Bookworm reimage decision pending); pi5 admin should stay on wired .145.
- Rejected: fail2ban on LAN-only key-auth hosts — near-useless, biggest self-lockout risk.

### Pi OS / flashing / PiKVM research (2026-07-03, uncommitted)
- Decisions recorded but not yet committed: research files `58fc42` (OS selection), `418471` (flashing — `/dev/rdiskN` not `/dev/diskN`, else buffered-IO slow writes), `cafa85` (PiKVM: DIY V2 + MS2130 dongle cheapest; v3 HAT best; do NOT use RPi Imager custom settings with PiKVM OS).
- Status: open — `docs/raspberry-pi/{os-selection,os-flashing,pikvm,pikvm-upgrade}.md` untracked in working tree as of 2026-07-03.

## bookshelf

### Kobo `api_endpoint` port-append bug
- Symptom: Kobo sync half-broken after pointing device at CWA.
- Root cause: `domain:port` in `api_endpoint` makes firmware append the port to every other `[OneStoreServices]` entry. Use `IP:port` or a reverse-proxied domain.
- Evidence: research `5a7d8f`; [docs/wiki/kobo/kobo-ereader-conf.md](~/Projects/bookshelf/docs/wiki/kobo/kobo-ereader-conf.md) line ~59.
- Status: fixed/documented.

### Libra Colour config overwrite + missing covers
- Symptom: `api_endpoint` reverts to `storeapi.kobo.com` after sync; cover images broken.
- Root cause: Kobo sync handshake restores `eReader.conf` on newer devices (server-side, no firmware version pinned — gap: never root-caused upstream). Covers need extra `image_host` / `image_url_*template` entries on Libra Colour.
- Evidence: research `5a7d8f`, `5b9ff2`, `baff01`; docs/wiki/kobo/.
- Status: open upstream; workarounds documented (re-edit before sync, DNS intercept). Related non-bug: missing Beta Features menu = parental mode on or `devmodeon` not typed, NOT a firmware removal.

### Scaffolding committed then removed (deliberate pattern)
- 19 raw `docs/sources/*.txt` research dumps removed after synthesis into `docs/wiki/kobo/` — `b908a09`. Session `TASKS.md` removed, content absorbed into NAS_SETUP.md, `.claude/tasks/` gitignored — `47670eb`.
- Status: settled convention — raw sources and session artifacts are scaffolding; synthesize, then delete.

### Btrfs shared-folder trap
- Symptom: can't turn a pre-made directory into a DSM shared folder.
- Root cause: DSM shared folders on Btrfs are subvolumes; `mkdir` first blocks creation. Never `btrfs subvolume create` directly either — DSM must register it.
- Evidence: [NAS_SETUP.md](~/Projects/bookshelf/NAS_SETUP.md) line ~49; [macknet docs/synology/storage.md](~/Projects/macknet/docs/synology/storage.md).
- Status: fixed/documented.

## steamdeck

### Demons Roots FPS drops
- Symptom: FPS craters on talksprite portrait swaps; heat throttling.
- Root cause: stock NW.js v0.29 (Chromium 61, 2017) slow bitmap ops with no GPU accel under Proton/Wine.
- Fix: native Linux NW.js compat tools; **v0.76.1 is ACTIVE** (Steam overlay works), v0.112.0 fallback (faster, overlay broken — `gameoverlayrenderer.so` LD_PRELOAD can't reach Chromium's sandboxed GPU process; `--in-process-gpu` required, and without it gamescope SIGTERMs the GPU subprocess). NW.js v0.88+ has a process-exit regression — pin v0.87 for in-place binary swaps.
- Evidence: [docs/games/demons-roots/status.md](~/Projects/steamdeck/docs/games/demons-roots/status.md); research `65e741`, `ba9be1`, `24c24a`, `4f8a2c`; commits `8b5e442`, `5161b84`.
- Status: fixed.

### GOG Galaxy DeelevateStrategy failure (the EnableLUA saga)
- Symptom: Galaxy stopped launching mid-project; service IPC died in <1ms.
- Root cause: a Proton prefix update silently wrote `EnableLUA=1` to the Wine registry (~4 min before first failure) → Wine reports process elevated → Galaxy picks `DeelevateStrategy` instead of `InitClientStrategy` → Wine SCM kills `GalaxyClientService`. Fix: `EnableLUA=0` in `system.reg`.
- Ruled out (with DB backup + rollback proof): Galaxy DB state, Proton version ("GE-Proton9-14 broken" claim from a research agent was WRONG — logs showed successful runs), `scriptinterpreter.exe` copy, AppCompatFlags, window hunting.
- Evidence: [docs/games/demons-roots/investigation.md](~/Projects/steamdeck/docs/games/demons-roots/investigation.md) — includes an explicit **DO NOT REPEAT** list; read it before touching Galaxy.
- Status: launch fixed; cloud saves still blocked by Wine SCM killing GalaxyClientService (affects all GOG games) — open, upstream.

### OLED wifi periodic drops
- Symptom: latency spikes, ~20 Mbps cap, stream crashes every few minutes.
- Root cause: two OLED-only (ath11k) bugs — wifi power management silently re-enables after sleep/wake; ath11k firmware regression in linux-neptune.
- Evidence: research `30bd5e`; fix = SteamOS main channel firmware.
- Status: mitigated locally; upstream open.

### Steam Input doc split — rejected structure
- `input-modes.md` grouping rejected (mode_shift is a technique, not a mode → lives in advanced-bindings); two-stage-trigger split flagged as navigation trap. Spec gaps found and folded in (`radial_menu_style`, `gyro_axis`). `controller_action ts_n` is undocumented — do not use ([docs/steam-input/binding-strings.md](~/Projects/steamdeck/docs/steam-input/binding-strings.md)).
- Evidence: research `plan-proposer-b95289.md` / `plan-critic-70f38b.md`, `skill-proposer-a3f7c2.md` / `skill-critic-17b9c5.md`.
- Status: superseded by shipped `docs/steam-input/` layout (`8b5e442`).

### Stale agent worktree (housekeeping, open)
- `.claude/worktrees/agent-abf29b3f8851c49dc/` on disk + local branch `worktree-agent-abf29b3f8851c49dc`. Branch tip `d08ba68` is an ancestor of main — fully merged, zero unique commits. Not git-tracked (`git ls-files` empty for it).
- Status: open — safe to `git worktree remove` + `git branch -d`.
- Related: `.claude/cache/<slug>.json` convention conflicts with global `.claude/research/` pattern — flagged in research `44290d`, not fully reconciled. Old-convention research filenames (`vdf-format-93bb56.md`, no date prefix) coexist with new — never migrated.

## dotfiles

### Orphan lockfile = all 30 Dependabot alerts
- `package-lock.json` with no manifest entries pointing at it generated every open alert; removed in `a2b21b9`. That commit carries a `Co-Authored-By: Claude` trailer — the later `b086304` ("pref: never add Co-Authored-By trailers") is the rule's origin commit.
- Status: fixed; trailer rule now global.

### Superseded eras
- Mac-specific bash files removed in favor of `Multi-OS/` (`414e12e`, `9e989f0`); bash-era churn (`.bashrc`/`.bash_profile` = top churn files, 10 changes each) superseded by zsh/oh-my-zsh (`997a9f1`). Remote branch `bash-aliases` is fully merged into master — dead, safe to delete.
- Status: superseded.

### Sync tooling fixes
- `70fc9cb`: sync.py printed duplicate output when moving+linking in one pass. `6eb0a90`: credential scanner gained `--filter` to strip flagged lines in-place.
- Status: fixed. Open: README badge points at `mccormack-christopher/dotfiles`, remote is `cmccormack/dotfiles`.

## keylimepi

Only 2 commits; one battle: README pointed at the wrong GitHub URL, fixed in `dfb3e37`. No archaeology yet.

## Cross-portfolio patterns

1. **Zero revert commits in all 5 repos** — mistakes are fixed forward. Mine removal commits, research files, and "DO NOT REPEAT" doc sections, not `git log --grep=revert`.
2. **Adversarial agent pairs are the decision record** — architect/critic (macknet), proposer/critic + promote/skeptic (steamdeck). The critic is sometimes overruled; read both sides before assuming the shipped design was uncontested.
3. **Scaffolding-then-delete** — raw sources, session TASKS, orphan lockfiles get committed then deliberately removed (`b908a09`, `47670eb`, `a2b21b9`). A file's absence at HEAD doesn't mean it never mattered; `git log --diff-filter=D` finds it.
4. **Agent research can be wrong** — the "GE-Proton9-14 broken" claim was disproven by primary logs. Verify research-file claims against logs/registry/DB before acting.
5. **Session/agent artifacts leak into repos** (steamdeck worktree+branch, bookshelf TASKS.md) — each repo eventually adds gitignore entries; check `.gitignore` history for what leaked.
6. **Rename fallout lives in `.claude/`** — `43498f7` shows skills/commands break silently on restructure.

Gaps (un-mined as of 2026-07-03): macknet synology-docs research (reference-only), steamdeck `action-sets`/`creative-techniques`/`vdf-format` research bodies, gog-galaxy decision-tree doc, dotfiles pre-2020 history detail, keylimepi/macknet uncommitted working trees.

## Provenance and maintenance

Compiled 2026-07-03 from `git log`/`git show` on all 5 live repos, every `.claude/research/*.md` in macknet/bookshelf/steamdeck, and repo docs greps. All hashes confirmed via `git show <hash>` at compile time.

Re-verify:
```bash
for r in macknet bookshelf keylimepi steamdeck dotfiles; do git -C ~/Projects/$r log --oneline -5; done
git -C ~/Projects/steamdeck worktree list && git -C ~/Projects/steamdeck branch
git -C ~/Projects/macknet status --short   # pi docs still uncommitted?
ls ~/Projects/{macknet,bookshelf,steamdeck}/.claude/research/
```
Stale when: pi4 Bookworm reimage happens, steamdeck worktree is pruned, Galaxy cloud-save bug is fixed upstream, or new research files postdate 2026-07-03.
