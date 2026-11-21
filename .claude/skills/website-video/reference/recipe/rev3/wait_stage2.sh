#!/bin/zsh
# wait on the PROCESSES (never a filename), hard timeout 90 min, then launch stage2 in the background
cd /Volumes/Extreme/_edit_work/website-video-828
T0=$(date +%s)
while kill -0 22423 2>/dev/null || kill -0 26705 2>/dev/null; do
  sleep 15
  if [ $(( $(date +%s)-T0 )) -gt 5400 ]; then echo "WAIT TIMEOUT after 90 min"; exit 2; fi
done
grep -q 'RENDER COMPLETE' logs/base.log || { echo "BASE DID NOT COMPLETE:"; tail -3 logs/base.log; exit 1; }
grep -q 'RENDER COMPLETE' logs/gfx2.log || { echo "GFX2 DID NOT COMPLETE:"; tail -3 logs/gfx2.log; exit 1; }
echo "base + gfx2 complete after $(( $(date +%s)-T0 ))s of waiting; launching stage2"
ls -la base.mov gfx/*.mov | awk '{print $5, $9}'
nohup ./run_bg.sh stage2 ./stage2.sh > /dev/null 2>&1 &
echo "stage2 launched pid $!"
