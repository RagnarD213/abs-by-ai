#!/bin/bash
# Round 2 media, in order. Each step logs a marker line; a failed step stops the chain.
set -e
cd /Volumes/Extreme/_edit_work/ro02
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:$PATH"
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
echo "MARK resumed"
echo "MARK hf start $(date +%H:%M)"
nice -n 10 python3 "$SK/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render
echo "MARK stills start $(date +%H:%M)"
python3 recipe/stills.py
echo "MARK first start $(date +%H:%M)"
python3 recipe/review_media.py first
FM="round2/first-minute/DRAFT - RO-02 round 2 - first minute.mp4"
python3 recipe/hair_first.py "$FM" round2/first-minute/hair.json
python3 "$SK/audio/audio_gate.py" "$FM" --ab "round2/first-minute/RO-02 round 2 - audio A-B vs Muhammad.mp4" || echo "MARK audio gate returned non-zero"
echo "MARK context start $(date +%H:%M)"
python3 recipe/review_media.py context
python3 recipe/review_media.py verify
echo "MARK CHAIN DONE $(date +%H:%M)"
