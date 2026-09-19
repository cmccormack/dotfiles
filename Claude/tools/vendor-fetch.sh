#!/usr/bin/env bash
# Verbatim vendor-doc fetch for the vendor-docs agent. WebFetch returns model-summarised
# prose, so it cannot produce canonical copies; this wrapper can, and it keeps the
# allowlist honest: the URL host must be a WebFetch(domain:...) entry in the global
# settings.json, and the output path must sit under a docs/vendor/ tree.
# Usage: vendor-fetch.sh <url> <out-file> [--raw|--render]
#   --raw     curl only (raw.githubusercontent.com, llms.txt, ?action=raw); default for
#             hosts in RAW_HOSTS
#   --render  headless Chromium via ~/.claude/tools/web_fetch.py, body as markdown
# Exit 64 bad input or path, 65 domain not allowlisted, 66 fetch failed or empty.
set -u
SETTINGS="$HOME/.claude/settings.json"
RAW_HOSTS="raw.githubusercontent.com"
url=${1:-}; out=${2:-}; mode=${3:-}
[ -n "$url" ] && [ -n "$out" ] || { echo "usage: vendor-fetch.sh <url> <out-file> [--raw|--render]" >&2; exit 64; }
case $url in https://*) ;; *) echo "https only: $url" >&2; exit 64 ;; esac
case $out in */docs/vendor/*) ;; *) echo "out-file must be under a docs/vendor/ tree: $out" >&2; exit 64 ;; esac
case $out in *..*) exit 64 ;; esac
host=${url#https://}; host=${host%%/*}; host=${host##*@}; host=${host%%:*}
case $host in ""|*[!A-Za-z0-9.-]*) echo "bad host: $url" >&2; exit 64 ;; esac
python3 - "$host" "$SETTINGS" <<'EOF'; rc=$?; [ $rc -eq 0 ] || exit $rc
import json, sys
host, settings = sys.argv[1], sys.argv[2]
try:
    allow = {e[len("WebFetch(domain:"):-1] for e in json.load(open(settings))["permissions"]["allow"] if e.startswith("WebFetch(domain:")}
except Exception as exc:
    print(f"cannot read allowlist {settings}: {exc}", file=sys.stderr); sys.exit(64)
if host not in allow:
    print(f'BLOCKED: "WebFetch(domain:{host})" is not in dotfiles/Claude/settings.json', file=sys.stderr); sys.exit(65)
EOF
[ -z "$mode" ] && { case " $RAW_HOSTS " in *" $host "*) mode=--raw ;; *) case $url in *.txt|*.md|*action=raw*) mode=--raw ;; *) mode=--render ;; esac ;; esac; }
mkdir -p "$(dirname "$out")"
tmp=$(mktemp) || exit 66
if [ "$mode" = --raw ]; then
  curl -fsSL --max-time 60 -A "vendor-fetch (deckops docs mirror)" -o "$tmp" "$url" || { rm -f "$tmp"; echo "fetch failed: $url" >&2; exit 66; }
else
  "$HOME/.local/pipx/venvs/playwright/bin/python" "$HOME/.claude/tools/web_fetch.py" "$url" --output "$tmp.json" >/dev/null 2>&1 || { rm -f "$tmp" "$tmp.json"; echo "render failed: $url" >&2; exit 66; }
  python3 - "$tmp.json" "$tmp" <<'EOF' || { rm -f "$tmp" "$tmp.json"; exit 66; }
import json, sys
d = json.load(open(sys.argv[1]))
if d.get("error") or not d.get("body_markdown", "").strip():
    print(f"render empty: {d.get('error') or 'no body'}", file=sys.stderr); sys.exit(1)
open(sys.argv[2], "w").write(d["body_markdown"])
EOF
  rm -f "$tmp.json"
fi
[ -s "$tmp" ] || { rm -f "$tmp"; echo "empty body: $url" >&2; exit 66; }
{ printf 'source: %s\nfetched: %s\nmethod: %s\n\n' "$url" "$(date +%F)" "${mode#--}"; cat "$tmp"; } > "$out"
rm -f "$tmp"
echo "$out $(wc -c < "$out" | tr -d ' ') bytes"
