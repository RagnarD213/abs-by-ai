#!/usr/bin/env python3
"""RA-01 audio: the tight cut of the lav, then the ONE shared voice chain, then the bed.

`_shared/audio` is the standard: pick_lav decided the pull per file (dual-mono -> mid), the cut is
made on that pulled signal, and voice_chain.py is the only chain. Nothing here processes audio
itself. The end hold is silence padded after the last word.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
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
# RA-06: a +3 dB ride on "Then get a personalized workout and nutrition plan to make your abs real" (tight 37.12-41.42 s),
# which sits 3.5-4.5 dB under the lines around it (reviewer round 1, item 12). Re-audit: "make your abs real" alone is ~5 dB low
# (he trails off), so it gets +7.5 dB in total. ROUND 3: "and replaced them with AI." measured 5 dB under its sentence (review M5): +3.5 dB; (measured -17.1 LUFS after +5.5, against -14.6 and -12.7 either side); "An AI trainer can design..." +2 dB. 80 ms ramps.
for t0, t1, db in [tuple(float(v) for v in r.split(":")) for r in os.environ.get("RIDE", "22.40:23.85:3.5,23.95:27.48:2.0,37.12:41.42:2.5,39.98:41.42:5.0").split(",") if r]:
    g = np.ones(len(x), np.float32); a0, a1 = int(t0*SR), int(t1*SR); rmp = int(0.08*SR); k = 10**(db/20)
    g[a0:a1] = k; g[a0:a0+rmp] = np.linspace(1, k, rmp); g[a1-rmp:a1] = np.linspace(k, 1, rmp); x = x*g
wv = wave.open("cut_audio.wav", "w"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes()); wv.close()
print(f"cut_audio.wav  {len(x)/SR:.3f}s  ({len(CUT['pieces'])} pieces, {XF/SR*1000:.0f} ms crossfades)")

BED = os.environ.get("BED", "/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3")
BEDDB = os.environ.get("BED_DB", "-32")
OUT = os.environ.get("OUT", "mix.wav")
cmd = [sys.executable, f"{SH}/voice_chain.py", "--in", "cut_audio.wav", "--out", OUT,
       "--bed", BED, "--bed-db", BEDDB, "--work", "audiowork" + ("" if OUT == "mix.wav" else "_" + OUT[:-4])]
# RA-06: this roll's fitted tone is RA-05's (same roll, same lav, minutes apart); EQ= adds Dan's bass lift
# (RA-14 round 3: "Let's do the voice with a bass lift"; VIDEO-RULES 2026-10-12, +3 dB at 120 Hz)
if os.environ.get("EQ"):
    cmd += ["--eq", os.environ["EQ"]]
# ⚠ LOCK THE MIX TO THE PICTURE. The end hold is frame-snapped in the plan, so the picture is a
# frame or two longer than dur + END_HOLD; the chain's own --frame-lock makes the mix exactly the
# picture's length (bed and all) instead of leaving the audio short, which is what failed the audio
# gate's `length` row. This is the module's flag, not a hand-rolled pad.
LOCK = os.environ.get("LOCK")
if LOCK:
    cmd += ["--frame-lock", LOCK]
print(" ".join(cmd))
subprocess.run(cmd, check=True)
print(OUT, "written")
