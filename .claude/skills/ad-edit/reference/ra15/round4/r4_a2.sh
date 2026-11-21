#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra15
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-15 r4 a2')"
set -x
python3 s04c_body.py > logs/s04c_r4.log 2>&1 || exit 2
python3 s05_plan15.py > logs/s05_r4.log 2>&1 || exit 3
echo "R4_A_COMPLETE $(date +%T)"
