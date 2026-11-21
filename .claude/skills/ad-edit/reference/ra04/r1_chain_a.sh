#!/bin/bash
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -x
env BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py || exit 1
python3 s09_align.py || exit 2
python3 s04_track.py || exit 3
echo CHAIN_A_COMPLETE
