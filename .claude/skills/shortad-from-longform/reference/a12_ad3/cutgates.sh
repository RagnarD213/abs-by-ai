#!/bin/zsh
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert/cut
F=ad3_vertical_9x16_59s.mp4
AUD="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
echo "cutgates start $(date)"
python3 ../watch.py $F              > logs/watch.log 2>&1    ; tail -10 logs/watch.log
python3 ../zwatch_sheets.py         > logs/sheets.log 2>&1   ; tail -2 logs/sheets.log
python3 ../caption_sync_check.py $F > logs/capsync.log 2>&1  ; tail -3 logs/capsync.log
python3 ../zhairgate2.py $F         > logs/hairgate.log 2>&1 ; tail -5 logs/hairgate.log
python3 "$AUD/audio_gate.py" $F --reference-mix his_mix.wav --verbatim --ab AB_audio_his-vs-ours_59s.mp4 > logs/audio_gate.log 2>&1 ; tail -6 logs/audio_gate.log
echo "CUTGATES DONE $(date)"
