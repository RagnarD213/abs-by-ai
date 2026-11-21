#!/bin/bash
# scan.py every relaxed-pose take as it lands (SL-06 R6 final batch); one line per take in scan/auto.log
cd /Volumes/Extreme/_edit_work/sl06/round6
while true; do
  for f in veo/[A-F]7[0-2]q-flow-t*.mp4; do
    [ -e "$f" ] || continue; b=$(basename "$f" .mp4); [ -e "scan/$b.json" ] && continue
    sleep 3; python3 scan.py ${b:0:1} "$f" --json scan/$b.json 2>/dev/null | grep "windows pass" >> scan/auto.log
  done
  [ -e scan/STOP ] && exit 0; sleep 30
done
