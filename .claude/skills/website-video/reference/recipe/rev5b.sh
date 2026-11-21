#!/bin/zsh
# REV 5 chain after the (staged) mix: audio -> captions -> the delivery gates.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== 2 audio (rev-2 approved chain, unchanged)  $(date +%H:%M:%S)"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== 3 captions  $(date +%H:%M:%S)"; python3 captions.py
echo "== 4 gates  $(date +%H:%M:%S)"; ./deliver.sh
echo "REV5B DONE  $(date +%H:%M:%S)"
