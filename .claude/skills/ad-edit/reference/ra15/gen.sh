#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra15/aiprompts
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
for i in I1 I2 I4 I5; do
  ( "$CI" --prompt-file ${i}_start.txt --out ../round1/frames/${i}-start.png > ${i}_start.log 2>&1; echo "${i} start exit $?" >> gen.log ) &
done
wait
for i in I1 I2 I4 I5; do
  [ -s ../round1/frames/${i}-start.png ] && ( "$CI" --prompt-file ${i}_end.txt --image ../round1/frames/${i}-start.png --out ../round1/frames/${i}-end.png > ${i}_end.log 2>&1; echo "${i} end exit $?" >> gen.log ) &
done
wait
echo FRAMES_COMPLETE >> gen.log
