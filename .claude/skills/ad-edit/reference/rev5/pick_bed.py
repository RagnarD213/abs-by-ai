#!/usr/bin/env python3
"""Choose the music bed by MEASUREMENT, not by taste (the /ad-edit rule).

Two criteria, both scored against Muhammad's own bed rather than an abstract ideal:

  1. SPECTRAL SHAPE -- his bed, sampled in a speech gap, is strongly bass-weighted and
     nearly absent in the 1-8 kHz band where the voice lives. A bed with midrange energy
     fights the dialogue and is exactly what makes a mix sound amateur.
  2. FLATNESS -- energy must not swing over the 236 s it has to cover, or the sidechain
     pumps and the bed draws attention to itself.
"""
import subprocess, glob
import numpy as np

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
SR = 44100
BANDS = [(60, 150), (150, 400), (400, 1000), (1000, 3000), (3000, 8000)]
# measured off Muhammad's mix in its quietest 1 s window (relative dB, band means)
HIS = np.array([26.3, 25.0, 14.8, 11.5, 3.3])
HIS = HIS - HIS.max()

def load(p):
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def shape(a):
    n = 1 << 15
    acc = np.zeros(n // 2 + 1)
    hops = range(0, max(1, len(a) - n), n)
    k = 0
    for i in hops:
        acc += np.abs(np.fft.rfft(a[i:i + n] * np.hanning(n))); k += 1
    acc /= max(k, 1)
    fr = np.fft.rfftfreq(n, 1 / SR)
    v = np.array([20 * np.log10(acc[(fr >= lo) & (fr < hi)].mean() + 1e-12) for lo, hi in BANDS])
    return v - v.max()

print(f"{'track':<18}{'dur':>7}{'shape err':>11}{'flatness':>10}{'score':>8}   band profile")
best = None
for p in sorted(glob.glob("*.mp3")):
    a = load(p)
    dur = len(a) / SR
    s = shape(a)
    err = float(np.abs(s - HIS).mean())
    # flatness: std of 4 s RMS blocks, in dB
    h = SR * 4
    e = 20 * np.log10(np.sqrt((a[:len(a)//h*h].reshape(-1, h) ** 2).mean(1)) + 1e-9)
    flat = float(e.std())
    score = err + flat * 1.5
    print(f"{p[:-4]:<18}{dur:6.0f}s{err:10.1f}{flat:9.1f}{score:8.1f}   "
          + " ".join(f"{x:5.1f}" for x in s))
    if best is None or score < best[0]: best = (score, p, dur)
print(f"\nHIS bed profile:      " + " ".join(f"{x:5.1f}" for x in HIS))
print(f"\nPICK: {best[1]}  ({best[2]:.0f}s, needs 236s -> "
      f"{'loop x%d' % int(np.ceil(236/best[2])) if best[2] < 236 else 'long enough'})")
