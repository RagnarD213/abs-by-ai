#!/bin/zsh
# usage: run_take.sh TAKEFILE SPECKEY  (whole-take motion gate)
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/RO-14/round2
python3 "$P/.claude/skills/_shared/framecheck/clipcheck.py" veo/$1 --spec motion/specs/$2.take.spec.json > logs/clipcheck_${1%.mp4}.log 2>&1
echo "$1 exit $? $(grep -E 'VERDICT' logs/clipcheck_${1%.mp4}.log | tail -1)" >> logs/clipcheck_retakes.out
