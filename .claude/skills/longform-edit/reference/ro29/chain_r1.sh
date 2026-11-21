#!/bin/bash
# RO-29 round 1, after the HyperFrames renders: stills, first minute, audio gate, hair (1080 + 540), context for every item, checks, page.
W=/Volumes/Expansion/_edit_work/RO-29/round1; cd $W
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"
export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-29
python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render2.log 2>&1 || { echo "HF2 FAILED"; tail -5 logs/hf_render2.log; exit 1; }; echo "HF2 done"
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS $(grep -c . logs/stills.log) exit $?"
python3 -u -X faulthandler recipe/review_media.py first > logs/first.log 2>&1; echo "EXIT $?" >> logs/first.log
echo "FIRST: $(grep -E 'first minute to|EXIT' logs/first.log | tr '\n' ' ')"
tail -1 logs/first.log | grep -q "EXIT 0" || { echo "FIRST FAILED"; tail -5 logs/first.log; exit 1; }
grep -E '^\{' logs/first.log | tail -1 > review/first-minute/fidelity.json
F="review/first-minute/DRAFT - RO-29 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-29 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
sed -e 's/first minute.mp4"; wd = f"{W}\/review\/first-minute\/_hair"/first minute - REVIEW 540p.mp4"; wd = f"{W}\/review\/first-minute\/_hair540"/' -e 's/hair.json/hair540.json/' recipe/hair_first.py > recipe/hair_first540.py
python3 recipe/hair_first540.py > logs/hair_first540.log 2>&1 || true; echo "HAIR 540: $(tail -1 logs/hair_first540.log)"
python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT done ($(grep -c '^context' logs/context.log)) exit $?"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY done"
mkdir -p review/options/voice; cp options/voice/*.mp3 review/options/voice/
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
echo "CHAIN COMPLETE"
