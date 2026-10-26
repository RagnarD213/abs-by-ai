#!/bin/bash
# Uses the Codex subscription. Never regenerates an existing source automatically.
set -euo pipefail
cd "$(dirname "$0")/../../.."
REVIEW="Short-form video content/covers/review/ds55-five-minute-exercises-20261026"
for choice in A B C D E; do
  [ ! -s "$REVIEW/sources/$choice.png" ] || continue
  args=()
  if [ "$choice" != C ]; then args+=(--image "$REVIEW/sources/identity-reference.jpg"); fi
  .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds55-20261026/prompts/$choice.txt" --out "$REVIEW/sources/$choice.png" "${args[@]}" > "$REVIEW/sources/$choice-generation.log" 2>&1 &
done
wait
