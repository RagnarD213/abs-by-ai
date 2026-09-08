#!/bin/zsh
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== tight"; python3 tight.py
echo "== gfx plates"; python3 gfx.py plates
python3 gfx.py name num1 flyblind num2 num3 cancel > logs/gfx_w1.log 2>&1 &
python3 gfx.py pool before today > logs/gfx_w2.log 2>&1 &
python3 gfx.py tellai trylist mealbul > logs/gfx_w3.log 2>&1 &
python3 gfx.py trial price solved cta > logs/gfx_w4.log 2>&1 &
wait
tail -n3 logs/gfx_w*.log
echo "STAGE1 DONE"
