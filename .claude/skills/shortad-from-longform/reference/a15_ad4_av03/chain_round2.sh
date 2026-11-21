#!/bin/zsh
# After the base is rebuilt on his picture frames: re-measure, re-crop, captions, then the four renders and their scans.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/AV-03
K="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16/kit_negscan.py"
step() { echo "== $1 $(date +%H:%M:%S)"; }
fail() { echo "$1 FAILED"; tail -6 $2; exit 1; }
# measure, crop, captions and labels were run at 15:55-16:10
rm -f ad4_9x16.mp4 ad4_9x16.mp4.* ad4_1x1.mp4 ad4_1x1.mp4.* cut/ad4_9x16_59s.mp4 cut/ad4_9x16_59s.mp4.* cut_sq/ad4_1x1_59s.mp4 cut_sq/ad4_1x1_59s.mp4.* plan.json plan_sq.json cut/plan.json cut_sq/plan.json logs/mux_v.log logs/mux_s.log
./chain_all.sh || exit 1
for a in 9x16 1x1; do ./gates9.sh $a; ./gates9.sh $a cut; done
rm -rf negscan negscan_v negscan_s cut/negscan cut_sq/negscan
python3 "$K" sheet --build . --video ad4_9x16.mp4 --n 30 | tail -1; mv negscan negscan_v
python3 "$K" sheet --build . --video ad4_1x1.mp4 --n 30 | tail -1; mv negscan negscan_s
python3 "$K" sheet --build cut --video ad4_9x16_59s.mp4 --n 30 | tail -1
python3 "$K" sheet --build cut_sq --video ad4_1x1_59s.mp4 --n 30 | tail -1
step "ROUND 3 FILES AND SCANS DONE"
