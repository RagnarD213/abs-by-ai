#!/bin/bash
# RA-04 round 4 c: after both watch-pass judges. flow_b crop below the app header (both plates), tour from 6.25 s (past the app's page
# slide), captions as an exact image sequence (the concat list was one frame late), dan03/dan09 FAR with a calmer follow. Same mix.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4c')"
echo "SLOT $(date +%T)"
set -x
python3 round4/r4_plate9.py > logs/r4c_plate9.log 2>&1 || exit 2
PLATES_ONLY=1 python3 gfx16_04.py > logs/r4c_gfx16.log 2>&1 || exit 2
python3 s06_inserts04.py flow_b tour > logs/r4c_s06_9.log 2>&1 || exit 3
python3 s07_captions.py 9x16 > logs/r4c_s07_9.log 2>&1 || exit 4
python3 s10_render04r4.py 9x16 > logs/r4c_s10_9.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_9x16_r4c.mp4 || exit 7
echo "R4C_9x16_DONE $(date +%T)"
python3 s06_inserts16_04.py flow_b tour > logs/r4c_s06_16.log 2>&1 || exit 9
python3 s07_captions.py 16x9 > logs/r4c_s07_16.log 2>&1 || exit 10
python3 s10_render04r4.py 16x9 > logs/r4c_s10_16.log 2>&1 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_16x9_r4c.mp4 || exit 12
echo "R4C_CHAIN_COMPLETE $(date +%T)"
