#!/bin/zsh
# render the five shorts one after another, each waiting for a build slot (cap 2 across sessions)
cd /Volumes/Extreme/_edit_work/sl09/round2
for S in "$@"; do
  python3 waitslot.py sl09-render-$S
  python3 batch.py plan $S > logs_plan_$S.txt 2>&1 && python3 batch.py gfx $S > logs_gfx_$S.txt 2>&1 && python3 batch.py render $S > logs_render_$S.txt 2>&1
  echo "$S exit $? $(date +%H:%M:%S)"
done
echo ALLDONE
