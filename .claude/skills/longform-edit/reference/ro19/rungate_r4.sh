#!/bin/zsh
# RO-19 round 4: the delivery gate, launched from a script FILE. A launching shell whose own command line holds the gate command is counted as a running build
# by wait_for_build_slot (_shared/rolls/roll_sidecar.py active_builds), and the gate then waits for itself forever (74 minutes at 0 % CPU on 2026-10-13).
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
export PATH="$P/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ro19/round4/film
G="$P/.claude/skills/_shared/deliver/gate.py"
nice -n 5 python3 "$G" "RO-19 round 4 - full film.mp4" --format longform --plan plan.json > logs/gate.log 2>&1
echo "GATE EXIT $?"
