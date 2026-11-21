#!/bin/bash
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
set -x
python3 r2_s83b_clips.py D1 > round2/logs/s83b_d1.log 2>&1 || exit 10
python3 r2_s86_assemble.py work > round2/logs/s86w.log 2>&1 || exit 13
python3 r2_s86_assemble.py cuts > round2/logs/s86c.log 2>&1 || exit 15
echo "R2_FIX_COMPLETE $(date +%T)"
