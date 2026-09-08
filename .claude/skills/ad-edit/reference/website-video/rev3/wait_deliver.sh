#!/bin/zsh
# wait on stage2's PROCESS, then run the delivery gates in the foreground of this waiter (hard timeout 2 h)
cd /Volumes/Extreme/_edit_work/website-video-828
T0=$(date +%s)
while kill -0 29029 2>/dev/null; do
  sleep 20
  if [ $(( $(date +%s)-T0 )) -gt 7200 ]; then echo "STAGE2 WAIT TIMEOUT"; exit 2; fi
done
echo "stage2 exited after $(( $(date +%s)-T0 ))s"; tail -4 logs/stage2.log
grep -q 'STAGE2 DONE' logs/stage2.log || { echo "STAGE2 FAILED -- not running the gates"; exit 1; }
echo "launching delivery gates"
./run_bg.sh deliver ./deliver.sh
echo "deliver exited"; tail -6 logs/deliver.log
