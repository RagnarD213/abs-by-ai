#!/bin/zsh
# DS-36 R1: wait for this version's key piece and its graphics (plate included), then build it as one render-queue step.
V=$1; W=/Volumes/Expansion/_edit_work/DS-36/r1; cd $W
P=$([ $V = scripted ] && echo S || echo O)
until [ -f key/$P.done ] && [ -f $V/plate-manifest.json ]; do sleep 20; done
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-36 -- zsh recipe/build.sh $V
