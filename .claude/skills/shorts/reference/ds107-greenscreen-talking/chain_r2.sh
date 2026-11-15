#!/bin/bash
# DS-107 R2: Dan's R1 picks locked (Balanced voice, colour A); the opener B0 plays 1.25x (picture only); B7 starts 0.23 s later.
set -Eeo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
W=/Volumes/Extreme/_edit_work/DS-107/r2; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH" GATE_GROUP=DS-107
S=$(date +%s); VOICES_ONLY=balanced python3 recipe/prep.py > logs/prep.log 2>&1; echo "$(date +%T) $(( $(date +%s)-S ))s prep (Balanced voice)" >> logs/build-times.txt; tail -1 logs/prep.log
VOICE=balanced LOOK=r5warm bash recipe/build.sh
