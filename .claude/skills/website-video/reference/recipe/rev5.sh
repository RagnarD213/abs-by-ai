#!/bin/zsh
# REV 5 chain (2026-09-08) -- Dan's rev-4 review: two Veo clip-tail artifacts trimmed away and the goal-image card
# removed. The framing is APPROVED and LOCKED, so punched.mov is REUSED as is (proved frame-by-frame: the only 29
# frames whose crop differs sit under the opaque ai_d3 insert). Chain: MOV-vs-beat check -> mix -> the approved
# rev-2 audio chain, unchanged -> captions -> the delivery gates.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== 0 every MOV vs its beat (lesson 95)  $(date +%H:%M:%S)"
python3 - <<'PY'
import subprocess, os, layout as L
FFP="/Volumes/Extreme/_edit_work/bin/ffprobe"; bad=[]
items=[(n,b) for n,b in L.GFX]+[(n,b) for n,b,_,_ in L.AIV]
for n,(a,b) in items:
    d=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",f"gfx/{n}.mov"],capture_output=True,text=True).stdout)
    need=b-a; ok=(abs(d-need)<0.1) or (n.startswith("ai_") and 0<=d-need<=0.2)
    print(f"  {n:10s} mov {d:6.2f}  beat {need:6.2f}  {'OK' if ok else 'MISMATCH'}")
    if not ok: bad.append(n)
assert not bad, f"MOV length != beat: {bad}"
PY
echo "== 1 mix  $(date +%H:%M:%S)"; python3 layout.py mix
echo "== 2 audio (rev-2 approved chain, unchanged)  $(date +%H:%M:%S)"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== 3 captions  $(date +%H:%M:%S)"; python3 captions.py
echo "== 4 gates  $(date +%H:%M:%S)"; ./deliver.sh
echo "REV5 DONE  $(date +%H:%M:%S)"
