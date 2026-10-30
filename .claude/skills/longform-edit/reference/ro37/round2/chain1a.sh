#!/bin/bash
# RO-37 round 2, stage 1a (light slot: network-bound): gym stills, the background plan, the sparse geometry mattes
# (every 15th frame of every cut-out shot, $2.07) and the first minute's mattes ($3.56).
set -e
R=/Volumes/Expansion/_edit_work/RO-37/round2; cd $R/recipe
python3 prep_bg.py photos
python3 plan_bg.py > $R/logs/plan.txt
python3 matte.py run geo --cap-usd 3 --threads 14
python3 matte.py run first-minute --cap-usd 4 --threads 14
echo CHAIN1A_DONE
