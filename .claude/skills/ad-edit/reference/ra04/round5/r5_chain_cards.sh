#!/bin/bash
# RA-04 round 5: the gen plates (both aspects), the gen and lock cards.
cd /Volumes/Extreme/_edit_work/ra04
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('RA-04 r5 cards')"
echo "SLOT $(date +%T)"
python3 round5/r5_cards.py > logs/r5_cards.log 2>&1 || { echo "R5_CARDS_FAILED"; tail -20 logs/r5_cards.log; exit 3; }
tail -6 logs/r5_cards.log
echo "R5_CARDS_CHAIN_COMPLETE $(date +%T)"
