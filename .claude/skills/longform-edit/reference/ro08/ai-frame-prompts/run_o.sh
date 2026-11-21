#!/bin/zsh
# opener frames: OT-1 and O6-start from prompts; then O6-end (edit of O6-start) and OT-2..4 (edits of OT-1); then OT-5 (edit of OT-4)
CI="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/codex-image.sh"
cd /Volumes/Extreme/_edit_work/ro08/aiframes
g(){ [ -s $1.png ] && return; if [ -n "$2" ]; then "$CI" --prompt-file prompts/$1.txt --out $1.png --image $2 > $1.log 2>&1; else "$CI" --prompt-file prompts/$1.txt --out $1.png > $1.log 2>&1; fi; echo "$1 exit $?"; }
g OT-1 & g O6-start & wait
g O6-end O6-start.png & g OT-2 OT-1.png & g OT-3 OT-1.png & g OT-4 OT-1.png & wait
g OT-5 OT-4.png
echo "OPENER FRAMES DONE"
