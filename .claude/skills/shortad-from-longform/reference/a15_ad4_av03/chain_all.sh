#!/bin/zsh
# AV-03 + AS-02: the four pictures, one render at a time, each waiting for a free slot (two-build cap).
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/AV-03
step() { echo "== $1 $(date +%H:%M:%S)"; }
./wait_slot.sh > logs/wait_r1.log 2>&1
step "vertical master"; nice -n 5 python3 render9.py --out picture.mp4 > logs/render_v.log 2>&1 || { echo "RENDER V FAILED"; tail -5 logs/render_v.log; exit 1; }
python3 zmux.py picture.mp4 ad4_9x16.mp4 > logs/mux_v.log 2>&1 || { echo "MUX V FAILED"; tail -5 logs/mux_v.log; exit 1; }; tail -2 logs/mux_v.log
step "vertical cutdown"; python3 zcut_build.py > logs/zcut_build_v.log 2>&1 || { echo "CUT BUILD V FAILED"; tail -5 logs/zcut_build_v.log; exit 1; }
./wait_slot.sh > logs/wait_r2.log 2>&1
nice -n 5 python3 render9.py --cutplan cut_plan.json --out cut/picture.mp4 > logs/render_vc.log 2>&1 || { echo "RENDER VC FAILED"; tail -5 logs/render_vc.log; exit 1; }
(cd cut && python3 ../zmux.py picture.mp4 ad4_9x16_59s.mp4 his_mix.wav > logs/mux.log 2>&1) || { echo "MUX VC FAILED"; tail -5 cut/logs/mux.log; exit 1; }; tail -1 cut/logs/mux.log
./wait_slot.sh > logs/wait_r3.log 2>&1
step "square master"; nice -n 5 python3 render9.py --aspect 1x1 --out picture_sq.mp4 > logs/render_s.log 2>&1 || { echo "RENDER S FAILED"; tail -5 logs/render_s.log; exit 1; }
python3 zmux.py picture_sq.mp4 ad4_1x1.mp4 > logs/mux_s.log 2>&1 || { echo "MUX S FAILED"; tail -5 logs/mux_s.log; exit 1; }; tail -2 logs/mux_s.log
step "square cutdown"; python3 zcut_build.py --sq > logs/zcut_build_s.log 2>&1 || { echo "CUT BUILD S FAILED"; tail -5 logs/zcut_build_s.log; exit 1; }
./wait_slot.sh > logs/wait_r4.log 2>&1
nice -n 5 python3 render9.py --aspect 1x1 --cutplan cut_plan.json --out cut_sq/picture.mp4 > logs/render_sc.log 2>&1 || { echo "RENDER SC FAILED"; tail -5 logs/render_sc.log; exit 1; }
(cd cut_sq && python3 ../zmux.py picture.mp4 ad4_1x1_59s.mp4 his_mix.wav > logs/mux.log 2>&1) || { echo "MUX SC FAILED"; tail -5 cut_sq/logs/mux.log; exit 1; }; tail -1 cut_sq/logs/mux.log
step "ALL FOUR RENDERED"
