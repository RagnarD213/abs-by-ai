#!/usr/bin/env python3
"""round 3: the motion gate (clipcheck.py) on every AI clip's used range in the five shorts, one at a time, inside the build cap."""
import subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"A0083": "0:62", "A0159": "14:154", "AI_B1": "7:135", "AI_B2a": "2:52", "AI_B2b": "7:55", "AI_E3": "12:88", "AI_F2": "17:116", "AI_B1_fix": "7:135", "AI_B2b_full": "0:95", "AI_F2_r3": "2:102"}
for k, fr in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    buildcap.wait(f"SL-07 clipcheck {k}")
    kk = k.replace("_full", "").replace("_r3", ""); r = subprocess.run([sys.executable, CC, f"clips/{kk}.mp4", "--spec", f"clips/specs/{kk}.spec.json", "--frames", fr], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-2500:] + r.stderr[-800:], flush=True)
open("r3probe/clipcheck.done", "w").write("ok")
