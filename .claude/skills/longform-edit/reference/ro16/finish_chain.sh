#!/bin/zsh
# RO-16 round 2 post-render chain on the exact master: audio gate, SRT/chapters/plan, watch pass, dense hair check.
# usage: finish_chain.sh   (run after build.py wrote round2/RO16_MASTER.mp4)
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro16/round2
mkdir -p logs
cp ../tmp_base.mp4 base.mp4
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" RO16_MASTER.mp4 --untreated RO16_MASTER.mp4.audio_untreated.json --ab "RO-16 audio AB (Muhammad then ours).mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log
ffmpeg -v error -y -i RO16_MASTER.mp4 -vn -ac 1 -ar 16000 final16k.wav
python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1
echo TX_DONE
python3 ../recipe/finish.py RO16_MASTER.mp4
python3 "$P/.claude/skills/_shared/deliver/watch.py" RO16_MASTER.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1
grep -E "naked|graphics present|frozen" logs/watch.log || true
python3 ../recipe/haircheck.py RO16_MASTER.mp4 plan.json logs/haircheck.json > logs/haircheck.log 2>&1
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair', d['samples'], d['min_top_px'], len(d['under_20']))"
echo CHAIN_DONE
