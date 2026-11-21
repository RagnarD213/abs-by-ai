#!/bin/bash
# RA-15 round 3 e: levels re-assigned (wide for the big-gesture holds), flow card crop per segment, both masters.
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 fix e')"
echo "SLOT $(date +%T)"
set -x
python3 s06_inserts15.py flow > logs/s06_e.log 2>&1 || exit 3
python3 s06_inserts16.py flow > logs/s06_16_e.log 2>&1 || exit 4
python3 s10_render05.py 9x16 > logs/s10_e.log 2>&1 || exit 7
python3 s10_render05.py 16x9 > logs/s10_16_e.log 2>&1 || exit 8
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_9x16_r3.mp4 || exit 9
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_16x9_r3.mp4 || exit 10
echo "FIX_E_COMPLETE $(date +%T)"
