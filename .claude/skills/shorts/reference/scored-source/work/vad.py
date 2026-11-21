#!/usr/bin/env python3
"""Voice-activity map for a SCORED source.

silencedetect measures the whole mix. Muhammad's cut runs a music bed the whole way, and
the bed swells: the pause at 43.54-43.98 measures -16 dB, LOUDER than the speech before it,
while a real speech gap elsewhere reads -33 dB. So "quiet in the mix" is not "no speech
here", and a silence-based snap either refuses every cut or lands one on a music swell.

Ground truth used instead: energy in the speech band (300-7000 Hz) relative to a rolling
local floor. The bed on this cut is bass-tilted, so band-limiting alone buys ~10 dB, and
the local floor absorbs the swells.
"""
import json, sys
import numpy as np, wave

src = sys.argv[1]; out = sys.argv[2]
w = wave.open(src); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.
w.close()

HOP = int(0.010 * sr); NFFT = 1024
n = (len(a) - NFFT) // HOP
win = np.hanning(NFFT)
idx = np.arange(NFFT)[None, :] + (np.arange(n) * HOP)[:, None]
S = np.abs(np.fft.rfft(a[idx] * win, axis=1))
freqs = np.fft.rfftfreq(NFFT, 1 / sr)
band = (freqs >= 300) & (freqs <= 7000)
e = 20 * np.log10(np.maximum(1e-9, np.sqrt((S[:, band] ** 2).mean(1))))

# rolling 4 s 15th-percentile floor, then speech = 8 dB over the local floor
Wf = int(4.0 / 0.010)
pad = np.pad(e, (Wf // 2, Wf // 2), mode='edge')
floor = np.array([np.percentile(pad[i:i + Wf], 15) for i in range(0, len(e), 5)])
floor = np.repeat(floor, 5)[:len(e)]
speech = e > floor + 8.0

# close 60 ms holes inside a word, then drop bursts under 80 ms
def close(m, k):
    m = m.copy()
    off = np.where(~m)[0]
    if len(off):
        runs = np.split(off, np.where(np.diff(off) != 1)[0] + 1)
        for r in runs:
            if len(r) <= k and r[0] > 0 and r[-1] < len(m) - 1: m[r] = True
    return m
def prune(m, k):
    m = m.copy()
    on = np.where(m)[0]
    if len(on):
        for r in np.split(on, np.where(np.diff(on) != 1)[0] + 1):
            if len(r) < k: m[r] = False
    return m
speech = prune(close(speech, 6), 8)

gaps = []
off = np.where(~speech)[0]
if len(off):
    for r in np.split(off, np.where(np.diff(off) != 1)[0] + 1):
        g0, g1 = r[0] * 0.010, (r[-1] + 1) * 0.010
        if g1 - g0 >= 0.08: gaps.append([round(g0, 3), round(g1, 3)])
json.dump(gaps, open(out, 'w'))
print(f'{len(gaps)} speech gaps >= 80 ms over {len(e)*0.010:.1f}s')
