#!/bin/zsh
# run the delivery gate on one delivered SL-06 short: rungate.sh D   (never from a shell line containing the gate's own name)
S=$1; cd /Volumes/Extreme/_edit_work/sl06
N=$(python3 -c "import plans;print(plans.NAME['$S'])")
cd build/$S/gate && nice python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/zepbound-tips-$N.mp4" --format short --plan plan.json > gate_run.log 2>&1; grep -E "^\s*(FAIL|\?\?\?\?|NEEDS|UNCONF|NOT MEAS)|DELIVERY GATE|passed|WAIT" gate_run.log | cut -c1-420
