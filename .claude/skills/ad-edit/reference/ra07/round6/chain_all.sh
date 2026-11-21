#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra07
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
python3 -c "
import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import buildcap; buildcap.wait('ra07 r6 assemble')"
python3 s86r6_assemble.py work
echo WORK_DONE
"$FF" -v error -i round6/work/picture_9x16.mp4 -frames:v 903 -f framemd5 - | grep -v "^#" | awk -F, '{print $6}' > round6/r6.md5
cmp -s round6/r6.md5 round3/r2.md5 && echo "FIRST30 IDENTICAL" || echo "FIRST30 DIFFERS"
python3 s86r6_assemble.py cuts
echo CUTS_DONE
