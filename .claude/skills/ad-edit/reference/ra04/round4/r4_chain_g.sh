#!/bin/bash
# RA-04 round 4 g: the 9:16 with the held crops (r4_track.py round 4 f: still at his median wherever he stays within 16 %), the flow_a
# and tour cards of chain f. Full stage 1 (the Dan segments change). Same mix.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r4g')"
echo "SLOT $(date +%T)"
set -x
python3 s10_render04r4.py 9x16 > logs/r4g_s10_9.log 2>&1 || exit 5
"$FF" -nostdin -y -v error -i picture_9x16.mp4 -i mix_r4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round4/master_9x16_r4g.mp4 || exit 7
echo "R4G_COMPLETE $(date +%T)"
