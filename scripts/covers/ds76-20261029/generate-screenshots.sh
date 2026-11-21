#!/bin/bash
# DS-76 round 2: three touched-up real screenshots (Dan, 2026-10-29). Codex subscription, gpt-6.1-sol high.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds76-pull-ups-20261029"
for k in F G H; do
  [ -s "$R/sources/$k.png" ] && continue
  ( .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds76-20261029/prompts/$k.txt" --out "$R/sources/$k.png" --image "$R/sources/$k-screenshot.png" > "$R/sources/$k-generation.log" 2>&1; echo "$k exit $?" ) &
done
wait
