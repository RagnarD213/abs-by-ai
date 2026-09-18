#!/bin/bash
# ROUND 2, re-cut: s25_hard.py measured EIGHT visibly-jumping splices on the delivered picture and
# the plan had only covered three (the word pairs carried from round 1 no longer match this cut).
# The Dan segmentation is rebuilt from the measured list; the cards, the captions and the mix are
# unchanged (proved: identical card frame counts, identical total, identical CTA beats, and the mix
# is locked to a picture whose length has not changed), so only the CTA overlays and the two
# pictures are rebuilt.
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver"
python3 s11_cta.py 9x16
python3 s11_cta.py 16x9
python3 s10_render.py 9x16
python3 s10_render.py 16x9
for K in 9x16 16x9; do
  python3 s14_deliver.py mux $K | tail -2
  if [ "$K" = "9x16" ]; then python3 "$AG" master_$K.mp4 --ab AB_ref-vs-ours.mp4 || true
  else python3 "$AG" master_$K.mp4 || true; fi
  python3 s15_txmaster.py $K master_$K.mp4 | head -1
  python3 s09_align.py master_$K.mp4 speech_$K.json | tail -1
  python3 s13_watch.py neg $K master_$K.mp4 | tail -1
  python3 s12_gateplan.py $K master_$K.mp4
  python3 s34_strips.py $K master_$K.mp4
done
python3 s25_hard.py master_9x16.mp4 | tail -12
for K in 9x16 16x9; do
  rm -rf watchpass_$K
  python3 "$SH/watch.py" master_$K.mp4 --plan recipe-RA-01/gate_plan_$K.json --out watchpass_$K | tail -12
done
echo RECUT_DONE
