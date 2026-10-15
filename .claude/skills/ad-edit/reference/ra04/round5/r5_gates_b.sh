#!/bin/bash
# RA-04 round 5 gates, part B: gate plans and watch passes on the delivered files (after s20_neg.py recorded the look).
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/top 3 tips for getting abs - RA-04"
export WATCH_ROOT=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/ra04_watch SEG_DIR_9x16=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_9x16 SEG_DIR_16x9=/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/832e82d6-028b-4170-a2a1-5bd6ac575611/scratchpad/seg_16x9
for a in 9x16 16x9; do
  M="$D/top 3 tips for getting abs | claude | $a | RA-04.mp4"
  rm -rf $WATCH_ROOT/watch_$a
  python3 round5/s_gateplan04.py $a "$M" || { echo "PLAN FAIL $a"; exit 3; }
  python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 watch')"
  python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" "$M" --plan round5/plan_$a.json --out $WATCH_ROOT/watch_$a --log $WATCH_ROOT/watch_$a/logs/watch_pass.json > logs/r5_watch_$a.log 2>&1 || { echo "WATCH FAIL $a"; tail -5 logs/r5_watch_$a.log; exit 4; }
  sed -n 2,6p logs/r5_watch_$a.log
done
echo GATES_B_COMPLETE
