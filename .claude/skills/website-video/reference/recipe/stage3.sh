#!/bin/zsh
# REV 2 stage 3: num2 lower third was 0.15 s short of its rev-2 beat (built under rev 1's beat sheet)
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== num2 rebuild"; FORCE=1 python3 gfx.py num2
python3 - <<'PY'
import subprocess, beats as B
FFP="/Volumes/Extreme/_edit_work/bin/ffprobe"
for n in ("name","num1","flyblind","num2","num3","cancel"):
    d=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",f"gfx/{n}.mov"],capture_output=True,text=True).stdout)
    a,b=B.BEATS[n.upper()]; assert abs(d-(b-a))<0.1, (n,d,b-a); print(f"  {n} {d:.2f}s == beat {b-a:.2f}s")
PY
echo "== mix";   python3 layout.py mix
echo "== audio"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== captions"; python3 captions.py
echo "== gates"; ./deliver.sh
echo "STAGE3 DONE"
