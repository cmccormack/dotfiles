#!/usr/bin/env bash
# Read-only device access for Claude agents. Fixed hosts, fixed verbs, dedicated key.
# The real boundary is the forced command bound to that key on each device; this
# wrapper only shapes the request and makes failures legible.
# Usage: dev-ro.sh <deck-oled|deck-lcd|gaming-pc> <verb> [args]
set -u
KEY="$HOME/.ssh/agent_ro_ed25519"
usage() { echo "usage: dev-ro.sh <host> <verb> [args]  (dev-ro.sh <host> verbs)" >&2; exit 64; }
[ $# -ge 2 ] || usage
host=$1; verb=$2; shift 2

case $host in
  deck-oled) target=deck@192.168.1.30; port=22; platform=deck ;;
  deck-lcd)  target=deck@192.168.1.25; port=22; platform=deck ;;
  gaming-pc) target=svc-agent@192.168.1.40; port=2222; platform=pc ;;
  *) echo "unknown host: $host" >&2; usage ;;
esac

deck_verbs="verbs journal nm nm-conf iw steam-log flatpak pw-top file"
pc_verbs="verbs sunshine-log sunshine-conf streaming-log controller-log steam-log localconfig-grep audio-endpoints event-log file"
[ $platform = deck ] && verbs=$deck_verbs || verbs=$pc_verbs
case " $verbs " in *" $verb "*) ;; *) echo "unknown verb for $host: $verb (allowed: $verbs)" >&2; exit 64 ;; esac

for a in "$@"; do
  case $a in
    *[!A-Za-z0-9._/:@\\=-]*) echo "rejected argument: $a" >&2; exit 64 ;;
  esac
done

[ -r "$KEY" ] || { echo "BLOCKED: agent key $KEY missing" >&2; exit 66; }

run() {
  perl -e 'alarm shift; exec @ARGV' 30 \
    ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=5 \
        -o ControlMaster=no -o ControlPath=none -o StrictHostKeyChecking=yes \
        -o ServerAliveInterval=5 -o ServerAliveCountMax=2 \
        -p "$port" "$target" "$verb $*"
}

run; rc=$?
if [ $rc -eq 255 ]; then sleep 2; run; rc=$?; fi
if [ $rc -eq 255 ] || [ $rc -eq 142 ]; then
  echo "BLOCKED: $host unreachable, owner must wake it (never wake a device from an agent)" >&2
  exit 69
fi
exit $rc
