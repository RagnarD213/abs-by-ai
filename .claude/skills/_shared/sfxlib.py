#!/usr/bin/env python3
"""sfxlib — transition one-shots synthesised from scratch (numpy -> 48k stereo WAV).

Why synthesised rather than downloaded
--------------------------------------
Every graphic entrance in a modern edit wants a whoosh or a pop. Sourcing those means
either an account-walled library (freesound needs an API key) or a licence that has to
be tracked per asset for the rest of the channel's life. These are simple sounds --
filtered noise with an envelope, and a decaying pitch drop -- so generating them costs
nothing, carries no attribution, and lets the timbre be tuned to the edit.

  whoosh(dur=0.42, f0=420, f1=4200, f2=900)   graphic slides/scales in
  pop(freq=880)                               a bullet or a chip appears
  riser(dur=0.9)                              lift into a full-screen title card
  sub_drop()                                  weight under a hard layout change

All return a mono float array at SR; write with save().
"""
import numpy as np, wave, struct

SR = 48000

def _env(n, attack=0.006, decay=1.0, curve=3.2):
    """Fast attack, exponential-ish decay over the whole one-shot."""
    a = max(1, int(attack * SR))
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a)
    tail = np.linspace(0, 1, n - a)
    e[a:] = (1 - tail) ** curve
    return e * decay

def _biquad_bp(x, fc, q=1.6):
    """Band-pass with a per-sample centre frequency (fc is an array the length of x)."""
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i in range(len(x)):
        w0 = 2 * np.pi * min(max(fc[i], 30.0), SR * 0.45) / SR
        alpha = np.sin(w0) / (2 * q)
        c = np.cos(w0)
        b0, b1, b2 = alpha, 0.0, -alpha
        a0, a1, a2 = 1 + alpha, -2 * c, 1 - alpha
        xi = x[i]
        yi = (b0 * xi + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1 = x1, xi
        y2, y1 = y1, yi
        y[i] = yi
    return y

def whoosh(dur=0.42, f0=420.0, f1=4200.0, f2=900.0, q=1.2, seed=7, gain=1.0):
    """Noise through a band-pass that sweeps up then back down -- an air movement."""
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n)
    noise = np.cumsum(noise) / 40.0 + noise * 0.6          # tilt toward pink
    t = np.linspace(0, 1, n)
    # up on the first 45% of the sound, down after -- the classic transition contour
    fc = np.where(t < 0.45, f0 + (f1 - f0) * (t / 0.45) ** 0.7,
                            f1 + (f2 - f1) * ((t - 0.45) / 0.55) ** 1.4)
    # two band-pass stages: one 6 dB/oct skirt leaks enough broadband noise that the
    # result reads as hiss rather than as air moving (measured centroid 7 kHz vs 3 kHz)
    y = _biquad_bp(_biquad_bp(noise, fc, q), fc, q) * _env(n, 0.01, 1.0, 2.0)
    y *= np.sin(np.pi * t) ** 0.6                           # soften both ends
    return _norm(y) * gain

def pop(freq=880.0, dur=0.11, drop=0.45, gain=0.85):
    """Short pitched blip with a downward glide -- a UI 'tick' for small reveals."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 - drop * (t / dur) ** 1.5)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.28 * np.sin(2 * ph)) * _env(n, 0.002, 1.0, 4.5)
    return _norm(y) * gain

def riser(dur=0.9, f0=180.0, f1=2600.0, gain=0.8, seed=3):
    """Noise sweeping upward with no fall -- points at the thing that lands next."""
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    fc = f0 * (f1 / f0) ** (t ** 1.35)
    y = _biquad_bp(_biquad_bp(noise, fc, 2.4), fc, 2.4) * (t ** 1.6)
    y[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return _norm(y) * gain

def sub_drop(dur=0.55, f0=110.0, f1=38.0, gain=0.7):
    """Low sine falling away -- weight under a full-screen layout change."""
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    f = f0 * (f1 / f0) ** (t ** 0.8)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - t) ** 2.2
    return _norm(y) * gain

def _norm(y):
    m = np.max(np.abs(y))
    return y / m if m > 1e-9 else y

def save(path, y, sr=SR, stereo=True):
    y = np.clip(y, -1, 1)
    data = np.stack([y, y], axis=1) if stereo else y[:, None]
    pcm = (data * 32767).astype("<i2").tobytes()
    with wave.open(path, "wb") as w:
        w.setnchannels(data.shape[1]); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm)
    return path

def build_pack(outdir="."):
    """Render the standard pack used by the modern-edit style. Returns {name: path}."""
    import os
    os.makedirs(outdir, exist_ok=True)
    pack = {
        "whoosh":      whoosh(0.42, 420, 4200, 900, gain=1.0),
        "whoosh_soft": whoosh(0.34, 500, 2600, 800, q=1.0, seed=11, gain=0.62),
        "whoosh_out":  whoosh(0.36, 3200, 900, 320, q=1.1, seed=19, gain=0.7),
        "pop":         pop(920),
        "pop_soft":    pop(700, 0.10, 0.40, gain=0.55),
        "riser":       riser(0.75),
        "sub":         sub_drop(),
    }
    return {k: save(os.path.join(outdir, f"sfx_{k}.wav"), v) for k, v in pack.items()}

if __name__ == "__main__":
    import sys
    print(build_pack(sys.argv[1] if len(sys.argv) > 1 else "."))
