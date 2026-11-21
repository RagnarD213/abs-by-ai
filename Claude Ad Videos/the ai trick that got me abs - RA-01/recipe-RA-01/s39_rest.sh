#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"
python3 s34_strips.py 9x16 master_9x16.mp4
K=16x9
python3 s14_deliver.py mux $K | tail -2
python3 "$AG" master_$K.mp4 || true
python3 s15_txmaster.py $K master_$K.mp4 | head -1
python3 s09_align.py master_$K.mp4 speech_$K.json | tail -1
python3 s13_watch.py neg $K master_$K.mp4 | tail -1
python3 s12_gateplan.py $K master_$K.mp4
python3 s34_strips.py $K master_$K.mp4
python3 s25_hard.py master_9x16.mp4 | tail -14
for K in 9x16 16x9; do
  rm -rf watchpass_$K
  python3 "$SH/watch.py" master_$K.mp4 --plan recipe-RA-01/gate_plan_$K.json  --out watchpass_$K --log watchpass_$K/watch_pass.json | tail -14
done
echo REST_DONE
