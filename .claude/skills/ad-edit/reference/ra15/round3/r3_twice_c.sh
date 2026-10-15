#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SH_A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 twice c')"
set -x
BAD=$(cat round3/bad9.txt); [ -n "$BAD" ] && { python3 s06_inserts15.py $BAD > logs/s06_twice_c.log 2>&1 || exit 4; }
SKIP1=1 python3 s10_render05.py 9x16 > logs/s10_twice_c.log 2>&1 || exit 8
python3 s10_render05.py 16x9 > logs/s10_16_twice.log 2>&1 || exit 9
EQ=$(python3 -c "import json;print(json.load(open('mix_bass.wav.voice_chain.json'))['eq'])")
python3 "$SH_A/voice_chain.py" --in cut_audio.wav --out mix_bass_r3c.wav --bed music/Realizer.mp3 --bed-db -32 --work audiowork_bass_r3c --eq "$EQ" --frame-lock picture_9x16.mp4 > logs/s08_twice_lock.log 2>&1 || exit 10
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_9x16_r3.mp4 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_16x9_r3.mp4 || exit 12
echo "TWICE_C_COMPLETE $(date +%T)"
