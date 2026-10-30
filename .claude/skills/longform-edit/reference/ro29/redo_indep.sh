#!/bin/bash
# RO-29 R1 after the independent check: new graphics/clips/timings, fresh blocks + context, first minute, gates, page.
W=/Volumes/Expansion/_edit_work/RO-29/round1; cd $W
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"
export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-29
for f in A7-start A7-end; do cp aiframes/$f.png review/aiframes/; ffmpeg -v error -y -i aiframes/$f.png -q:v 3 review/aiframes/$f.jpg; done
python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render3.log 2>&1 || { echo "HF3 FAILED"; tail -5 logs/hf_render3.log; exit 1; }; echo "HF3 done"
mkdir -p review/_old_pre_indep; mv review/blocks review/context review/_old_pre_indep/ 2>/dev/null
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS exit $?"
python3 -u -X faulthandler recipe/review_media.py first > logs/first.log 2>&1; echo "FIRST exit $? $(grep 'first minute to' logs/first.log)"
grep -E '^\{' logs/first.log | tail -1 > review/first-minute/fidelity.json
F="review/first-minute/DRAFT - RO-29 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-29 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
python3 recipe/hair_first540.py > logs/hair_first540.log 2>&1 || true; echo "HAIR 540: $(tail -1 logs/hair_first540.log)"
python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT exit $? ($(ls review/context | grep -c 540p))"
python3 recipe/review_media.py verify > logs/verify.log 2>&1; echo "VERIFY exit $?"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
