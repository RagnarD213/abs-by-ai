#!/usr/bin/env python3
"""Vertical (1080x1920, 24 fps) rebuild of ZEESHAN's design system for "this picture got me abs".

Every token was MEASURED off his finished 16:9 render (2026-09-10), not guessed:
  field (20,32,22) flat dark green, no grid     | photo cards: black border, square corners
  checklist header (145,150,100) on black        | check marks (95,195,74) on a light disc
  checklist item boxes (58,63,62) translucent    | wall-poster callout stroke (167,186,90)
  lower-third accent bar (0,82,0)                | CTA bar: black, thin white top rule, tracked white type
  "The Problem": field-green box + tracked type  | "#1/#2": field-green number chip + heavy white type
His type is Manrope throughout (tracked Medium for labels and the CTA, Bold/ExtraBold for statements).

Layout rules for the phone (vertical translation of his 16:9 frame):
  * captions sit at CAP_Y = 1400 (the band the caption-sync gate reads, 1385-1495)
  * his persistent CTA bar sits ABOVE the captions (1206-1334); it runs 2.3 minutes, so it cannot mute them
  * lower thirds live in 1040-1340; nothing that must be read goes below 1660 (Reels/Shorts UI)
  * media whose aspect does not fill the frame goes in HIS card on HIS field -- the mirror of his own logic
    (in 16:9 he cards the portrait photos; in 9:16 the landscape clips are the ones that need the card)
"""
import sys, math
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, ease_out_cubic, ease_out_expo, ease_in_out, clamp01

VW, VH, FPS = 1080, 1920, 24.0
FIELD      = (20, 32, 22)
LIME       = (167, 186, 90)      # his callout stroke; also the karaoke highlight (green-dominant: the sync gate sees it)
CHECK      = (95, 195, 74)
HDR_OLIVE  = (145, 150, 100)
ITEM_BOX   = (58, 63, 62)
ACCENT     = (0, 82, 0)
INK        = (255, 255, 255)
INK_CTA    = (240, 238, 246)
CAP_Y      = 1400
CTA_BOX    = (60, 1206, 1020, 1334)
MARGIN     = 60

def field():
    return Image.new("RGBA", (VW, VH), FIELD + (255,))

# ------------------------------------------------------------------ type
def tracked_width(txt, f, track):
    return sum(f.getlength(c) for c in txt) + track * max(0, len(txt) - 1)

def draw_tracked(d, xy, txt, f, fill, track=0.0, anchor_x="l"):
    """Letter-spaced text on the BASELINE (anchor 'ls'; skill trap 11: per-character 'lt' garbles lowercase).
    xy = (x, top-of-ascender) like a whole-string 'lt' draw; anchor_x 'l' | 'c' | 'r'."""
    x, y = xy
    w = tracked_width(txt, f, track)
    if anchor_x == "c": x -= w / 2
    elif anchor_x == "r": x -= w
    base = y + f.getmetrics()[0]
    for c in txt:
        d.text((x, base), c, font=f, fill=fill, anchor="ls")
        x += f.getlength(c) + track
    return w

def wrap(txt, f, maxw, track=0.0):
    out, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if cur and tracked_width(t, f, track) > maxw: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out

def shadowed(im, draw_fn, blur=6, alpha=150):
    """Soft drop shadow under whatever draw_fn paints (his AI label and titles carry one)."""
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(sh), (0, 0, 0, alpha))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    draw_fn(ImageDraw.Draw(im), None)

# ------------------------------------------------------------------ media helpers
def cover(img, w, h, ox=0.5, oy=0.5):
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height)
    im = img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS)
    x0 = int((im.width - w) * ox); y0 = int((im.height - h) * oy)
    return im.crop((x0, y0, x0 + w, y0 + h))

def card_on(canvas, media_rgb, cx, cy, w, border=10):
    """His photo card: the media with a solid black border, square corners, centred at (cx, cy), width w."""
    h = round(w * media_rgb.height / media_rgb.width)
    m = media_rgb.resize((w, h), Image.LANCZOS)
    x0, y0 = round(cx - w / 2), round(cy - h / 2)
    ImageDraw.Draw(canvas).rectangle([x0 - border, y0 - border, x0 + w + border - 1, y0 + h + border - 1], fill=(0, 0, 0, 255))
    canvas.paste(m, (x0, y0))
    return (x0, y0, x0 + w, y0 + h)

def ai_label(canvas, x_right, y_bottom, size=54, txt="AI-Generated"):
    """His AI label: plain white Manrope over the picture, bottom-right, with a soft shadow for legibility.
    Standing rule: it is burned in, and it never sits over a face (callers place it at the bottom of the media)."""
    f = font(size, "SemiBold")
    w = f.getlength(txt); x = x_right - w; y = y_bottom - f.getmetrics()[0] - f.getmetrics()[1]
    def paint(d, col): d.text((x, y), txt, font=f, fill=col or (236, 244, 228, 255), anchor="lt")
    shadowed(canvas, paint, blur=5, alpha=170)

# ------------------------------------------------------------------ overlays (RGBA, full frame)
def blank(): return Image.new("RGBA", (VW, VH), (0, 0, 0, 0))

def fade(t, dur, tin=0.18, tout=0.12):
    a = clamp01(t / tin) if tin > 0 else 1.0
    if dur is not None: a = min(a, clamp01((dur - t) / tout) if tout > 0 else 1.0)
    return ease_in_out(a)

def checklist(t, t_items, dur):
    """IN TODAY'S EPISODE: black header box with his olive caps, then three items that build on his cues, each a
    translucent dark box with a green check on a light disc. Lower half of the frame, over Dan's torso -- the same
    'boxes on the footage' treatment he uses over the fridge."""
    im = blank(); d = ImageDraw.Draw(im)
    fh = font(46, "Bold"); fi = font(40, "SemiBold")
    items = ["How I Got Limitless Motivation To Work Out And Eat Healthy",
             "What I Needed To Do To Lose My Belly Fat And Get Six-Pack Abs",
             "How You Can Generate A Goal Picture Of Yourself With Abs For Free"]
    y = 760
    a = fade(t, dur)
    hw = fh.getlength("IN TODAY'S EPISODE") + 80
    d.rectangle([VW / 2 - hw / 2, y, VW / 2 + hw / 2, y + 86], fill=(0, 0, 0, int(235 * a)))
    draw_tracked(d, (VW / 2, y + 18), "IN TODAY'S EPISODE", fh, HDR_OLIVE + (int(255 * a),), 0.0, "c")
    y += 112
    for k, txt in enumerate(items):
        ta = t - t_items[k]
        if ta < 0: break
        b = fade(ta, dur - t_items[k]) * a
        dy = int((1 - ease_out_cubic(clamp01(ta / 0.25))) * 16)
        lines = wrap(txt, fi, VW - 2 * MARGIN - 150)
        bh = 26 + len(lines) * 50
        x0 = MARGIN + 96
        d.rounded_rectangle([x0, y + dy, VW - MARGIN, y + dy + bh], radius=16, fill=ITEM_BOX + (int(205 * b),))
        cx, cy = MARGIN + 38, y + dy + bh / 2
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(226, 230, 226, int(235 * b)))
        d.line([(cx - 17, cy + 1), (cx - 5, cy + 14), (cx + 18, cy - 13)], fill=CHECK + (int(255 * b),), width=9, joint="curve")
        for j, ln in enumerate(lines):
            d.text((x0 + 26, y + dy + 13 + j * 50), ln, font=fi, fill=(255, 255, 255, int(255 * b)), anchor="lt")
        y += bh + 20
    return im

def problem_lt(t, t_sub, dur):
    """'The Problem' in a field-green box (tracked Medium), 'No Time, No Motivation.' in a black box (tracked Bold)."""
    im = blank(); d = ImageDraw.Draw(im)
    f1 = font(58, "Medium"); f2 = font(50, "Bold")
    a = fade(t, dur); x = MARGIN; y = 1060
    w1 = tracked_width("The Problem", f1, 6)
    d.rectangle([x, y, x + w1 + 44, y + 92], fill=FIELD + (int(245 * a),))
    draw_tracked(d, (x + 22, y + 14), "The Problem", f1, (236, 242, 232, int(255 * a)), 6)
    if t >= t_sub:
        b = fade(t - t_sub, dur - t_sub) * a
        w2 = tracked_width("No Time, No Motivation.", f2, 5)
        d.rectangle([x - 10, y + 128, x + w2 + 34, y + 216], fill=(0, 0, 0, int(240 * b)))
        draw_tracked(d, (x + 12, y + 144), "No Time, No Motivation.", f2, (255, 255, 255, int(255 * b)), 5)
    return im

def ifyousaw_lt(t, dur):
    """His black lower third with the dark-green accent bar. His two lines re-wrapped to three for 1080 wide."""
    im = blank(); d = ImageDraw.Draw(im)
    f = font(48, "ExtraBold")
    lines = ["If You Saw Yourself With Abs,", "You'd Be MOTIVATED To Make", "Your Dream Body A Reality."]
    a = fade(t, dur); y = 1070; h = 36 + 62 * len(lines)
    d.rectangle([MARGIN + 18, y, VW - MARGIN, y + h], fill=(0, 0, 0, int(225 * a)))
    d.rectangle([MARGIN, y, MARGIN + 18, y + h], fill=ACCENT + (int(255 * a),))
    for j, ln in enumerate(lines):
        d.text((MARGIN + 50, y + 18 + j * 62), ln, font=f, fill=(255, 255, 255, int(255 * a)), anchor="lt")
    return im

def num_lt(t, num, text, dur):
    """'#1 You Don't Need More Knowledge' -- his field-green number chip and heavy white statement, above the CTA bar."""
    im = blank(); d = ImageDraw.Draw(im)
    fn = font(44, "Medium"); ft = font(46, "ExtraBold")
    a = fade(t, dur); x = MARGIN
    lines = wrap(text, ft, VW - 2 * MARGIN - 110)
    y = 1190 - 60 * len(lines)
    cw = fn.getlength(num) + 28
    d.rectangle([x, y, x + cw, y + 62], fill=FIELD + (int(245 * a),))
    d.text((x + 14, y + 8), num, font=fn, fill=(220, 226, 216, int(255 * a)), anchor="lt")
    def paint(dd, col):
        for j, ln in enumerate(lines):
            dd.text((x + cw + 20, y + 4 + j * 60), ln, font=ft, fill=col or (255, 255, 255, int(255 * a)), anchor="lt")
    shadowed(im, paint, blur=6, alpha=int(200 * a))
    return im

def cta_bar(t, dur):
    """His persistent CTA: a black bar with a thin white top rule and tracked light type. His one line
    ('See Yourself With Abs - Tap The Button Below') becomes two lines for 1080 wide; every word is his."""
    im = blank(); d = ImageDraw.Draw(im)
    f = font(44, "Medium")
    a = fade(t, dur, tin=0.25, tout=0.15)
    x0, y0, x1, y1 = CTA_BOX
    d.rectangle([x0, y0, x1, y1], fill=(6, 6, 6, int(215 * a)))
    d.rectangle([x0, y0, x1, y0 + 2], fill=(226, 222, 216, int(240 * a)))
    draw_tracked(d, (VW / 2, y0 + 12), "See Yourself With Abs", f, INK_CTA + (int(255 * a),), 3.2, "c")
    draw_tracked(d, (VW / 2, y0 + 70), "Tap The Button Below", f, INK_CTA + (int(255 * a),), 3.2, "c")
    return im

def final_label(t, dur):
    """'Final Result AI' -- his black label beside the app result."""
    im = blank(); d = ImageDraw.Draw(im)
    f = font(56, "Bold"); a = fade(t, dur)
    w = f.getlength("Final Result AI")
    d.rectangle([MARGIN, 96, MARGIN + w + 40, 96 + 84], fill=(0, 0, 0, int(240 * a)))
    d.text((MARGIN + 20, 108), "Final Result AI", font=f, fill=(255, 255, 255, int(255 * a)), anchor="lt")
    return im

def flash(frame_rgb, k):
    """His one-frame white flash: a screen blend toward white (k=1 is pure white)."""
    import numpy as np
    a = np.asarray(frame_rgb, dtype=np.float32) / 255.0
    return Image.fromarray(((1 - (1 - a) * (1 - k)) * 255).clip(0, 255).astype("uint8"))

# ------------------------------------------------------------------ full-frame graphics beats
def title_visualizing(t, lt):
    """VISUALIZING YOUR GOAL fading up, then his tracked staircase 'One Of The / Most Powerful Ways / To Motivate
    Yourself' line by line (his cue times in `lt`)."""
    im = field(); d = ImageDraw.Draw(im)
    fh = font(72, "ExtraBold"); fs = font(50, "Medium")
    a = ease_in_out(clamp01((t - lt[0]) / 0.30))
    draw_tracked(d, (VW / 2, 740), "VISUALIZING YOUR GOAL", fh, (255, 255, 255, int(255 * a)), 0, "c")
    stair = [("One Of The", 120), ("Most Powerful Ways", 200), ("To Motivate Yourself", 280)]
    for k, (txt, x) in enumerate(stair):
        b = ease_in_out(clamp01((t - lt[k + 1]) / 0.40))
        if b <= 0: continue
        draw_tracked(d, (x, 860 + k * 76), txt, fs, (255, 255, 255, int(255 * b)), 9)
    return im

def title_free(t):
    """'Get a Free AI Image of Yourself / with Abs': his type-in with the tracking collapsing onto the settled line,
    with a soft white glow (measured 101.25 -> settled 101.9)."""
    im = field()
    f = font(66, "Bold")
    k = ease_out_expo(clamp01(t / 0.65))
    track = 26 * (1 - k); off = 160 * (1 - k); a = 0.25 + 0.75 * k
    lines = ["Get a Free AI Image", "of Yourself with Abs"]
    def paint(d, col):
        for j, ln in enumerate(lines):
            draw_tracked(d, (VW / 2 + off, 820 + j * 92), ln, f, col or (255, 255, 255, int(255 * a)), track, "c")
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0)); paint(ImageDraw.Draw(glow), (255, 255, 255, int(110 * a)))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    paint(ImageDraw.Draw(im), None)
    return im

def endcard(t, t_second):
    im = field(); d = ImageDraw.Draw(im)
    f1 = font(68, "Bold"); f2 = font(60, "Bold")
    a = ease_in_out(clamp01(t / 0.25))
    d.text((VW / 2, 760), "See Yourself With Abs — Free", font=f1, fill=(255, 255, 255, int(255 * a)), anchor="mt")
    if t >= t_second:
        b = ease_in_out(clamp01((t - t_second) / 0.2))
        d.text((VW / 2, 880), "Tap The Button Below", font=f2, fill=(255, 255, 255, int(255 * b)), anchor="mt")
    return im

def callout_stroke(im, box, t, width=9):
    """His lime highlight box around the photo on the door, drawn on and settled."""
    d = ImageDraw.Draw(im)
    p = ease_out_cubic(clamp01(t / 0.35))
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = 1.10 - 0.10 * p
    hw, hh = (x1 - x0) / 2 * s, (y1 - y0) / 2 * s
    d.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], radius=12, outline=LIME + (int(255 * p),), width=width)
