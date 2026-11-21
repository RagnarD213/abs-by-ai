#!/bin/bash
# DS-77 round 2 (Dan, 2026-11-06): four new touched-up real screenshots. Codex subscription, gpt-6.1-sol high.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds77-t-bar-rows-20261105/sources"
for k in I J K L; do
  [ -s "$R/$k.png" ] && continue
  ( .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds77-20261105/prompts/$k.txt" --out "$R/$k.png" --image "$R/screenshot-$k.png" --image "$R/identity-reference.jpg" > "$R/$k-generation.log" 2>&1; echo "$k exit $?" ) &
done
wait
