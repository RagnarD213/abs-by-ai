#!/bin/zsh
# SL-06 r5: deliver + watch each short as soon as its render (r5log/queue_ABC.log) finishes
cd /Volumes/Extreme/_edit_work/sl06
for S in A B C; do
  until grep -qE "DONE $S|FAIL $S" r5log/queue_ABC.log; do sleep 15; done
  if grep -q "FAIL $S" r5log/queue_ABC.log; then echo "RENDER FAIL $S"; continue; fi
  ./deliver_watch.sh $S > r5log/dw_$S.log 2>&1; echo "WATCHED $S $(date +%T)"
done
echo "CHAIN DONE"
