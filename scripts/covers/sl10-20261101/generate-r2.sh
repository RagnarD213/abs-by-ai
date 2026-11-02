#!/bin/bash
# Round 2: the pen swap on the What Killed My Urge To Drink pick, four new clock images for Stop Drinking 3 Hours Before Bed. Codex gpt-6.1-sol high.
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/sl10-alcohol-20261101"; P=scripts/covers/sl10-20261101/prompts-r2
.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$P/s4-A2.txt" --out "$R/sources/s4-A2-raw.png" --image "$R/sources/s4-A.png" --image "$R/sources/pen-reference.png" > "$R/sources/s4-A2.log" 2>&1 &
for k in I J K L; do
  .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$P/s3-$k.txt" --out "$R/sources/s3-$k.png" --image "$R/sources/identity-reference.jpg" --image "$R/sources/identity-reference-2.jpg" > "$R/sources/s3-$k.log" 2>&1 &
done
wait; echo done
