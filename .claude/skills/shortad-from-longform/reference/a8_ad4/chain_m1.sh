#!/bin/zsh
# Master render -> his audio muxed untouched -> every gate on the exact file (the a7 chain3 order, Ad 4 names)
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad4-vert
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
V=ad4_vertical_9x16.mp4
python3 render8.py --out picture.mp4 > logs/render_full1.log 2>&1 && tail -1 logs/render_full1.log || { echo "RENDER FAILED $(date)"; exit 1; }
python3 zmux.py picture.mp4 $V > logs/mux.log 2>&1 && tail -2 logs/mux.log || { echo "MUX FAILED $(date)"; exit 1; }
python3 "$AG" $V --reference-mix his_mix.wav --verbatim --ab AB_audio_his-vs-ours.mp4 > logs/audio_gate.log 2>&1; tail -2 logs/audio_gate.log
rm -rf watch; python3 watch.py $V > logs/watch.log 2>&1; python3 zwatch_sheets.py watch/sheets >> logs/watch.log 2>&1; tail -8 logs/watch.log
python3 caption_sync_check.py $V > logs/capsync.log 2>&1; tail -3 logs/capsync.log
python3 zhairgate2.py $V > logs/hairgate2.log 2>&1; tail -1 logs/hairgate2.log
python3 landing_check.py $V > logs/landing.log 2>&1; tail -3 logs/landing.log
echo "master gates done $(date)"
