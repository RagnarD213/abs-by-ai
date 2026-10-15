#!/bin/bash
# RO-18 round 1, after the first-minute render: gate, hair, every context clip, checks, page.
W=/Volumes/Extreme/_edit_work/RO-18/round1; cd $W
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"
export PATH="$P/Media/video_edit/bin:$PATH"
slot() { (cd "$P" && python3 -c "import sys; sys.path.insert(0,'.claude/skills/_shared'); import buildcap; buildcap.wait('RO-18 $1', quiet=True)"); }
slot stills; python3 recipe/stills.py > logs/stills.log 2>&1; echo "STILLS $(grep -c . logs/stills.log)"
slot first; nice -n 5 python3 -u -X faulthandler recipe/review_media.py first > logs/first.log 2>&1; echo "EXIT $?" >> logs/first.log
echo "FIRST: $(grep -E 'first minute to|EXIT' logs/first.log | tr '\n' ' ')"
tail -1 logs/first.log | grep -q "EXIT 0" || { echo "FIRST FAILED"; exit 1; }
grep -E '^\{' logs/first.log | tail -1 > review/first-minute/fidelity.json
F="review/first-minute/DRAFT - RO-18 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-18 round 1 - audio A-B vs reference.mp4" > logs/gate_first.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first.log 2>&1 || true; echo "HAIR FIRST: $(tail -1 logs/hair_first.log)"
slot context; nice -n 5 python3 -u recipe/review_media.py context_all > logs/context.log 2>&1; echo "CONTEXT done ($(grep -c '^context' logs/context.log)) exit $?"
python3 recipe/review_media.py verify > logs/verify.log 2>&1 || true; echo "VERIFY done"
python3 recipe/page_extra.py > logs/page_extra.log 2>&1; python3 recipe/page.py > logs/page.log 2>&1; echo "PAGE: $(tail -1 logs/page.log)"
echo "CHAIN B COMPLETE"
