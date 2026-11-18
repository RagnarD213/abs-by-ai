#!/bin/bash
# Install the ETA refresh LaunchAgent on THIS Mac (the M6 only: it reads the M2 over ssh).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"
PY="$(xcrun --find python3 2>/dev/null || command -v python3)"
L=com.absbyai.edit-eta; AG="$HOME/Library/LaunchAgents"
sed -e "s|__ROOT__|$ROOT|g" -e "s|__HOME__|$HOME|g" -e "s|__PYTHON__|$PY|g" "$HERE/$L.plist" > "$AG/$L.plist"
launchctl bootout "gui/$(id -u)/$L" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$AG/$L.plist"
echo "installed $L (every 10 minutes); log ~/Library/Logs/absbyai-edit-eta.log"
