#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r3 16x9 fix')"
echo "SLOT $(date +%T)"
set -x
python3 gfx16.py > logs/gfx16b.log 2>&1 || exit 2
python3 s07_captions.py 16x9 > logs/s07_16b.log 2>&1 || exit 4
SKIP1=1 python3 s10_render05.py 16x9 > logs/s10_16b.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_16x9_r3.mp4 || exit 7
echo "R3_FIX16_COMPLETE $(date +%T)"
