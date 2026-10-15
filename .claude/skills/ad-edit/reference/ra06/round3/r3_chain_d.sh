#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
SH="$REPO/.claude/skills/_shared"

set -x
python3 "$SH/audio/audio_gate.py" draft_9x16.mp4 --ab "round3/audio A-B - RA-06 round 3.mp4" --untreated mix.wav.audio_untreated.json > logs/agate_r3.log 2>&1; echo "audio gate exit $?"
python3 "$SH/cut/junk.py" draft_9x16.mp4 --out logs/junk_r3.json > logs/junk_r3.log 2>&1; echo "junk exit $?"
cp hard_splices.json round1/recipe_r1/hard_splices_r1.json
python3 s25_hard.py draft_9x16.mp4 > logs/hard_r3.log 2>&1; echo "hard exit $?"
echo CHAIN_R3D_COMPLETE
