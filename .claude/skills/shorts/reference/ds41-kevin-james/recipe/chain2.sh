#!/bin/zsh
# DS-36 R1 build 2 (after the scripted independent review and the off-cuff gate): prep -> shot times -> graphics -> framing -> build.
set -e -o pipefail
V=$1; W=/Volumes/Expansion/_edit_work/DS-41/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-41
python3 recipe/prep.py $V | tail -1
SHOTS_ONLY=1 python3 recipe/framing.py $V | tail -1
python3 recipe/graphics.py $V > $V/graphics.log 2>&1 || { echo GRAPHICS FAIL; tail -3 $V/graphics.log; exit 1; }; tail -1 $V/graphics.log | cut -c1-200
python3 recipe/framing.py $V > $V/framing.log 2>&1 || { echo FRAMING FAIL; tail -5 $V/framing.log; exit 1; }; grep -E "'id': 'S[0-9]+'|'id': 'P[WR]'" $V/framing.log | cut -c1-150
python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-41 -- zsh recipe/build.sh $V
