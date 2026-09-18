#!/usr/bin/env python3
"""D3 proof: the delivered mix's TAIL envelope, round 3 beside round 2.

The round-2 review measured a 5 ms envelope and found the bed fall to -56..-65 dBFS from 55.94 s
and step to -42 dBFS at 56.060 s (~15 dB inside 5 ms). This re-measures the same way, on the
DELIVERED files, and reports the largest 5 ms step and the largest 50 ms step in the tail.

  s48_tail.py [master_9x16.mp4 [round2/master_9x16.mp4]]
"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L

NEW = sys.argv[1] if len(sys.argv) > 1 else "master_9x16.mp4"
OLD = sys.argv[2] if len(sys.argv) > 2 else "round2/master_9x16.mp4"
SR = 48000
import os
T0 = float(os.environ.get("TAIL_T0", 55.40))   # AFTER the last word ends (55.22 s): the bed alone
T1 = float(os.environ.get("TAIL_T1", 57.19))   # the last frame
# ⚠ the window must start after the last word. A window that includes speech measures the gaps
# BETWEEN WORDS (60+ dB) and says nothing about the bed, which is what D3 is about.


def pcm(p):
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def env(x, step):
    h = int(step*SR); a, b = int(T0*SR), int(T1*SR)
    seg = x[a:b]
    n = len(seg)//h
    e = np.array([20*np.log10(np.sqrt(np.mean(seg[i*h:(i+1)*h]**2))+1e-12) for i in range(n)])
    t = T0 + (np.arange(n)+0.5)*step
    return t, e


rep = {}
for name, p in (("round3", NEW), ("round2", OLD)):
    if not os.path.exists(p):
        rep[name] = {"_missing": p}; continue
    x = pcm(p)
    r = {}
    for step, key in ((0.005, "step_5ms"), (0.050, "step_50ms")):
        t, e = env(x, step)
        d = np.diff(e)
        i = int(np.argmax(np.abs(d)))
        r[key] = dict(max_abs_step_db=round(float(abs(d[i])), 1),
                      at_s=round(float(t[i+1]), 3),
                      min_dbfs=round(float(e.min()), 1), max_dbfs=round(float(e.max()), 1),
                      span_db=round(float(e.max()-e.min()), 1))
        if step == 0.005:
            r["envelope_5ms_55.8_56.3"] = [(round(float(tt), 3), round(float(ee), 1))
                                           for tt, ee in zip(t, e) if 55.80 <= tt <= 56.30]
    rep[name] = r
    print(f"{name} {p}")
    for k in ("step_5ms", "step_50ms"):
        v = r[k]
        print(f"   {k}: largest |step| {v['max_abs_step_db']} dB at {v['at_s']} s; "
              f"tail envelope {v['min_dbfs']}..{v['max_dbfs']} dBFS (span {v['span_db']} dB)")
os.makedirs("r3", exist_ok=True)
json.dump(dict(window=[T0, T1], files={"round3": os.path.abspath(NEW), "round2": os.path.abspath(OLD)},
               **rep), open("r3/tail_envelope.json", "w"), indent=1)
print("-> r3/tail_envelope.json")
