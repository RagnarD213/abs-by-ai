#!/bin/bash
# DS-49 Why I Stopped Drinking Coconut Water: five image sources. Codex subscription, gpt-6.1-sol high.
# A/B/D/E: AI Dan (real identity reference + the film's pool as scene reference). C: empty background plate for the real studio cutout.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds49-coconut-water-20261029"
for k in A B C D E; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=()
    if [ "$k" != C ]; then args+=(--image "$R/sources/identity-reference.jpg" --image "$R/sources/scene-reference.jpg"); fi
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds49-20261029/prompts/$k.txt" --out "$R/sources/$k.png" ${args[@]+"${args[@]}"} > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
