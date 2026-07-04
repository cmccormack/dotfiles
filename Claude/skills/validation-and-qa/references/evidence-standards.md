# Evidence standards by change type

## The no-CI reality

Nothing runs automatically in any repo — zero `.github/workflows` across the portfolio. The only
compensating control is the /git-commit flow's agent code-review gate (Step 3 of
`~/.claude/skills/git-commit.md`): an agent reviews the staged diff and must return LGTM. That gate
reads the diff — it never executes tests. Therefore:

- Run the relevant suite locally BEFORE invoking /git-commit.
- A session must never claim "tests pass" without the pasted run output in the transcript.

## Acceptance discipline

Before making the change, write down what success looks like as numbers or observables:

- predicted test count after the change ("19 → 21 passed, 0 failed"),
- expected command output ("`docker compose ps` shows cwa `Up (healthy)`"),
- expected diff shape ("check-mode reports changed=1, exactly the ssh config task").

Then produce that output and compare. If the prediction was wrong, say so — a surprise that happens
to pass is still a finding. "Works on my glance" is not evidence; a claim about behavior is a
command plus its output, nothing less.

## Standard per change type

| Change | Required evidence |
|---|---|
| Pure Python code | Relevant pytest suite run, pasted counts + exit line (commands in [test-inventory.md](test-inventory.md)). New behavior needs a new test, not just a passing old suite. |
| docker-compose / service | Concrete health check after apply: `docker compose ps` showing `Up`/`healthy`, plus one request proving the service answers (e.g. `curl -sf http://host:port/ >/dev/null && echo OK`). Runbooks live in homelab-operations; only the evidence bar lives here. |
| Ansible playbook | Check-mode diff BEFORE the real run: `ansible-playbook <play>.yml --check --diff`, pasted. Then the real run's `PLAY RECAP` (ok/changed/failed counts). A second `--check` run showing `changed=0` proves idempotence. |
| Claude config / skill | Diagnostics before and after: run the relevant diagnostics-toolkit script (skill size gate, memory budget, session audit) and paste both outputs so the delta is visible. |
| Docs / markdown | Link check on touched files, e.g. `grep -oE '\]\([^)]+\)' <file>.md` and confirm each relative path exists (`ls` each); render-check tables if edited. |
| Shell script (setup.sh etc.) | `bash -n <script>` at minimum; `shellcheck` if available; a real run only on a disposable target, with its output captured. |

## Provenance and maintenance

Written 2026-07-03 from `git-commit.md` (read directly) and the portfolio survey confirming zero CI
(`ls ~/Projects/{macknet,bookshelf,keylimepi,steamdeck,dotfiles}/.github 2>/dev/null` — all absent).
Re-verify: re-run that `ls`; if any repo gains CI, this file's premise changes — rewrite the
no-CI section.
