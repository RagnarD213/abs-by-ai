#!/bin/bash
# DS-107 R1 build 2: K1 as a transparent overlay, W = 1040, Balanced voice tone-fitted, captions aligned to the delivered ASR
set -Eeo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH" GATE_GROUP=DS-107
S=$(date +%s); python3 recipe/graphics.py > main/graphics.log 2>&1; echo "$(date +%T) $(( $(date +%s)-S ))s graphics (K1 overlay)" >> logs/build-times.txt; tail -1 main/graphics.log | cut -c1-120
VOICE=balanced LOOK=r5warm bash recipe/build.sh
