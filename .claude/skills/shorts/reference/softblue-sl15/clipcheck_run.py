#!/usr/bin/env python3
"""SL-15: the motion gate (clipcheck.py) on each AI clip's used range, one at a time, inside the build cap."""
import subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"A4": "0:94", "A1": "7:108", "A1a": "7:49", "A1b": "150:186", "A4c": "0:85", "A1c": "146:182", "A1d": "0:26", "A1e": "5:26"}
for k, fr in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    buildcap.wait(f"SL-15 clipcheck {k}")
    kk = k[:2]; r = subprocess.run([sys.executable, CC, f"clips/{kk}.mp4", "--spec", f"clips/specs/{kk}.spec.json", "--frames", fr, "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-3000:] + r.stderr[-800:], flush=True)
