#!/usr/bin/env python3
"""SL-18: the motion gate (clipcheck.py) on each AI clip's used range (source frames), one at a time, in the render queue."""
import subprocess, sys
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"DESK": "0:111", "DATEA": "0:110", "A0061": "28:124", "A0085": "13:63", "A0089a": "59:178", "A0089b": "179:238", "A0089c": "239:319"}
for k, fr in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    r = subprocess.run([sys.executable, CC, f"clips/{k.rstrip('abc') if k.startswith('A0089') else k}.mp4", "--spec", f"clips/specs/{k.rstrip('abc') if k.startswith('A0089') else k}.spec.json", "--frames", fr, "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-3000:] + r.stderr[-800:], flush=True)
