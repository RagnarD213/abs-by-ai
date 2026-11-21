#!/usr/bin/env python3
"""RA-01 audio: the tight cut of the lav, then the ONE shared voice chain, then the bed.

`_shared/audio` is the standard: pick_lav decided the pull per file (dual-mono -> mid), the cut is
made on that pulled signal, and voice_chain.py is the only chain. Nothing here processes audio
itself. The end hold is silence padded after the last word.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra05/round2")
import ra01lib as L
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
CUT = json.load(open("cut.json"))
END_HOLD = L.END_HOLD          # one place (ra01lib)
SR = 48000

w = wave.open("lav.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768.0
XF = int(0.006*SR)                       # 6 ms equal-power crossfade at each splice: no click
# RA-05 ROUND 2: LENGTH-PRESERVING crossfade. Round 1 overlapped each piece's first 6 ms onto the previous piece's last 6 ms,
# so every splice shortened the talk by 6 ms (17 splices: 0.10 s), and the voice ran ahead of his lips by up to that much
# at the end. Now each join borrows 3 ms either side of the cut point, so the audio is exactly as long as the pieces.
H2 = XF//2
x = np.zeros(int(round(sum(p["src_out"]-p["src_in"] for p in CUT["pieces"])*SR)) + XF, np.float32)
pos = 0
r = np.linspace(0, 1, XF, dtype=np.float32); fin, fout = np.sin(r*np.pi/2), np.cos(r*np.pi/2)
n_p = len(CUT["pieces"])
for i, p in enumerate(CUT["pieces"]):
    s0, s1 = int(round(p["src_in"]*SR)), int(round(p["src_out"]*SR))
    a0 = s0 - (H2 if i else 0); a1 = s1 + (H2 if i < n_p-1 else 0)
    seg = a[a0:a1].copy()
    if i: seg[:XF] *= fin
    if i < n_p-1: seg[-XF:] *= fout
    st = pos - (H2 if i else 0)
    x[st:st+len(seg)] += seg
    pos += s1 - s0
x = x[:pos]
out = [x]
x = np.concatenate(out)
# RA-05 ROUND 2: THE SPEED-UP. The talk is cut at normal speed above, then played at L.SPEED with ffmpeg atempo (pitch kept),
# BEFORE the voice chain; the music bed is not sped (the chain lays it under the finished voice). The end hold is appended
# afterwards at normal length.
SP = float(os.environ.get("SPEED_OVERRIDE") or CUT.get("speed") or 1.0)
if SP != 1.0:
    import tempfile
    td = tempfile.mkdtemp(prefix="ra05sp_")
    wi = wave.open(f"{td}/in.wav", "w"); wi.setnchannels(1); wi.setsampwidth(2); wi.setframerate(SR)
    wi.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes()); wi.close()
    STRETCH = os.environ.get("STRETCH", "rb")
    if STRETCH == "atempo":
        subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", f"{td}/in.wav", "-af", f"atempo={SP}",
                        "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", f"{td}/sp.wav"], check=True)
    else:   # Rubber Band R3, pitch + formants kept (rb_stretch.py; "rbsmooth" = smooth transients, long window)
        subprocess.run([os.path.expanduser("~/.cache/absbyai/rbvenv/bin/python"), "rb_stretch.py", f"{td}/in.wav",
                        f"{td}/sp.wav", str(SP)] + (["smooth"] if STRETCH == "rbsmooth" else []), check=True)
    print("stretch:", STRETCH)
    ws = wave.open(f"{td}/sp.wav"); x = np.frombuffer(ws.readframes(ws.getnframes()), np.int16).astype(np.float32)/32768.0
    print(f"atempo {SP}: {len(out) and sum(len(o) for o in out)/SR:.3f}s -> {len(x)/SR:.3f}s (film talk {CUT['dur']:.3f}s)")
need = int(round((CUT["dur"]+END_HOLD)*SR))
if len(x) < need:
    x = np.concatenate([x, np.zeros(need-len(x), np.float32)])
x = x[:need]
CA = os.environ.get("CUTWAV", "cut_audio.wav")
wv = wave.open(CA, "w"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes()); wv.close()
print(f"cut_audio.wav  {len(x)/SR:.3f}s  ({len(CUT['pieces'])} pieces, {XF/SR*1000:.0f} ms crossfades)")

BED = os.environ.get("BED", "/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3")
BEDDB = os.environ.get("BED_DB", "-32")
cmd = [sys.executable, f"{SH}/voice_chain.py", "--in", CA, "--out", "mix.wav",
       "--bed", BED, "--bed-db", BEDDB, "--work", os.environ.get("WORK", "audiowork")]
# RA-05 ROUND 2: the voice WITH THE BASS LIFT (Dan's RA-14 pick, applied here): round 1's fitted tone for this roll plus a
# wide +3 dB at 120 Hz (RA-04's mixB method, VIDEO-RULES 2026-10-12). EQ env = the full chain to use instead of fitting.
if os.environ.get("EQ"):
    cmd += ["--eq", os.environ["EQ"]]
OUTW = os.environ.get("OUTW")
if OUTW:
    cmd[cmd.index("mix.wav")] = OUTW
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
