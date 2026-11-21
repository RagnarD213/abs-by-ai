#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra06
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
set -x
python3 s09_align.py > logs/s09_g.log 2>&1 || exit 2
python3 s07_captions.py 9x16 > logs/s07_g.log 2>&1 || exit 4
SKIP1=1 python3 s10_render06.py 9x16 > logs/s10_g.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
bash r1_chain_d.sh > logs/chain_d_g.log 2>&1 || exit 8
echo CHAIN_G_COMPLETE
