#!/bin/bash
# DS-49 round 2 (Dan, 2026-10-29): three A-style designs, pouring coconut water into a sink. F/G outdoor kitchen, H indoor.
# Codex subscription, gpt-6.1-sol high. Identity reference for all; the film's pool frame as scene reference for F/G.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds49-coconut-water-20261029"
for k in F G H; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=(--image "$R/sources/identity-reference.jpg")
    if [ "$k" != H ]; then args+=(--image "$R/sources/scene-reference.jpg"); fi
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds49-20261029/prompts/$k.txt" --out "$R/sources/$k.png" "${args[@]}" > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
