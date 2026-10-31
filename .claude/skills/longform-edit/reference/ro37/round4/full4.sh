#!/bin/bash
# round 4: render the film in six chunks (each can be redone alone), join, add the voice
cd /Volumes/Expansion/_edit_work/RO-37/round4
RQ="/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py"
E=473.6; N=6
for i in 0 1 2 3 4 5; do
  a=$(python3 -c "print(round($i*$E/$N,3))"); b=$(python3 -c "print(round(($i+1)*$E/$N,3) if $i < 5 else 480)")
  [ -f r4/full/c$i.mp4 ] && continue
  python3 "$RQ" run --group RO-37 --label "RO-37 R4 film part $((i+1))/6" -- bash -c "cd /Volumes/Expansion/_edit_work/RO-37/round4; PYTHONPATH=recipe ~/.cache/ro37-matte/bin/python recipe/assemble.py r4/full/c$i.tmp.mp4 --t0 $a --t1 $b --plan bg_plan4.json --manifest hf4/manifest4.json && mv r4/full/c$i.tmp.mp4 r4/full/c$i.mp4 && mv r4/full/c$i.tmp.mp4.build.json r4/full/c$i.build.json" > r4/full/c$i.log 2>&1 &
done
wait
ls r4/full/c?.mp4 | wc -l
