# Cross-Project Skill Library

[View on GitHub](https://github.com/cmccormack/dotfiles/blob/master/docs/2026-07-skill-library.md)

Built 2026-07-03/04. A knowledge base under [Claude/skills/](../Claude/skills/) — live
globally via the `~/.claude/skills` symlink — so that any Claude session (including
cheaper Sonnet-class ones) can debug, extend, validate, and advance the portfolio
without senior context. Authored by parallel agents against ground truth in the five
active repos (macknet, bookshelf, keylimepi, steamdeck, dotfiles), then reviewed,
fact-checked, and fixed as a set.

## Why

Owner-identified problems (2026-07-03): the costliest failures were burned Claude
sessions (token blowouts, wrong-path agents, ignored rules) and homelab misconfig.
Discipline rules lived as CLAUDE.md prose and were routinely violated — 6 oversized
skills, 44 forbidden YAML fields in memory files at baseline. The fix: move knowledge
into trigger-loaded skills and enforcement into mechanical gates, judged by measured
numbers, never by eye.

## The 13 skills

| Skill | What it holds |
|---|---|
| [change-control](../Claude/skills/change-control/SKILL.md) | Change classes and gates; the three taboos (NAS rollback, no untested network changes, no unattended destructive ops); everything exits through /git-commit |
| [debugging-playbook](../Claude/skills/debugging-playbook/SKILL.md) | Symptom→cause→check→fix tables: uv, compose, Ansible, UniFi/Synology clients, bookshelf, Pi fleet, burned sessions |
| [failure-archaeology](../Claude/skills/failure-archaeology/SKILL.md) | ~20 settled battles with git-verified evidence, so nobody re-fights them |
| [homelab-architecture](../Claude/skills/homelab-architecture/SKILL.md) | Topology, design decisions with rationale, invariants, weak points, domain APIs as used here |
| [claude-config](../Claude/skills/claude-config/SKILL.md) | Every config axis: symlink sync, settings/hooks, session logging, skill routing, memory system |
| [python-env](../Claude/skills/python-env/SKILL.md) | uv-only stack, per-repo pins, machine bootstrap, eight verified traps |
| [homelab-operations](../Claude/skills/homelab-operations/SKILL.md) | Per-system runbooks with STOP gates on prod-touching steps |
| [diagnostics-toolkit](../Claude/skills/diagnostics-toolkit/SKILL.md) | Four tested scripts: skill_lint, memory_audit, research_scaffold, session_stats — measure, don't eyeball |
| [validation-and-qa](../Claude/skills/validation-and-qa/SKILL.md) | Evidence standards per change type; test inventory (150 passing at authoring) |
| [docs-house-style](../Claude/skills/docs-house-style/SKILL.md) | README/CLAUDE.md/INDEX templates, memory and research file schemas, skill authoring style |
| [new-project-bootstrap](../Claude/skills/new-project-bootstrap/SKILL.md) | New-repo and retrofit runbooks to house standard, with a measurable definition of done |
| [claude-discipline-campaign](../Claude/skills/claude-discipline-campaign/SKILL.md) | The flagship: phased, number-gated campaign to enforce session discipline mechanically |
| [workflow-research-methodology](../Claude/skills/workflow-research-methodology/SKILL.md) | Evidence bar, predict-numbers-first experiments, open research frontier |

Format: each skill is a ≤30-line `SKILL.md` router with a standalone `## Summary`,
depth in `references/`, executables in `scripts/`. Every reference ends with a dated
"Provenance and maintenance" section containing re-verification commands.

## Enforcement shipped alongside

- [check_skill_size.py](../Claude/hooks/check_skill_size.py) — global PreToolUse guard
  (promoted from macknet): blocks heavy skills from loading inline, fail-open.
- Four legacy flat skills trimmed to the size gate; lint now 17/17 clean.
- NAS "tested rollback" bar codified in
  [gates.md](../Claude/skills/change-control/references/gates.md).
- Memory debt cleared (44 forbidden fields, over-budget files); `node_type`/
  `originSessionId` grandfathered as harness-managed — the memory daemon re-injects
  them, so the old strip rule fought the platform.

## Results

Baseline → close: skill-gate violations 6→0, memory violations 24 files→0, guard hook
macknet-only→global. Also: macknet and steamdeck got real READMEs.

Commits: dotfiles `59942f4` `e32bc8f` `aaa7809` `02cf062`; macknet `26a60d2`;
steamdeck `0d8ce20`.

## Open items

PostToolUse lint-on-write hook (event semantics unverified); macknet's now-redundant
local guard hook; steamdeck's 7 legacy research filenames (rename vs grandfather);
periodic pytest re-runs. Full engagement detail:
`~/Projects/.claude/research/2026-07-04-skill-library-final-report-3fe064.md`.
