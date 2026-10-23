#!/usr/bin/env python3
"""Brighten and clean up footage stills of Dan for posts (Dan, 2026-10-22: "brighten and improve the workout
screenshots as much as possible"). Writes <name>-enh.jpg beside each input; never touches the original.

    python3 .claude/skills/instagram-posts/reference/enhance.py STILL.jpg [...] [--strength 1.0]

Per image: levels from the 0.5 / 99.7 luminance percentiles, a gamma lift that brings mid-tones toward a bright
outdoor look (more when the frame is dark), a little vibrance, and a light unsharp mask. Colour balance is kept
(same curve on R, G, B), so skin does not shift. Look at the result; drop --strength for a gentler pass.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageFilter


def enhance(path, strength=1.0):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    lo, hi = np.percentile(lum, 0.5), np.percentile(lum, 99.7)
    lo = min(lo, 0.06) * strength
    hi = max(hi, 0.80)
    a = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
    mid = float(np.median(np.clip((lum - lo) / max(hi - lo, 1e-3), 0, 1)))
    target = 0.50
    g = np.log(target) / np.log(max(min(mid, 0.95), 0.05)) if mid < target else 1.0
    g = 1 - (1 - max(g, 0.62)) * strength
    a = a ** g
    # vibrance: push low-saturation pixels more than saturated ones
    mx, mn = a.max(axis=2, keepdims=True), a.min(axis=2, keepdims=True)
    sat = mx - mn
    m = a.mean(axis=2, keepdims=True)
    a = np.clip(m + (a - m) * (1 + 0.18 * strength * (1 - sat)), 0, 1)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    out = out.filter(ImageFilter.UnsharpMask(radius=1.6, percent=int(55 * strength), threshold=2))
    dest = os.path.splitext(path)[0] + "-enh.jpg"
    out.save(dest, quality=94)
    return dest, mid, g


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--strength", type=float, default=1.0)
    x = ap.parse_args()
    for p in x.images:
        d, mid, g = enhance(p, x.strength)
        print(f"{d}  (mid-tone before {mid:.2f}, gamma {g:.2f})")
