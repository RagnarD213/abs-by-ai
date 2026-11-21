#!/bin/bash
# after the key: render the film in six chunks (each can be redone alone), join, add voice A
cd /Volumes/Expansion/_edit_work/RO-37/round3
RQ="/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py"
E=475.6; N=6
for i in 0 1 2 3 4 5; do
  a=$(python3 -c "print(round($i*$E/$N,3))"); b=$(python3 -c "print(round(($i+1)*$E/$N,3))")
  [ -f r3/full/c$i.mp4 ] && continue
  python3 "$RQ" run --group RO-37 --label "RO-37 R3 film part $((i+1))/6" -- bash -c "cd /Volumes/Expansion/_edit_work/RO-37/round3; PYTHONPATH=recipe ~/.cache/ro37-matte/bin/python recipe/assemble.py r3/full/c$i.tmp.mp4 --t0 $a --t1 $b --plan bg_plan3.json --manifest hf3/manifest3.json && mv r3/full/c$i.tmp.mp4 r3/full/c$i.mp4 && mv r3/full/c$i.tmp.mp4.build.json r3/full/c$i.build.json" > r3/full/c$i.log 2>&1 &
done
wait
ls r3/full/c?.mp4 | wc -l > r3/full/parts.txt
echo FULL_PARTS7_DONE >> logs_refine_all.log
