#!/bin/zsh
# usage: record.sh TAKE A:B SPECKEY REVIEW.md  -> window gate, then record the reviewer's file into its stamp, then verify
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"; export PATH="$P/Media/video_edit/bin:$PATH"; C="$P/.claude/skills/_shared/framecheck/clipcheck.py"
cd /Volumes/Extreme/_edit_work/RO-14/round2
python3 $C veo/$1 --spec motion/specs/$3.take.spec.json --frames $2 > logs/win_${1%.mp4}.log 2>&1; g=$?
python3 $C veo/$1 --frames $2 --review $4 >> logs/win_${1%.mp4}.log 2>&1
python3 $C veo/$1 --frames $2 --verify >> logs/win_${1%.mp4}.log 2>&1; v=$?
echo "$1 $2 gate=$g verify=$v" >> logs/recorded.out
