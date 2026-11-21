#!/bin/bash
# RA-06 round 4: LT2 as a narrow bottom-left strip in 16:9 (watch judge: the full-width strip covered his abs), captions, re-composite.
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
FF="$REPO/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0, '$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-06 R4 16x9 LT2')"
set -x
python3 gfx16.py > logs/gfx16_r4b.log 2>&1 || exit 2
python3 s07_captions16.py 16x9 > logs/s07_16_r4b.log 2>&1 || exit 4
SKIP1=1 python3 s10_render06.py 16x9 > logs/s10_16_r4c.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart /Volumes/Expansion/_edit_work/ra06_r4/master_16x9.mp4 || exit 7
echo "R4_CHAIN16B_COMPLETE $(date +%T)"
