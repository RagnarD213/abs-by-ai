#!/bin/zsh
# DS-41 R1: key the four pieces one after another, each as its own render-queue step (heavy lane).
W=/Volumes/Expansion/_edit_work/DS-41/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
for P in watchA watchB S O; do
  python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-41 --label "DS-41 key $P" -- zsh recipe/run_key.sh $P > key_$P.log 2>&1
  echo "KEY $P exit $? $(tail -1 key_$P.log | cut -c1-120)"
done
echo KEYS FINISHED
