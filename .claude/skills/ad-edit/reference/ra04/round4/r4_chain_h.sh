#!/bin/bash
# RA-04 round 4 h: held crops centred on the middle of his range (dan10 opened with his arm cut). Same cards and mix.
# and tour cards of chain f. Full stage 1 (the Dan segments change). Same mix.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4h')"
echo "SLOT $(date +%T)"
set -x
SEG_DIR=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/5abf4002-2528-40e8-a8c6-00d823854f7b/scratchpad/seg_9x16 python3 s10_render04r4.py 9x16 > logs/r4h_s10_9.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_9x16_r4h.mp4 || exit 7
echo "R4H_COMPLETE $(date +%T)"
