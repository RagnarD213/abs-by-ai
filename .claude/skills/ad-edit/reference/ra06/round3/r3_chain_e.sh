#!/bin/bash
# RA-06 round 3 fixes after the independent review: vacuum panel (split rebuilt by hand), "replaced them with AI" ride.
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
FF="$REPO/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0, '$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-06 R3 fixes')"
set -x
head -1 r1_audio.sh > /tmp/_ra06_mix_only.sh && bash /tmp/_ra06_mix_only.sh || exit 1
SKIP1=1 python3 s10_render06.py 9x16 > logs/s10_r3e.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart draft_9x16.mp4 || exit 7
bash r3_chain_d.sh > logs/chain_r3d2.log 2>&1 || exit 8
echo CHAIN_R3E_COMPLETE
