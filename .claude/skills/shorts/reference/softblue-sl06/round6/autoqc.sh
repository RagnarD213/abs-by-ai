#!/bin/bash
# run qc_take.py (v2: tremor bars) on every Veo take in veo/ (SL-06 R6); results appended to qc2/auto.log
cd /Volumes/Extreme/_edit_work/sl06/round6
while true; do
  for f in veo/[A-F]6*-flow-t*.mp4; do
    [ -e "$f" ] || continue; b=$(basename "$f" .mp4); [ -e "qc2/$b.qc.json" ] && continue
    sleep 3; nf=""; [[ "$b" == ?66* || "$b" == ?67* || "$b" == ?68* || "$b" == ?69* ]] && nf="--variant h"
    python3 qc_take.py ${b:0:1} "$f" $nf --out qc2 2>/dev/null | grep -E "PASS|FAIL" >> qc2/auto.log
  done
  [ -e qc2/STOP ] && exit 0; sleep 30
done
