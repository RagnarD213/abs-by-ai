#!/bin/bash
# round 1 rebuild after the independent review: ride, captions word, plan, graphics copy, split, inserts, render, QC
cd /Volumes/Extreme/_edit_work/ra06
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -x
bash r1_audio.sh > logs/s08_f.log 2>&1 || exit 1
python3 s09_align.py > logs/s09_f.log 2>&1 || exit 2
python3 s05_plan06.py > logs/s05_f.log 2>&1 || exit 3
python3 s04b_holdstart.py beats.json > logs/s04b_f.log 2>&1 || exit 4
bash r1_chain_c.sh > logs/chain_c_f.log 2>&1 || exit 5
bash r1_chain_d.sh > logs/chain_d_f.log 2>&1 || exit 6
echo CHAIN_F_COMPLETE
