#!/bin/zsh
# DS-36: gate plan + delivery gate only, keeping the judged qa/watch_pass.json (gates.sh would regenerate qa and drop the judging)
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-107
NAME="Metabolism Not The Reason SFC R1"
python3 recipe/gateplan.py > main/gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 main/gateplan.log; exit 1; }
cd $W/main; python3 "$R/.claude/skills/_shared/deliver/gate.py" "review/$NAME.mp4" --format short --plan gate-plan.json > deliver_gate.log 2>&1; echo "gate rc=$?"
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log | cut -c1-230
echo "GATE_ONLY DONE"
