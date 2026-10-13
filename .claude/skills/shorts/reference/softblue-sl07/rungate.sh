#!/bin/zsh
# run the delivery gate on one delivered short: rungate.sh S1
S=$1; SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/softblue-sl07"
N=$(cd "$SK" && python3 -c "import plans;print(plans.NAME['$S'])")
cd /Volumes/Extreme/_edit_work/sl07/build/$S/gate && nice python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/belly-fat-90-days-$N.mp4" --format short --plan plan.json > gate_run.log 2>&1; grep -E "^\s*(FAIL|\?\?\?\?|NEEDS|UNCONF|NOT MEAS)|DELIVERY GATE|passed|WAIT" gate_run.log | cut -c1-420 
