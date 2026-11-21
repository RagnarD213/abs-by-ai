#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra05
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 s06_inserts05.py pose > logs/s06_f.log 2>&1 || exit 3
SKIP1=1 python3 s10_render05.py 9x16 > logs/s10_f.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart draft_9x16.mp4 || exit 7
python3 page05.py --media || exit 10
echo CHAIN_F_COMPLETE
