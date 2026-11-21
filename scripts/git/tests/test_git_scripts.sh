#!/bin/bash
# Tests for safe-push.sh (stale and live blocking files, --adopt-stale) and drift-check.sh
# (the 24-hour JAM). Everything runs in throwaway clones under a temp folder, never here.
#
# Usage: scripts/git/tests/test_git_scripts.sh

here=$(cd "$(dirname "$0")/.." && pwd -P)
root=$(mktemp -d "${TMPDIR:-/tmp}/git-scripts-test.XXXXXX")
trap 'rm -rf "$root"' EXIT
pass=0
fail=0

ok()  { pass=$((pass + 1)); echo "  ok   $1"; }
bad() { fail=$((fail + 1)); echo "  FAIL $1"; [ -n "${2:-}" ] && echo "$2" | sed 's/^/       /'; }
check() { # check <name> <condition result> [detail]
  if [ "$2" -eq 0 ]; then ok "$1"; else bad "$1" "${3:-}"; fi
}

# A fresh origin, a "main folder" clone and a second clone that plays GitHub's other pushers.
setup() {
  w="$root/$1"
  mkdir -p "$w"
  git init -q --bare -b main "$w/origin.git"
  git clone -q "$w/origin.git" "$w/main" 2>/dev/null
  cd "$w/main" || exit 1
  git config user.email t@example.com; git config user.name test
  mkdir -p scripts/git
  cp "$here/safe-push.sh" "$here/drift-check.sh" scripts/git/
  printf 'line %s\n' 1 2 3 4 5 6 7 8 9 10 > shared.txt
  printf 'line %s\n' 1 2 3 4 5 6 7 8 9 10 > shared2.txt
  git add -A && git commit -q -m base && git push -q origin main
  git clone -q "$w/origin.git" "$w/other"
  git -C "$w/other" config user.email o@example.com; git -C "$w/other" config user.name other
}

upstream_edit() { # GitHub gets a newer first line of the named files
  local f
  for f in "$@"; do
    sed -i.bak '1s/.*/line 1 from GitHub/' "$w/other/$f" && rm "$w/other/$f.bak"
  done
  git -C "$w/other" commit -q -am "upstream edit" && git -C "$w/other" push -q origin main
}

local_edit() { echo "unsaved edit from another session" >> "$w/main/$1"; }
backdate()   { touch -t "$(date -v-3H '+%Y%m%d%H%M' 2>/dev/null || date -d '3 hours ago' '+%Y%m%d%H%M')" "$w/main/$1"; }
push_mine()  { echo "mine $RANDOM" > mine.txt; out=$(scripts/git/safe-push.sh "$@" -m "my change" -- mine.txt 2>&1); rc=$?; }

echo "safe-push: blocking file edited in the last 2 hours"
setup live; upstream_edit shared.txt; local_edit shared.txt
push_mine --adopt-stale
check "stops with exit 2" $([ $rc -eq 2 ]; echo $?) "$out"
check "says the owner is live" $(echo "$out" | grep -q "owner is live, retry later"; echo $?) "$out"
check "leaves the other session's edit on disk, uncommitted" $(git diff --quiet HEAD -- shared.txt; [ $? -eq 1 ]; echo $?)
check "pushes nothing" $([ "$(git rev-list --count origin/main..HEAD)" -eq 1 ]; echo $?)
check "makes no backup" $([ ! -d tmp ]; echo $?)

echo "safe-push: blocking file older than 2 hours, no flag"
setup stale; upstream_edit shared.txt; local_edit shared.txt; backdate shared.txt
push_mine
check "stops with exit 2" $([ $rc -eq 2 ]; echo $?) "$out"
check "says to commit these and re-run" $(echo "$out" | grep -q "commit these and re-run"; echo $?) "$out"
check "prints the last-modified time" $(echo "$out" | grep -q "shared.txt | last modified .* | stale"; echo $?) "$out"
check "leaves the edit uncommitted" $(git diff --quiet HEAD -- shared.txt; [ $? -eq 1 ]; echo $?)

echo "safe-push: blocking file older than 2 hours, --adopt-stale"
setup adopt; upstream_edit shared.txt; local_edit shared.txt; backdate shared.txt
push_mine --adopt-stale
check "pushes with exit 0" $([ $rc -eq 0 ]; echo $?) "$out"
check "GitHub has everything" $([ "$(git rev-parse HEAD)" = "$(git -C "$w/origin.git" rev-parse main)" ]; echo $?)
check "the stale file was committed under the standard message" \
  $(git log --format=%s -- shared.txt | grep -q "Commit pending edits from earlier sessions so main can merge"; echo $?)
check "the file keeps the old session's edit" $(grep -q "unsaved edit from another session" shared.txt; echo $?)
check "the file also has GitHub's change" $(grep -q "line 1 from GitHub" shared.txt; echo $?)
check "a backup sits under tmp/" $(grep -qs "unsaved edit from another session" tmp/safe-push-adopt-*/shared.txt; echo $?)

echo "safe-push: one stale file and one live file, --adopt-stale"
setup mixed; upstream_edit shared.txt shared2.txt; local_edit shared.txt; local_edit shared2.txt; backdate shared.txt
push_mine --adopt-stale
check "stops with exit 2" $([ $rc -eq 2 ]; echo $?) "$out"
check "adopts nothing" $(git diff --quiet HEAD -- shared.txt; [ $? -eq 1 ] && [ ! -d tmp ]; echo $?)

echo "drift-check: age of the oldest unpushed commit"
setup drift
out=$(scripts/git/drift-check.sh); rc=$?
check "level with GitHub is OK, exit 0" $([ $rc -eq 0 ] && echo "$out" | grep -q "Git drift OK"; echo $?) "$out"
echo a > a.txt; git add a.txt; git commit -q -m fresh
out=$(scripts/git/drift-check.sh); rc=$?
check "a fresh unpushed commit is still OK" $([ $rc -eq 0 ]; echo $?) "$out"
old=$(( $(date +%s) - 90000 ))
echo b > b.txt; git add b.txt
GIT_COMMITTER_DATE="@$old" GIT_AUTHOR_DATE="@$old" git commit -q -m "25 hours old"
out=$(scripts/git/drift-check.sh); rc=$?
check "an unpushed commit over 24 hours old exits non-zero" $([ $rc -eq 2 ]; echo $?) "$out"
check "and prints one JAM line" $([ "$(echo "$out" | wc -l)" -eq 1 ] && echo "$out" | grep -q "Git drift JAM"; echo $?) "$out"
git push -q origin main
out=$(scripts/git/drift-check.sh); rc=$?
check "after the push it is OK again" $([ $rc -eq 0 ]; echo $?) "$out"

echo
echo "$pass passed, $fail failed"
[ $fail -eq 0 ]
