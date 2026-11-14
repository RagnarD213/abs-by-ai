#!/bin/bash
# DS-107 R1 key measurements (chroma-key README bar): 9.35 s of stretch Ka in the R2 measuring geometry over pale/navy/pink,
# then mcflicker (edge flicker vs the camera's own picture, motion removed) and measure_r2 (rim, see-through, islands).
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH" GATE_GROUP=DS-107
T0=110.36; S=$(date +%s)
python3 recipe/measure_render.py $T0 main/measure | tail -1
python3 recipe/ds44_mcflicker.py main/measure/pale.mp4 main/measure/mc.json $T0 | tail -3
python3 recipe/ds44_measure_r2.py main/measure/pale.mp4 main/measure/navy.mp4 main/measure/m.json $T0 | tail -3
echo "MEASURE WALL $(( $(date +%s)-S ))s"
echo CHAIN_DONE
