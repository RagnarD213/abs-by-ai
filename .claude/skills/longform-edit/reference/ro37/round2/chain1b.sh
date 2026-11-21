#!/bin/bash
# RO-37 round 2, stage 1b (heavy slot): background clips, big type, one still per background segment, the first
# minute's lower thirds, the first minute.
set -e
R=/Volumes/Expansion/_edit_work/RO-37/round2; cd $R/recipe
GS="/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg"
python3 prep_bg.py clips
python3 -c "import r2; [r2.shot_geo(s) for s in r2.shots2() if not s['covered'] and not s['closeup']]; print('geo ok')"
python3 "$GS/hfbg.py" $R/bg_plan.json $R/hf/bg --render
python3 stills.py
python3 lt2.py --render --only G02,G03,G04,G05
mkdir -p $R/review/first-minute
FM="$R/review/first-minute/DRAFT - First Time At The Gym R2 - first minute.mp4"
python3 assemble.py $R/review/first-minute/picture.mp4 --t0 0 --t1 61.0944
bash mux.sh $R/review/first-minute/picture.mp4 /Volumes/Expansion/_edit_work/RO-37/round1/review/first-minute/voice_A.wav 0 "$FM"
echo CHAIN1B_DONE
