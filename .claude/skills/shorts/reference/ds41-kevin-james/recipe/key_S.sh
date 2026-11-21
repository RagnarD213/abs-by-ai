#!/bin/zsh
# DS-41 R1: the rest of the scripted stretches (Sa is already running), one render-queue step each.
W=/Volumes/Expansion/_edit_work/DS-41/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
until [ -f key/Sa.done ]; do sleep 15; done
for P in Sb Sc Sd; do
  python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-41 --label "DS-41 key $P" -- zsh recipe/run_key.sh $P > key_$P.log 2>&1
  echo "KEY $P exit $? $(tail -1 key_$P.log | cut -c1-120)" >> key_talk.log
done
echo SCRIPTED KEYS FINISHED >> key_talk.log
