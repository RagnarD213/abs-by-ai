#!/bin/zsh
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
W=/Volumes/Extreme/_edit_work/ro19; cd $W
RS="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/review_server.py"
step() { echo "$1 $(date +%H:%M)" >> chain.log }
: > chain.log
nice -n 10 python3 recipe/stills20.py > stills.log 2>&1 || step "STILLS FAILED"; step "STILLS DONE"
python3 recipe/pagecopy19.py >> chain.log 2>&1; python3 recipe/page20.py >> chain.log 2>&1 || step "PAGE FAILED"
python3 "$RS" 8863 $W/round1 >> chain.log 2>&1; step "PAGE UP"
RO20_CTX=lt nice -n 10 python3 recipe/round1.py context > context.log 2>&1 || step "CONTEXT FAILED"; step "CONTEXT DONE"
python3 recipe/page20.py >> chain.log 2>&1; python3 "$RS" 8863 $W/round1 >> chain.log 2>&1; step "CHAIN COMPLETE"
