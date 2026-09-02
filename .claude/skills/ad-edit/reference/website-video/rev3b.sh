#!/bin/zsh
# REV 3, second pass: the head track refined from the delivered frames (headtrack_refine.py) -> new
# head-anchored plan -> punch -> mix -> the approved rev-2 audio chain, unchanged -> captions -> gates.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== plan  $(date +%H:%M:%S)"; python3 layout.py plan | head -2
echo "== punch  $(date +%H:%M:%S)"; python3 layout.py punch
echo "== mix    $(date +%H:%M:%S)"; python3 layout.py mix
echo "== audio (rev-2 approved chain, unchanged)  $(date +%H:%M:%S)"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== captions  $(date +%H:%M:%S)"; python3 captions.py
echo "== gates  $(date +%H:%M:%S)"; AUDIO_GATE_SOFT=1 ./deliver.sh
echo "REV3B DONE  $(date +%H:%M:%S)"
