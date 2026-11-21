#!/bin/bash
# RA-04 round 4: the 16:9 after r4_chain.sh (graphics done): cards, captions, picture, mux with mix_r4.wav.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4 16x9')"
echo "SLOT $(date +%T)"
set -x
python3 s06_inserts16_04.py > logs/r4_s06_16.log 2>&1 || exit 9
python3 s07_captions.py 16x9 > logs/r4_s07_16.log 2>&1 || exit 10
python3 s10_render04r4.py 16x9 > logs/r4_s10_16.log 2>&1 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_16x9_r4.mp4 || exit 12
echo "R4_CHAIN16_COMPLETE $(date +%T)"
