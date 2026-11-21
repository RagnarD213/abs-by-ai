#!/bin/bash
# usage: run_queue.sh ID[:ref] ...  -- two at a time, retried once after 60 s on failure
cd /Volumes/Extreme/_edit_work/RO-14/round1/aiframes
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
one() { spec=$1; id=${spec%%:*}; ref=""; [ "$spec" != "$id" ] && ref=${spec##*:}
  for try in 1 2 3; do
    if [ -n "$ref" ]; then "$CI" --prompt-file prompts/$id.txt --image $ref.png --out $id.png --effort medium > logs_$id.txt 2>&1
    else "$CI" --prompt-file prompts/$id.txt --out $id.png --effort medium > logs_$id.txt 2>&1; fi
    [ -s $id.png ] && { echo "$id ok"; return; }; sleep 90; done; echo "$id FAILED"; }
set -- "$@"
while [ $# -gt 0 ]; do
  one "$1" & p1=$!; shift
  if [ $# -gt 0 ]; then one "$1" & p2=$!; shift; wait $p2; fi
  wait $p1
done
