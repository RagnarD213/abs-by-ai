#!/bin/zsh
set -e
cd /Volumes/Extreme/_edit_work/ro02
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 recipe/edl.py | tail -1
python3 recipe/shots.py | head -1
python3 recipe/assemble_audio.py
nice -n 5 python3 recipe/asr_assembled.py 2>/dev/null | tail -1
python3 recipe/words_out.py
python3 recipe/resolve.py
echo RETIME_DONE
