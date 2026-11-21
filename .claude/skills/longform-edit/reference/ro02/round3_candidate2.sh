#!/bin/zsh
# Candidate 2: graphics for the re-timed plan, segment + cutaway scans, the whole film, then the finish chain.
set -e
cd /Volumes/Extreme/_edit_work/ro02
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:$PATH"
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
echo "MARK hf $(date +%H:%M)"
nice -n 10 python3 "$SK/hyperframes/from_plan.py" --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render
recipe/round3_render.sh
recipe/finish_chain.sh
echo "MARK ALL DONE $(date +%H:%M)"
