#!/bin/zsh
# DS-36: gate plan + delivery gate only, keeping the judged qa/watch_pass.json (gates.sh would regenerate qa and drop the judging)
V=$1; W=/Volumes/Expansion/_edit_work/DS-41/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-41
NAME="Kevin James Cheat SFC R1 - $([ $V = scripted ] && echo scripted || echo off the cuff)"
python3 recipe/gateplan.py $V > $V/gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 $V/gateplan.log; exit 1; }
cd $W/$V; python3 "$R/.claude/skills/_shared/deliver/gate.py" "review/$NAME.mp4" --format short --plan gate-plan.json > deliver_gate.log 2>&1; echo "gate rc=$?"
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log | cut -c1-230
echo "GATE_ONLY $V DONE"
