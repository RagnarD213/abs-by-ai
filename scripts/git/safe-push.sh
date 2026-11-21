#!/bin/bash
# The one way a session pushes from the shared main folder.
#
# Usage: scripts/git/safe-push.sh [--adopt-stale] -m "commit message" -- <path> [<path> ...]
#
# Commits ONLY the named paths, merges origin/main (never rebases, never stashes), pushes.
# Other sessions' uncommitted edits stay on disk untouched. If one of them is in the way it
# stops and lists the files with their last-modified times instead of guessing.
#
# Rules (Dan, 2026-10-05, AGENTS.md "Delivery and deployment"):
#   - A shared file (.claude/skills/_shared/, AGENTS.md, CLAUDE.md, Docs/, scripts/, any skill
#     file another job uses) is pushed with this script the moment it is edited.
#   - When this stops on exit 2 and EVERY blocking file was last modified more than 2 hours
#     ago, clear it: re-run with --adopt-stale. That backs the files up under tmp/, commits
#     them as they are and carries on with the merge and push. If any blocking file is newer
#     than 2 hours its owner is live: put up the board note and retry at the end of the task.
#
# Exit codes: 0 pushed, 1 usage or refused to start, 2 stopped on another session's files,
#             3 merge conflict (needs a hand merge), 4 push failed.

set -u

MAX_TRIES=3
STALE_SECS=7200          # a blocking file untouched this long has no live owner
ADOPT_MSG="Commit pending edits from earlier sessions so main can merge"
adopt=0
msg=""
paths=()

usage() {
  echo "usage: scripts/git/safe-push.sh [--adopt-stale] -m \"commit message\" -- <path> [<path> ...]" >&2
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    -m) [ $# -ge 2 ] || usage; msg="$2"; shift 2 ;;
    --adopt-stale) adopt=1; shift ;;
    --) shift; while [ $# -gt 0 ]; do paths+=("$1"); shift; done ;;
    -h|--help) usage ;;
    *) echo "safe-push: unknown argument: $1" >&2; usage ;;
  esac
done

[ -n "$msg" ] || { echo "safe-push: refused, no commit message (-m)" >&2; exit 1; }
[ ${#paths[@]} -gt 0 ] || { echo "safe-push: refused, no paths given. Name the files to commit after --" >&2; exit 1; }

top=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "safe-push: refused, not inside a git repository" >&2; exit 1; }
gitdir=$(cd "$(git rev-parse --git-dir)" && pwd -P)
commondir=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
if [ "$gitdir" != "$commondir" ]; then
  echo "safe-push: refused, this is a worktree. Worktrees push from their own clean checkout with plain git." >&2
  exit 1
fi
branch=$(git symbolic-ref --quiet --short HEAD || true)
if [ "$branch" != "main" ]; then
  echo "safe-push: refused, branch is '${branch:-detached}', not main" >&2
  exit 1
fi
for marker in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD rebase-merge rebase-apply; do
  if [ -e "$gitdir/$marker" ]; then
    echo "safe-push: refused, a merge, rebase or cherry-pick is in progress ($marker). Finish or abort it first." >&2
    exit 1
  fi
done

finish() { # finish <exit code> <stopped-on text>
  local counts ahead behind
  counts=$(git rev-list --left-right --count HEAD...origin/main 2>/dev/null || echo "? ?")
  ahead=$(echo "$counts" | awk '{print $1}')
  behind=$(echo "$counts" | awk '{print $2}')
  local verb="NOT pushed"
  [ "$1" -eq 0 ] && verb="pushed"
  echo "safe-push: $verb $(git rev-parse --short HEAD) | ahead $ahead / behind $behind | stopped on: $2"
  exit "$1"
}

# --- step 2: commit only the named paths -------------------------------------------------
git add -- "${paths[@]}" || { echo "safe-push: git add failed, nothing committed" >&2; exit 1; }
if git diff --cached --quiet HEAD -- "${paths[@]}"; then
  echo "safe-push: nothing to commit in the named paths, pushing earlier commits if any"
else
  # A commit with paths takes only those paths, even if another session has files staged.
  git commit -q -m "$msg" -- "${paths[@]}" || { echo "safe-push: git commit failed" >&2; exit 1; }
  echo "safe-push: committed $(git rev-parse --short HEAD)"
fi

cd "$top" || exit 1

is_site_data() { # root *-data.json: the live site writes these, GitHub's version wins
  case "$1" in
    */*) return 1 ;;
    *-data.json) return 0 ;;
    *) return 1 ;;
  esac
}

same_as_origin() { # local file is byte-identical to origin/main's copy
  local f="$1" theirs mine
  [ -f "$f" ] && [ ! -L "$f" ] || return 1
  theirs=$(git rev-parse --verify --quiet "origin/main:$f") || return 1
  mine=$(git hash-object -- "$f") || return 1
  [ "$mine" = "$theirs" ]
}

# --- step 4: look at what the merge would touch, without touching the disk --------------
preflight() {
  clear_tracked=()
  clear_untracked=()
  blockers=()
  blocker_paths=()
  local f
  while IFS= read -r -d '' f; do
    if git cat-file -e "HEAD:$f" 2>/dev/null; then
      git diff --quiet HEAD -- "$f" && continue          # clean, the merge handles it
      if same_as_origin "$f" || is_site_data "$f"; then
        clear_tracked+=("$f")
      else
        blockers+=("$f"); blocker_paths+=("$f")
      fi
    else
      [ -e "$f" ] || [ -L "$f" ] || continue              # not on disk, nothing in the way
      if same_as_origin "$f"; then
        clear_untracked+=("$f")
      else
        blockers+=("$f"); blocker_paths+=("$f")
      fi
    fi
  done < <(git diff --name-only --no-renames -z HEAD...origin/main)

  # Anything another session has staged blocks a merge outright.
  while IFS= read -r -d '' f; do
    local known=0 c
    for c in ${clear_tracked[@]+"${clear_tracked[@]}"} ${clear_untracked[@]+"${clear_untracked[@]}"} ${blockers[@]+"${blockers[@]}"}; do
      [ "$c" = "$f" ] && { known=1; break; }
    done
    [ $known -eq 1 ] || { blockers+=("$f (staged)"); blocker_paths+=("$f"); }
  done < <(git diff --cached --name-only --no-renames -z HEAD)
}

mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; }

# Sorts the blockers into stale (untouched for 2 hours or more) and live, and prints each
# one's last-modified time. A file missing from disk has no time to read, so it counts as live.
age_blockers() {
  stale_paths=()
  live_count=0
  local now i f m age when
  now=$(date +%s)
  for i in "${!blockers[@]}"; do
    f="${blocker_paths[$i]}"
    m=""
    { [ -e "$f" ] || [ -L "$f" ]; } && m=$(mtime "$f")
    if [ -z "$m" ]; then
      live_count=$((live_count + 1))
      echo "  ${blockers[$i]} | missing on disk, no modified time | treat as live"
      continue
    fi
    age=$((now - m))
    when=$(date -r "$m" '+%Y-%m-%d %H:%M' 2>/dev/null || date -d "@$m" '+%Y-%m-%d %H:%M')
    if [ "$age" -ge $STALE_SECS ]; then
      stale_paths+=("$f")
      echo "  ${blockers[$i]} | last modified $when ($((age / 3600)) h ago) | stale"
    else
      live_count=$((live_count + 1))
      echo "  ${blockers[$i]} | last modified $when ($((age / 60)) min ago) | LIVE"
    fi
  done
}

# Backs the stale blockers up under tmp/ and commits them exactly as they are on disk.
adopt_stale() {
  local dir f
  dir="tmp/safe-push-adopt-$(date +%Y%m%d-%H%M%S)"
  for f in "${stale_paths[@]}"; do
    mkdir -p "$dir/$(dirname "$f")" && cp -pR "$f" "$dir/$f" || {
      echo "safe-push: could not back up '$f', nothing adopted"
      finish 2 "backup failed"
    }
  done
  echo "safe-push: backed up ${#stale_paths[@]} stale file(s) to $dir/"
  git add -- "${stale_paths[@]}" && git commit -q -m "$ADOPT_MSG" -- "${stale_paths[@]}" || {
    echo "safe-push: could not commit the stale files, nothing merged"
    finish 2 "adopt commit failed"
  }
  echo "safe-push: committed the stale files as they were: $(git rev-parse --short HEAD)"
}

merge_origin() {
  preflight
  if [ ${#blockers[@]} -gt 0 ]; then
    echo "safe-push: another session's uncommitted edits are in the way of GitHub's changes:"
    age_blockers
    if [ $live_count -eq 0 ] && [ $adopt -eq 1 ]; then
      adopt_stale
      preflight
      if [ ${#blockers[@]} -gt 0 ]; then
        echo "safe-push: STOPPED, files are still in the way after adopting:"
        printf '  %s\n' "${blockers[@]}"
        finish 2 "${#blockers[@]} file(s) still in the way after adopting"
      fi
    elif [ $live_count -eq 0 ]; then
      echo "safe-push: STOPPED before merging. Your commit is kept locally. Nothing on disk was changed."
      echo "safe-push: every file above is older than 2 hours, so no owner is live: commit these and re-run."
      echo "safe-push: run the same command again with --adopt-stale (it backs them up to tmp/ first)."
      finish 2 "${#blockers[@]} stale file(s), re-run with --adopt-stale"
    else
      echo "safe-push: STOPPED before merging. Your commit is kept locally. Nothing on disk was changed."
      echo "safe-push: $live_count file(s) changed inside the last 2 hours: owner is live, retry later."
      echo "safe-push: put one board entry up and run this again at the end of your task."
      finish 2 "$live_count live file(s) with another session's edits"
    fi
  fi
  local f
  for f in ${clear_tracked[@]+"${clear_tracked[@]}"}; do
    git checkout -q HEAD -- "$f"
    echo "safe-push: cleared '$f' (same bytes as GitHub, or site data where GitHub wins)"
  done
  for f in ${clear_untracked[@]+"${clear_untracked[@]}"}; do
    git rm -q --cached --ignore-unmatch -- "$f" 2>/dev/null
    rm -f -- "$f"
    echo "safe-push: cleared untracked '$f' (same bytes as GitHub, the merge brings it back)"
  done

  local ahead out
  ahead=$(git rev-list --count origin/main..HEAD)
  if [ "$ahead" -eq 0 ]; then
    out=$(git merge --ff-only -q origin/main 2>&1) && return 0
  else
    out=$(git merge --no-ff --no-edit -q origin/main 2>&1) && return 0
  fi

  if [ -e "$gitdir/MERGE_HEAD" ]; then
    local conflicted=() only_data=1
    while IFS= read -r -d '' f; do
      conflicted+=("$f")
      is_site_data "$f" || only_data=0
    done < <(git diff --name-only --diff-filter=U -z)
    if [ ${#conflicted[@]} -gt 0 ] && [ $only_data -eq 1 ]; then
      git checkout -q --theirs -- "${conflicted[@]}" && git add -- "${conflicted[@]}" && git commit -q --no-edit && {
        echo "safe-push: site data conflict resolved with GitHub's version: ${conflicted[*]}"
        return 0
      }
    fi
    git merge --abort
    echo "safe-push: MERGE CONFLICT, merge aborted. Your commit is kept locally, nothing is lost. Needs a hand merge:"
    printf '  %s\n' ${conflicted[@]+"${conflicted[@]}"}
    finish 3 "merge conflict in ${#conflicted[@]} file(s), needs a hand merge"
  fi
  echo "safe-push: git refused to start the merge:"
  echo "$out" | sed 's/^/  /'
  finish 2 "git refused the merge (see above)"
}

# --- steps 3 to 6: fetch, merge if behind, push, retry if GitHub moved -------------------
try=1
while [ $try -le $MAX_TRIES ]; do
  if ! git fetch -q origin; then
    echo "safe-push: git fetch failed (network or credentials)"
    finish 4 "fetch failed"
  fi
  if [ "$(git rev-list --count HEAD..origin/main)" -gt 0 ]; then
    merge_origin
  fi
  if [ "$(git rev-list --count origin/main..HEAD)" -eq 0 ]; then
    finish 0 "nothing"            # already on GitHub
  fi
  if pushout=$(git push origin main 2>&1); then
    git fetch -q origin
    finish 0 "nothing"
  fi
  # A "remote rejected" can be a false failure: check what GitHub actually has.
  git fetch -q origin
  if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]; then
    echo "safe-push: push reported an error but GitHub has the commit"
    finish 0 "nothing"
  fi
  echo "safe-push: push attempt $try of $MAX_TRIES did not land:"
  echo "$pushout" | sed 's/^/  /'
  try=$((try + 1))
done

finish 4 "push failed after $MAX_TRIES tries"
