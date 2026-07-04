---
name: workflow-research-methodology
description: Load when proposing a workflow, tooling, or infra change; evaluating whether an experiment "worked"; deciding to adopt or retire an idea; judging if evidence is strong enough to change config; or looking for high-value open problems to work on next. Covers the evidence bar (one mechanism explains all observations, adversarial pass before adoption), predict-numbers-before-running, the hunch-to-adopted-or-retired lifecycle, and the portfolio's open research frontier.
---

## Summary
An idea becomes an accepted change here only through a fixed pipeline: hunch → dated,
tokened research file → measured experiment with numbers predicted BEFORE running →
adversarial pass by a second agent → adopted via change-control + `/git-commit`, or
retired with the failure written down. An experiment without a predicted number is a
wander, not a test. `frontier.md` lists the open problems worth that effort.

## Routing

| Situation | Read |
|---|---|
| Proposing a change; judging evidence; adopting or retiring an idea | [references/methodology.md](references/methodology.md) |
| Picking what to work on; assessing an open problem's first steps | [references/frontier.md](references/frontier.md) |

## When NOT to use this skill
- Executing the discipline campaign (enforcement work itself) → `claude-discipline-campaign`.
- Day-to-day evidence for commits (tests, verification before push) → `validation-and-qa`.
- Gating and classifying a change that is already decided → `change-control`.
- Digging into past incidents → `failure-archaeology`; live debugging → `debugging-playbook`.
