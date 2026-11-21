#!/bin/bash
# RA-15 round 3: the 16:9 master from the same edit. Cards (s06_inserts16.py), captions (16:9 lifts over the lower thirds), picture,
# mux with the same frame-locked V2 mix as the 9:16 (same frame count, checked).
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r3 16x9')"
echo "SLOT $(date +%T)"
set -x
python3 s06_inserts16.py > logs/s06_16.log 2>&1 || exit 3
python3 s07_captions.py 16x9 > logs/s07_16.log 2>&1 || exit 4
python3 s10_render05.py 16x9 > logs/s10_16.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_16x9_r3.mp4 || exit 7
echo "R3_CHAIN16_COMPLETE $(date +%T)"
