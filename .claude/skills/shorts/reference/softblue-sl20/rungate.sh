#!/bin/zsh
# run the delivery gate on one delivered short: rungate.sh A
S=$1
N=$(cd /Volumes/Expansion/_edit_work/SL-20/recipe && python3 -c "import plans;print(plans.NAME['$S'])")
cd /Volumes/Expansion/_edit_work/SL-20/build/$S/gate && nice python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/$N.mp4" --format short --plan plan.json > gate_run.log 2>&1; grep -E "^\s*(FAIL|\?\?\?\?|NEEDS|UNCONF|NOT MEAS)|DELIVERY GATE|passed|WAIT" gate_run.log | cut -c1-420
