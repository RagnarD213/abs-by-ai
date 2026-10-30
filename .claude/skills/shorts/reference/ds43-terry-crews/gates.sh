#!/bin/zsh
# DS-43 R1: rerun the gate tail of build.sh (gate plan, watch pass, delivery gate) on the existing master:  zsh recipe/gates.sh scripted|offcuff
V=$1; W=/Volumes/Expansion/_edit_work/DS-43/r1; cd $W
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-43
NAME="Terry Crews Fasting SFC R1 - $([ $V = scripted ] && echo scripted || echo off the cuff)"
python3 recipe/gateplan.py $V > $V/gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 $V/gateplan.log; exit 1; }; tail -1 $V/gateplan.log | cut -c1-160
cd $W/$V; M="review/$NAME.mp4"; rm -rf qa; mkdir -p qa
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$M" --plan gate-plan.json --out qa --log qa/watch_pass.json --clips > qa/watch.log 2>&1; echo "watch rc=$?"; tail -4 qa/watch.log | cut -c1-200
python3 "$R/.claude/skills/_shared/deliver/gate.py" "$M" --format short --plan gate-plan.json > deliver_gate.log 2>&1; echo "gate rc=$?"
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log | cut -c1-230
echo "GATES $V DONE"
