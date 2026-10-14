#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > logs/s08_a.log 2>&1 || exit 1
EQ=$(python3 -c "import json;print(json.load(open('mix.wav.voice_chain.json'))['eq'])")
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_bass.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass --eq "$EQ,equalizer=f=120:t=q:w=0.8:g=+3.0" > logs/s08_bass.log 2>&1 || exit 4
python3 s09_align.py > logs/s09_a.log 2>&1 || exit 2
python3 s04_track.py > logs/s04_a.log 2>&1 || exit 3
echo CHAIN_A_COMPLETE
