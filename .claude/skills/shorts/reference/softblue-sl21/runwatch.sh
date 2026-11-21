#!/bin/zsh
# watch pass on one delivered short, inside the build cap: runwatch.sh C
S=$1; R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
N=$(cd /Users/danielrose/Projects/_edit_work/SL-21/recipe && python3 -c "import plans;print(plans.NAME['$S'])")
G=/Users/danielrose/Projects/_edit_work/SL-21/build/$S/gate
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared');import buildcap;buildcap.wait('SL-21 watch $S')"
rm -rf $G/watch
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$R/Short-form video content/$N.mp4" --plan $G/plan.json --out $G/watch --log $G/logs/watch_pass.json > $G/watch_run.log 2>&1
echo "WATCH_EXIT $?" >> $G/watch_run.log
