#!/bin/zsh
# RO-17 round 4: full film render behind the two-build cap, then the finish chain
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
cd /Volumes/Extreme/_edit_work/RO-17/round3
python3 -c "import sys;sys.path.insert(0,'$P/.claude/skills/_shared');import buildcap;buildcap.wait('RO-17 r4 full render')"
python3 recipe/build.py range 0 452.15 final/RO17_MASTER.mp4 && echo "RENDER COMPLETE" || { echo "RENDER FAILED ($?)"; exit 1; }
