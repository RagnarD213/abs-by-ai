#!/bin/bash
# RA-06 round 4: re-composite the approved 9:16 with two labels moved for the caption-clearance gate (I4 chip, Stomach Vacuum label).
# Stage 1 (Dan's segments) is not re-run: SKIP1=1 reuses seg_9x16 exactly.
cd /Volumes/Extreme/_edit_work/ra06
REPO="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$REPO/Media/video_edit/bin:$PATH"
FF="$REPO/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0, '$REPO/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-06 R4 9x16 labels')"
set -x
SKIP1=1 python3 s10_render06.py 9x16 > logs/s10_9_r4.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af apad -t 45.712333 -c:a aac -b:a 256k -movflags +faststart /Volumes/Expansion/_edit_work/ra06_r4/master_9x16.mp4 || exit 7
echo "R4_CHAIN9_COMPLETE $(date +%T)"
