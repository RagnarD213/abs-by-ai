#!/bin/zsh
set -e
export GATE_GROUP=DS-27
export PATH='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin:'$PATH
W='/Volumes/Expansion/_edit_work/DS-27/round1'
python3 "$W/recipe/graphics.py"
python3 "$W/recipe/render.py" Opening
python3 "$W/recipe/render.py" Equipment-context
python3 "$W/recipe/render.py" Daily-workouts-context
python3 "$W/recipe/qa.py" Opening
python3 "$W/recipe/qa.py" Equipment-context
python3 "$W/recipe/qa.py" Daily-workouts-context
printf 'PACKET_RENDER_AND_MEASURE_DONE\n'
