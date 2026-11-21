#!/bin/zsh
# The <=0:59 cutdown: rendered from the master's beats through cut_plan.json, muxed with HIS mix cut at the seams (no
# filter), then every gate from inside cut/ (skill A6.18: generated modules resolve files next to themselves).
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad4-vert
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
V=ad4_vertical_9x16_59s.mp4
python3 render8.py --cutplan cut_plan.json --out cut/picture.mp4 > logs/render_cut4.log 2>&1 && tail -1 logs/render_cut4.log || { echo "CUT RENDER FAILED $(date)"; exit 1; }
cd cut
python3 ../zmux.py picture.mp4 $V his_mix.wav > logs/mux.log 2>&1 && tail -2 logs/mux.log || { echo "CUT MUX FAILED $(date)"; exit 1; }
python3 "$AG" $V --reference-mix his_mix.wav --verbatim --ab AB_audio_his-vs-ours_59s.mp4 > logs/audio_gate.log 2>&1; tail -2 logs/audio_gate.log
rm -rf watch; python3 watch.py $V > logs/watch.log 2>&1; python3 ../zwatch_sheets.py watch/sheets >> logs/watch.log 2>&1; tail -6 logs/watch.log
python3 ../caption_sync_check.py $V > logs/capsync.log 2>&1; tail -3 logs/capsync.log
python3 ../zhairgate2.py $V > logs/hairgate2.log 2>&1; tail -1 logs/hairgate2.log
python3 landing_check.py $V > logs/landing.log 2>&1; tail -3 logs/landing.log
echo "cut gates done $(date)"
