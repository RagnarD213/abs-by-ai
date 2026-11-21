#!/bin/bash
# usage: gen.sh OUT_ID PROMPT_ID IMG1 [IMG2]  -- one Codex image edit, 3 tries, 90 s apart
cd /Volumes/Extreme/_edit_work/RO-17/round3/aiframes
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
out=$1; pid=$2; shift 2; args=(); for i in "$@"; do args+=(--image "$i"); done
for try in 1 2 3; do
  "$CI" --prompt-file prompts/$pid.txt "${args[@]}" --out $out.png --effort medium > logs_$out.txt 2>&1
  [ -s $out.png ] && { echo "$out ok"; exit 0; }; sleep 90; done; echo "$out FAILED"; exit 1
