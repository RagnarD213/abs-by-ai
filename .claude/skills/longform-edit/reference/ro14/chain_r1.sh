#!/bin/bash
# RO-14 round 1 chain, after hair_pre and the voice fit. Prints a marker per step. Waits for a build slot before each heavy step.
W=/Volumes/Extreme/_edit_work/RO-14/round1; cd $W
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"
export PATH="$P/Media/video_edit/bin:$PATH"
slot() { (cd "$P" && python3 -c "import sys; sys.path.insert(0,'.claude/skills/_shared'); import buildcap; buildcap.wait('RO-14 $1', quiet=True)"); }
until [ -s fit/eq_B_bass3.txt ] && ! pgrep -f "recipe/hair_pre.py" >/dev/null; do sleep 15; done
python3 recipe/crop_y.py > logs/crop_y.log 2>&1; echo "CROP_Y done: $(head -1 logs/crop_y.log)"
slot hf; nice -n 5 python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render.log 2>&1 || { echo "HF RENDER FAILED"; tail -5 logs/hf_render.log; exit 1; }
n=$(python3 -c "import json,os;m=json.load(open('hf/manifest.json'));print(sum(1 for x in m if not os.path.exists(x.get('mov','') or 'x')))"); echo "HF done, missing renders: $n"
python3 recipe/dupscan.py > logs/dupscan.log 2>&1; echo "DUPSCAN: $(tail -1 logs/dupscan.log)"
slot stills; python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS done ($(grep -c . logs/stills.log) lines)"
slot first; nice -n 5 python3 recipe/review_media.py first > logs/first.log 2>&1; tail -1 logs/first.log > review/first-minute/fidelity.json; echo "FIRST done"
F="review/first-minute/DRAFT - RO-14 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-14 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
slot context; nice -n 5 python3 recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT done ($(grep -c context logs/context.log))"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY done"
echo "CHAIN COMPLETE"
