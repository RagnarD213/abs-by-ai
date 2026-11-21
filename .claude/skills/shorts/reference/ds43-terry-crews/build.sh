#!/bin/zsh
# DS-43 R1 build of ONE version, one render-queue step:  zsh recipe/build.sh scripted|offcuff
# audio + edit list, framing (needs the key), captions + mix, assembly, key bar, audio gate, gate plan (delivered ASR), watch pass,
# delivery gate. Graphics (graphics.py) render before it.
set -e -o pipefail
V=$1; W=/Volumes/Expansion/_edit_work/DS-43/r2; cd $W
R="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-43
NAME="Terry Crews Fasting SFC R2 - $([ $V = scripted ] && echo scripted || echo off the cuff)"
for p in watchF S O; do [ -f key/$p.done ] || { echo "KEY $p NOT DONE"; exit 1; }; done
python3 recipe/prep.py $V | tail -1
[ -n "$AUDIO_ONLY" ] || python3 recipe/framing.py $V > $V/framing.log 2>&1 || { echo FRAMING FAIL; tail -5 $V/framing.log; exit 1; }
grep -E "'id': 'P[WR]'|'id': 'S0'" $V/framing.log | cut -c1-220 || true
if python3 -c "import json,sys;a=[(s['id'],round(s['a'],3),round(s['b'],3)) for s in json.load(open('$V/shots.json'))];b=[(s['id'],round(s['a'],3),round(s['b'],3)) for s in json.load(open('$V/shots-times.json'))];sys.exit(0 if a==b and __import__('os').path.exists('$V/plate-manifest.json') else 1)"; then echo "graphics: shot times unchanged, keeping the rendered graphics"
else python3 recipe/graphics.py $V > $V/graphics.log 2>&1 || { echo GRAPHICS FAIL; tail -3 $V/graphics.log; exit 1; }; fi
python3 recipe/captions.py $V house_bass15
WORKERS=${RENDERQ_CORES:-4} python3 recipe/assemble.py $V --voice house_bass15 ${AUDIO_ONLY:+--mux-only} > $V/assemble.log 2>&1 || { echo ASSEMBLE FAIL; tail -5 $V/assemble.log; exit 1; }; tail -1 $V/assemble.log
T0=$([ $V = scripted ] && echo 2054.50 || echo 2149.21)
[ -n "$AUDIO_ONLY$SKIP_MEASURE" ] || python3 recipe/measure_render.py $V $T0 $V/measure | tail -1 || true
[ -n "$AUDIO_ONLY$SKIP_MEASURE" ] || python3 recipe/ds44_mcflicker.py $V/measure/pale.mp4 $V/measure/mc.json $T0 | tail -2 || true
[ -n "$AUDIO_ONLY$SKIP_MEASURE" ] || python3 recipe/ds44_measure_r2.py $V/measure/pale.mp4 $V/measure/navy.mp4 $V/measure/m.json $T0 | tail -2 || true
cd $W/$V; M="review/$NAME.mp4"
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared/audio');import common as C;C.stash_untreated('mix-untreated.wav',C.pcm('mix-untreated.wav',af='pan=mono|c0=0.5*c0+0.5*c1'),note='untreated timeline: the clip original sound (same segments as the film) + the raw C1730 lav pieces, pan mono')"
python3 "$R/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated mix-untreated.wav --ab "review/$NAME - audio AB.mp4" > audio_gate.log 2>&1 || true; grep -E "FAIL|AUDIO GATE" audio_gate.log | head -8
cd $W; python3 recipe/gateplan.py $V > $V/gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 $V/gateplan.log; exit 1; }; tail -1 $V/gateplan.log | cut -c1-160
cd $W/$V; rm -rf qa; mkdir -p qa
python3 "$R/.claude/skills/_shared/deliver/watch.py" "$M" --plan gate-plan.json --out qa --log qa/watch_pass.json --clips > qa/watch.log 2>&1 || true; grep -E "scan|frozen|naked|graphics present|boundaries" qa/watch.log | head || true
python3 "$R/.claude/skills/_shared/deliver/gate.py" "$M" --format short --plan gate-plan.json > deliver_gate.log 2>&1 || true
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log | cut -c1-230 || true
echo "BUILD $V DONE"
