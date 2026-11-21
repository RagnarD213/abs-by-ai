#!/bin/zsh
# RO-06 round 6 post-render chain on the exact master: audio gate, SRT/chapters/plan, watch pass, dense hair check, graphics checks.
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro06/round6
M="RO-06 round 6 - full film.mp4"
mkdir -p logs qc
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated "$M.audio_untreated.json" --ab "RO-06 audio AB (reference then ours).mp4" > logs/audio_gate.log 2>&1 || echo AUDIO_GATE_NONZERO
grep -E "AUDIO GATE|FAIL" logs/audio_gate.log
ffmpeg -nostdin -v error -y -i "$M" -vn -ac 1 -ar 16000 final16k.wav
nice -n 10 python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > logs/tx.log 2>&1 || echo TX_NONZERO
echo TX_DONE
python3 ../recipe/finish6.py "$M" > logs/finish.log 2>&1 || { echo FINISH_FAILED; tail -5 logs/finish.log; }
tail -22 logs/finish.log
python3 "$P/.claude/skills/_shared/deliver/watch.py" "$M" --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || echo WATCH_NONZERO
grep -E "naked|graphics present|frozen|black" logs/watch.log || true
python3 ../recipe/hair_fm.py "$M" qc > logs/hair.log 2>&1 || echo HAIR_NONZERO
tail -3 logs/hair.log | cut -c1-600
python3 "$P/.claude/skills/_shared/hyperframes/checks.py" ../hf/manifest.json --film "$M" --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -12 logs/checks.log
echo CHAIN_DONE
