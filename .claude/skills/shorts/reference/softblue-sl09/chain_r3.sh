#!/bin/zsh
# R3: render, keep true peak, clear stale watch images, deliver copy + watch pass, per short
cd /Volumes/Extreme/_edit_work/sl09/round2
for S in "$@"; do
  ./render_all.sh $S
  grep -q "rendered" logs_render_$S.txt || { echo "$S RENDER FAILED"; continue; }
  python3 fix_tp.py $S
  rm -rf build/$S/gate/watch/strips build/$S/gate/watch/sheets
  python3 post.py $S
  echo "$S CHAIN DONE $(date +%H:%M:%S)"
done
echo CHAINALL
