#!/bin/zsh
# DS-41 R1: key the on-screen stretches of both takes, one render-queue step each (heavy lane), scripted first.
W=/Volumes/Expansion/_edit_work/DS-41/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
while ! grep -q "KEYS FINISHED" key_all.log; do sleep 20; done
for P in Sa Sb Sc Sd Oa Ob Oc Od Oe; do
  python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-41 --label "DS-41 key $P" -- zsh recipe/run_key.sh $P > key_$P.log 2>&1
  echo "KEY $P exit $? $(tail -1 key_$P.log | cut -c1-120)"
  [ $P = Sd ] && echo SCRIPTED KEYS FINISHED
done
echo TALK KEYS FINISHED
