#!/usr/bin/env python3
"""SL-16: the motion gate (clipcheck.py) on each AI clip's used range, one at a time, inside the build cap."""
import subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"OT": "0:230", "A6": "38:120", "A5": "0:118", "A7": "14:122", "A0158": "0:75", "OTb": "94:230", "A7b": "14:70"}
for k, fr in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    buildcap.wait(f"SL-16 clipcheck {k}")
    kk = k.rstrip("b") if k in ("OTb", "A7b") else k; r = subprocess.run([sys.executable, CC, f"clips/{kk}.mp4", "--spec", f"clips/specs/{kk}.spec.json", "--frames", fr, "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-3000:] + r.stderr[-800:], flush=True)
