#!/bin/zsh
# run the delivery gate on one delivered short: rungate.sh S1
S=$1; SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/softblue-sl03"
N=$(cd "$SK" && python3 -c "import plans;print(plans.NAME['$S'])")
cd /Volumes/Extreme/_edit_work/sl03/r2/$S/gate && nice python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/daily-salad-$N.mp4" --format short --plan plan.json 2>&1 | grep -E "^\s+(FAIL|\?\?\?\?|NEEDS)|DELIVERY GATE|passed" 
