#!/bin/bash
# RO-21 key calibration: plate over a long stretch, then two 3 s excerpts at fast-hand moments, check renders + measures.
set -euo pipefail
cd /Volumes/Expansion/_edit_work/RO-21/recipe/key
python3 plate16.py 3000 7000 plate
export MIN_FRAMES=60
./run_key.sh CAL1 4180 100
./run_key.sh CAL2 8980 100
for n in CAL1 CAL2; do
  python3 render16.py /Volumes/Expansion/_edit_work/RO-21/key/$n.mkv 0 100 /Volumes/Expansion/_edit_work/RO-21/key/$n pale,navy,pink
done
python3 measure16.py "/Volumes/Expansion/_edit_work/RO-21/key/CAL1 pale.mp4" "/Volumes/Expansion/_edit_work/RO-21/key/CAL1 navy.mp4" /Volumes/Expansion/_edit_work/RO-21/key/CAL1_measure.json 4180 100 || true
python3 mcflicker16.py "/Volumes/Expansion/_edit_work/RO-21/key/CAL1 pale.mp4" /Volumes/Expansion/_edit_work/RO-21/key/CAL1_mcflicker.json 4180 100 || true
python3 measure16.py "/Volumes/Expansion/_edit_work/RO-21/key/CAL2 pale.mp4" "/Volumes/Expansion/_edit_work/RO-21/key/CAL2 navy.mp4" /Volumes/Expansion/_edit_work/RO-21/key/CAL2_measure.json 8980 100 || true
python3 mcflicker16.py "/Volumes/Expansion/_edit_work/RO-21/key/CAL2 pale.mp4" /Volumes/Expansion/_edit_work/RO-21/key/CAL2_mcflicker.json 8980 100 || true
echo CAL CHAIN DONE
