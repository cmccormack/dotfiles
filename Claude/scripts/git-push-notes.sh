#!/bin/bash
# Pushes the current branch and the Claude session notes (refs/notes/claude) in ONE push,
# with SSH timeouts and up to three attempts. GitHub's SSH endpoint stalls now and then
# (measured 2026-09-19: a push that normally takes 1.6 s hung past 120 s twice in one
# session); without a timeout each stall eats the whole tool budget and needs a hand retry.
# Usage: git-push-notes.sh [remote]
set -uo pipefail

REMOTE="${1:-origin}"
ATTEMPTS="${GIT_PUSH_ATTEMPTS:-3}"
PER_TRY="${GIT_PUSH_TIMEOUT:-40}"
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o ConnectTimeout=10 -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o BatchMode=yes}"

branch=$(git symbolic-ref --quiet --short HEAD) || { echo "detached HEAD, nothing to push" >&2; exit 1; }
refspecs=("$branch")
git notes --ref=claude show HEAD &>/dev/null && refspecs+=("refs/notes/claude")

# perl alarm: macOS has no timeout(1). 142 = killed by the alarm.
try_push() { perl -e 'alarm shift; exec @ARGV' "$PER_TRY" git push "$REMOTE" "${refspecs[@]}"; }

for ((i = 1; i <= ATTEMPTS; i++)); do
  out=$(try_push 2>&1); rc=$?
  if [ $rc -eq 0 ]; then
    echo "$out" | grep -E -- '->|up-to-date' || echo "$out"
    [ ${#refspecs[@]} -eq 2 ] && echo "Notes pushed to $REMOTE"
    exit 0
  fi
  if [ $rc -eq 142 ]; then echo "attempt $i/$ATTEMPTS: push hung past ${PER_TRY}s" >&2
  else echo "attempt $i/$ATTEMPTS failed (rc=$rc): $(echo "$out" | tail -1)" >&2; fi
  [ $i -lt "$ATTEMPTS" ] && sleep $((i * 3))
done
echo "push to $REMOTE failed after $ATTEMPTS attempts; branch $branch is still ahead" >&2
exit 1
