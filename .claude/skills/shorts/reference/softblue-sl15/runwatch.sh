#!/bin/zsh
# watch pass on one delivered short, inside the build cap: runwatch.sh C
S=$1; R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
N=$(cd /Volumes/Extreme/_edit_work/SL-15 && python3 -c "import plans;print(plans.NAME['$S'])")
G=/Volumes/Extreme/_edit_work/SL-15/build/$S/gate
if [ -f /Volumes/Extreme/_edit_work/SL-15/build/$S/delivered.sha ] && grep -q "$(cat /Volumes/Extreme/_edit_work/SL-15/build/$S/delivered.sha)" $G/logs/watch_pass.json 2>/dev/null; then echo "watch pass already run on this file"; exit 0; fi
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared');import buildcap;buildcap.wait('SL-15 watch $S')"
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$R/Short-form video content/spraytan-$N.mp4" --plan $G/plan.json --out $G/watch --log $G/logs/watch_pass.json > $G/watch_run.log 2>&1
echo "WATCH_EXIT $?" >> $G/watch_run.log
