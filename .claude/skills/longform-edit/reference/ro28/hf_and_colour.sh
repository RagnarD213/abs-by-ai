#!/bin/bash
cd /Volumes/Expansion/_edit_work/ro28/round1
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 recipe/colour_options.py > logs/colour.log 2>&1; echo "COLOUR EXIT $?" >> logs/colour.log
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render > logs/hf_render.log 2>&1; echo "HF EXIT $?" >> logs/hf_render.log
