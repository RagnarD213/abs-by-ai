#!/bin/bash
# Git drift alarm: how far the main folder is from GitHub.
#
# Usage: scripts/git/drift-check.sh          prints one line, exit 1 on WARN
#        scripts/git/drift-check.sh --hook   PostToolUse hook: silent unless WARN, always exit 0
#
# WARN when main is 3 or more commits ahead of origin/main (commits stranded on the Mac)
# or 40 or more behind. Reads the last fetch; refetches when it is older than 30 minutes
# (in the background in hook mode, so the hook never waits on the network).

AHEAD_WARN=3
BEHIND_WARN=40
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
line="Git drift $state: main folder is ahead $ahead / behind $behind against GitHub (last fetch ${age_min} min ago)."

if [ $hook -eq 0 ]; then
  echo "$line"
  [ "$state" = "WARN" ] && exit 1
  exit 0
fi

[ "$state" = "WARN" ] || exit 0
warned=$(mtime "$gitdir/drift-warn-stamp")
[ $((now - warned)) -lt $WARN_EVERY ] && exit 0
touch "$gitdir/drift-warn-stamp"
advice="Commits are not reaching GitHub. Push with scripts/git/safe-push.sh; if it stops, report the files and add one board entry instead of committing more on top."
printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s %s"}}\n' "$line" "$line" "$advice"
exit 0
