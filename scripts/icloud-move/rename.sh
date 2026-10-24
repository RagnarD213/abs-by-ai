#!/bin/zsh
# Waits for a quiet moment (render queue empty, no Codex image/exec job, nothing cloud-only), then moves
# ~/Library/Mobile Documents/.../Documents/NAME out of iCloud Drive to ~/Projects/NAME with evacuate.py
# (piece by piece, a symlink left at every old path), and points ~/Documents/NAME straight at ~/Projects/NAME.
# rename.sh [NAME]   NAME defaults to Claude (moved 2026-10-23); Codex was moved with "rename.sh Codex".
set -u
HERE=${0:A:h}
NAME=${1:-Claude}
OLD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/$NAME"
NEW="$HOME/Projects/$NAME"
LOG="$HOME/Projects/.icloud-move.log"
RQ="$HOME/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py"
mkdir -p "$HOME/Projects"
say(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

[ -d "$OLD" ] && [ ! -L "$OLD" ] || { say "ABORT old path is not a real folder"; exit 1; }

quiet(){
  # Renders only touch the Claude folder; other folders need only the Codex check below.
  [ "$NAME" = Claude ] && { st=$(python3 "$RQ" status 2>&1) || return 1; } || st=""
  echo "$st" | grep -qE "running [0-9]|waiting, in order" && return 1
  pgrep -f "codex exec|codex-image.sh" >/dev/null && return 1
  return 0
}
dataless(){ find "$OLD" -flags +dataless 2>/dev/null; }

say "watcher started"
last=0; n=1
while true; do
  now=$(date +%s)
  if [ $((now - last)) -ge 600 ]; then
    d=$(dataless); n=$(print -r -- "$d" | grep -c .); last=$now
    say "$NAME cloud-only items: $n"
    # bird stalls for hours on big batches; restarting it (it relaunches) cleared the stall in October 2026
    [ "$n" -gt 0 ] && [ "$n" -eq "${prev:-0}" ] && killall bird 2>/dev/null
    prev=$n
    [ "$n" -gt 0 ] && print -r -- "$d" | tr '\n' '\0' | xargs -0 -n 50 brctl download 2>/dev/null
  fi
  if [ "$n" -eq 0 ] && quiet; then
    d=$(dataless); n=$(print -r -- "$d" | grep -c .)
    [ "$n" -gt 0 ] && { say "new cloud-only items at quiet moment: $n"; continue; }
    quiet || continue
    say "quiet moment: moving"
    python3 "$HERE/evacuate.py" "$OLD" "$NEW" --log "$LOG" > /dev/null 2>&1
    rc=$?
    if [ -L "$OLD" ]; then
      ln -s "$NEW" "$HOME/Documents/.$NAME.new" && mv -fh "$HOME/Documents/.$NAME.new" "$HOME/Documents/$NAME"
      say "DONE rc=$rc; ~/Documents/$NAME -> $(readlink "$HOME/Documents/$NAME")"
      exit 0
    fi
    say "INCOMPLETE rc=$rc; the parts already moved work through symlinks; rerun to finish"
    exit 1
  fi
  sleep 10
done
