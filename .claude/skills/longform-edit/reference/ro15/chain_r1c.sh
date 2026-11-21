#!/bin/bash
# RO-15 round 1, after the independent check's fixes: graphics (changed only), crops, stills, first minute, every context clip, checks, page.
W=/Volumes/Extreme/_edit_work/RO-15/round1; cd $W
P="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"; RQ="$SH/renderq/renderq.py"
export PATH="$P/Media/video_edit/bin:$PATH"; export GATE_GROUP=RO-15
nice -n 5 python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render2.log 2>&1; echo "HF: exit $?"
python3 recipe/crop_y.py > logs/crop_y.log 2>&1; echo "CROP_Y: $(head -1 logs/crop_y.log)"
python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS: exit $?"
python3 "$RQ" run --group RO-15 -- python3 -u recipe/review_media.py first > logs/first.log 2>&1; echo "FIRST: exit $? $(grep -E 'first minute to' logs/first.log)"
grep -E '^\{' logs/first.log | tail -1 > review/first-minute/fidelity.json
F="review/first-minute/DRAFT - RO-15 round 1 - first minute.mp4"
python3 "$RQ" run --group RO-15 --light -- python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-15 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
python3 "$RQ" run --group RO-15 -- python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT: exit $? ($(grep -c '^context' logs/context.log))"
python3 "$RQ" run --group RO-15 -- python3 -u recipe/review_media.py context_one A1 A2 A3 A4 A5 A6 A7 A8 > logs/context_ai.log 2>&1; echo "CONTEXT AI: exit $?"
rm -rf review/checks; python3 recipe/review_media.py verify > logs/verify.log 2>&1; echo "VERIFY: exit $? $(grep -vc PASS logs/verify.log) not PASS"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
cd "$P" && python3 .claude/skills/_shared/review_server.py 9715 $W/review > $W/logs/serve.log 2>&1; echo "SERVE: $(head -1 $W/logs/serve.log)"
echo "CHAIN COMPLETE"
