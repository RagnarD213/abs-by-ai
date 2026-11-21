#!/bin/bash
# DS-77 How To Do T-Bar Rows: five Codex sources. Codex subscription, gpt-6.1-sol high.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds77-t-bar-rows-20261105"
P=scripts/covers/ds77-20261105/prompts
for k in A B C D E; do
  [ -s "$R/sources/$k.png" ] && continue
  (
    args=()
    case $k in
      A|B) args=(--image "$R/sources/identity-reference.jpg" --image "$R/sources/exercise-reference.jpg");;
      D) args=(--image "$R/sources/screenshot-1.5.png");;
      E) args=(--image "$R/sources/screenshot-13.0.png");;
    esac
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$P/$k.txt" --out "$R/sources/$k.png" ${args[@]+"${args[@]}"} > "$R/sources/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
done
wait
