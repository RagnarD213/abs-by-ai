#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra07
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "
import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import buildcap; buildcap.wait('ra07 r4 assemble')"
python3 s86r4_assemble.py work
echo WORK_DONE
"$FF" -v error -i round4/work/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round4/r4.md5
cmp -s round4/r4.md5 round3/r2.md5 && echo "FIRST30 IDENTICAL" || echo "FIRST30 DIFFERS"
python3 s86r4_assemble.py cuts
echo CUTS_DONE
