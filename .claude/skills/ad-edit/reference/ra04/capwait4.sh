#!/bin/bash
# Wait until fewer than two video builds are running, then run "$@".
# A build = one process GROUP containing ffmpeg/whisper/gate.py/render*.py/qc_style work.
# Counting process groups (not processes) is what separates "one build with three helpers"
# from "three builds".  Our own group is excluded.
MYPG=$(ps -o pgid= -p $$ | tr -d ' ')
builds() {
  ps -Ao pgid,command \
   | grep -E 'ffmpeg|whisper|render[^ ]*\.py|gate\.py|qc_style' \
   | grep -v -E 'grep -E|capwait|ugrep|/rg |ripgrep' \
   | awk -v me="$MYPG" '{gsub(/ /,"",$1); if ($1 != me) print $1}' \
   | sort -u | wc -l | tr -d ' '
}
t0=$(date +%s)
while :; do
  n=$(builds)
  [ "$n" -lt 2 ] && break
  el=$(( $(date +%s) - t0 ))
  [ $el -gt 7200 ] && { echo "capwait: timed out after ${el}s with $n builds"; exit 9; }
  sleep 4
done
echo "capwait: $(date +%T) free slot (other builds=$(builds)) -> $*"
exec "$@"
