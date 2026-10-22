#!/bin/bash
# RA-09 chain A: cut audio at 1.06x (Rubber Band), the chain's fitted voice on THIS cut, CTC alignment, head track.
cd /Volumes/Expansion/_edit_work/RA-09
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
echo "START $(date +%T)"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 STRETCH=rb OUTW=mix_fit.wav WORK=audiowork_fit python3 s08_audio.py > logs/s08.log 2>&1 || { echo FAIL_s08; exit 1; }
python3 s09_align.py mix_fit.wav words_aligned.json > logs/s09.log 2>&1 || { echo FAIL_s09; exit 3; }
python3 s04_track.py > logs/s04.log 2>&1 || { echo FAIL_s04; exit 4; }
echo "CHAIN_A_PART1 $(date +%T)"
EQ=$(python3 -c "import json;print(json.load(open('mix_fit.wav.voice_chain.json'))['eq'])"); echo "$EQ" > eq_fit_r1.txt
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_b15.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_b15 --eq "$EQ,equalizer=f=120:t=q:w=0.8:g=+1.5" > logs/mix_b15.log 2>&1 || { echo FAIL_b15; exit 5; }
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_b30.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_b30 --eq "$EQ,equalizer=f=120:t=q:w=0.8:g=+3.0" > logs/mix_b30.log 2>&1 || { echo FAIL_b30; exit 6; }
echo "OPTIONS_COMPLETE $(date +%T)"
