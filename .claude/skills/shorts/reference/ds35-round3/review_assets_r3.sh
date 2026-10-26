#!/bin/zsh
set -e
TASK_ROOT=/Volumes/Expansion/_edit_work/DS-35/round3
export GATE_GROUP=DS-35
for VERSION in scripted off_the_cuff; do
 python3 "$TASK_ROOT/recipe/preservation_r3.py" "$VERSION"
done
python3 "$TASK_ROOT/recipe/review_media_r3.py"
