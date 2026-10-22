#!/bin/zsh
# final R2 key: stage 1.5 on the R1 4K cache (with watch boxes), pale/navy/pink renders, both measures. Waits for a build slot.
set -e
cd /Volumes/Extreme/_edit_work/ds40/r2/key
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
python3 -c "import sys; sys.path.insert(0,'$SH'); import buildcap; buildcap.wait('ds40 r2 stage15')"
rm -rf ../cache_r2 && python3 stage15_temporal.py ../../r1/cache ../src_u8.npy ../cache_r2 ../watch.json | tail -1
python3 -c "import sys; sys.path.insert(0,'$SH'); import buildcap; buildcap.wait('ds40 r2 render')"
./render_pair.sh ../cache_r2 r2 | tail -1
python3 stage2_comp.py ../cache_r2 B_warmvivid "../renders/r2 pink.mp4" pink
python3 stage2_comp.py ../../r1/cache B_warmvivid "../renders/r1 pink.mp4" pink
cd ../measure && python3 mcflicker.py "../renders/r2 pale.mp4" mc_r2.json 2>/dev/null | tail -1
echo FINAL DONE
