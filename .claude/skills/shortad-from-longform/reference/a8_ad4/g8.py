#!/usr/bin/env python3
"""Ad 4 graphics = the approved Ad 5 design system (g5.py, Dan 2026-09-11: "all the graphics look good") + the devices
Muhammad's Ad 4 adds, measured off his V4 HD frames (hdf/):

  * num_lower_third -- his numbered point: an olive tab carrying the white digit, a black bar with two white Bold lines
    (1 AI can design..., 2 The people telling you..., 3 The label..., 4 Nobody is checking...)
  * bullets_body(..., tails=[(text, time), ...]) -- his windows close on one OR TWO oblique olive lines
    (NOT WHAT'S TRENDING / NOT WHAT WORKED FOR SOME GUY ON YOUTUBE; IT'S ALL AFFILIATE LINKS; NOT THE MARKETING)
  * robot_label -- his "AI-generated video" italic tag + dashed arrow, pointing DOWN at the clip (vertical translation)
  * real_chip -- the standing label on Dan's REAL after pictures (AGENTS.md, Dan 2026-09-11):
    "Real picture of me — not AI-generated", same chip style as AI-GENERATED, low at the waist line, never over a face
"""
import sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
from g5 import *          # noqa: F401,F403 -- the approved system, unchanged
import g5 as _G
from PIL import Image, ImageDraw
from motionlib import font, wrap, text_size, oblique, ease_out_cubic, ease_in_out, clamp01

# ------------------------------------------------------------------ HIS PACE for every text reveal (audit 1, 2026-09-11)
# His lower thirds show a complete line 4-8 frames after the tab; his bullets are full in ~6 frames (bright-pixel count on his
# 256x144 cut: 0 -> 357 over 955-961); his olive tails pop within 1-2 frames. g5's reveals (bar 0.34 s, line n over 0.80 s
# after 0.20 + 0.55n s, bullets over 1.0 s) left "AI can read the label" readable for 6 frames of a 1.5 s hold.
LT_GROW, LT_HEAD, LT_STAG, LT_TYPE = 0.15, 0.06, 0.10, 0.25
BUL_TYPE, TAIL_TYPE = 0.30, 0.25

def lower_third(lines, t, dur, y_bottom=1600, weights=None, sizes=None):
    """g5.lower_third (his olive tab + black bar + white type), at his pace."""
    AVAIL = VW - 2*40 - 96
    fs = []
    for n, s in enumerate(lines):
        sz = (sizes[n] if sizes else (44 if n == 0 else 52))
        w8 = (weights[n] if weights else ("SemiBold" if n == 0 else "ExtraBold"))
        while sz > 24 and text_size(s, font(sz, w8))[0] > AVAIL: sz -= 2
        fs.append(font(sz, w8))
    ws = [text_size(s, f)[0] for s, f in zip(lines, fs)]; lhs = [int(f.size*1.30) for f in fs]
    bw = min(max(ws) + 96, VW - 2*40); bh = sum(lhs) + 34
    bx, by = (VW-bw)//2 + 22, y_bottom - bh; TAB = 26
    im = blank(); d = ImageDraw.Draw(im)
    o = 1.0 - ease_in_out(clamp01((t-(dur-0.12))/0.12)); gw = ease_out_cubic(clamp01(t/LT_GROW))
    d.rounded_rectangle([bx-TAB-14, by, bx-14, by+bh], radius=8, fill=OLIVE+(int(235*o*gw),))
    d.rounded_rectangle([bx, by, bx+int(bw*gw), by+bh], radius=8, fill=(0, 0, 0, int(232*o)))
    yy = by + 17
    for n, (s, f, lh) in enumerate(zip(lines, fs, lhs)):
        k = clamp01((t - LT_HEAD - n*LT_STAG)/LT_TYPE)
        draw_type(d, s, f, bx + (bw - text_size(s, f)[0])//2, yy, INK+(int(255*o),), k); yy += lh
    return im

def title_card(headline, sub, t, dur=None):
    """g5.title_card at HIS pace (audit 2: YOU LOCK IN sat on an empty card for 10 frames, headline complete at +25 against
    his +15, sub-line at +45 against his +25): card in 0.25 s, headline from +2 frames complete by ~+14, sub by ~+25."""
    fh, fs = font(96, "ExtraBold"), font(46, "SemiBold")
    hl = wrap(headline.upper(), fh, VW-2*150); sl = wrap(sub, fs, VW-2*150) if sub else []
    lh, ls = int(fh.size*1.06), int(fs.size*1.20)
    inner = len(hl)*lh + (40+len(sl)*ls if sl else 0); ch = inner + 150
    box = (72, (VH-ch)//2 - 120, VW-72, (VH-ch)//2 - 120 + ch)
    im = field().convert("RGBA")
    k0 = ease_out_back(clamp01(t/0.25)); o = fade(t, dur, tin=0.01, tout=0.2) if dur else 1.0
    cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
    hw, hh = (box[2]-box[0])/2*(0.94+0.06*k0), (box[3]-box[1])/2*(0.94+0.06*k0)
    rrect(im, [cx-hw, cy-hh, cx+hw, cy+hh], 30, fill=CARD_OL+(int(255*o),), glow=26)
    lay = blank(); d = ImageDraw.Draw(lay); y = box[1] + 75
    for n, ln in enumerate(hl):
        draw_type(d, ln, fh, (VW - text_size(ln, fh)[0])//2, y, INK+(int(255*o),), clamp01((t-0.05-n*0.10)/0.40)); y += lh
    im.alpha_composite(oblique(lay, 9.0, pivot_y=box[1]+75+len(hl)*lh/2))
    if sl:
        y += 40; d2 = ImageDraw.Draw(im)
        for n, ln in enumerate(sl):
            draw_type(d2, ln, fs, (VW - text_size(ln, fs)[0])//2, y, INK+(int(255*o),), clamp01((t-0.40-n*0.10)/0.40)); y += ls
    return im

# ------------------------------------------------------------------ his numbered lower third
def num_lower_third(num, lines, t, dur, y_bottom=1600, size=44):
    """Olive tab with the digit (his 1-4 points), black bar with the lines typing on. Line weights both Bold (his)."""
    AVAIL = VW - 2*40 - 110
    fs = []
    for s in lines:
        sz = size
        while sz > 24 and text_size(s, font(sz, "Bold"))[0] > AVAIL - 60: sz -= 2
        fs.append(font(sz, "Bold"))
    ws = [text_size(s, f)[0] for s, f in zip(lines, fs)]; lhs = [int(f.size*1.28) for f in fs]
    bw = min(max(ws) + 80, VW - 2*40 - 96); bh = sum(lhs) + 30
    TAB = 70; bx = (VW - (bw + TAB + 12))//2 + TAB + 12; by = y_bottom - bh
    im = blank(); d = ImageDraw.Draw(im)
    o = 1.0 - ease_in_out(clamp01((t-(dur-0.12))/0.12)); gw = ease_out_cubic(clamp01(t/LT_GROW))
    d.rounded_rectangle([bx-TAB-12, by, bx-12, by+bh], radius=8, fill=OLIVE+(int(240*o*gw),))
    fd = font(int(bh*0.62), "ExtraBold")
    d.text((bx-12-TAB//2, by+bh//2+2), num, font=fd, fill=INK+(int(255*o*gw),), anchor="mm")
    d.rounded_rectangle([bx, by, bx+int(bw*gw), by+bh], radius=8, fill=(0, 0, 0, int(232*o)))
    yy = by + 15
    for n, (s, f, lh) in enumerate(zip(lines, fs, lhs)):
        k = clamp01((t - LT_HEAD - n*LT_STAG)/LT_TYPE)
        draw_type(d, s, f, bx + (bw - text_size(s, f)[0])//2, yy, INK+(int(255*o),), k); yy += lh
    return im

# ------------------------------------------------------------------ bullets with one or more olive tails
TAIL_F = 58
def bullets_text_h2(header, items, tails, fh, fb):
    ft = font(TAIL_F, "ExtraBold"); maxw = VW - 2*MARGIN - 38
    th = sum(len(wrap(tx, ft, maxw))*int(ft.size*1.08) + 22 for tx, _ in tails) + (20 if tails else 0)
    return _G.bullets_text_h(header, items, fh, fb) + th

def bullets_body2(t, header, items, item_times, tails=(), dur=None):
    """His bullet screen (g5.bullets_body's layout) closed by one or two oblique olive lines, each typing on at ITS cue --
    at HIS pace: an item is complete in BUL_TYPE s, a tail in TAIL_TYPE s (g5 took 1.0 s and 0.55 s)."""
    fh, fb = font(46, "ExtraBold"), font(50, "SemiBold"); maxw = VW - 2*MARGIN
    ft = font(TAIL_F, "ExtraBold")
    hl = wrap(header.upper(), fh, maxw) if header else []
    hlh, lh = int(fh.size*1.10), int(fb.size*1.14)
    y_after = (len(hl)*hlh + 46 if header else 0) + sum(len(wrap(it, fb, maxw))*lh + 34 for it in items)
    def base(d, im, tt, ty):
        a = fade(tt, dur, tin=0.01, tout=0.14) if dur else 1.0
        if header:
            k = clamp01((tt-0.04)/0.25); wdt = 0
            for n_, h in enumerate(hl):
                wdt = max(wdt, draw_type(d, h, fh, MARGIN, ty + n_*hlh, OLIVE+(int(255*a),), clamp01((k-n_*0.25)*1.4)))
            yb = ty + (len(hl)-1)*hlh + fh.size + 16
            d.rectangle([MARGIN, yb, MARGIN+int(wdt*clamp01(k*1.2)), yb+6], fill=OLIVE+(int(255*a),))
            ty += len(hl)*hlh + 46
        for n, it in enumerate(items):
            k = clamp01((tt - item_times[n])/BUL_TYPE)
            if k <= 0: break
            lines = wrap(it, fb, maxw)
            d.rectangle([MARGIN, ty+18, MARGIN+14, ty+32], fill=tuple(int(v*clamp01(k*4)*a) for v in OLIVE))
            type_lines(d, lines, fb, MARGIN+38, ty, INK+(int(255*a),), k, lead=1.14)
            ty += len(lines)*lh + 34
    def body(d, im, tt, ty):
        base(d, im, tt, ty)
        a = fade(tt, dur, tin=0.01, tout=0.14) if dur else 1.0
        y = ty + y_after + 20
        for tx, tc in tails:
            lines = wrap(tx, ft, maxw - 38)
            if tt >= tc:
                k = clamp01((tt - tc)/TAIL_TYPE)
                lay = blank(); dd = ImageDraw.Draw(lay)
                for n, ln in enumerate(lines):
                    draw_type(dd, ln, ft, MARGIN+38, y + n*int(ft.size*1.08), OLIVE+(int(255*a),), clamp01((k - n*0.3)*1.4))
                im.alpha_composite(oblique(lay, 9.0, pivot_y=y + len(lines)*int(ft.size*1.08)/2))
            y += len(lines)*int(ft.size*1.08) + 22
    return body, bullets_text_h2(header, items, tails, fh, fb)

# ------------------------------------------------------------------ his "AI-generated video" tag + dashed arrow
def robot_label(im, cx, y_text, y_tip, t):
    """Italic-looking white tag (Manrope SemiBold under his 9-degree oblique) with a dashed arrow down to the clip."""
    f = font(60, "SemiBold"); txt = "AI-generated video"
    k = clamp01((t - 0.10)/0.45)
    lay = blank(); d = ImageDraw.Draw(lay); w = text_size(txt, f)[0]
    draw_type(d, txt, f, cx - w//2, y_text, INK+(255,), k)
    im.alpha_composite(oblique(lay, 9.0, pivot_y=y_text + f.size//2))
    d = ImageDraw.Draw(im); ka = clamp01((t - 0.35)/0.40)
    y0 = y_text + f.size + 18; y1 = y0 + int((y_tip - y0)*ka)
    y = y0
    while y < y1 - 10:
        d.line([(cx, y), (cx, min(y + 12, y1 - 10))], fill=INK+(255,), width=5); y += 22
    if ka >= 1.0:
        d.polygon([(cx - 17, y_tip - 20), (cx + 17, y_tip - 20), (cx, y_tip)], fill=INK+(255,))

# ------------------------------------------------------------------ the standing real-picture label (Dan, 2026-09-11)
REAL_TXT = "Real picture of me — not AI-generated"
def real_chip(im, y_top=1195, size=44):
    """Black rounded chip, white Manrope SemiBold, centred, top at the waist line (1180-1230), above the caption band
    (1385-1495) and never over a face. One line at 44 px fits inside 1080 with 44 px margins."""
    fl = font(size, "SemiBold")
    while text_size(REAL_TXT, fl)[0] + 40 > VW - 88 and size > 30: size -= 2; fl = font(size, "SemiBold")
    lw, lh = text_size(REAL_TXT, fl)
    bx = (VW - lw - 40)//2
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, y_top, bx+lw+40, y_top+lh+26], radius=10, fill=(0, 0, 0, 215))
    d.text((bx+20, y_top+13), REAL_TXT, font=fl, fill=INK+(255,), anchor="lt")
