#!/bin/zsh
set -e
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"; export GATE_GROUP=DS-107
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W/recipe
export Y_BOTTOM=3840 ROWS=2880 WORKERS=2 MIN_N=10
S=$(date +%s)
python3 "$R/.claude/skills/_shared/chroma-key/calibrate.py" --code $W/recipe --src "/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4" \
  --t0 $1 --dur $2 --out $W/key/cal_$3 --plate $W/key/plate_out.npy --n 3
echo "CAL $3 WALL $(( $(date +%s)-S ))s"
