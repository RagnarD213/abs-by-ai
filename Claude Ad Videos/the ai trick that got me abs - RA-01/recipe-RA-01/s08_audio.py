#!/usr/bin/env python3
"""RA-01 audio: the tight cut of the lav, then the ONE shared voice chain, then the bed.

`_shared/audio` is the standard: pick_lav decided the pull per file (dual-mono -> mid), the cut is
made on that pulled signal, and voice_chain.py is the only chain. Nothing here processes audio
itself. The end hold is silence padded after the last word.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
CUT = json.load(open("cut.json"))
END_HOLD = L.END_HOLD          # one place (ra01lib)
SR = 48000

w = wave.open("lav.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768.0
XF = int(0.006*SR)                       # 6 ms equal-power crossfade at each splice: no click
out = []
for i, p in enumerate(CUT["pieces"]):
    s0, s1 = int(round(p["src_in"]*SR)), int(round(p["src_out"]*SR))
    seg = a[s0:s1].copy()
    if i and len(seg) > XF and len(out[-1]) > XF:
        r = np.linspace(0, 1, XF)
        prev = out[-1]
        prev[-XF:] = prev[-XF:]*np.cos(r*np.pi/2) + seg[:XF]*np.sin(r*np.pi/2)
        seg = seg[XF:]
    out.append(seg)
x = np.concatenate(out)
need = int(round((CUT["dur"]+END_HOLD)*SR))
if len(x) < need:
    x = np.concatenate([x, np.zeros(need-len(x), np.float32)])
x = x[:need]
wv = wave.open("cut_audio.wav", "w"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes()); wv.close()
print(f"cut_audio.wav  {len(x)/SR:.3f}s  ({len(CUT['pieces'])} pieces, {XF/SR*1000:.0f} ms crossfades)")

BED = os.environ.get("BED", "/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3")
BEDDB = os.environ.get("BED_DB", "-32")
cmd = [sys.executable, f"{SH}/voice_chain.py", "--in", "cut_audio.wav", "--out", "mix.wav",
       "--bed", BED, "--bed-db", BEDDB, "--work", "audiowork"]
# ⚠ LOCK THE MIX TO THE PICTURE. The end hold is frame-snapped in the plan, so the picture is a
# frame or two longer than dur + END_HOLD; the chain's own --frame-lock makes the mix exactly the
# picture's length (bed and all) instead of leaving the audio short, which is what failed the audio
# gate's `length` row. This is the module's flag, not a hand-rolled pad.
LOCK = os.environ.get("LOCK")
if LOCK:
    cmd += ["--frame-lock", LOCK]
print(" ".join(cmd))
subprocess.run(cmd, check=True)
print("mix.wav written")
