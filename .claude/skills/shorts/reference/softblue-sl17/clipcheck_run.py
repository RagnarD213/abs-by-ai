#!/usr/bin/env python3
"""SL-17: the motion gate (clipcheck.py) on each AI clip's used range, one at a time, inside the render queue."""
import subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"fork": ("Nutrition-B-approved-motion", "0:150")}     # short A uses clip t 0.00-5.00 (frames 0-149)
for k, (f, fr) in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    buildcap.wait(f"SL-17 clipcheck {k}")
    r = subprocess.run([sys.executable, CC, f"clips/{f}.mp4", "--spec", f"clips/specs/{k}.spec.json", "--frames", fr, "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-3000:] + r.stderr[-800:], flush=True)
