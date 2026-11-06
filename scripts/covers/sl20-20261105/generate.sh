#!/bin/bash
# SL-20 Invest In Your Health Shorts: 15 Codex sources (5 per Short). Codex subscription, gpt-6.1-sol high.
set -uo pipefail
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/sl20-invest-20261105/sources"
P=scripts/covers/sl20-20261105/prompts
for k in ${@:-s1A s1B s1C s1D s1E s2A s2B s2C s2D s2E s3A s3B s3C s3D s3E}; do
  [ -s "$R/$k.png" ] && continue
  (
    args=()
    case $k in *C) ;; *) args=(--image "$R/identity-reference.jpg");; esac
    .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$P/$k.txt" --out "$R/$k.png" ${args[@]+"${args[@]}"} > "$R/$k-generation.log" 2>&1
    echo "$k exit $?"
  ) &
  sleep 2
done
wait
