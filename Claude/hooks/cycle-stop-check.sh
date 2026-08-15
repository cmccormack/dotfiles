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

Tradeoff on the closing-line check (2d in the task spec): last_assistant_message
turned out to be handed to us directly, which is much more reliable than
transcript parsing, but it's still soft/best-effort by design, if it's missing
or doesn't match we only warn via systemMessage, never hard-block solely on it.
The placeholder and Claimed-by checks are the hard gates.
"""
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
            soft_notes.append(
                "final assistant message did not end with the required closing line "
                f"'{CLOSING_LINE}' (see cycle/references/session-end.md)"
            )

    if hard_failures:
        reason = f"cycle-stop-check: RESUME.md at {scope} is not handoff-ready.\n\n"
        reason += "\n".join(f"- {f}" for f in hard_failures)
        if soft_notes:
            reason += "\n\nAlso noted (not blocking):\n" + "\n".join(f"- {n}" for n in soft_notes)
        print(json.dumps({"decision": "block", "reason": reason}))
        return

    if soft_notes:
        print(json.dumps({"systemMessage": "cycle-stop-check: " + "; ".join(soft_notes)}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
