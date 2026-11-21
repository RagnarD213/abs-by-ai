#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra07
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
export WORK=round6/work_ph
python3 -c "
import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import buildcap; buildcap.wait('ra07 r6 placeholder film')"
python3 s86r6_assemble.py work
"$FF" -v error -i round6/work_ph/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round6/r6ph.md5
cmp -s round6/r6ph.md5 round3/r2.md5 && echo "FIRST30 IDENTICAL" || echo "FIRST30 DIFFERS"
python3 s86r6_assemble.py cuts
"$FF" -nostdin -y -v error -i round6/work_ph/picture_9x16.mp4 -i round3/mix_bass_r3.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart "round6/Fire Your Trainer AD R6 - whole 9x16 (home curls placeholder).mp4"
echo CHAIN_PH_DONE
