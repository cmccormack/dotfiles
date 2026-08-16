#!/usr/bin/env python3
"""Stop hook: enforce /cycle RESUME.md handoff discipline before a session ends.

Named .sh to match the cycle skill's docs (session-end.md references
"cycle-stop-check.sh" by name), but implemented in Python: JSON parsing and the
multiline placeholder / "## Claimed by" regex work are far more reliable here
than in bash, and this is the first BLOCKING Stop hook in this repo so
robustness matters more than language purity. Registered in settings.json as
`python3 $HOME/.claude/hooks/cycle-stop-check.sh` (no shell wrapper needed).

Fail-open: any internal error must never block a session from ending (same
try/except-around-main pattern as check_skill_size.py). This hook is a no-op,
near-zero cost, for the vast majority of repos/locations that don't use /cycle:
it returns immediately once no TODO.md+ISSUES.md+RESUME.md scope is found
between cwd and the git repo root.

JSON contract verified against https://code.claude.com/docs/en/hooks (fetched
2026-08-15): Stop hooks receive `stop_hook_active` and `last_assistant_message`
directly in the input payload (no transcript_path parsing needed for the
closing-line check). To block, exit 0 and print {"decision": "block", "reason":
"..."} to stdout; reason is required when decision is "block". Omitting
"decision" allows the stop. `systemMessage` surfaces a non-blocking warning to
the user.

Closing-line check (hard gate since 2026-08-15, was soft/systemMessage-only at
launch): a real session ended without the closing line despite RESUME.md being
otherwise clean (no placeholder, empty Claimed-by), and the systemMessage warning
was not enough to catch it, so this hard-blocks in that specific case.

Gated by a marker (2026-08-16): Claude Code's Stop hook fires after EVERY
assistant turn, not just when a session is truly ending, so the closing-line
check on its own hard-blocked ordinary mid-conversation replies too. It is now
gated on the marker cycle-mark-active.py writes when the `cycle` skill is
invoked: if this session never claimed cycle work at this scope, the check is
skipped entirely; if it did but no tracker-file commit has landed since the
claim, the check is skipped (nothing to hand off yet) or soft (mid-edit,
uncommitted); it only hard-blocks once a tracker-file commit has landed since
the claim and the closing line is still missing, that is the actual "looked
done but wasn't" signature the 2026-08-15 incident needs.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TRACKER_FILES = ("TODO.md", "ISSUES.md", "RESUME.md")
CLOSING_LINE = "\U0001f504 Ready to /clear and run /cycle."
PLACEHOLDER_RE = re.compile(r"<[^<>]+>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CLAIMED_BY_RE = re.compile(r"^##\s*Claimed by\s*$", re.M)
NEXT_HEADING_RE = re.compile(r"^##\s", re.M)
STATE_DIR = Path.home() / ".claude" / "state" / "cycle-active"


def find_repo_root(cwd):
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def find_scope(cwd, repo_root):
    d = Path(cwd).resolve()
    root = Path(repo_root).resolve()
    seen = set()
    while d not in seen:
        seen.add(d)
        if all((d / f).is_file() for f in TRACKER_FILES):
            return d
        if d == root or d.parent == d:
            return None
        d = d.parent
    return None


def check_placeholders(text):
    stripped = COMMENT_RE.sub("", text)
    return PLACEHOLDER_RE.findall(stripped)


def check_claimed_by(text):
    m = CLAIMED_BY_RE.search(text)
    if not m:
        return None  # section missing entirely isn't this check's concern
    rest = text[m.end():]
    nxt = NEXT_HEADING_RE.search(rest)
    body = rest[:nxt.start()] if nxt else rest
    body = body.strip()
    return body or None


def git_dirty(scope):
    try:
        out = subprocess.run(
            ["git", "-C", str(scope), "status", "--porcelain", "--", *TRACKER_FILES],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return []
    if out.returncode != 0:
        return []
    return [line[3:] for line in out.stdout.splitlines() if line.strip()]


def read_marker(scope):
    key = hashlib.sha1(str(scope).encode()).hexdigest()
    marker_path = STATE_DIR / f"{key}.json"
    try:
        return marker_path, json.loads(marker_path.read_text())
    except Exception:
        return marker_path, None


def committed_since(scope, created_utc):
    try:
        out = subprocess.run(
            ["git", "-C", str(scope), "log", f"--since={created_utc}",
             "--oneline", "--", *TRACKER_FILES],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return False
    return out.returncode == 0 and bool(out.stdout.strip())


def main():
    payload = json.load(sys.stdin)

    if payload.get("stop_hook_active"):
        return  # one shot per stretch of work; never re-trap on a stuck condition

    cwd = payload.get("cwd") or "."
    repo_root = find_repo_root(cwd)
    if not repo_root:
        return  # not inside a git repo; nothing to enforce

    scope = find_scope(cwd, repo_root)
    if scope is None:
        return  # this repo/location isn't using /cycle

    resume_path = scope / "RESUME.md"
    text = resume_path.read_text(encoding="utf-8", errors="replace")

    hard_failures = []

    placeholders = check_placeholders(text)
    if placeholders:
        sample = ", ".join(placeholders[:5])
        hard_failures.append(
            f"RESUME.md ({resume_path}) still has unresolved template placeholder(s): "
            f"{sample}. Fill in every <...> marker before ending the session."
        )

    claimed = check_claimed_by(text)
    if claimed:
        hard_failures.append(
            f"RESUME.md ({resume_path}) '## Claimed by' section is not empty "
            f'("{claimed[:80]}"). Clear it before ending the session, a non-empty '
            "claim means the work was left mid-flight without a proper handoff."
        )

    soft_notes = []

    dirty = git_dirty(scope)
    if dirty:
        soft_notes.append(
            "tracker file(s) uncommitted at scope: " + ", ".join(dirty) +
            " (not a hard blocker, may be about to be committed as the session's last step)"
        )

    marker_path, marker = read_marker(scope)
    session_id = payload.get("session_id")
    marker_active = bool(marker) and marker.get("session_id") == session_id
    closed_out_clean = False

    if marker_active and committed_since(scope, marker["created_utc"]):
        last_msg = payload.get("last_assistant_message")
        if not last_msg:
            soft_notes.append(
                "could not check closing line: last_assistant_message was empty/missing "
                "in the Stop hook payload"
            )
        else:
            rstripped = last_msg.rstrip()
            last_line = rstripped.splitlines()[-1].strip() if rstripped else ""
            if last_line != CLOSING_LINE:
                hard_failures.append(
                    "final assistant message did not end with the required closing line "
                    f"'{CLOSING_LINE}' on its own line (see cycle/references/session-end.md)"
                )
            else:
                closed_out_clean = True
    elif marker_active and dirty:
        soft_notes.append(
            "cycle session active with uncommitted tracker changes, "
            "closing-line check deferred until a handoff commit lands"
        )
    # else: no active-cycle marker for this session, or nothing committed yet —
    # this Stop event isn't a cycle handoff attempt, skip the closing-line check.

    if hard_failures:
        reason = f"cycle-stop-check: RESUME.md at {scope} is not handoff-ready.\n\n"
        reason += "\n".join(f"- {f}" for f in hard_failures)
        if soft_notes:
            reason += "\n\nAlso noted (not blocking):\n" + "\n".join(f"- {n}" for n in soft_notes)
        print(json.dumps({"decision": "block", "reason": reason}))
        return

    if closed_out_clean:
        try:
            marker_path.unlink(missing_ok=True)
        except Exception:
            pass

    if soft_notes:
        print(json.dumps({"systemMessage": "cycle-stop-check: " + "; ".join(soft_notes)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
