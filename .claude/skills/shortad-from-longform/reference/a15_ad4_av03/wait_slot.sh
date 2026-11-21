#!/bin/zsh
# Exit 0 once fewer than two heavy encodes are running on three samples in a row (the two-build cap).
ok=0
while [ $ok -lt 3 ]; do
  n=$(ps -Ao pcpu,command | grep -E 'bin/ffmpeg' | grep -v grep | awk '$1>=50' | wc -l | tr -d ' ')
  if [ "$n" -le 1 ]; then ok=$((ok+1)); else ok=0; fi
  sleep 15
done
echo "slot free $(date)"
