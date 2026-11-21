#!/usr/bin/env python3
"""Clipped-word adjudicator with its OWN control set.

A word-presence miss in a joint re-transcription is not evidence on its own —
Whisper re-spells the last word of a phrase when the phrase that follows changed
("proteins"->"protein"). The decisive measurement is the energy envelope of the
audio LEADING INTO the joint, compared against the same audio in the SOURCE, and
scored against joints INHERITED from the approved v3 edit in the SAME file
(same encoder, same loudnorm, same 30 ms render.py fade).
Usage: python3 tailtest.py cons|sub30 <out_time> [...]"""
import json, subprocess, wave, struct, math, random, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRCWAV = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/"
              "Media/longform-raw/absbyai-0803-shoot/invest-health/C1511.wav")
V = sys.argv[1]
NAME = "INVEST_HEALTH_conservative" if V == "cons" else "INVEST_HEALTH_sub30"
VID = HERE / V / "out" / f"{NAME}.mp4"
edl = json.load(open(HERE / V / "edl.json"))["ranges"]
new = {j["i"] for j in json.load(open(HERE / V / "new_joints.json"))["joints"]}
offs, acc = [], 0.0
for r in edl:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)
def env(src, a, dur, step=0.010):
    p = Path("/tmp/_tt.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(src),
                    "-t", f"{dur:.3f}", "-vn", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(p)], check=True)
    w = wave.open(str(p)); n = w.getnframes()
    sm = struct.unpack(f"<{n}h", w.readframes(n)); w.close()
    st = int(step * 48000)
    return [20*math.log10((sum(x*x for x in sm[i:i+st])/st)**0.5/32768 + 1e-9)
            for i in range(0, n - st, st)]
def demean(v):
    m = sum(v)/len(v); return [x-m for x in v]
def score(src_out, out_t):
    """min dB deviation of the render's last 150 ms from the source's, after
    cross-correlating away the render's accumulated frame-rounding drift."""
    S = demean(env(SRCWAV, src_out - 1.60, 1.60))
    R = demean(env(VID, max(0, out_t - 4.2), 6.8))
    best, lag0 = None, 0
    for lag in range(0, len(R) - len(S)):
        c = sum(a*b for a, b in zip(S, R[lag:lag+len(S)]))
        if best is None or c > best: best, lag0 = c, lag
    return min(r - s for r, s in zip(R[lag0+len(S)-15:lag0+len(S)], S[-15:]))
inherited = [i for i in range(len(edl)-1) if (i+1) not in new]
random.seed(5)
ctrl = sorted(score(edl[i]["end"], offs[i+1]) for i in random.sample(inherited, 10))
floor = ctrl[0]
print(f"control (v3-approved joints in this same file, n=10): "
      f"{ctrl[0]:+.1f} .. {ctrl[-1]:+.1f} dB, median {ctrl[len(ctrl)//2]:+.1f}")
for arg in sys.argv[2:]:
    t = float(arg)
    i = min(range(len(offs)), key=lambda k: abs(offs[k] - t))
    s = score(edl[i-1]["end"], offs[i])
    verdict = "CLIPPED" if s < floor - 3 else "INTACT (Whisper re-spelling)"
    print(f"  joint @ {t:8.1f}s  {edl[i-1]['beat'][:24]:26s} min dev {s:+6.1f} dB  -> {verdict}")
