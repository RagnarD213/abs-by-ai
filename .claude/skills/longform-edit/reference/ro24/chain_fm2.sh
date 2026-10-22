#!/bin/bash
# RO-24 round 1, second half: key comparison clips, key numbers, then every check on the exact first-minute export.
set -uo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round1; R="$W/recipe"
echo "== key comparisons"
python3 "$R/keycompare.py" "$W/key/fm/K1.mkv" 300 660 "$W/review/key" --tag=-hook
python3 "$R/keycompare.py" "$W/key/fm/K2.mkv" 60 300 "$W/review/key" --tag=-sharon
python3 "$R/keycompare.py" "$W/key/fm/K2.mkv" 380 470 "$W/review/key" --tag=-hands1
python3 "$R/keycompare.py" "$W/key/fm/K3.mkv" 120 215 "$W/review/key" --tag=-hands2
python3 "$R/keycompare.py" "$W/key/fm/K2.mkv" 600 660 "$W/review/key" --tag=-gaps
echo "== key numbers"
for k in K1 K2 K3; do python3 "$R/keynum.py" "$W/key/fm/$k.mkv" 15 "$W/checks/keynum-$k.json" > /dev/null; done
echo "CHAIN FM2 DONE"
