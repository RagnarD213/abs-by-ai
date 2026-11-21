#!/bin/bash
# DS-107 R1 build, one render-queue step:  zsh recipe/build.sh   (env VOICE, LOOK, AUDIO_ONLY=1 remixes on the existing picture)
# prep (audio + edit list) -> framing (needs the key) -> graphics if shot times moved -> captions + mix -> assembly -> audio gate ->
# gate plan (delivered ASR) -> watch pass -> delivery gate. Each heavy step's wall clock goes to logs/build-times.txt.
set -Eeo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-107
V=${VOICE:-house_bass15}; L=${LOOK:-r5warm}; NAME="Metabolism Not The Reason SFC R1"
T(){ S=$(date +%s); "$@"; local rc=$?; echo "$(date +%T) $(( $(date +%s)-S ))s rc=$rc cores=${RENDERQ_CORES:-?} $*" | cut -c1-160 >> logs/build-times.txt; return $rc; }   # R1: the wrapper used to swallow a failing step (a broken graphics.py went unnoticed for three builds)
for p in Ka Kb Kc Kd Ke Kf Kg; do [ -f key/$p.done ] || { echo "KEY $p NOT DONE"; exit 1; }; done
T python3 recipe/prep.py --no-audio | tail -1
[ -n "$AUDIO_ONLY" ] || T python3 recipe/framing.py > main/framing.log 2>&1 || { echo FRAMING FAIL; tail -5 main/framing.log; exit 1; }
if [ -z "$FORCE_GFX" ] && python3 -c "import json,sys;a=[(s['id'],round(s['a'],3),round(s['b'],3)) for s in json.load(open('main/shots.json')) if s['id'][0] in 'TK'];m={x['id']:x for x in json.load(open('main/graphics-manifest.json'))};w=json.load(open('main/words_out.json'));k=m.get('K1');sys.exit(0 if k and any(abs(k['a']-s_[1])<1e-3 for s_ in a if s_[0]=='K1') and abs(m['G03']['b']-(w[-1]['t1']))<5 and json.load(open('main/graphics-manifest.json'))[0].get('_edl_frames')==json.load(open('main/edl.json'))['total_frames'] else 1)"; then echo "graphics: up to date for this edit list"
else T python3 recipe/graphics.py > main/graphics.log 2>&1 || { echo GRAPHICS FAIL; tail -3 main/graphics.log; exit 1; }; fi
python3 recipe/captions.py $V
T python3 recipe/assemble.py --voice $V --look $L ${AUDIO_ONLY:+--mux-only} > main/assemble.log 2>&1 || { echo ASSEMBLE FAIL; tail -5 main/assemble.log; exit 1; }; tail -1 main/assemble.log
cd $W/main; M="review/$NAME.mp4"
python3 -c "import sys;sys.path.insert(0,'$R/.claude/skills/_shared/audio');import common as C;C.stash_untreated('mix-untreated.wav',C.pcm('mix-untreated.wav',af='pan=mono|c0=0.5*c0+0.5*c1'),note='untreated timeline: the raw C1908 lav pieces (a:0 c0), pan mono')"
T python3 "$R/.claude/skills/_shared/audio/audio_gate.py" "$M" --untreated mix-untreated.wav --ab "review/$NAME - audio AB.mp4" > audio_gate.log 2>&1 || true; grep -E "FAIL|AUDIO GATE" audio_gate.log | head -8
cd $W; T python3 recipe/gateplan.py > main/gateplan.log 2>&1 || { echo GATEPLAN FAIL; tail -5 main/gateplan.log; exit 1; }; tail -1 main/gateplan.log | cut -c1-160
cd $W/main; rm -rf qa; mkdir -p qa
T python3 "$R/.claude/skills/_shared/deliver/watch.py" "$M" --plan gate-plan.json --out qa --log qa/watch_pass.json --clips > qa/watch.log 2>&1 || true; grep -E "scan|frozen|naked|graphics present|boundaries" qa/watch.log | head || true
T python3 "$R/.claude/skills/_shared/deliver/gate.py" "$M" --format short --plan gate-plan.json > deliver_gate.log 2>&1 || true
grep -E "^\s+(FAIL|\?\?\?\?)|passed|DELIVERY GATE" deliver_gate.log | cut -c1-230 || true
echo "BUILD DONE"
echo CHAIN_DONE
