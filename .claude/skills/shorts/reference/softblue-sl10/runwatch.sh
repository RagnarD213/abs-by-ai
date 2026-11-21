#!/bin/zsh
# watch pass on one delivered short, inside the build cap: runwatch.sh C
S=$1; R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"
N=$(cd /Volumes/Expansion/_edit_work/SL-10 && python3 -c "import plans;print(plans.NAME['$S'])")
G=/Volumes/Expansion/_edit_work/SL-10/build/$S/gate
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$R/Short-form video content/alcohol-$N.mp4" --plan $G/plan.json --out $G/watch --log $G/logs/watch_pass.json > $G/watch_run.log 2>&1
echo "WATCH_EXIT $?" >> $G/watch_run.log
