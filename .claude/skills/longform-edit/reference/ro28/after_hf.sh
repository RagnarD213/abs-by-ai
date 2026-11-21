#!/bin/bash
W=/Volumes/Expansion/_edit_work/ro28/round1; cd $W
until [ -f logs/hf_render.log ] && grep -q "HF EXIT" logs/hf_render.log; do sleep 20; done
grep -q "HF EXIT 0" logs/hf_render.log || { echo "HF FAILED"; tail -5 logs/hf_render.log; exit 1; }
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --group RO-28 -- bash recipe/chain_r1.sh
