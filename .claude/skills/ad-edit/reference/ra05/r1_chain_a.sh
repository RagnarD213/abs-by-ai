#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra05
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py > logs/s08_a.log 2>&1 || exit 1
python3 s09_align.py > logs/s09_a.log 2>&1 || exit 2
python3 s04_track.py > logs/s04_a.log 2>&1 || exit 3
echo CHAIN_A_COMPLETE
