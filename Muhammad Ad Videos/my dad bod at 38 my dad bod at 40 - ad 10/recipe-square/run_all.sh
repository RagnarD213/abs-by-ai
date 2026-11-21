#!/bin/zsh
# round 2 rebuild: full picture -> camcheck -> mux/gates ; cut picture -> mux/gates (two builds at once)
D0=$HOME/abs-review/as06-ad10/recipe-square
source $D0/env.sh
cd $Q
( python3 "$KL/sq_render_ad10.py" picture --build $B --out $Q > run_pic_full6.log 2>&1; (cd $B && python3 camcheck.py $Q/picture.mp4 1080 1080 6 > $Q/camcheck_full.log 2>&1); $D0/run_sq_full.sh > run_chain6.log 2>&1 ) &
( python3 "$KL/sq_render_ad10.py" picture --cut --build $B --out $Q > run_pic_cut6.log 2>&1; SKIP_PIC=1 $D0/run_sq_cut.sh > run_chain6c.log 2>&1 ) &
wait
echo ALL DONE
