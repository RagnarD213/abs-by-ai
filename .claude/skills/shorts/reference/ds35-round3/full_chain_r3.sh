#!/bin/zsh
set -e
TASK_ROOT=/Volumes/Expansion/_edit_work/DS-35/round3
export GATE_GROUP=DS-35
for VERSION in scripted off_the_cuff; do
 python3 "$TASK_ROOT/recipe/render_r3.py" "$VERSION"
done
for VERSION in scripted off_the_cuff; do
 python3 "$TASK_ROOT/recipe/qa_r3.py" prep "$VERSION"
done
print 'BOTH_R3_COMPLETE_WITH_CURRENT_PLANS'
for VERSION in scripted off_the_cuff; do
 python3 "$TASK_ROOT/recipe/audio_exact_r3.py" "$VERSION"
 python3 "$TASK_ROOT/recipe/qa_r3.py" watch "$VERSION"
 python3 "$TASK_ROOT/recipe/qa_r3.py" rows "$VERSION"
done
print 'BOTH_R3_CANDIDATES_MEASURED'
