#!/bin/zsh
# usage: run.sh start|end   (starts: from ref.png; ends: edit of the matching start frame). Four at a time.
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
cd /Volumes/Extreme/_edit_work/ro08/aiframes
gen(){ id=$1; kind=$2
  [ -s $id-$kind.png ] && return
  if [ $kind = start ]; then img=ref.png; [ $id = A8 ] && img=""; else img=$id-start.png; fi
  if [ -n "$img" ]; then "$CI" --prompt-file prompts/$id-$kind.txt --out $id-$kind.png --image $img > $id-$kind.log 2>&1
  else "$CI" --prompt-file prompts/$id-$kind.txt --out $id-$kind.png > $id-$kind.log 2>&1; fi
  echo "$id-$kind exit $?"; }
for grp in "A1 A2 A3 A4" "A5 A6 A7 A8"; do for id in ${=grp}; do gen $id $1 & done; wait; done
echo "RUN $1 DONE"
