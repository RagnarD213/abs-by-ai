#!/bin/bash
# RO-29: EDL -> assembled audio -> shots -> assembled ASR -> words_out -> hair measure -> crops
cd /Volumes/Expansion/_edit_work/RO-29/round1
export PATH="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -e
python3 recipe/edl.py > logs/edl.log
python3 recipe/assemble_audio.py > logs/assemble.log 2>&1
python3 recipe/shots.py > logs/shots.log 2>&1
ffmpeg -nostdin -v error -y -i assembled_untreated.wav -af "pan=mono|c0=c0" -ar 16000 assembled16k.wav
bash recipe/asr_assembled.sh > logs/asr_assembled.log 2>&1
python3 recipe/hair_pre.py > logs/hair_pre.log 2>&1
python3 recipe/crop_y.py > logs/crop_y.log 2>&1
echo REBUILD OK
