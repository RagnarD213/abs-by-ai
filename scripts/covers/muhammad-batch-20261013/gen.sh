#!/bin/bash
# Run every Codex image job in assets/jobs.json that has no output yet, six at a time (ChatGPT subscription, no API spend).
cd "$(dirname "$0")/../../.." || exit 1
R="Short-form video content/covers/review/muhammad-batch-20261013"
python3 - "$R" <<'PY' > "$R/assets/todo.tsv"
import json,sys,os
for j in json.load(open(sys.argv[1]+'/assets/jobs.json')):
    if not os.path.exists(j['out']): print(j['prompt'],j['out'],j['ref'],sep='\t')
PY
n=0
while IFS=$'\t' read -r p o r; do
  ( if [ -n "$r" ]; then .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$p" --out "$o" --image "$r"; else .claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file "$p" --out "$o"; fi ) >> "$R/assets/gen.log" 2>&1 &
  n=$((n+1)); if [ $((n%6)) -eq 0 ]; then wait; fi
done < "$R/assets/todo.tsv"
wait; echo "done: $(ls "$R/assets/gen"/*.png 2>/dev/null | wc -l) images"
