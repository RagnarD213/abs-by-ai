#!/bin/bash
# RO-37 round 1, everything after a timeline change: graphics (unchanged ones are skipped), first minute, its hair check,
# the internal full-length source + context clips, then the presentation/colour samples.
set -e
W=/Volumes/Expansion/_edit_work/RO-37/round1; R=$W/recipe
python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py" --plan $W/plan_resolved.json --words $W/words_out.json --out $W/hf --shots $W/shots.json --render > $W/logs/hf2.log 2>&1
bash $R/fm_chain.sh
python3 $R/hair_fm.py
bash $R/ctx_chain.sh
python3 $R/pres_samples.py
echo R1_ALL_DONE
