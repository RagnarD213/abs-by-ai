#!/bin/zsh
# deliver.py copy + watch pass for one short (SL-06 round 2)
cd /Volumes/Extreme/_edit_work/sl06; S=$1
N=$(python3 -c "import plans;print(plans.NAME['$S'])")
V="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/zepbound-tips-$N.mp4"
rm -rf build/$S/gate/watch build/$S/gate/logs/findings.json
nice -n 5 python3 deliver.py copy $S 2>&1 | grep -v Warn | tail -4
nice -n 5 python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" "$V" --plan build/$S/gate/plan.json --out build/$S/gate/watch --log build/$S/gate/logs/watch_pass.json 2>&1 | grep -E "scan:|frozen|naked|graphics|boundaries"
