#!/bin/bash
# Five image sources. Codex subscription, current supported stable Sol at high effort.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds84-hamstring-curls-20261028"
for k in A B C D E; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=()
    if [ "$k" != C ]; then args+=(--image "$R/sources/identity-reference.jpg" --image "$R/sources/exercise-reference.jpg"); fi
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds84-20261028/prompts/$k.txt" --out "$R/sources/$k.png" "${args[@]}" > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
