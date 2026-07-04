# Research Methodology — how a hunch becomes an accepted change

Every historical example below is a real file in this portfolio. Read it before citing it.

## 1. The evidence bar

**One mechanism must explain ALL observations, including the negatives.** A story that
covers the headline symptom but leaves an inconvenient data point unexplained is not done.

House example — `~/Projects/macknet/.claude/research/2026-06-28-pi-adversarial-review-a69fef.md`:
the recon story was "Pis stale but `apt list --upgradable` = 0, so patched." The negative
observation (`apt-daily.service` reporting SUCCESS on a box untouched for 9 months) didn't
fit. The single mechanism that explained everything: no `APT::Periodic::Update-Package-Lists`
config, so the timer fired as a no-op and package lists were frozen at 2024-09. "0 upgradable"
was comparing installed packages against 9-month-old lists. One mechanism, all observations,
including the one that looked like good news.

**Before adopting, the claim must survive an adversarial pass** — assign a second agent to
refute it, not to review it politely. This is established house practice:

- `2026-06-28-pi-adversarial-review-a69fef.md` (macknet) — the reviewer confirmed 3 of 4
  recon conclusions but killed the "20G dead images" figure (real: 15G total, images only
  1.47GB; `docker system df` double-counts shared layers) and downgraded "safe to keep
  running" to "idle but unpatched, contained on LAN."
- `~/Projects/steamdeck/.claude/research/2026-06-08-skeptic-analysis-44290d.md` +
  `2026-06-08-promote-analysis-ef5cfd.md` — paired skeptic/promoter agents on whether
  project CLAUDE.md rules deserved user-level promotion; the skeptic blocked most of them.
- `~/Projects/steamdeck/.claude/research/skill-proposer-a3f7c2.md` + `skill-critic-17b9c5.md`,
  `plan-proposer-b95289.md` + `plan-critic-70f38b.md` — proposer/critic pairs for skill and
  plan authoring.
- `~/Projects/macknet/.claude/research/2026-06-21-macknet-critic-78f16f.md` — critic assigned
  to the ubiquiti→macknet restructure before it landed.

Give the adversary a concrete verdict format ("VERDICT ON YOUR N CONCLUSIONS", confirm /
refute / overstated per item) and, where possible, independent access to the ground truth
(the pi review re-ran the SSH checks itself rather than trusting the recon transcript).

## 2. Predict the numbers BEFORE running

State the predicted measurements in the research file before starting the experiment.
**An experiment without a predicted number is a wander, not a test.**

Measurement primitives already wired into this portfolio:

| Metric | Source | Command |
|---|---|---|
| Tool calls, sessions, per-session activity | `.claude/logs/session.jsonl` (PreToolUse/Stop hooks, every repo) | `wc -l`, `jq`, `/token-audit` |
| Token/context usage patterns | same log via the audit skill | `/token-audit` |
| Rule-violation counts (skill size, memory budget) | diagnostics-toolkit scripts; prototype hook `~/Projects/macknet/.claude/hooks/check_skill_size.py` | run the script, count hits |
| Test counts / pass rates | pytest suites in macknet, dotfiles, steamdeck | `uv run pytest --co -q \| wc -l` (steamdeck: `uv run --with pytest ...` — pytest undeclared there) |
| Which session made which change | git-notes correlation (`refs/notes/claude` via `~/.claude/scripts/git-correlate.sh`) | `git notes --ref=claude show <sha>` |

Write the prediction as a falsifiable line: "after X, `check_skill_size.py` violations drop
from 4 to 0" — not "skills should get better."

## 3. Idea lifecycle

1. **Hunch → research file.** Everything starts as a dated, tokened file:
   `.claude/research/YYYY-MM-DD-topic-{token}.md`, `{token}` = `os.urandom(3).hex()`, first
   line `agent-token: {token}`. Real instances: a device symptom became
   `~/Projects/steamdeck/.claude/research/2026-06-19-oled-network-drop-30bd5e.md`; a
   purchase decision became `~/Projects/macknet/.claude/research/2026-07-03-pi-os-selection-58fc42.md`
   (evaluation criteria stated up front, then eight candidates scored against them).
2. **Scratchpad / branch experiment.** Isolate it — scratch scripts, a worktree, or a branch;
   never live gear (that gate is `change-control`).
3. **Measured trial** with the section-2 predictions written first.
4. **Adversarial pass** (section 1) on the conclusion.
5. **Either adopt or retire — both are written down:**
   - **Adopted:** promote into `dotfiles/Claude/` config or a skill. That directory is live
     via the `~/.claude` symlink, so the write itself is a Claude-config-class change —
     route through `change-control`, commit via `/git-commit`. Example: the ubiquiti→macknet
     restructure survived its critic (`2026-06-21-macknet-critic-78f16f.md` — which endorsed
     "single repo, flat src/ layout" while rejecting the monorepo framing) and landed; the
     Kobo USB `eReader.conf` method from
     `~/Projects/bookshelf/.claude/research/2026-06-19-kobo-custom-sync-baff01.md` was
     adopted into bookshelf's KOBO_SETUP.md.
   - **Retired:** the research file records why it failed, and the one-line verdict goes to
     project memory as an L1 decision. Real retirements: `aiounifi` and `pyunifi` rejected in
     favor of a custom aiohttp client (macknet memory `sdk_research.md` — "custom aiohttp
     client chosen; aiounifi and pyunifi rejected"); the "NW.js needs a successor fork"
     premise refuted in `~/Projects/steamdeck/.claude/research/2026-06-09-nwjs-forks-ba9be1.md`
     (official repo alive, ~monthly releases — investigation closed); the multi-package
     monorepo scaffold rejected as premature in `2026-06-21-macknet-critic-78f16f.md`.

A retired idea with a written cause is a success of the process. A silently abandoned
branch is the failure mode.

## 4. Where good ideas historically came from

Mined from the research trail — these are the actual triggers, use them as prompts:

- **A device misbehaving during real use.** Steam Deck OLED WiFi drops →
  `2026-06-19-oled-network-drop-30bd5e.md` (root-caused to two ath11k/power-management bugs).
- **An anomaly noticed during routine ops.** Pi maintenance recon surfaced the fake
  "0 upgradable" → the apt no-op discovery (`2026-06-28-pi-adversarial-review-a69fef.md`).
  The anomaly, not the maintenance task, produced the insight.
- **A vendor path being blocked.** Kobo's Beta Features menu missing → USB config-edit
  research (`2026-06-19-kobo-custom-sync-baff01.md`, bookshelf).
- **Friction with the workflow itself.** Duplicate rules between project and user CLAUDE.md →
  the skeptic/promote pair (steamdeck, 2026-06-08); doubts about skill quality → the
  skill-proposer/critic pair. Meta-work gets the same pipeline as device work.
- **A purchase or build forcing a decision.** Pi 5 arrival → OS selection, flashing, PiKVM
  research (`2026-07-03-pi-os-selection-58fc42.md`, `2026-07-03-pi-flashing-418471.md`,
  `2026-07-03-pikvm-cafa85.md`) that fed macknet and keylimepi.

Common shape: a concrete observation that contradicts an assumption. Ideas that started as
"wouldn't it be nice" (the multi-integration monorepo) are the ones the critics killed.

## Provenance and maintenance

Written 2026-07-03 from the research trails in macknet, bookshelf, steamdeck, and the
portfolio/conventions surveys (`~/Projects/.claude/research/2026-07-03-portfolio-survey-aa87cf.md`,
`2026-07-03-claude-conventions-f6c417.md`). Re-verify with:

- `ls ~/Projects/{macknet,bookshelf,steamdeck}/.claude/research/` — cited files still exist.
- `grep -l "agent-token" ~/Projects/*/.claude/research/*.md | wc -l` — convention still live.
- `ls ~/.claude/scripts/ ~/Projects/macknet/.claude/hooks/` — measurement primitives present.
- If a cited file is gone, replace the example with a current one; do not cite from memory.
