#!/bin/bash
# DS-01 Top 5 Ab Exercises covers. Codex subscription (GPT-6.1 Sol, high). Never regenerates an existing source.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/ds01-top5-ab-exercises-20261027"
one(){ k=$1; [ -s "$R/sources/$k.png" ] && return 0
  args=()
  case $k in *-C) ;; *) args+=(--image "$R/sources/identity-reference.jpg");; esac
  case $k in *-A) args+=(--image "$R/sources/scene-pool.jpg");; *-B) args+=(--image "$R/sources/scene-gym.jpg");; esac
  .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/ds01-20261027/prompts/$k.txt" --out "$R/sources/$k.png" "${args[@]}" > "$R/sources/$k-generation.log" 2>&1; echo "$k exit $?"; }
export -f one; export R
ls scripts/covers/ds01-20261027/prompts | sed 's/.txt//' | xargs -P 5 -I{} bash -c 'one {}'
