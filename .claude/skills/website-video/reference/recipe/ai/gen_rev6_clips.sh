#!/bin/zsh
cd /Volumes/Extreme/_edit_work/website-video-828/ai
for n in "$@"; do
  echo "== clip $n $(date +%H:%M:%S)"
  node veo.js rev6/$n.jpg prompts/${n}_video.txt rev6/$n.mp4 8 16:9 | tee logs/rev6_veo_$n.log
  echo "clip $n exit $?"
done
echo "CLIPS DONE $* $(date +%H:%M:%S)"
