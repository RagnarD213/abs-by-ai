#!/bin/bash
# RO-17 round 2 review media, after hf/ is rendered. Run from anywhere; prints a marker per step.
set -e
W=/Volumes/Extreme/_edit_work/RO-17/round2; cd $W
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS done"
nice -n 5 python3 recipe/review_media.py first > logs/first.log 2>&1; tail -1 logs/first.log > review/first-minute/fidelity.json; echo "FIRST done"
F="review/first-minute/DRAFT - RO-17 round 2 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-17 round 2 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE done"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR done"
nice -n 5 python3 recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT done"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY done"
python3 recipe/page_extra.py && python3 recipe/page.py; echo "PAGE done"
echo "CHAIN COMPLETE"
