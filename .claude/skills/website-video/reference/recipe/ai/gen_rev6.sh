#!/bin/zsh
# REV 6 generations: 4 stills (C1 toe-touch NEW from the man reference; D1/D2/D3 in-place edits chicken -> steak)
# then 4 Veo clips. Sequential, logged. ~$0.13/still + ~$1.20/clip = ~$5.35 for one clean pass.
cd /Volumes/Extreme/_edit_work/website-video-828/ai
GI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/gemini-image.js"
gen() { # name promptfile refimage
  echo "== still $1 $(date +%H:%M:%S)"
  node "$GI" generate --prompt-file prompts/$2 --out rev6/$1.jpg --tier draft --aspect 16:9 --image $3 --env ~/.absbyai-secrets.env | tee logs/rev6_still_$1.log
}
STAGE=${1:-all}
if [[ $STAGE == all || $STAGE == stills ]]; then
gen C1t C1t_still.txt stills/A.jpg
gen D1s D1s_still.txt stills/D1b.jpg
gen D2s D2s_still.txt stills/D2.jpg
gen D3s D3s_still.txt stills/D3.jpg
echo "STILLS DONE $(date +%H:%M:%S)"
fi
if [[ $STAGE == all || $STAGE == clips ]]; then
for n in C1t D1s D2s D3s; do
  echo "== clip $n $(date +%H:%M:%S)"
  node veo.js rev6/$n.jpg prompts/${n}_video.txt rev6/$n.mp4 8 16:9 | tee logs/rev6_veo_$n.log
  echo "clip $n exit $?"
done
fi
echo "GEN REV6 DONE $(date +%H:%M:%S)"
