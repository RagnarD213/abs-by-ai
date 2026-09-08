#!/bin/zsh
# wait on the rev3 PROCESS (never a filename), hard timeout 100 min, print why it exited
cd /Volumes/Extreme/_edit_work/website-video-828
T0=$(date +%s); PID=""
while [ -z "$PID" ]; do
  PID=$(pgrep -f "run_bg.sh ${1:-rev3} " | head -1)
  [ -n "$PID" ] && break
  sleep 5; [ $(( $(date +%s)-T0 )) -gt 90 ] && { echo "rev3 never started"; exit 3; }
done
echo "waiting on ${1:-rev3} pid $PID"
while kill -0 $PID 2>/dev/null; do
  sleep 20
  if [ $(( $(date +%s)-T0 )) -gt 6000 ]; then echo "WAIT TIMEOUT after 100 min -- rev3 still running"; exit 2; fi
done
echo "rev3 exited after $(( $(date +%s)-T0 ))s"
tail -8 logs/${1:-rev3}.log
if grep -q 'RENDER COMPLETE' logs/${1:-rev3}.log; then echo "REV3 COMPLETE -- ready to review"; else echo "REV3 FAILED"; exit 1; fi
