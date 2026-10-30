#!/bin/zsh
# RO-29 round 2: full film with colour A, warm bass plus voice, every AI clip and graded B-roll.
set -e
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"
export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-29
W=/Volumes/Expansion/_edit_work/RO-29/round2; O=$W/final; M=$O/RO29_MASTER.mp4
cd $W
python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render2.log 2>&1; echo "HF done"
N=$(python3 -c "import json;S=json.load(open('shots.json'));print(S[-1]['out_f1']/(30000/1001))")
python3 -u -c "import sys;sys.path.insert(0,'recipe');import build as B;B.render_range(0.0,$N,'$M')" > $O/logs/build.log 2>&1
echo "BUILD done $(ls -la $M | awk '{print $5}')"
cd $O
cp $M.base.mp4 base.mp4
python3 "$SH/audio/audio_gate.py" $M --untreated $M.audio_untreated.json --ab "RO-29 audio AB vs reference.mp4" > logs/audio_gate.log 2>&1 || true
grep -E "AUDIO GATE" logs/audio_gate.log || true
ffmpeg -v error -y -i $M -vn -ac 1 -ar 16000 final16k.wav
python3 "$P/.claude/skills/longform-edit/reference/ro05/tx.py" final16k.wav final.whisper.json > /dev/null 2>&1; echo TX_DONE
python3 $W/recipe/negscan.py > logs/negscan.log 2>&1; python3 $W/recipe/negscan.py record "[]" >> logs/negscan.log 2>&1
python3 $W/recipe/finish.py $M > logs/finish.log 2>&1; tail -1 logs/finish.log
python3 "$SH/deliver/watch.py" $M --plan plan.json --out watch --log logs/watch_pass.json > logs/watch.log 2>&1 || true
grep -E "naked|graphics present|frozen" logs/watch.log || true
python3 $W/recipe/haircheck.py $M plan.json logs/haircheck.json > logs/haircheck.log 2>&1 || true
python3 -c "import json;d=json.load(open('logs/haircheck.json'))['summary'];print('hair', d['samples'], d['min_top_px'], len(d['under_20']))" || true
python3 "$SH/hyperframes/checks.py" $W/hf/manifest.json --film $M --film-t0 0 --out checks > logs/checks.log 2>&1 || echo CHECKS_NONZERO
tail -5 logs/checks.log
python3 "$SH/deliver/gate.py" $M --plan plan.json --format longform > logs/gate.log 2>&1 || echo GATE_NONZERO
tail -15 logs/gate.log
echo CHAIN_R2_DONE
