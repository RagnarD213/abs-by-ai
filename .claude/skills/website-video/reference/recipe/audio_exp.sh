#!/bin/zsh
# REV 6 audio experiment on a 150-s excerpt (keeps the gate's 20-120 s window): candidates -> gate rows (no stamp)
cd /Volumes/Extreme/_edit_work/website-video-828; export PATH=/Volumes/Extreme/_edit_work/bin:$PATH
mkdir -p audio/exp; SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
run() { # name env...
  n=$1; shift; echo "===== $n  $(date +%H:%M:%S)"
  env VIN=nocap.mov VOUT=audio/exp/$n.wav T_MAX=150 MUSIC_DB=-44 COMP=0 "$@" python3 audio4.py 2>&1 | grep -v "^  premix\|limiter delay"
  python3 - "$n" <<'PY'
import sys, io, contextlib
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
import audio_gate as G
buf=io.StringIO()
with contextlib.redirect_stdout(buf): r=G.gate(f"audio/exp/{sys.argv[1]}.wav", stamp=False)
for l in buf.getvalue().splitlines():
    if any(k in l for k in ("early decay","spread","voice-over-floor","tone:","words stop","loudness","true peak","comb","damage","VERDICT","PASS","FAIL")): print("   ",l.strip())
PY
}
run r5_baseline DEREVERB=0
run dr_ok DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45
run dr_ok_soft DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45 EXPAND="agate=threshold=0.009:ratio=1.5:range=0.5:attack=4:release=250:knee=6"
run dr_ok_noexp DEREVERB=1 DR_ALPHA=0.30 DR_D1=22 DR_D2=70 DR_FLOOR=-10 DR_SMOOTH=0.45 EXPAND=none
echo "AUDIO EXP DONE $(date +%H:%M:%S)"
