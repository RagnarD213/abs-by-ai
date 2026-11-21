#!/bin/zsh
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"; cd /Volumes/Extreme/_edit_work/website-video-828
for a in tag ai_a ai_b ai_c1 ai_c2 ai_d2 ai_d3 macro hub; do
  s=$(date +%s); python3 build_inserts.py $a || { echo "FAILED $a"; exit 1; }; echo "  [$a took $(( $(date +%s)-s )) s]"
done
echo "INSERTS COMPLETE $(date +%H:%M:%S)"
