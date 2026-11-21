#!/bin/zsh
# website video: env -> tight -> plan -> gfx (4 workers) -> punch -> mix -> audio -> captions -> qc
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== env";   python3 env.py
echo "== tight"; python3 tight.py
echo "== beats"; python3 beats.py
echo "== plan";  python3 layout.py plan
echo "== gfx";
python3 gfx.py plates
python3 gfx.py name num1 flyblind num2 num3 cancel > logs/gfx_w1.log 2>&1 &
python3 gfx.py pool before today > logs/gfx_w2.log 2>&1 &
python3 gfx.py tellai trylist mealbul > logs/gfx_w3.log 2>&1 &
python3 gfx.py trial price solved cta > logs/gfx_w4.log 2>&1 &
wait
tail -n2 logs/gfx_w*.log
echo "== punch"; python3 layout.py punch
echo "== mix";   python3 layout.py mix
echo "== audio"; python3 audio.py
echo "== captions"; python3 captions.py
echo "PIPELINE DONE"
