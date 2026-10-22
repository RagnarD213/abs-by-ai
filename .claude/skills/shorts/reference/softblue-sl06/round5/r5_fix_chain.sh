#!/bin/zsh
# SL-06 r5 fix: re-render C (needle above the Step 1 bar) and F (cut in the pause), then deliver + watch each
cd /Volumes/Extreme/_edit_work/sl06
RQ="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py"
for S in C F; do
  python3 "$RQ" run --label "sl06 render $S (fix)" -- nice -n 5 python3 batch.py render $S > r5log/render2_$S.log 2>&1 || { echo "RENDER FAIL $S"; continue; }
  grep -q rendered r5log/render2_$S.log || { echo "RENDER FAIL $S"; continue; }
  echo "DONE $S $(date +%T)"
  ./deliver_watch.sh $S > r5log/dw2_$S.log 2>&1; echo "WATCHED $S $(date +%T)"
done
echo "CHAIN DONE"
