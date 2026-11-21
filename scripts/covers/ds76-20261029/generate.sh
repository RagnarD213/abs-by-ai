#!/bin/bash
# DS-76 How To Do Pull-Ups: five image sources. Codex subscription, gpt-6.1-sol high.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds76-pull-ups-20261029"
for k in A B C D E; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=()
    if [ "$k" != C ]; then args+=(--image "$R/sources/identity-reference.jpg" --image "$R/sources/exercise-reference.jpg"); fi
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds76-20261029/prompts/$k.txt" --out "$R/sources/$k.png" ${args[@]+"${args[@]}"} > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
