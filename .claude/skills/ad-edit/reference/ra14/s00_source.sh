#!/bin/bash
# RA-14 source prep: lav pick measured on the Cheat Code takes, lav pull, envelope, chunked medium.en transcript.
cd /Volumes/Extreme/_edit_work/ra14
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/pick_lav.py" "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1667.MP4" --ss 340 --t 70 > logs/pick_lav.log 2>&1; echo "pick_lav exit $?" >> logs/pick_lav.log
python3 s01_env.py > logs/s01.log 2>&1 || { echo SOURCE_FAILED s01; exit 1; }
bash s02_tx.sh > logs/s02.log 2>&1 || { echo SOURCE_FAILED s02; exit 1; }
echo SOURCE_COMPLETE
