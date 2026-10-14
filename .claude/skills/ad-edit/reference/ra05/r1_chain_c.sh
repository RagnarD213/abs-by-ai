#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra05
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 gfx05.py > logs/gfx_c.log 2>&1 || exit 2
grep -E "^(flow|tour|LT|CTA)" logs/gfx_c.log
python3 s06_inserts05.py > logs/s06_c.log 2>&1 || exit 3
python3 s07_captions.py 9x16 > logs/s07_c.log 2>&1 || exit 4
python3 s10_render05.py 9x16 > logs/s10_c.log 2>&1 || exit 5
env BED=music/Realizer.mp3 BED_DB=-32 LOCK=picture_9x16.mp4 python3 s08_audio.py > logs/s08_c2.log 2>&1 || exit 6
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
echo CHAIN_C_COMPLETE
