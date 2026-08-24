#!/usr/bin/env python3
"""Full-ad 5 ms RMS envelope of the LAV channel (right), measured off CUT_v2_graded.mp4.

env.json only covered the first 76 s (the 60 s sample span). Pause removal across the
whole ad needs the whole envelope. Right channel only -- see tight.py: the roll carries
two different microphones and the left one is the far mic.
"""
import json, subprocess
import numpy as np

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
BASE = "CUT_v2_graded.mp4"
SR   = 48000
HOP  = 0.005

raw = subprocess.run([FF, "-v", "error", "-i", BASE, "-map", "0:a",
                      "-af", "pan=mono|c0=c1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
h = int(HOP * SR)
n = len(a) // h
e = np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1) + 1e-12)
db = 20 * np.log10(e)
json.dump({"hop": HOP, "db": [round(float(x), 2) for x in db]}, open("env_full.json", "w"))
print(f"env_full.json  {n} frames  covers {n*HOP:.1f}s")
print(f"floor p05 {np.percentile(db,5):.1f} dB  p50 {np.percentile(db,50):.1f}  p95 {np.percentile(db,95):.1f}")
