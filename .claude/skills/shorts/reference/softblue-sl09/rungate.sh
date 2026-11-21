#!/bin/zsh
# run the delivery gate on one delivered short: rungate.sh A   (never from a shell line that itself says gate.py: the gate would wait on its own launcher)
S=$1; W9=/Volumes/Extreme/_edit_work/sl09/round2
N=$(cd $W9 && python3 -c "import plans;print(plans.NAME['$S'])")
cd $W9/build/$S/gate && nice python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/$N.mp4" --format short --plan plan.json > gate_run.log 2>&1; grep -E "^\s*(FAIL|\?\?\?\?|NEEDS|UNCONF|NOT MEAS)|DELIVERY GATE|passed|WAIT" gate_run.log | cut -c1-420
