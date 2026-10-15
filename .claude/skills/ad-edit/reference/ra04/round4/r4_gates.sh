#!/bin/bash
# RA-04 round 4: measurements, label chips, gate plans and watch passes on the delivered files.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/top 3 tips for getting abs - RA-04"
for a in 9x16 16x9; do ./round4/r4_measure.sh $a "$D/top 3 tips for getting abs | claude | $a | RA-04.mp4" > logs/r4c_measure_$a.log 2>&1 || { echo "MEASURE FAIL $a"; exit 1; }; done
python3 round4/s_chips04.py > logs/r4c_chips.log 2>&1 || { echo CHIPS FAIL; exit 2; }
for a in 9x16 16x9; do
  rm -rf round4/watch_$a
  python3 round4/s_gateplan04.py $a "$D/top 3 tips for getting abs | claude | $a | RA-04.mp4" || { echo "PLAN FAIL $a"; exit 3; }
  python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 watch')"
  python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" "$D/top 3 tips for getting abs | claude | $a | RA-04.mp4" --plan round4/plan_$a.json --out round4/watch_$a --log round4/watch_$a/logs/watch_pass.json > logs/r4c_watch_$a.log 2>&1 || { echo "WATCH FAIL $a"; exit 4; }
  sed -n 2,6p logs/r4c_watch_$a.log
done
grep -h "candidates" logs/junk_9x16.log logs/junk_16x9.log
echo GATES_PREP_COMPLETE
