#!/bin/zsh
# RO-02 round 3 post-render chain on the exact master: audio gate, SRT/chapters/plan, watch pass, dense hair check, graphics checks.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro02/round3
mkdir -p logs
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" RO02_MASTER.mp4 --untreated RO02_MASTER.mp4.audio_untreated.json --ab "RO-02 audio AB (Muhammad then ours).mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log || true
ffmpeg -v error -y -i RO02_MASTER.mp4 -vn -ac 1 -ar 16000 final16k.wav
nice -n 10 python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1
echo TX_DONE
python3 /Volumes/Extreme/_edit_work/ro02/recipe/finish.py RO02_MASTER.mp4
python3 "$P/.claude/skills/_shared/deliver/watch.py" RO02_MASTER.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
grep -E "naked|graphics present|frozen" logs/watch.log || true
python3 /Volumes/Extreme/_edit_work/ro02/recipe/haircheck.py RO02_MASTER.mp4 plan.json logs/haircheck.json > logs/haircheck.log 2>&1
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair', d['samples'], d['min_top_px'], len(d['under_20']))"
python3 "$P/.claude/skills/_shared/hyperframes/checks.py" /Volumes/Extreme/_edit_work/ro02/hf/manifest.json --film RO02_MASTER.mp4 --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -25 logs/checks.log
echo CHAIN_DONE
