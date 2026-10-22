#!/usr/bin/env python3
"""Colour-correct a footage still for a post (Dan, 2026-10-22: "anytime you use a screenshot in these carousels, it's
properly color corrected and looking optimal before you put it in ... not just putting in raw footage").

Two stages:
  1. BASE GRADE from the camera roll (only when extracting from a video). Raw rolls from the 8/28 shoot (C1672-C1685)
     and the 7/8 welcome-video shoot (C02xx-0xx) are S-Log3: they look flat and grey until the approved LUT goes on
     (_shared/cliplib/README.md, "Grades Dan approved for filmed B-roll"; recipe broll-cuts-20260929/cut.py).
     8/3 (C15xx), 10/15 (C17xx), GoPro and library B#### clips are already Rec.709: no LUT.
  2. FINISHING PASS on every still: neutral white balance from the grey/white parts of the frame (concrete, stucco,
     sky-lit walls) so skin is not orange or grey, levels, a local lift of shaded areas (Dan backlit
     on the 8/28 blue-mat rolls), exposure lifted toward a bright outdoor look weighted on
     the middle of the frame (where Dan is), a gentle S-curve, vibrance that spares skin, orange skin pulled back to
     a natural chroma (low sun turns skin orange on the 8/3 and 8/28 rolls), light sharpening.

    # from a video (crop is in source pixels; size is the slide box the crop is resized to)
    python3 grade_still.py --src ROLL.MP4 --t 64.0 --out OUT-graded.jpg [--crop x,y,w,h] [--size 1080x660]
                           [--grade auto|w07|h115|h130|b130|p145|none] [--strength 1.0] [--wb 1.0] [--ev 0]
    # an existing still (finishing pass only)
    python3 grade_still.py --still STILL.jpg [--out STILL-graded.jpg] [...]

Prints the before/after measurements (mean brightness, saturation, skin warmth). LOOK at the result next to an
approved slide (template-r1-mockups/C1-the-fix-02.jpg) before using it.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FF = os.path.join(ROOT, "Media", "video_edit", "bin", "ffmpeg")
LUT_A = "/Volumes/Extreme/_edit_work/broll-cuts-20260929/slog3_709_e{}.cube"   # 0.70, 0.85
LUT_B = "/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e{}.cube"     # 1.00 .. 1.60


def lut(e):
    p = (LUT_A if e in ("0.70", "0.85") else LUT_B).format(e)
    if not os.path.exists(p):
        sys.exit(f"LUT missing: {p} (Extreme drive mounted?)")
    return f"lut3d=file='{p}':interp=tetrahedral"


GRADES = {
    "w07": lambda: [lut("0.70"), "eq=saturation=0.88"],                     # 7/8 welcome-video rolls C02xx-0xx
    "h115": lambda: [lut("1.15"), "eq=saturation=0.88"],                    # 8/28 hard sun C1673-C1677
    "h130": lambda: [lut("1.30"), "eq=saturation=0.88"],
    "b130": lambda: [lut("1.30"), "eq=saturation=0.88", "colortemperature=temperature=8500:pl=1"],  # 8/28 blue mat
    "p145": lambda: [lut("1.45"), "eq=saturation=0.88"],                    # 8/28 patio C1684-C1685
    "none": lambda: [],
}


def auto_grade(src):
    """Pick the approved base grade from the roll name."""
    b = os.path.basename(src).upper()
    if re.match(r"C02\d\d-\d+", b):
        return "w07"
    m = re.match(r"C(\d{4})\.MP4$", b)
    if m:
        n = int(m.group(1))
        if 1679 <= n <= 1683:
            return "b130"
        if 1684 <= n <= 1685:
            return "p145"
        if 1672 <= n <= 1678:
            return "h115"
    return "none"   # library B####, 8/3 C15xx, 8/14 C16xx, 10/15 C17xx, GoPro: already Rec.709


def extract(src, t, grade, crop):
    vf = []
    if crop:
        x, y, w, h = crop
        vf.append(f"crop={w}:{h}:{x}:{y}")
    vf.append("scale=iw:ih:in_color_matrix=bt709:in_range=tv:out_range=pc")
    vf += GRADES[grade]()
    vf.append("format=rgb48le")
    fd, tmp = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
                    "-vf", ",".join(vf), "-pix_fmt", "rgb48be", tmp], check=True)
    im = Image.open(tmp)
    a = np.asarray(im).astype(np.float32)
    a = a / (65535.0 if a.max() > 255 else 255.0)
    os.remove(tmp)
    return a


LW = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def measure(a):
    lum = a @ LW
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    skin = (r > g) & (g > b) & (r - b > 0.10) & (lum > 0.18) & (lum < 0.9) & ((r - g) < 0.6 * (r - b) + 0.02)
    sk = a[skin].mean(0) if skin.sum() > 200 else np.array([np.nan] * 3)
    # skin chroma: HSV saturation of skin-hued pixels (orange skin reads high, ~0.5+; natural ~0.30-0.42)
    hsat = sat / np.maximum(mx, 1e-3)
    warmth = float(np.median(hsat[skin])) if skin.sum() > 200 else float("nan")
    return dict(L=float(lum.mean() * 255), med=float(np.median(lum) * 255), S=float(sat.mean() * 255),
                skin_warmth=warmth, skin_frac=float(skin.mean()))


def tame_glare(a, cap=0.30):
    """Low sun can leave a hot yellow streak on skin (B0427 / C1679 ab-wheel back). Pull bright, strongly saturated
    yellow-orange pixels (hue 32-66 deg) down to a pale highlight. Opt-in (--glare): it also hits yellow objects."""
    mx, mn = a.max(2), a.min(2)
    c = mx - mn
    s = c / np.maximum(mx, 1e-4)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
    w = np.clip(1 - np.abs(hue - 49) / 17, 0, 1) * np.clip((mx - 0.45) / 0.2, 0, 1) * np.clip((s - cap) / 0.15, 0, 1)
    w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    s_new = s + (np.minimum(s, cap) - s) * w
    scale = np.where(c > 1e-4, (s_new * mx) / np.maximum(c, 1e-4), 1)
    out = mx[..., None] - (mx[..., None] - a) * scale[..., None]
    # nudge the hue of the treated area back toward skin (a touch more red, less green)
    out[..., 1] -= 0.035 * w
    return np.clip(out, 0, 1)


def tame_skin(a, cap=0.40, keep=0.35):
    """Pull over-saturated orange skin back toward natural: compress HSV saturation above `cap` for hues 0-50 deg."""
    mx, mn = a.max(2), a.min(2)
    c = mx - mn
    s = c / np.maximum(mx, 1e-4)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
    w = np.clip(1 - np.abs(hue - 28) / 32, 0, 1) * (mx > 0.12)   # orange to sun-yellow skin
    s2 = np.where(s > cap, cap + (s - cap) * keep, s)
    s_new = s + (s2 - s) * w
    # rebuild: same max (value) and hue, new saturation
    scale = np.where(c > 1e-4, (s_new * mx) / np.maximum(c, 1e-4), 1)
    return np.clip(mx[..., None] - (mx[..., None] - a) * scale[..., None], 0, 1)


def center_weights(h, w):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx / w - 0.5) / 0.35) ** 2 + ((yy / h - 0.55) / 0.40) ** 2
    return np.exp(-d)


def finish(a, strength=1.0, wb=1.0, ev=0.0, target=0.47, sat_target=0.20, skin_cap=0.40, shadows=0.35, skin_target=0.58, glare=False):
    h, w, _ = a.shape
    a = np.clip(a, 0, 1)
    lum = a @ LW
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    # 1. white balance from near-neutral mid/high pixels (concrete, stucco, white chairs, shirt-free surfaces)
    neutral = (sat < np.percentile(sat, 35)) & (lum > np.percentile(lum, 30)) & (lum < np.percentile(lum, 99))
    if neutral.sum() > 500 and wb > 0:
        m = a[neutral].mean(0)
        gains = m.mean() / np.maximum(m, 1e-3)
        gains = np.clip(gains, 0.86, 1.16) ** wb
        # keep a hint of warmth: outdoor sun is not paper-white
        gains = gains * np.array([1.012, 1.0, 0.985], dtype=np.float32)
        a = np.clip(a * gains / (gains @ LW), 0, 1)
        lum = a @ LW
    # 2. levels
    lo = float(np.percentile(lum, 0.4))
    hi = float(np.percentile(lum, 99.6))
    lo = min(lo, 0.08) * strength
    hi = max(hi, 0.75)
    a = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
    lum = a @ LW
    # 2b. local shadow lift: brighten areas that sit in shade (Dan backlit by low sun) without lifting the bright
    #     background; gain from a heavily blurred luminance map, so edges do not halo
    if shadows > 0:
        L8 = Image.fromarray((lum * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(w, h) * 0.025))
        bl = np.asarray(L8).astype(np.float32) / 255.0
        gain = np.clip((0.55 / np.maximum(bl, 0.06)) ** shadows, 1.0, 1.0 + 1.2 * shadows)
        gain = np.where(bl < 0.55, gain, 1.0)
        a = 1 - (1 - a) ** gain[..., None]     # lift that compresses toward white instead of clipping
        lum = a @ LW
    # 3. exposure: gamma so the centre-weighted median lands on target (bright outdoor look)
    wts = center_weights(h, w)
    order = np.argsort(lum, axis=None)
    cw = np.cumsum(wts.ravel()[order])
    cmed = float(lum.ravel()[order][np.searchsorted(cw, cw[-1] / 2)])
    gmed = float(np.median(lum))
    mid = 0.6 * cmed + 0.4 * gmed
    tgt = min(0.62, max(0.30, target * (2 ** (ev * 0.5))))
    g = np.log(tgt) / np.log(min(max(mid, 0.04), 0.95))
    # Dan's skin is the subject: when enough skin is in frame, also aim his skin at a bright, natural level
    r_, g2, b_ = a[..., 0], a[..., 1], a[..., 2]
    sk = (r_ > g2) & (g2 > b_) & (r_ - b_ > 0.06) & ((r_ - g2) < 0.6 * (r_ - b_) + 0.02) & (lum > 0.06)
    if sk.mean() > 0.03:
        s_med = float(np.median(lum[sk]))
        s_tgt = min(0.70, skin_target * (2 ** (ev * 0.5)))
        g_s = np.log(s_tgt) / np.log(min(max(s_med, 0.04), 0.95))
        g = min(g, 0.4 * g + 0.6 * g_s)
    g = float(np.clip(g, 0.55, 1.08))   # never darken a bright frame much
    g = 1 - (1 - g) * strength
    a = a ** g
    # 4. gentle S-curve on luminance (contrast without crushing), applied as a ratio to keep hue
    lum = a @ LW
    k = 0.10 * strength
    lum2 =np.clip(lum + k * (lum - 0.5) * (1 - np.abs(2 * lum - 1)), 0, 1)
    ratio = np.where(lum > 1e-4, lum2 / np.maximum(lum, 1e-4), 1)
    a = np.clip(a * ratio[..., None], 0, 1)
    # 5. vibrance toward a natural saturation, sparing skin
    lum = a @ LW
    mx, mn = a.max(2), a.min(2)
    sat = mx - mn
    cur = float(sat.mean())
    boost = np.clip((sat_target / max(cur, 1e-3)) - 1, -0.15, 0.45) * strength
    r, g_, b = a[..., 0], a[..., 1], a[..., 2]
    skin = (r > g_) & (g_ > b) & (r - b > 0.08)
    amt = boost * (1 - np.clip(sat / 0.6, 0, 1))
    amt = np.where(skin, np.minimum(amt, 0.10 * strength), amt)
    m = lum[..., None]
    a = np.clip(m + (a - m) * (1 + amt[..., None]), 0, 1)
    if skin_cap < 1:
        a = tame_skin(a, cap=skin_cap)
    if glare:
        a = tame_glare(a)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    out = out.filter(ImageFilter.UnsharpMask(radius=1.4, percent=int(60 * strength), threshold=2))
    return out, dict(gamma=g, mid=mid, sat_boost=float(boost))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src")
    ap.add_argument("--t", type=float)
    ap.add_argument("--still")
    ap.add_argument("--out")
    ap.add_argument("--crop", help="x,y,w,h in source pixels")
    ap.add_argument("--size", help="WxH output size (resize after crop)")
    ap.add_argument("--grade", default="auto", choices=["auto"] + list(GRADES))
    ap.add_argument("--strength", type=float, default=1.0)
    ap.add_argument("--wb", type=float, default=1.0, help="white-balance strength 0..1")
    ap.add_argument("--ev", type=float, default=0.0, help="brighter (+) / darker (-) than the default target")
    ap.add_argument("--sat", type=float, default=0.20, help="target mean saturation 0..1")
    ap.add_argument("--skin", type=float, default=0.40, help="cap on skin colour saturation (1 = off)")
    ap.add_argument("--shadows", type=float, default=0.35, help="local lift of shaded areas 0..1 (0 = off)")
    ap.add_argument("--glare", action="store_true", help="also tame hot yellow sun streaks on skin")
    ap.add_argument("--no-finish", action="store_true")
    x = ap.parse_args()
    crop = [int(v) for v in x.crop.split(",")] if x.crop else None
    if x.src:
        grade = auto_grade(x.src) if x.grade == "auto" else x.grade
        a = extract(x.src, x.t, grade, crop)
        out = x.out or os.path.splitext(os.path.basename(x.src))[0] + f"-{x.t:.2f}-graded.jpg"
        tag = f"{os.path.basename(x.src)} @ {x.t:.2f}s base={grade}"
    elif x.still:
        im = Image.open(x.still).convert("RGB")
        if crop:
            im = im.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
        a = np.asarray(im).astype(np.float32) / 255.0
        out = x.out or os.path.splitext(x.still)[0] + "-graded.jpg"
        tag = f"{os.path.basename(x.still)} (finish only)"
    else:
        sys.exit("give --src and --t, or --still")
    before = measure(a)
    if x.no_finish:
        img, info = Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)), {}
    else:
        img, info = finish(a, x.strength, x.wb, x.ev, sat_target=x.sat, skin_cap=x.skin, shadows=x.shadows, glare=x.glare)
    if x.size:
        W, H = [int(v) for v in x.size.lower().split("x")]
        img = img.resize((W, H), Image.LANCZOS)
    img.save(out, quality=94)
    after = measure(np.asarray(img).astype(np.float32) / 255.0)
    f = lambda d: f"L{d['L']:.0f} med{d['med']:.0f} S{d['S']:.0f} skin-chroma {d['skin_warmth']:.2f}"
    print(f"{out}\n   {tag}\n   before {f(before)}\n   after  {f(after)}  {', '.join(f'{k} {v:.2f}' for k, v in info.items())}")


if __name__ == "__main__":
    main()
