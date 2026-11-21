#!/bin/zsh
# RO-14 round 2 post-render chain (from RO-17 round 3) on the exact master: audio gate, SRT/chapters/plan, watch pass, dense hair check, graphics checks.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/RO-14/round2/final_r4
mkdir -p logs
[ -f base.mp4 ] || mv tmp_base.mp4 base.mp4   # round 4: base rendered beside the master (SSD full)
[ -f RO14_MASTER.mp4.audio_gate.json ] || python3 "$P/.claude/skills/_shared/audio/audio_gate.py" RO14_MASTER.mp4 --untreated RO14_MASTER.mp4.audio_untreated.json --ab "RO-14 audio AB (untreated then ours).mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log
[ -f final.whisper.json ] || ffmpeg -v error -y -i RO14_MASTER.mp4 -vn -ac 1 -ar 16000 final16k.wav
[ -f final.whisper.json ] || python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1
echo TX_DONE
python3 /Volumes/Extreme/_edit_work/RO-14/round2/recipe/finish.py RO14_MASTER.mp4
python3 "$P/.claude/skills/_shared/deliver/watch.py" RO14_MASTER.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
grep -E "naked|graphics present|frozen" logs/watch.log || true
python3 /Volumes/Extreme/_edit_work/RO-14/round2/recipe/haircheck.py RO14_MASTER.mp4 plan.json logs/haircheck.json > logs/haircheck.log 2>&1
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair', d['samples'], d['min_top_px'], len(d['under_20']))"
python3 "$P/.claude/skills/_shared/hyperframes/checks.py" /Volumes/Extreme/_edit_work/RO-14/round2/hf/manifest.json --film RO14_MASTER.mp4 --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -25 logs/checks.log
echo CHAIN_DONE
