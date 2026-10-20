#!/bin/zsh
# SL-06 round 5: render the six shorts one at a time, each waiting for a build slot (buildcap, cap 2 across sessions)
cd /Volumes/Extreme/_edit_work/sl06
for S in "$@"; do
  python3 -c "import sys; sys.path.insert(0,'/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared'); import buildcap; buildcap.wait('sl06 render $S')"
  echo "START $S $(date +%T)"
  nice -n 5 python3 batch.py render $S > r5log/render_$S.log 2>&1 && echo "DONE $S $(date +%T)" || echo "FAIL $S $(date +%T)"
done
echo "ALL DONE"
