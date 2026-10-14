#!/bin/bash
# RA-15 round 2: rebuild the plates, the three AI clip cards and the shortened macro card, captions, the 9:16 picture, mux V2 (mix_bass.wav).
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r2 chain')"
echo "SLOT $(date +%T)"
set -x
[ -n "$SKIP_GFX" ] || { PLATES_ONLY=1 python3 gfx15.py > logs/gfx_r2.log 2>&1 || exit 2; }
python3 s06_inserts15.py ${INSERTS:-macro fridge restaurant cutout} > logs/s06_r2.log 2>&1 || exit 3
python3 s07_captions.py 9x16 > logs/s07_r2.log 2>&1 || exit 4
python3 s10_render05.py 9x16 > logs/s10_r2.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_bass.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart draft_9x16.mp4 || exit 7
echo "R2_CHAIN_COMPLETE $(date +%T)"
