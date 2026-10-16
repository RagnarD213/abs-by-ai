#!/bin/bash
# RA-06 round 4: the 16:9 picture from the same edit and mux with the approved mix (same frame count as the 9:16).
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
FF="$REPO/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0, '$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-06 R4 16x9')"
echo "SLOT $(date +%T)"
set -x
python3 s10_render06.py 16x9 > logs/s10_16_r4.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart /Volumes/Expansion/_edit_work/ra06_r4/master_16x9.mp4 || exit 7
echo "R4_CHAIN16_COMPLETE $(date +%T)"
