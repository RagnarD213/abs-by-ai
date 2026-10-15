#!/bin/bash
# RA-06 round 3: rebuild the full 9:16 from the round 3 plan (waits for a build slot first, cap 2).
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
FF="$REPO/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0, '$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-06 R3 chain c')" || exit 9
set -x
python3 s05_plan06.py > logs/s05_r3.log 2>&1 || exit 1
python3 gfx06.py > logs/gfx_r3.log 2>&1 || exit 2
python3 s06_split.py > logs/split_r3.log 2>&1 || exit 3
python3 s06_inserts06.py > logs/s06_r3.log 2>&1 || exit 3
python3 s07_captions.py 9x16 > logs/s07_r3.log 2>&1 || exit 4
python3 s10_render06.py 9x16 > logs/s10_r3.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
echo CHAIN_R3C_COMPLETE
