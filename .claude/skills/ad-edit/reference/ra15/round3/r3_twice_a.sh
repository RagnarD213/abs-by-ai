#!/bin/bash
# RA-15 round 3 c: after the "twice" fix in cut.json: cut audio, the approved V2 chain (same EQ), CTC word timing, head track, hold starts, plan.
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 twice a')"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > logs/s08_twice.log 2>&1 || exit 1
EQ=$(python3 -c "import json;print(json.load(open('mix_bass.wav.voice_chain.json'))['eq'])")
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_bass_r3c.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass_r3c --eq "$EQ" > logs/s08_twice_bass.log 2>&1 || exit 2
python3 s09_align.py mix_bass_r3c.wav words_aligned.json > logs/s09_twice.log 2>&1 || exit 3
python3 s04_track.py > logs/s04_twice.log 2>&1 || exit 4
python3 s04b_holdstart.py beats.json > logs/s04b_twice.log 2>&1 || exit 5
python3 s05_plan15.py > logs/s05_twice.log 2>&1 || exit 6
python3 s04b_holdstart.py beats.json > logs/s04b_twice2.log 2>&1 || exit 7
python3 s05_plan15.py > logs/s05_twice2.log 2>&1 || exit 8
echo "TWICE_A_COMPLETE $(date +%T)"
