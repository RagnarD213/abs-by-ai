#!/bin/zsh
# REV 4 chain (2026-09-08). Runs after punch #1 (layout.py punch on the base hair track) has finished:
#   refine the hair track on the delivered-scale picture -> plan -> punch #2 -> every MOV probed against its beat
#   (lesson 95) -> mix (graphics + the tagged AI inserts with alpha fades + both PiPs) -> the APPROVED rev-2 audio
#   chain, untouched -> captions -> the delivery gates (audio gate + stamp, qc incl. the hair gate, watch, review copy).
set -e
export PATH="/Volumes/Extreme/_edit_work/bin:$PATH"
cd /Volumes/Extreme/_edit_work/website-video-828
WAIT_PID=${1:-}
if [ -n "$WAIT_PID" ]; then
  echo "waiting for punch #1 (pid $WAIT_PID)  $(date +%H:%M:%S)"; n=0
  while kill -0 $WAIT_PID 2>/dev/null; do sleep 20; n=$((n+20)); if [ $n -gt 5400 ]; then echo "punch #1 did not finish in 90 min"; exit 1; fi; done
  grep -q "punched.mov done" logs/punch_r4a.log || { echo "punch #1 did not report done"; tail -5 logs/punch_r4a.log; exit 1; }
fi
if [ "${SKIP_REFINE:-0}" = "1" ]; then echo "== refine skipped (already stored in hairtrack.json for this cut)"; else
  echo "== refine (hair on the delivered-scale picture)  $(date +%H:%M:%S)"; python3 hairtrack_refine.py | tail -40; fi
echo "== plan  $(date +%H:%M:%S)"; python3 layout.py plan | head -4
echo "== punch #2  $(date +%H:%M:%S)"; python3 layout.py punch
echo "== inserts complete?"; grep -q "INSERTS COMPLETE" logs/inserts_r4.log || { echo "inserts not complete"; tail -5 logs/inserts_r4.log; exit 1; }
echo "== ai_d1 (the regenerated D1 clip)"; python3 build_inserts.py ai_d1
echo "== every MOV vs its beat (lesson 95)"
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
echo "== mix    $(date +%H:%M:%S)"; python3 layout.py mix
echo "== audio (rev-2 approved chain, unchanged)  $(date +%H:%M:%S)"; MUSIC_DB=-44 COMP=0 python3 audio3.py
echo "== captions  $(date +%H:%M:%S)"; python3 captions.py
echo "== gates  $(date +%H:%M:%S)"; ./deliver.sh
echo "REV4 DONE  $(date +%H:%M:%S)"
