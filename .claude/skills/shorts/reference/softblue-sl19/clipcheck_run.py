#!/usr/bin/env python3
"""SL-19: the motion gate (clipcheck.py) on each AI clip's used range (24 fps clip frames), with the film's own frame specs (RO-17 round3 aiframes/specs)."""
import subprocess, sys
CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
R = {"A3": "0:73", "A2": "0:127", "A10": "0:46"}      # A10: 0-2.46 s only (0:97 FAILED: the tin placed on the sofa back at f60-84, outside the crop; cut to the part before it)
for k, fr in R.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    r = subprocess.run([sys.executable, CC, f"clips/{k}.mp4", "--spec", f"clips/specs/{k}.spec.json", "--frames", fr, "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"== {k} {fr} exit {r.returncode}\n" + r.stdout[-3000:] + r.stderr[-800:], flush=True)
    v = subprocess.run([sys.executable, CC, f"clips/{k}.mp4", "--frames", fr, "--verify", "--out", "clips/clipcheck"], capture_output=True, text=True)
    print(f"   verify exit {v.returncode}: {v.stdout[-400:]}", flush=True)
