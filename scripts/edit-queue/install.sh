#!/bin/sh
# Install (or remove) the overnight edit queue's two launchd jobs for this user.
#   scripts/edit-queue/install.sh            install + start. The queue starts PAUSED if no PAUSE decision exists yet.
#   scripts/edit-queue/install.sh uninstall  stop + remove both jobs (scripts, job list and scoreboard are untouched)
set -eu
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH= cd -- "$HERE/../.." && pwd)"
AGENTS="$HOME/Library/LaunchAgents"
DOMAIN="gui/$(id -u)"
for L in com.absbyai.edit-queue com.absbyai.edit-queue-review; do
  launchctl bootout "$DOMAIN/$L" 2>/dev/null || true
  rm -f "$AGENTS/$L.plist"
done
[ "${1:-}" = "uninstall" ] && { echo "Removed. Nothing runs on its own now."; exit 0; }
mkdir -p "$AGENTS" "$HOME/Library/Logs/absbyai-edit-queue"
# First install starts paused: un-pausing is a deliberate act (dispatcher.py resume).
[ -f "$HERE/.installed-once" ] || { python3 "$HERE/dispatcher.py" pause >/dev/null; : > "$HERE/.installed-once"; }
for L in com.absbyai.edit-queue com.absbyai.edit-queue-review; do
  sed -e "s|__ROOT__|$ROOT|g" -e "s|__HOME__|$HOME|g" "$HERE/launchd/$L.plist" > "$AGENTS/$L.plist"
  launchctl bootstrap "$DOMAIN" "$AGENTS/$L.plist"
done
echo "Installed. Dispatcher ticks every 15 min; review page: http://127.0.0.1:8830"
[ -f "$HERE/PAUSE" ] && echo "The queue is PAUSED (scripts/edit-queue/PAUSE exists). Resume: python3 scripts/edit-queue/dispatcher.py resume"
echo "Logs: ~/Library/Logs/absbyai-edit-queue/"
