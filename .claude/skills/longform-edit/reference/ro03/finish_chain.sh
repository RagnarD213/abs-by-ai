#!/bin/zsh
# RO-03 round 2 post-render chain on the exact master: audio gate (whole film, then the speech alone), SRT/chapters/plan,
# watch pass, dense hair check, graphics checks. Absolute paths (README trap: symlinked folders).
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
W=/Volumes/Extreme/_edit_work/ro03
cd $W/round2
M=RO03_MASTER.mp4
mkdir -p logs
cp $W/film_audio.wav.audio_untreated.json $M.audio_untreated.json          # the film's untreated assembly, measured when the film was mixed (round 1)
cp $W/film_audio.wav.voice_chain.json $M.voice_chain.json
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" $M --untreated $M.audio_untreated.json --ab "RO-03 audio AB (reference then ours).mp4" > logs/audio_gate.log 2>&1 || echo AUDIO_GATE_NONZERO
grep -E "AUDIO GATE|FAIL" logs/audio_gate.log
(cd $W && python3 recipe/speechcheck.py) > logs/speechcheck.log 2>&1 || echo SPEECHCHECK_NONZERO
cat logs/speechcheck.log
python3 "$P/.claude/skills/_shared/audio/audio_gate.py" $W/tmp/tune/speech_only.wav --untreated $W/tmp/tune/speech_only.wav.audio_untreated.json > logs/audio_gate_speech_only.log 2>&1 || echo SPEECH_GATE_NONZERO
grep -E "AUDIO GATE|FAIL" logs/audio_gate_speech_only.log
ffmpeg -nostdin -v error -y -i $M -vn -ac 1 -ar 16000 final16k.wav
nice -n 10 python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > logs/tx.log 2>&1 || echo TX_NONZERO
echo TX_DONE
python3 $W/recipe/finish.py $M > logs/finish.log 2>&1 || { echo FINISH_FAILED; tail -5 logs/finish.log; }
tail -12 logs/finish.log
python3 "$P/.claude/skills/_shared/deliver/watch.py" $M --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || echo WATCH_NONZERO
grep -E "naked|graphics present|frozen|black" logs/watch.log || true
python3 "$P/.claude/skills/longform-edit/reference/ro02/haircheck.py" $M plan.json logs/haircheck.json > logs/haircheck.log 2>&1 || echo HAIR_NONZERO
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair samples', d['samples'], 'valid', d['valid'], 'min', d['min_top_px'], 'median', d['median_top_px'], 'under 20:', len(d['under_20']))"
python3 "$P/.claude/skills/_shared/hyperframes/checks.py" $W/hf/manifest.json --film $M --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -14 logs/checks.log
echo CHAIN_DONE
