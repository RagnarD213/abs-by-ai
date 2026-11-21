#!/bin/bash
# RO-21: key every range in round1/key_ranges.json once (keyonce.py stamps; first minute first). Run through the render queue.
set -uo pipefail
cd /Volumes/Expansion/_edit_work/RO-21/recipe/key
KO="/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/chroma-key/keyonce.py"
K=/Volumes/Expansion/_edit_work/RO-21/key
export MIN_FRAMES=40
# ranges: all, or only those whose film start is below/at-or-above $SPLIT seconds (FIRST=1: below)
LIST=$(mktemp); python3 -c "
import json, os; s = float(os.environ.get('SPLIT', '1e9')); first = os.environ.get('FIRST', '1') == '1'
for r in json.load(open('/Volumes/Expansion/_edit_work/RO-21/round1/key_ranges.json')):
    if (r['film'][0][0] < s) == first: print(r['name'], r['f0'], r['n'])" > $LIST
while read NAME F0 N <&3; do
  python3 "$KO" $K/$NAME.done --inputs stage1_16.py keylib.py stage15_temporal.py write16.py box16.py $K/plate_q.npy --params "$F0 $N RIM4" \
     --clear $K/$NAME -- bash ./run_key.sh $NAME $F0 $N < /dev/null || echo "KEY FAILED $NAME"
done 3< $LIST
echo KEY ALL DONE
