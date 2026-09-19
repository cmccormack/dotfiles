# Gaming setup agents: plan of record

[View on GitHub](https://github.com/cmccormack/dotfiles/blob/main/Claude/docs/agents-plan.md)

Status: v3, 2026-09-19. Adversarial review applied (gaming research token 97ff7e).
Agent names APPROVED by owner 2026-09-19. Phase 0 (device access, allowlist, agents dir) applied and tested 2026-09-19, see deckops/docs/agent-access.md; Phase A is next.

Owner goal: when a question comes up about controllers, the Decks, streaming, audio,
the gaming PC, the network, or a game, the main session dispatches a domain agent to
research and propose repairs while the conversation continues.

## Owner decisions (2026-09-19)
- Roster: all eight agents, including `gaming-pc` and `no-mans-sky` (No Man's Sky will
  be fleshed out soon). Review recommended six; overruled.
- Location: `dotfiles/Claude/agents/` symlinked to `~/.claude/agents/`, agent `*.md`
  files only. This plan lives outside that directory so agents cannot read the exit key.
- Devices: read-only for agents, through wrapper scripts, never bare ssh.
- Docs: agents propose only; `vendor-docs` alone writes, and only under
  `<repo>/docs/vendor/`. One vendor tree per repo plus `gaming/docs/vendor/INDEX.md`
  linking across repos (reads outside the working directory prompt inside a subagent).
- Models: Sonnet for domain agents, Opus for review, Fable when a review is complex.
- Many agents are welcome (owner, 2026-09-19) as long as each is fine-tuned for one kind
  of research. The limit is routing quality, not count: descriptions must be precise and
  disjoint. Two tiers: cross-cutting agents are global in `dotfiles/Claude/agents/`;
  narrow specialists (per-game agents first) live in `gaming/.claude/agents/` so their
  descriptions load only in gaming sessions. Same format, same dispatch, no global prompt
  tax, so the review's "earn a slot" bar does not apply to specialists.
- `steamos` is the SteamOS layer only (not Deck hardware, not macOS); named `steamos`. Deck hardware topics get their own specialist if
  they earn one.

## Design rules
- Router, not encyclopedia. Hard budget per agent file: 60-line body (scope 5, evidence
  map 15, load-on-demand docs 10, recipes 15, output contract and failure block 15),
  description at most 25 words (descriptions are injected into every repo's prompt).
  Lint: `check_skill_size.py --agents` at dotfiles `/git-commit`; no hook can see agent
  files at write time.
- Knowledge lives in repo docs the agent loads on demand, never in the agent file.
- Names describe the domain, not the activity. Every agent researches and proposes.
- Version checks: the MAIN SESSION runs the haiku version check before dispatch and
  passes the result in the prompt. Agents have no `Agent` tool.
- Output contract: full detail to `<repo>/.claude/research/YYYY-MM-DD-<topic>-<token>.md`,
  first line `agent-token: <token>`, 10-line summary back. Two independent sources per
  fact (device state read directly is exempt). Evidence ceiling: grep logs, never cat
  whole files; 30k tokens of evidence per dispatch; declare truncation. Prohibited: git
  add/commit/push, `sed -i`, any write outside the research file, any edit to
  `dotfiles/Claude/settings.json`.
- Proposed repairs are written as a diff or exact command plus rollback inside the
  research file; the main session applies them serially under change-control.

## Naming convention (approved 2026-09-19)
Names say the domain, never the role or activity: game agents use the Steam store slug,
hardware and service agents use the product or layer name. Descriptions state the
trigger and must not overlap a sibling.

## Roster v1 (eight, names approved)

| Agent (proposed name) | Owns | Evidence it may read (via wrapper verbs) | Loads on demand |
|---|---|---|---|
| `game-streaming` | Apollo/Sunshine host config and logs, moonlight-qt clients, Steam Remote Play, encode/transport/client playback, audio capture pipeline | PC: sunshine.log, sunshine.conf, streaming_log.txt; Decks: console-linux.txt, pw-top, wpctl | deckops/docs/apollo.md, streaming-tuning.md; vendor: Sunshine config docs, Apollo README, moonlight-qt, Valve Remote Play FAQ |
| `steam-input` | Steam Input mechanics: VDF and API, action sets, chords, configsets, Remote Play controller forwarding and adoption, Steam Controller, Deck, Xbox | controller.txt on PC and Decks, Steam Controller Configs, controller_base | docs/steam-input/, /steam-input skill; vendor: partner.steamgames.com Steam Input |
| `steamos` | SteamOS layer: NetworkManager and iwd, power save, gamescope, atomic updates and keep-lists, Steam client logs, flatpak, suspend and resume | Decks: journalctl, nmcli, iw, flatpak, /etc/NetworkManager | steamdeck/docs/steam-deck/, deckops/scripts/bootstrap.sh; vendor: ValveSoftware/SteamOS issues, Arch wiki |
| `gaming-pc` | Windows layer: Steam client config keys (localconfig.vdf), overlay, WASAPI endpoint state, event logs, services, the vendored diag scripts | PC: localconfig.vdf, Steam logs, Get-ActiveAudioEndpoints, event log | deckops/docs/gaming-pc-access.md (to write), macknet/hosts/; vendor: Microsoft MMDevice/WASAPI, Steam client help |
| `home-network` | UniFi controller state, RF, QoS/DSCP and WMM, AP locks, roaming | macknet read-only CLIs: query, sta show | macknet/docs/; vendor: Ubiquiti help center |
| `vendor-docs` | Fetch official docs verbatim into `<repo>/docs/vendor/<vendor>/` with URL and date, keep the index, check allowlist coverage | none on devices | docs/allowlist-domains.md, web/docs/vendor/ pattern |
| `palworld` (gaming-scoped) | Everything Palworld: settings, Workshop mod manager, UE4SS, SmartPause, PalSchema, crash triage, wiki data | PC: ManagedMods, UE4SS.log, PalModSettings.ini; Decks: Proton paths | palworld/CLAUDE.md, palworld/data/, steamdeck/docs/games/palworld/status.md |
| `no-mans-sky` (gaming-scoped) | Everything No Man's Sky: settings, Steam Input API action sets and per-appid layout intent, VR side effects, Remote Play behaviour | PC: Steam Controller Configs/275850, screenshots dir | steamdeck/docs/games/no-mans-sky/ (to create); vendor: Hello Games support |

## Ownership rules (route every question to exactly one owner)
1. Layer beats symptom: the agent owning the layer where the mechanism lives owns the
   question, not the agent whose symptom was noticed.
2. Audio: `game-streaming` owns capture, encode, transport and playback. `gaming-pc`
   owns Windows endpoint state and is dispatched as an evidence contributor with one
   named question; it never proposes the streaming repair.
3. Radio: decided by evidence source. Answers from `iw`, `nmcli`, `journalctl` on a Deck
   belong to `steamos`; answers from controller `sta` stats, AP locks, QoS belong to
   `home-network`. `game-streaming` never owns WiFi and hands off with a named question.
4. Controllers: `steam-input` owns mechanics and forwarding. A per-game agent owns
   only per-appid binding intent and in-game action names. A fault that reproduces in a
   second title is `steam-input` by definition.
5. Per-game agents never touch a device layer; SteamOS, network and stream questions
   are handoffs.
6. `vendor-docs` is never first responder; it is dispatched by the main session or
   named as a prerequisite by another agent that hit a docs gap.
7. `gaming-pc` is the only agent that adds new PowerShell diag scripts, and only as
   proposals to `deckops/files/diag/`.

## Failure block (verbatim in every agent file that touches a device)
- Device unreachable: wrapper uses `BatchMode=yes`, `ConnectTimeout=5`, `timeout 30`,
  ControlMaster off. One retry, then stop. Never wake a device. Write the research file
  with a `## Blocked` section (host, verb, error); answer from repo docs only, label
  conclusions `unverified, device asleep`; summary line 1:
  `BLOCKED: <host> unreachable, owner must wake it`. Never fall back to another device.
- Domain blocked: summary line 1 carries the exact `"WebFetch(domain:<host>)"` string and
  the file `dotfiles/Claude/settings.json`; continue with what is reachable. Never route
  around the allowlist with curl or web_fetch.py; never present search snippets as the
  source.
- Two agents, one fault: one owner, one recommendation. A second agent is an evidence
  contributor with one named question; its file header carries `companion: <owner token>`.
  Never two agents writing one file. On finding the mechanism in another layer: stop and
  write `hand off to <agent>: <one question>`.
- Contradictory evidence: report both reads with timestamps, pick no winner. A proposal
  needing two mechanisms is not ready.

## Phase 0: enablement and security (gated, Class 3, before any agent exists)
Blast radius: global agents appear in every repo's prompt (eight descriptions, at most
25 words each); the allowlist changes apply to every session and subagent.
1. Approve agent names (owner).
2. Symlink `~/.claude/agents` to `dotfiles/Claude/agents`; add to the dotfiles link script.
3. Read-only device wrapper `~/.claude/tools/dev-ro.sh <host> <verb> [args]` with a fixed
   verb table (Deck: journal, nm, iw, steam-log, flatpak, pw-top, file <allowlisted path>;
   PC: sunshine-log, streaming-log, controller-log, localconfig-grep, audio-endpoints,
   event-log, file <allowlisted path>). PC verbs map to named vendored scripts in
   `deckops/files/diag/*.ps1`; `-EncodedCommand` is banned (it hides the command from
   prompts, logs and research files). Vendor the audio enumerator as
   `deckops/files/diag/Get-ActiveAudioEndpoints.ps1` (today in gitignored `.cache/`).
4. Real boundary: forced-command `authorized_keys` entries on both Decks and the PC for a
   dedicated agent key, so the server rejects anything outside the verb table. The
   wrapper alone is friction control, since `Bash(python3 *)` already grants local
   execution.
5. Global settings.json additions, validated with `python3 -m json.tool` before save,
   applied only through `update-config` via an Agent: `Bash(~/.claude/tools/dev-ro.sh:*)`,
   `Write(/Users/chris/Projects/<repo>/.claude/research/*)` for gaming, macknet,
   steamdeck (today only `Edit(...)` exists, so every agent's first write would stall),
   and the vendor WebFetch domains found in Phase A.
6. Security review of 3 to 5 (Opus), then owner go.

## Enrichment cycle (next session, after Phase 0)
- Phase A, gap audit: one `vendor-docs` run per agent lists the vendor docs it depends
  on, fetches what is missing verbatim into `<repo>/docs/vendor/`, writes a gap report.
- Phase B, learn: one run per domain agent, in parallel, propose-only. Each reads its
  vendor docs and writes, inside its research file, diffs for its agent file and for repo
  docs. The main session applies them serially (six agents editing shared docs would
  clobber each other). Seed facts from 2026-09-19 that would have changed a decision:
  Sunshine enumerates active endpoints only; Steam disables Steam Streaming Speakers
  outside its sessions; NetworkManager applies conf.d lexically; Remote Play forwards the
  dock dongle as a second controller; Workshop updates reset mod configs.
- Phase C, adversarial review (Opus; Fable if complex) of every proposed edit against the
  design rules and the evidence bar.
- Phase D, land through `/git-commit` in dotfiles and gaming. One MEMORY.md line at most.

## Exit test (blinded)
Prompts contain the owner's symptom only, no discriminators (bad: "zero network drops,
zero xruns"; good: "Moonlight audio pops while idle in Big Picture"). The answer key
stays in this file, which agents cannot read. Grade on process: correct owner accepted
the dispatch, evidence gathered through wrapper verbs, mechanism named, repair proposed
with rollback, sources cited. Three held-out questions per agent come from pre-2026-09-19
research files (tokens 0da952, 475c85, fa1451, e5e049, c56c61) whose facts are not in the
Phase B seed list. Budget: roughly 0.3M to 0.5M Sonnet input tokens per dispatch, 2.5M
to 4M for the whole test.

Seeded 2026-09-19 prompts and expected mechanisms:
- game-streaming: "Moonlight audio pops while idle in Big Picture." Key: capture source is
  the only active endpoint during ensure_only_display; enumerate endpoints.
- steam-input: "Steam Controller Select takes screenshots over Remote Play, fine over
  Moonlight." Key: two forwarded controllers, host-side layout, Apollo shows one pad.
- steamos: "WiFi power save is on again after a reboot." Key: Valve rewrites
  99-valve-wifi-backend.conf from the Developer toggle; lexical order beats 99-deckops.
- gaming-pc: "No achievement toasts over Remote Play." Key: EnableGameOverlay=0.
- home-network: "Pin the LCD to the Family Room AP." Key: macknet wifi_locks, hard block.
- palworld: "SmartPause stopped pausing." Key: Workshop update reset config.lua.

## Unowned today (named so silence is not the answer)
Emulation and the deckops provisioning pipeline: main session plus `/ansible-review` and
`/ansible-run`. chiaki-ng and PS5 streaming: `game-streaming` once its docs exist. Save
sync: unowned, revisit when it bites.
