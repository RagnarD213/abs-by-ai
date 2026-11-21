#!/bin/bash
cd /Volumes/Expansion/_edit_work/RO-29/round1
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS exit $?"
python3 -u recipe/review_media.py context_one P01 P02 > logs/context_one.log 2>&1; echo "CTX1 exit $?"
python3 recipe/review_media.py verify > logs/verify.log 2>&1; echo "VERIFY exit $?"
python3 -u recipe/review_media.py first > logs/first.log 2>&1; echo "FIRST exit $? $(grep 'first minute to' logs/first.log)"
grep -E '^\{' logs/first.log | tail -1 > review/first-minute/fidelity.json
SH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared"
F="review/first-minute/DRAFT - RO-29 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-29 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
python3 recipe/hair_first540.py > logs/hair_first540.log 2>&1 || true; echo "HAIR 540: $(tail -1 logs/hair_first540.log)"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
