#!/usr/bin/env python3
"""Render every graphic in spec.py as an alpha QTRLE .mov, in the MIL house palette.

Straight port of zepbound/r2/build_gfx.py, including both traps it recorded:
  1. `motionlib.bullets_build` UPPER-CASES its heading, which breaks the J2 camel-case
     rule on `AbsByAI.com`. The cards are drawn here instead.
  2. bullets_build is TOP-aligned, right for a narrow side panel and wrong for a 16:9
     full-screen card — a three-bullet card left the bottom 45 % of the frame empty.
     The block is measured first and centred.
"""
import os, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
os.environ.setdefault("MOTIONLIB_FFMPEG", "/Volumes/Extreme/_edit_work/bin/ffmpeg")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motionlib as M
from PIL import Image, ImageDraw, ImageFont
import spec

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "gfx"); os.makedirs(OUT, exist_ok=True)
PAL  = M.MIL
LX   = 180


# ---------------------------------------------------------------- the drift
# ⚠ `motionlib.card_in` animates its content in and then HOLDS. Measured on the first
# build of this video: 38 of 40 frozen runs the watch pass found were cards sitting dead
# still for 3.64 s each after their last bullet landed — 148 s of frozen screen. That is
# Dan's ad-1 rev-1 note 1 verbatim ("card_in animates its entrance then HOLDS"), and the
# five-longforms handoff listed it as an outstanding one-line fix on these very videos.
#
# A pure SCALE drift is not enough: scale_about resizes to INTEGER pixel dimensions, so
# the image only changes every few frames and the gaps between still read as frozen. The
# drift here is therefore a SUB-PIXEL affine translation resampled BILINEAR, which
# changes every pixel on every frame, plus a gentle scale push for the look.
#
# Amplitude is +/-16 px about centre (32 px of travel over the card). It stays inside the
# bracket frame's 30 px inset, so the corner brackets never clip.
DRIFT_PX = 16.0
DRIFT_K  = 0.018


def card_in_drift(out, dur, build, in_dur=0.42, out_dur=0.30, pal=PAL, fps=None):
    fps = fps or spec.FPS
    base = M.field_bg(pal).convert("RGBA")
    frames = []
    for i in range(M.nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (M.W, M.H), (0, 0, 0, 0))
        a_in  = M.ease_out_cubic(t / in_dur) if in_dur > 0 else 1.0
        a_out = 1.0 if t <= dur - out_dur else 1 - M.ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(M.with_alpha(base, min(a_in * 2.2, 1.0) * a_out))
        content = Image.new("RGBA", (M.W, M.H), (0, 0, 0, 0))
        build(content, t)
        k = (0.90 + 0.10 * M.ease_out_back(t / in_dur)) if in_dur > 0 else 1.0
        content = M.scale_about(content, k * (1.0 + DRIFT_K * (t / dur)), None)
        dy = DRIFT_PX * (2.0 * (t / dur) - 1.0)          # +16 px -> -16 px
        content = content.transform(content.size, Image.AFFINE, (1, 0, 0, 0, 1, dy),
                                    resample=Image.BILINEAR)
        im.alpha_composite(M.with_alpha(content, a_in * a_out))
        frames.append(im)
    return M.encode(frames, out, fps)


def _eyebrow(d, x, y, text, f, p):
    eu = text.upper(); ew, eh = M.text_size(eu, f)
    d.rectangle([x, y, x + (ew + 34) * p, y + eh + 20], fill=PAL.mid)
    if p > 0.5:
        d.text((x + 17, y + (eh + 20) / 2), eu, font=f, fill=(255, 255, 255), anchor="lm")
    return eh + 20


def factcard(key, dur, eyebrow, heading, bullets, textw=1560):
    fE = M.font(38, "Bold"); fH = M.font(100, "ExtraBold"); fB = M.font(54, "SemiBold")
    hlines = M.wrap(heading, fH, textw)
    blines = [M.wrap(b, fB, textw - 46) for b in bullets]
    EH, HL, BL = 58, int(100 * 1.02), int(54 * 1.02)
    blk = EH + 46 + len(hlines) * HL + 16 + 11 + 58 + sum(len(l) * BL + 34 for l in blines)
    y0 = (M.H - blk) / 2

    def build(im, t):
        d = ImageDraw.Draw(im)
        M.bracket_frame(im, PAL)
        y = y0
        y += _eyebrow(d, LX, y, eyebrow, fE, M.ease_out_cubic(t / 0.30)) + 46
        hp = M.ease_out_cubic((t - 0.16) / 0.40)
        if hp > 0.01:
            hy = y
            for ln in hlines:
                d.text((LX, hy), ln, font=fH, fill=PAL.ink, anchor="lt"); hy += HL
            hw = max(M.text_size(l, fH)[0] for l in hlines)
            d.rectangle([LX, hy + 16, LX + hw * hp, hy + 27], fill=PAL.accent)
        y += len(hlines) * HL + 16 + 11 + 58
        for i, lines in enumerate(blines):
            bp = M.ease_out_cubic((t - 0.62 - i * 0.30) / 0.42)
            if bp > 0.01:
                oy = int((1 - bp) * 16)
                d.rectangle([LX, y + oy + 20, LX + 18, y + oy + 38], fill=PAL.accent)
                yy = y + oy
                for ln in lines:
                    d.text((LX + 46, yy), ln, font=fB, fill=PAL.ink, anchor="lt"); yy += BL
            y += len(lines) * BL + 34
    return card_in_drift(f"{OUT}/card_{key}.mov", dur, build, pal=PAL)


def appcard(key, dur, eyebrow, heading, lines, shot):
    """Full-frame product card: app screen left, copy right, block centred."""
    ph = Image.open(shot).convert("RGB")
    ph.thumbnail((470, 880), Image.LANCZOS)
    fE = M.font(36, "Bold"); fH = M.font(78, "ExtraBold"); fB = M.font(46, "SemiBold")
    px, py = 200, (M.H - ph.height) // 2
    tx = px + ph.width + 120
    textw = M.W - tx - 140
    hlines = M.wrap(heading, fH, textw)
    blines = [M.wrap(l, fB, textw - 42) for l in lines]
    EH, HL, BL = 56, int(78 * 1.02), int(46 * 1.04)
    blk = EH + 40 + len(hlines) * HL + 14 + 10 + 50 + sum(len(l) * BL + 28 for l in blines)
    y0 = (M.H - blk) / 2

    def build(im, t):
        d = ImageDraw.Draw(im)
        M.bracket_frame(im, PAL)
        p = M.ease_out_cubic(t / 0.45)
        if p > 0.01:
            off = int((1 - p) * 26)
            im.paste(ph, (px, py + off))
            d.rounded_rectangle([px - 5, py - 5 + off, px + ph.width + 4,
                                 py + ph.height + 4 + off],
                                radius=18, outline=PAL.accent + (255,), width=4)
        y = y0
        y += _eyebrow(d, tx, y, eyebrow, fE, M.ease_out_cubic(t / 0.30)) + 40
        hp = M.ease_out_cubic((t - 0.16) / 0.40)
        if hp > 0.01:
            hy = y
            for ln in hlines:
                d.text((tx, hy), ln, font=fH, fill=PAL.ink, anchor="lt"); hy += HL
            hw = max(M.text_size(l, fH)[0] for l in hlines)
            d.rectangle([tx, hy + 14, tx + hw * hp, hy + 24], fill=PAL.accent)
        y += len(hlines) * HL + 14 + 10 + 50
        for i, ls in enumerate(blines):
            bp = M.ease_out_cubic((t - 0.62 - i * 0.26) / 0.40)
            if bp > 0.01:
                oy = int((1 - bp) * 14)
                d.rectangle([tx, y + oy + 16, tx + 15, y + oy + 31], fill=PAL.accent)
                yy = y + oy
                for ln in ls:
                    d.text((tx + 42, yy), ln, font=fB, fill=PAL.ink, anchor="lt"); yy += BL
            y += len(ls) * BL + 28
    return card_in_drift(f"{OUT}/card_{key}.mov", dur, build, pal=PAL)


if __name__ == "__main__":
    only = set(sys.argv[1:]) or None
    for key, a, b, lines in spec.CHIPS:
        if only and key not in only: continue
        if os.path.exists(f"{OUT}/chip_{key}.mov"): continue
        M.lower_third_bar(f"{OUT}/chip_{key}.mov", lines, dur=b - a, x=spec.X, pal=PAL,
                          size=44, lead_size=58, bar_color=PAL.accent, fps=spec.FPS)
        print("chip", key, flush=True)
    for key, sec, eye, head, bl in spec.CARDS:
        if only and key not in only: continue
        if os.path.exists(f"{OUT}/card_{key}.mov"): continue
        factcard(key, spec.CARD_AT[key][1], eye, head, bl)
        print("card", key, flush=True)
    for key, a, dur, eye, head, lines, shot in spec.APPCARDS:
        if only and key not in only: continue
        if os.path.exists(f"{OUT}/card_{key}.mov"): continue
        appcard(key, dur, eye, head, lines, shot)
        print("appcard", key, flush=True)
    print("DONE")
