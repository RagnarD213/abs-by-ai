#!/usr/bin/env python3
"""Rebuild V4[371.35, 451.65) with a cleared bed and the intro line at V4's own timing.

Why this shape:
  * Content ID's claim, the hash fingerprint and the 20-120 Hz signature all agree the
    claimed track occupies exactly V4 371.3 - 451.65 s. Nothing outside is touched.
  * The only speech inside is one line. Its onset in V4 measures 373.540 s (raw 373.500,
    so V4 = raw + 0.040), from a 1 ms cross-correlation of the music-free raw against V4
    that peaks at r=0.9926 and falls to 0.60 by +-30 ms.
  * The outro line sits AFTER the track stops, so it is left exactly as V4 recorded it.
"""
import numpy as np, wave, struct, sys

SR      = 44100
R_IN    = 371.28      # region start in V4 (Dan's speech ends 371.23; first 808 at 371.74)
R_OUT   = 451.64      # region end in V4 (outro line starts 451.662, measured)
V_AT    = 373.34      # where the voice clip's t=0 lands in V4 (raw 373.30 + 0.040)
FADE_IN = 0.15        # bed fade in from R_IN
FADE_OUT= 0.25        # bed fade out ending at R_OUT
BED_DB  = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0

DUCK, PRE, POST, RAMP_DN, RAMP_UP, GATE_DB = 0.30, 0.35, 0.45, 0.25, 0.55, -50.0

def rd(p):
    w = wave.open(p, 'rb'); assert w.getframerate() == SR
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.
    return a.reshape(-1, w.getnchannels())

n     = int(round((R_OUT - R_IN) * SR))
bed   = rd("wav/bed_slice.wav")[:n] * (10 ** (BED_DB / 20.0))
voice = rd("wav/voice_clip.wav")[:, 0]
v0    = int(round((V_AT - R_IN) * SR))
vtrack = np.zeros(n)
vtrack[v0:v0 + len(voice)] = voice

# --- duck the bed under speech (explicit gain, not sidechaincompress: the compressor
#     only reached 68% on short5 and Dan heard it) -----------------------------------
step = int(SR * 0.01); spans = []; cur = None
for i in range(len(vtrack) // step):
    s = vtrack[i*step:(i+1)*step]
    loud = 20*np.log10(np.sqrt(np.mean(s**2)) + 1e-12) > GATE_DB
    t = i * 0.01
    if loud and cur is None: cur = [t, t]
    elif loud: cur[1] = t
    elif cur is not None:
        if cur[1]-cur[0] > 0.10: spans.append(cur)
        cur = None
if cur: spans.append(cur)
merged = []
for s in spans:
    if merged and s[0]-merged[-1][1] < 0.8: merged[-1][1] = s[1]
    else: merged.append(list(s))
g = np.ones(n)
for s, e in merged:
    ia, ib = int(max(0.0, s-PRE)*SR), int(min(n/SR, e+POST)*SR)
    g[ia:ib] = DUCK
    r = int(RAMP_DN*SR); i0 = max(0, ia-r)
    g[i0:ia] = np.minimum(g[i0:ia], np.cos(np.linspace(0, np.pi/2, ia-i0))**2*(1-DUCK)+DUCK)
    r2 = int(RAMP_UP*SR); i1 = min(n, ib+r2)
    g[ib:i1] = np.minimum(g[ib:i1], np.sin(np.linspace(0, np.pi/2, i1-ib))**2*(1-DUCK)+DUCK)
bed *= g[:, None]

# --- bed fades at the region edges -------------------------------------------------
fi = int(FADE_IN*SR);  bed[:fi]  *= np.linspace(0, 1, fi)[:, None]
fo = int(FADE_OUT*SR); bed[-fo:] *= np.linspace(1, 0, fo)[:, None]

out = bed + vtrack[:, None]
for lbl, s, e in [("speech span", merged[0][0], merged[0][1])]:
    print(f"  {lbl}: {s:.2f} - {e:.2f}s region-local  (V4 {R_IN+s:.2f} - {R_IN+e:.2f})")
print(f"  ducked {(g<0.999).sum()/SR:.2f}s of {n/SR:.2f}s at {DUCK:.2f} ({20*np.log10(DUCK):+.1f} dB)")
print(f"  bed gain {BED_DB:+.2f} dB   region peak {20*np.log10(np.abs(out).max()):+.2f} dBFS")
data = out.astype(np.float32).tobytes()
hdr = (b'RIFF' + struct.pack('<I', 36+len(data)) + b'WAVEfmt ' +
       struct.pack('<IHHIIHH', 16, 3, 2, SR, SR*8, 8, 32) + b'data' + struct.pack('<I', len(data)))
open("wav/region_new.wav", 'wb').write(hdr + data)
print(f"  wrote wav/region_new.wav  {n/SR:.6f}s")
