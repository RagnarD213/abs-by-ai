#!/bin/bash
# DS-43 Terry Crews Fasting: five image sources. Codex subscription, gpt-6.1-sol high. C is an empty plate for a real studio cutout.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds43-terry-crews-20261030"
for k in "$@"; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=()
    if [ "$k" != C ]; then args+=(--image "$R/sources/identity-reference.jpg"); fi
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds43-20261030/prompts/$k.txt" --out "$R/sources/$k.png" ${args[@]+"${args[@]}"} > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
