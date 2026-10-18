#!/bin/zsh
# RO-17 round 5: full film render behind the two-build cap (A5 = the brief raisin pour), then the finish chain
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/RO-17/round3
python3 -c "import sys;sys.path.insert(0,'$P/.claude/skills/_shared');import buildcap;buildcap.wait('RO-17 r5 full render')"
RO17_BASE="$PWD/final/tmp_base.mp4" python3 -u recipe/build.py range 0 452.15 final/RO17_MASTER.mp4 && echo "RENDER COMPLETE" || { echo "RENDER FAILED ($?)"; exit 1; }
zsh recipe/finish_chain.sh && echo "CHAIN OK" || echo "CHAIN FAILED ($?)"
