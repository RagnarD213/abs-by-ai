#!/bin/bash
# RA-15 round 4 b: plates (16:9 manifest without the cutout), captions, both pictures, mux with the approved frame-locked V2 mix (same length, 1554 frames).
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r4 b')"
echo "SLOT $(date +%T)"
set -x
for t in 1 2 3; do python3 gfx16.py > logs/gfx16_r4.log 2>&1 && break; echo gfx16 retry $t; [ $t = 3 ] && exit 3; done
python3 s07_captions.py 9x16 > logs/s07_r4.log 2>&1 || exit 6
python3 s07_captions.py 16x9 > logs/s07_16_r4.log 2>&1 || exit 7
python3 s10_render05.py 9x16 > logs/s10_r4.log 2>&1 || exit 8
python3 s10_render05.py 16x9 > logs/s10_16_r4.log 2>&1 || exit 9
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_9x16_r4.mp4 || exit 11
"$FF" -nostdin -y -v error -i picture_16x9.mp4 -i mix_bass_r3c.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart master_16x9_r4.mp4 || exit 12
echo "R4_B_COMPLETE $(date +%T)"
