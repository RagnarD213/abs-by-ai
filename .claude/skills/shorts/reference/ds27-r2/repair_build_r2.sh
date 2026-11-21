#!/bin/zsh
set -e
export GATE_GROUP=DS-27
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-27/round2
python3 "$W/recipe/render.py" 'Home Workouts SFC R2'
python3 "$W/recipe/qa_full.py" prep asr audio watch > "$W/evidence/full-qa.log" 2>&1

python3 "$W/recipe/self_check.py" > "$W/evidence/self-check.log" 2>&1
echo "Independent review checkpoint: import real watch findings and scan evidence, then run qa_full.py gate. Never deliver from this build step alone."
