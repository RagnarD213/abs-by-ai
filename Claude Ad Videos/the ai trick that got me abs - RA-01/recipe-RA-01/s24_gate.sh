#!/bin/bash
# The delivery gate, on the file that actually goes out.
set -e
cd /Volumes/Extreme/_edit_work/ra01
K=$1; FMT=$2
python3 s12_gateplan.py $K master_$K.mp4
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" \
  master_$K.mp4 --format $FMT --plan recipe-RA-01/gate_plan_$K.json 2>&1 | tee logs/delivergate_$K.log || true
echo "GATE_$K DONE"
