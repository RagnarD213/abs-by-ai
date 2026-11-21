#!/bin/bash
# ROUND 2: every measurement that runs on the DELIVERED files, in order.
# (The watch pass's judging is done by hand between this script and s24_gate.sh.)
set -e
cd /Volumes/Extreme/_edit_work/ra01
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"
for K in 9x16 16x9; do
  python3 s12_gateplan.py $K master_$K.mp4
done
python3 s25_hard.py master_9x16.mp4
python3 s34_strips.py 9x16 master_9x16.mp4
python3 s34_strips.py 16x9 master_16x9.mp4
for K in 9x16 16x9; do
  rm -rf watchpass_$K
  python3 "$SH/watch.py" master_$K.mp4 --plan recipe-RA-01/gate_plan_$K.json --out watchpass_$K
done
echo EVIDENCE_DONE
