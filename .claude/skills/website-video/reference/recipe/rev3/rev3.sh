#!/bin/zsh
# REV 3 chain (2026-09-02). tight.py re-renders the 4K tight cut with the manual cut (the repeated
# line at 0:32) while the graphics whose geometry or length changed rebuild beside it -- the six
# lower thirds (moved to the bottom, gfx.py LT_BOTTOM), the before/today cards (new beats) and the
# phone PiP. Then: hard splices -> head track -> head-anchored plan -> every MOV probed against its
# beat (lesson 95) -> punch -> mix -> the APPROVED rev-2 audio chain, untouched -> captions -> gates.
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
echo "== tight (4K, manual cut) + graphics in parallel  $(date +%H:%M:%S)"
RENDER=1 python3 tight.py > logs/tight_r3.log 2>&1 &
P_T=$!
( FORCE=1 python3 gfx.py name num1 flyblind > logs/gfx_r3a.log 2>&1 ) &
P_A=$!
( FORCE=1 python3 gfx.py num2 num3 cancel > logs/gfx_r3b.log 2>&1 ) &
P_B=$!
( FORCE=1 python3 gfx2.py before today > logs/gfx2_r3.log 2>&1 && python3 layout.py pip > logs/pip_r3.log 2>&1 ) &
P_C=$!
for p in $P_T $P_A $P_B $P_C; do
  if ! wait $p; then echo "background job pid $p FAILED"; tail -3 logs/tight_r3.log logs/gfx_r3a.log logs/gfx_r3b.log logs/gfx2_r3.log logs/pip_r3.log; exit 1; fi
done
echo "tight + graphics done  $(date +%H:%M:%S)"; tail -2 logs/tight_r3.log
echo "== hard splices"; python3 hard_splices.py tight.mov tight_cuts.json hard_splices.json
echo "== headtrack"; python3 headtrack.py | tail -2
echo "== plan"; python3 layout.py plan
echo "== every MOV vs its beat (lesson 95)"
python3 - <<'PY'
import subprocess, layout as L
FFP="/Volumes/Extreme/_edit_work/bin/ffprobe"; bad=[]
for n,(a,b) in L.GFX:
    d=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",f"gfx/{n}.mov"],capture_output=True,text=True).stdout)
    ok=abs(d-(b-a))<0.1; print(f"  {n:10s} mov {d:6.2f}  beat {b-a:6.2f}  {'OK' if ok else 'MISMATCH'}")
    if not ok: bad.append(n)
assert not bad, f"MOV length != beat: {bad}"
PY
echo "== punch  $(date +%H:%M:%S)"; python3 layout.py punch
echo "== mix    $(date +%H:%M:%S)"; python3 layout.py mix
echo "== audio (rev-2 approved chain, unchanged)  $(date +%H:%M:%S)"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== captions  $(date +%H:%M:%S)"; python3 captions.py
echo "== gates  $(date +%H:%M:%S)"; ./deliver.sh
echo "REV3 DONE  $(date +%H:%M:%S)"
