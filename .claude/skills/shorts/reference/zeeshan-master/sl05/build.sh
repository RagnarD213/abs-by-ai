#!/bin/zsh
# SL-04 rebuild, in order: plan -> assets (chip names follow the plan) -> render.  ./build.sh A F
set -e
cd "${0:A:h}"
python3 plan_shots.py > /dev/null
rm -f assets/chip-*-s*.png(N)
python3 build-assets.py > /dev/null
python3 pill/make_pill5.py > /dev/null
nice node render.js "$@"
