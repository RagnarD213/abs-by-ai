#!/bin/zsh
set -e
export GATE_GROUP=DS-27
W='/Volumes/Expansion/_edit_work/DS-27/round1'
python3 "$W/recipe/render.py" Daily-workouts-context
python3 "$W/recipe/qa.py" Daily-workouts-context
python3 "$W/recipe/review_assets.py"
printf 'R1_PACKET_FINAL\n'
