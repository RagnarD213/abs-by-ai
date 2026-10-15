#!/bin/bash
# RO-14 round 1: rebuild what the independent check changed (graphics, stills, first minute, context for changed items, checks, page)
W=/Volumes/Extreme/_edit_work/RO-14/round1; cd $W
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; SH="$P/.claude/skills/_shared"; export PATH="$P/Media/video_edit/bin:$PATH"
slot() { (cd "$P" && python3 -c "import sys; sys.path.insert(0,'.claude/skills/_shared'); import buildcap; buildcap.wait('RO-14 $1', quiet=True)"); }
IDS="C24 G03 G04 P04 G18 G19 G21 G35 A4 G36 C11 C10 C12 T3 T4 G15 G23 G24 C23 G29 C09 G11 C13 A2 G13 C14 G17 G28 G34"
slot hf; nice -n 5 python3 "$SH/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render2.log 2>&1 || { echo "HF FAILED"; exit 1; }; echo "HF done"
python3 recipe/stills.py > logs/stills2.log 2>&1; echo "STILLS done"
slot first; nice -n 5 python3 recipe/review_media.py first > logs/first2.log 2>&1; tail -1 logs/first2.log > review/first-minute/fidelity.json; echo "FIRST done"
F="review/first-minute/DRAFT - RO-14 round 1 - first minute.mp4"
python3 "$SH/audio/audio_gate.py" "$F" --ab "review/first-minute/RO-14 round 1 - audio A-B vs reference.mp4" > logs/gate_first2.log 2>&1 || true; echo "GATE: $(grep -E 'AUDIO GATE' logs/gate_first2.log | tail -1)"
python3 recipe/hair_first.py > logs/hair_first2.log 2>&1 || true; echo "HAIR: $(tail -1 logs/hair_first2.log)"
cp "$F" "$P/Videos to Review/Not Losing Weight LFC R1 - first minute.mp4"; echo "VLC copy refreshed"
slot context; nice -n 5 python3 recipe/review_media.py context_one $IDS > logs/context2.log 2>&1; echo "CONTEXT done ($(grep -c fresh logs/context2.log))"
python3 recipe/review_media.py verify > logs/verify2.log 2>&1 || true; echo "VERIFY: $(grep -v PASS logs/verify2.log | grep -c .) non-pass lines"
echo "FIX CHAIN COMPLETE"
