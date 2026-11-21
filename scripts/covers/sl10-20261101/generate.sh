#!/bin/bash
# SL-10 Alcohol And Abs covers: twenty Codex images, five per Short. gpt-6.1-sol high on the subscription. C is an empty plate.
cd "$(dirname "$0")/../../.."
R="Short-form video content/covers/review/sl10-alcohol-20261101"
one() {
  n="$1"; k="${n#*-}"; [ -s "$R/sources/$n.png" ] && return 0
  args=(); if [ "$k" != C ]; then args+=(--image "$R/sources/identity-reference.jpg" --image "$R/sources/identity-reference-2.jpg"); fi
  .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "scripts/covers/sl10-20261101/prompts/$n.txt" --out "$R/sources/$n.png" ${args[@]+"${args[@]}"} > "$R/sources/$n-generation.log" 2>&1
  echo "$n exit $?"
}
export -f one; export R
ls scripts/covers/sl10-20261101/prompts | sed 's/.txt//' | xargs -P 5 -I{} bash -c 'one {}'
