# How to Do Failure Archaeology Yourself

The chronicle ages; these commands don't. Run them in any repo before re-investigating.

## 1. Reverts and abandonments (rarely fruitful here — Chris fixes forward)
```bash
git log --all -i --grep=revert --grep=rollback --grep=abandon --grep='back out' --oneline
```

## 2. Removal commits — the real signal in this portfolio
```bash
git log --diff-filter=D --name-only --oneline          # every deleted file, with the commit
git log --all -i --grep='remove\|clean up\|drop' --oneline
git show --stat <hash>                                   # why + what a removal touched
```

## 3. Dead and merged branches
```bash
git branch -a
git log --oneline main..<branch>                         # empty = fully merged, safe to delete
git merge-base --is-ancestor <branch> main && echo merged
git worktree list                                        # stale agent worktrees (steamdeck had one)
```

## 4. Churn hotspots — where the fights happened
```bash
git log --all --name-only --pretty=format: | grep -v '^$' | sort | uniq -c | sort -rn | head -15
git log --follow --oneline -- <hot-file>                 # then read the story of one file
```

## 5. The investigation record (richer than git here)
```bash
ls .claude/research/                                     # YYYY-MM-DD-topic-{6hex}.md; older files lack date prefix
grep -rn -i 'reject\|dead.end\|abandon\|superseded\|verdict\|DO NOT' .claude/research/
grep -rn -i 'workaround\|gotcha\|known issue\|do not \|deprecated' --include='*.md' docs/ *.md
```
Look for adversarial pairs (`*-proposer-*` / `*-critic-*`, `*-promote-*` / `*-skeptic-*`) — read BOTH sides; the shipped design sometimes overruled the critic.

## 6. Session correlation
```bash
git notes --ref=refs/notes/claude list                   # commit → Claude session id
git notes --ref=refs/notes/claude show <hash>
```

## 7. Verify before citing
```bash
git show <hash> --stat                                   # hash must exist; never cite from memory
git status --short                                       # uncommitted work = the open frontier
```

Rules: if the story is incomplete, record what IS known and mark the gap — never fabricate a root cause. Distrust research-file claims that contradict primary evidence (logs, registries, DBs); one agent claim here was flat wrong.

## Provenance and maintenance

Written 2026-07-03; commands exercised against all 5 live repos while compiling chronicle.md. Re-verify: run sections 1–5 in any repo and confirm output shapes match (e.g., `git log --diff-filter=D` in ~/Projects/bookshelf should still show `b908a09`, `47670eb`).
