#!/bin/bash
# RO-21 round 1 colour options: the same two moments (wide on the floating cards, tight on the studio set) in each grade.
set -euo pipefail
cd /Volumes/Expansion/_edit_work/RO-21/recipe; O=/Volumes/Expansion/_edit_work/RO-21/round1/colour
python3 manifest_r1.py
for g in warm rich natural; do
  python3 assemble_r1.py $O/wide_$g.mp4 --g0 240 --g1 420 --grade $g --stills 330
  python3 assemble_r1.py $O/tight_$g.mp4 --g0 660 --g1 840 --grade $g --stills 750
done
echo COLOUR DONE
