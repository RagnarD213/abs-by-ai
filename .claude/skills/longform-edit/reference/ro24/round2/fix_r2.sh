#!/bin/bash
set -uo pipefail
W=/Volumes/Expansion/_edit_work/RO-24/round2; R=$W/recipe; FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
cd $R
python3 $R/compare_r2.py 9.6 15.0 "$W/review/key/compare-wide-0m10.mp4" --zoom
python3 $R/compare_r2.py 57.8 62.9 "$W/review/key/compare-hands-0m58.mp4" --zoom
for f in compare-wide-0m10 compare-hands-0m58; do "$FF" -v error -y -ss 1.0 -i "$W/review/key/$f.mp4" -frames:v 1 -q:v 3 "$W/review/key/$f.jpg"; done
python3 $R/ctx_r2.py --only P6,G09,G10,P7,G11,G12,G13,G14
python3 $R/page_r2.py
echo "FIX R2 DONE"
