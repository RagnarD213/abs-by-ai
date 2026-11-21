#!/bin/bash
# RA-14 round 2: six opener frames on the Codex subscription (GPT-6.1 Sol, high). Starts first, then each END from its START.
H="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
cd /Volumes/Extreme/_edit_work/ra14/round2/opener
for k in o1 o2 o3; do
  ( "$H" --model gpt-6.1-sol --effort high --prompt-file prompts/${k}_start.txt --out raw/${k}_start.png > logs/${k}_start.log 2>&1; echo "$k start exit $?" >> logs/status.txt ) &
done
wait
for k in o1 o2 o3; do
  if [ -s raw/${k}_start.png ]; then
    ( "$H" --model gpt-6.1-sol --effort high --prompt-file prompts/${k}_end.txt --image raw/${k}_start.png --out raw/${k}_end.png > logs/${k}_end.log 2>&1; echo "$k end exit $?" >> logs/status.txt ) &
  else echo "$k end SKIPPED (no start)" >> logs/status.txt; fi
done
wait
echo "FRAMES DONE $(date +%T)" >> logs/status.txt
