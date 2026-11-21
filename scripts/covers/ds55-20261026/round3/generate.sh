#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../../.."
REVIEW="Short-form video content/covers/review/ds55-five-minute-exercises-20261026/round3"
for choice in 1 2 3; do
 [ ! -s "$REVIEW/sources/$choice-retouched.png" ] || continue
 .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds55-20261026/round3/$choice-prompt.txt" --image "$REVIEW/sources/$choice-original.png" --out "$REVIEW/sources/$choice-retouched.png" > "$REVIEW/sources/$choice-generation.log" 2>&1 &
done
wait
