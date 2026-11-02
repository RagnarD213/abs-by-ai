#!/bin/zsh
set -e
export GATE_GROUP=DS-27
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Expansion/_edit_work/DS-27/round2
python3 .claude/skills/_shared/audio/voice_chain.py --in "$W/untreated-cut.wav" --out "$W/voice.wav" --eq 'highpass=f=70,equalizer=f=120:t=q:w=0.8:g=1.5' --no-expander-because 'Expanded C1719 auditions clipped word endings; preserve approved Gentle Bass tone and full word tails.' --oversample 4 --work "$W/voice-work" > "$W/evidence/voice-chain.log" 2>&1
python3 "$W/recipe/render.py" 'Home Workouts SFC R2'

python3 "$W/recipe/qa_full.py" prep asr audio watch gate > "$W/evidence/full-qa.log" 2>&1
