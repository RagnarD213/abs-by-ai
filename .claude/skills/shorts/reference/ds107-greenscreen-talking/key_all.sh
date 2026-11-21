#!/bin/bash
# DS-107 R1: every on-screen stretch, one heavy render-queue step each, wall clock per piece (ROUTING-PROOF.md)
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
W=/Volumes/Extreme/_edit_work/DS-107/r1; cd $W
R="/Users/danielrose/Projects/Claude/Projects/Abs By AI"; export PATH="$R/Media/video_edit/bin:$PATH"
for P in Ka Kb Kc Kd Ke Kf; do
  S=$(date +%s); ST=$(date +%T)
  python3 "$R/.claude/skills/_shared/renderq/renderq.py" run --group DS-107 --label "DS-107 key $P" -- zsh recipe/run_key.sh $P > logs/key_$P.log 2>&1
  echo "KEY $P start $ST wall $(( $(date +%s)-S ))s $(tail -1 logs/key_$P.log | cut -c1-80)" | tee -a logs/key-times.txt
done
echo CHAIN_DONE
