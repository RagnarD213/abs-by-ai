#!/bin/zsh
# RO-14 round 3 post-render chain on the exact master (from round 2's finish_chain.sh): audio gate, transcript, SRT/chapters/plan,
# watch pass (judge runs after, by a fresh agent), dense hair check, every-frame hair edge (1080p + 540p review copy), graphics checks.
set -e
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; W=/Volumes/Extreme/_edit_work/RO-14/round3
export PATH="$P/Media/video_edit/bin:$PATH"
cd $W/final; mkdir -p logs
[ -f RO14_MASTER.mp4.audio_gate.json ] || python3 "$P/.claude/skills/_shared/audio/audio_gate.py" RO14_MASTER.mp4 --untreated RO14_MASTER.mp4.audio_untreated.json --ab "RO-14 audio AB (untreated then ours).mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log || true
[ -f final.whisper.json ] || ffmpeg -v error -y -i RO14_MASTER.mp4 -vn -ac 1 -ar 16000 final16k.wav
[ -f final.whisper.json ] || python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1
echo TX_DONE
python3 $W/recipe/finish.py RO14_MASTER.mp4
python3 "$P/.claude/skills/_shared/deliver/watch.py" RO14_MASTER.mp4 --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
grep -E "naked|graphics present|frozen" logs/watch.log || true
python3 $W/recipe/haircheck.py RO14_MASTER.mp4 plan.json logs/haircheck.json > logs/haircheck.log 2>&1
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair', d['samples'], d['min_top_px'], len(d['under_20']))"
[ -f "$W/review/media/RO-14 round 3 - full film REVIEW 540p.mp4" ] || ffmpeg -v error -y -i RO14_MASTER.mp4 -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart "$W/review/media/RO-14 round 3 - full film REVIEW 540p.mp4"
python3 $W/recipe/hairedge.py RO14_MASTER.mp4 $W/plan_resolved.json hairedge_1080.json > logs/hairedge_1080.log 2>&1 || echo HAIREDGE1080_NONZERO
python3 $W/recipe/hairedge.py "$W/review/media/RO-14 round 3 - full film REVIEW 540p.mp4" $W/plan_resolved.json hairedge_540.json > logs/hairedge_540.log 2>&1 || echo HAIREDGE540_NONZERO
tail -2 logs/hairedge_1080.log logs/hairedge_540.log
python3 "$P/.claude/skills/_shared/hyperframes/checks.py" $W/hf/manifest.json --film RO14_MASTER.mp4 --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -25 logs/checks.log
echo CHAIN_DONE
