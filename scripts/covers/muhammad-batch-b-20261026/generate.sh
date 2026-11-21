#!/bin/bash
# Uses the Codex subscription (GPT-6.1 Sol, high). Never regenerates an existing source automatically.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/muhammad-batch-b-20261026"
one(){ k=$1; [ -s "$R/sources/$k.png" ] && return 0
  args=(); case $k in *-C) ;; *) args+=(--image "$R/sources/identity-reference.jpg");; esac
  .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/muhammad-batch-b-20261026/prompts/$k.txt" --out "$R/sources/$k.png" "${args[@]}" > "$R/sources/$k-generation.log" 2>&1; echo "$k exit $?"; }
export -f one; export R
ls scripts/covers/muhammad-batch-b-20261026/prompts | sed 's/.txt//' | xargs -P 5 -I{} bash -c 'one {}'
