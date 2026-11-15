#!/bin/bash
# Git drift alarm: how far the main folder is from GitHub.
#
# Usage: scripts/git/drift-check.sh          prints one line, exit 1 on WARN, exit 2 on JAM
#        scripts/git/drift-check.sh --hook   PostToolUse hook: silent unless WARN, always exit 0
#
# WARN when main is 3 or more commits ahead of origin/main (commits stranded on the Mac)
# or 40 or more behind.
# JAM (exit 2) when the oldest commit that has not reached GitHub is more than 24 hours old.
# The morning brief clears a JAM with: scripts/git/safe-push.sh --adopt-stale (2026-10-05).
# Reads the last fetch; refetches when it is older than 30 minutes
# (in the background in hook mode, so the hook never waits on the network).

AHEAD_WARN=3
BEHIND_WARN=40
JAM_SECS=86400
FETCH_MAX_AGE=1800
WARN_EVERY=600

hook=0
[ "${1:-}" = "--hook" ] && hook=1

cd "$(dirname "$0")/../.." 2>/dev/null || exit 0
gitdir=$(git rev-parse --git-dir 2>/dev/null) || exit 0
gitdir=$(cd "$gitdir" && pwd -P)
commondir=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
branch=$(git symbolic-ref --quiet --short HEAD || true)

if [ "$gitdir" != "$commondir" ] || [ "$branch" != "main" ]; then
  [ $hook -eq 1 ] || echo "Git drift: not checked (this is not the main folder on branch main)"
  exit 0
fi

mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0; }
now=$(date +%s)
last=$(mtime "$gitdir/FETCH_HEAD")
stamp=$(mtime "$gitdir/drift-fetch-stamp")
[ "$stamp" -gt "$last" ] && last=$stamp

if [ $((now - last)) -gt $FETCH_MAX_AGE ]; then
  touch "$gitdir/drift-fetch-stamp"
  if [ $hook -eq 1 ]; then
    (git fetch -q origin </dev/null >/dev/null 2>&1 &)
  else
    git fetch -q origin 2>/dev/null
    last=$now
  fi
fi

counts=$(git rev-list --left-right --count main...origin/main 2>/dev/null) || exit 0
ahead=$(echo "$counts" | awk '{print $1}')
behind=$(echo "$counts" | awk '{print $2}')
age_min=$(( (now - last) / 60 ))

state="OK"
if [ "$ahead" -ge $AHEAD_WARN ] || [ "$behind" -ge $BEHIND_WARN ]; then
  state="WARN"
fi
oldest=$(git log --format=%ct origin/main..main 2>/dev/null | sort -n | head -1)
jam_note=""
if [ -n "$oldest" ] && [ $((now - oldest)) -gt $JAM_SECS ]; then
  state="JAM"
  jam_note=" Oldest unpushed commit is $(( (now - oldest) / 3600 )) hours old."
fi
line="Git drift $state: main folder is ahead $ahead / behind $behind against GitHub (last fetch ${age_min} min ago).$jam_note"
# The every-30-minutes checkout sync (scripts/two-mac/checkout-sync.py) writes its last result here.
sync_note=$(head -1 "$HOME/.absbyai-checkout-sync/status.txt" 2>/dev/null | tr -d '"\\' | cut -c1-700)
case "$sync_note" in
  STOPPED*) [ "$state" = "OK" ] && state="WARN"; line="$line Checkout sync $sync_note" ;;
esac

if [ $hook -eq 0 ]; then
  echo "$line"
  [ "$state" = "JAM" ] && exit 2
  [ "$state" = "WARN" ] && exit 1
  exit 0
fi

[ "$state" = "OK" ] && exit 0
warned=$(mtime "$gitdir/drift-warn-stamp")
[ $((now - warned)) -lt $WARN_EVERY ] && exit 0
touch "$gitdir/drift-warn-stamp"
advice="Push your own work with scripts/git/safe-push.sh as usual. If it stops on another session's files, your commit is safe: the checkout sync job (every 30 minutes on each Mac, scripts/two-mac/README.md) pushes it and levels this folder. If the line above says the sync STOPPED, do the fix it names; for files older than 2 hours safe-push.sh --adopt-stale still applies."
printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s %s"}}\n' "$line" "$line" "$advice"
exit 0
