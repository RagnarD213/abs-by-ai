#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra07/round2/aiprompts
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
R1=../../round1/frames
( "$CI" --prompt-file I3b_start.txt --image $R1/I3-end.png --out ../frames/I3b-start.png > I3b_start.log 2>&1; echo "I3b start exit $?" >> gen.log ) &
( "$CI" --prompt-file I4a_start.txt --image $R1/I3-end.png --image $R1/I4-start.png --out ../frames/I4a-start.png > I4a_start.log 2>&1; echo "I4a start exit $?" >> gen.log ) &
( "$CI" --prompt-file I4b_start.txt --image $R1/I3-end.png --out ../frames/I4b-start.png > I4b_start.log 2>&1; echo "I4b start exit $?" >> gen.log ) &
wait
for i in I3b I4a I4b; do
  [ -s ../frames/${i}-start.png ] && ( "$CI" --prompt-file ${i}_end.txt --image ../frames/${i}-start.png --out ../frames/${i}-end.png > ${i}_end.log 2>&1; echo "${i} end exit $?" >> gen.log ) &
done
wait
echo FRAMES_COMPLETE >> gen.log
