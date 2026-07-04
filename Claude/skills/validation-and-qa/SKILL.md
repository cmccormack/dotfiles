---
name: validation-and-qa
description: What counts as evidence in this portfolio and how to produce it. Load when about to claim something works or is fixed; before adding or running tests in macknet, dotfiles, steamdeck, bookshelf, or keylimepi; when deciding what evidence a change needs before /git-commit; when verifying a compose/service, Ansible, or config change actually took effect; or when asked whether anything here is tested.
---

## Summary

No CI exists anywhere in the portfolio — every claim of "works" must be backed by a command and its
pasted output, produced locally BEFORE /git-commit. Three pytest suites are the verified core
(macknet 19, dotfiles 102, steamdeck 29 — all passing 2026-07-03); everything else (scripts,
playbooks, setup.sh) is untested inventory. Define expected numbers before changing, not after.

## Rules

1. Run tests locally before invoking /git-commit — its agent code review reads the diff only; it never runs tests.
2. Never claim "tests pass" without the run's pasted output (counts + exit line).
3. Declare acceptance criteria BEFORE the change: predicted test count, expected health/diff output. "Works on my glance" is not evidence.
4. Every behavior claim in a summary or commit needs command + output; link the output, don't paraphrase it.
5. If a suite fails or can't run, record that honestly — a skipped suite is a finding, not a pass.

## Routing

| Need | Read |
|---|---|
| Which repos have tests, exact run commands, current pass state | [references/test-inventory.md](references/test-inventory.md) |
| Evidence required per change type (code/compose/Ansible/config/docs) | [references/evidence-standards.md](references/evidence-standards.md) |
| Writing new tests to house conventions (layout, fixtures, markers) | [references/adding-tests.md](references/adding-tests.md) |

## When NOT to use

Diagnosing a failure → debugging-playbook. Whether a change is allowed / gating policy → change-control. Service start/stop/deploy runbooks → homelab-operations.
