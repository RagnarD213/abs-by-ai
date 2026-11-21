#!/bin/bash
# RA-04 round 5: re-composite both films after a card change (Dan segments and mix unchanged), remux with mix_r5.wav.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r5 recomp')"
for a in 9x16 16x9; do
  SEG_DIR=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_$a SKIP1=1 python3 s10_render04r4.py $a > logs/r5_recomp_$a.log 2>&1 || { echo "RECOMP FAIL $a"; exit 5; }
  "$FF" -nostdin -y -v error -i picture_$a.mp4 -i mix_r5.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart round5/master_${a}_r5.mp4 || exit 7
done
echo "R5_RECOMP_COMPLETE $(date +%T)"
