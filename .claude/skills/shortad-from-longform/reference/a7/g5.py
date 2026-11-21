#!/usr/bin/env python3
"""Vertical (1080x1920, 29.97 fps) rebuild of MUHAMMAD's design system for Ad 5 "Every diet you've tried failed
for the same reason" (his V3 HD, 2026-09-10). Per-frame PIL functions for the Python compositor (render5.py).

Tokens are the ones measured off Muhammad's finished 16:9 cuts for the approved Ad 2 vertical (vlib.py, 2026-09-03)
and re-checked on this render: field (13,14,11) with his ~4 % grid, olive (140,153,91), card olive (90,100,58) with a
soft olive glow, black bars, white ink. Manrope throughout; his headlines are heavy oblique caps.

Layout for the phone (the vertical translation of his 16:9):
  * his TEXT LEFT / DAN RIGHT screens become DAN ABOVE (a full-width window, a DOWNSCALE of the conform) / TEXT BELOW
  * captions sit at CAP_Y = 1400 (the band caption_sync_check reads, 1385-1495); lower thirds and chips end above 1660
  * landscape media (his 16:9 stock and AI clips) sit in HIS olive card on HIS field -- the mirror of how he cards the
    portrait photos in 16:9 (skill rule 3: never a 2.7x full-bleed crop of a 16:9 source)
"""
import sys, math
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import motionlib as M
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from motionlib import font, wrap, text_size, oblique, ease_out_cubic, ease_out_expo, ease_out_back, ease_in_out, clamp01

VW, VH = 1080, 1920
FPS = 30000/1001
FIELD    = (13, 14, 11)
FIELD_HI = (23, 25, 19)
OLIVE    = (140, 153, 91)
CARD_OL  = (90, 100, 58)
INK      = (255, 255, 255)
INK_SOFT = (176, 184, 158)
RED      = (200, 30, 30)
CAP_Y  = 1400
MARGIN = 76
TOP_SAFE, BOT_SAFE = 150, 1660

# ------------------------------------------------------------------ background
_FIELD_CACHE = {}
def field(w=VW, h=VH, grid=True):
    key = (w, h, grid)
    if key in _FIELD_CACHE: return _FIELD_CACHE[key].copy()
    sm = Image.new("RGB", (54, 96)); px = sm.load()
    for y in range(96):
        for x in range(54):
            d = math.hypot((x-27)/27, (y-48)/48); k = clamp01(1 - d*0.8)
            px[x, y] = tuple(int(FIELD[i] + (FIELD_HI[i]-FIELD[i])*k) for i in range(3))
    im = sm.resize((w, h), Image.BICUBIC)
    if grid:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(g); P = 46
        for x in range(0, w, P): d.line([(x, 0), (x, h)], fill=(255, 255, 255, 9))
        for y in range(0, h, P): d.line([(0, y), (w, y)], fill=(255, 255, 255, 9))
        im = Image.alpha_composite(im.convert("RGBA"), g).convert("RGB")
    _FIELD_CACHE[key] = im
    return im.copy()

def blank(): return Image.new("RGBA", (VW, VH), (0, 0, 0, 0))

# ------------------------------------------------------------------ helpers
def rrect(im, box, radius, fill=None, outline=None, width=0, glow=0):
    if glow:
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle([box[0]-glow, box[1]-glow, box[2]+glow, box[3]+glow],
                                             radius=radius+glow, fill=OLIVE+(70,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(glow*0.9)))
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_lines(d, lines, f, x, y, fill, lead=1.12, align="l", w=None):
    lh = int(f.size*lead)
    for i, ln in enumerate(lines):
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0])//2
        d.text((xx, y + i*lh), ln, font=f, fill=fill, anchor="lt")
    return y + lh*len(lines)

def cover(img, w, h, ox=0.5, oy=0.5):
    img = M.oriented(img).convert("RGB")
    s = max(w/img.width, h/img.height)
    im = img.resize((max(1, int(round(img.width*s))), max(1, int(round(img.height*s)))), Image.LANCZOS)
    x0 = int((im.width-w)*ox); y0 = int((im.height-h)*oy)
    return im.crop((x0, y0, x0+w, y0+h))

def draw_type(d, txt, f, x, y, fill, k, tail=5, spread=0.75, cols=None):
    """Type-on reveal, every character on the BASELINE (anchor 'ls' -- skill trap 11). y = ascender line."""
    n = len(txt)
    if n == 0: return 0
    y = y + f.getmetrics()[0]; shown = k*(n+tail); ax = x
    for i, ch in enumerate(txt):
        lead = shown - i
        if lead <= 0: break
        w = text_size(ch, f)[0]
        if lead >= tail: a = 1.0; extra = 0
        else: a = clamp01(lead/tail); extra = int(w*spread*(1-a))
        base = fill if cols is None else cols[i]
        col = tuple(int(v*a) for v in base[:3]) + ((int(base[3]*a),) if len(base) > 3 else ())
        d.text((ax, y), ch, font=f, fill=col, anchor="ls"); ax += w + extra
    return ax - x

def type_lines(d, lines, f, x, y, fill, k, lead=1.14, align="l", w=None, stagger=0.55):
    lh = int(f.size*lead)
    for i, ln in enumerate(lines):
        kk = clamp01((k - i*stagger*(1.0/max(1, len(lines))))*(1+stagger))
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0])//2
        draw_type(d, ln, f, xx, y + i*lh, fill, kk)
    return y + lh*len(lines)

def fade(t, dur, tin=0.18, tout=0.14):
    a = clamp01(t/tin) if tin > 0 else 1.0
    if dur is not None: a = min(a, clamp01((dur-t)/tout) if tout > 0 else 1.0)
    return ease_in_out(a)

# ------------------------------------------------------------------ the window (Dan above, text below)
def window_rect(text_h):
    """Dan's window height from the beat's text: the text starts 74 px under the window and must END above BOT_SAFE
    (1660) -- the audit found the three-bullet builds running to y 1795 with the old 150 px allowance."""
    h = BOT_SAFE - 60 - 74 - text_h - 24
    h = max(700, min(1220, h))
    return (0, 60, VW, 60+h)

def _hole_at(rect, t, in_dur=0.42, grow=0.055):
    k = ease_out_back(clamp01(t/in_dur)) if in_dur > 0 else 1.0
    x0, y0, x1, y1 = rect; cx, cy = (x0+x1)/2, (y0+y1)/2; s = (1-grow) + grow*k
    hw, hh = (x1-x0)/2*s, (y1-y0)/2*s
    return (cx-hw, cy-hh, cx+hw, cy+hh)

def punch(plate, hole, radius):
    m = Image.new("L", plate.size, 255)
    ImageDraw.Draw(m).rounded_rectangle([int(v) for v in hole], radius=radius, fill=0)
    a = plate.getchannel("A")
    plate.putalpha(Image.composite(a, Image.new("L", plate.size, 0), m))
    return plate

def window_plate(rect, t, body=None, radius=0, in_dur=0.42, grow=0.045):
    """Opaque field plate with Dan's window punched out; body(d, im, t, ty) paints under the window."""
    im = field().convert("RGBA"); d = ImageDraw.Draw(im)
    if body: body(d, im, t, rect[3] + 74)
    return punch(im, _hole_at(rect, t, in_dur, grow), radius)

def bullets_text_h(header, items, fh, fb):
    maxw = VW - 2*MARGIN
    hl = wrap(header.upper(), fh, maxw) if header else []
    lh = int(fb.size*1.14)
    return (len(hl)*int(fh.size*1.10) + 46 if header else 0) + sum(len(wrap(it, fb, maxw))*lh + 34 for it in items)

def bullets_body(t, header, items, item_times, dur=None, tail=None, olive_items=()):
    """His bullet screen: olive caps header with an underline, then white bullets each typing on at ITS cue time.
    `tail` = an oblique olive line after the bullets (his 'COMPLETELY FREE'), (text, time)."""
    fh, fb = font(46, "ExtraBold"), font(50, "SemiBold"); maxw = VW - 2*MARGIN
    hl = wrap(header.upper(), fh, maxw) if header else []
    hlh, lh = int(fh.size*1.10), int(fb.size*1.14)
    def body(d, im, tt, ty):
        a = fade(tt, dur, tin=0.01, tout=0.14) if dur else 1.0
        if header:
            k = clamp01((tt-0.08)/0.42); wdt = 0
            for n_, h in enumerate(hl):
                wdt = max(wdt, draw_type(d, h, fh, MARGIN, ty + n_*hlh, OLIVE+(int(255*a),), clamp01((k-n_*0.25)*1.4)))
            yb = ty + (len(hl)-1)*hlh + fh.size + 16
            d.rectangle([MARGIN, yb, MARGIN+int(wdt*clamp01(k*1.2)), yb+6], fill=OLIVE+(int(255*a),))
            ty += len(hl)*hlh + 46
        for n, it in enumerate(items):
            k = clamp01((tt - item_times[n])/1.0)
            if k <= 0: break
            lines = wrap(it, fb, maxw)
            col = OLIVE if n in olive_items else INK
            d.rectangle([MARGIN, ty+18, MARGIN+14, ty+32], fill=tuple(int(v*clamp01(k*4)*a) for v in OLIVE))
            type_lines(d, lines, fb, MARGIN+38, ty, col+(int(255*a),), k, lead=1.14)
            ty += len(lines)*lh + 34
        if tail and tt >= tail[1]:
            k = clamp01((tt - tail[1])/0.5); ft = font(58, "ExtraBold")
            lay = blank(); dd = ImageDraw.Draw(lay)
            draw_type(dd, tail[0], ft, MARGIN+38, ty+10, OLIVE+(int(255*a),), k)
            im.alpha_composite(oblique(lay, 9.0, pivot_y=ty+40))
    return body, bullets_text_h(header, items, fh, fb) + (90 if tail else 0)

# ------------------------------------------------------------------ cards (media in his olive card on the field)
def card_hole(media_ar, has_text=False, top=150, bot=None):
    maxw = VW - 2*40
    bot = bot or (1330 if not has_text else 1240)
    maxh = bot - top; w, h = maxw, maxw/media_ar
    if h > maxh: h, w = maxh, maxh*media_ar
    cx, cy = VW//2, top + maxh/2
    w, h = int(w)//2*2, int(h)//2*2          # EVEN: an odd-width crop on yuv420p is rounded by ffmpeg and the raw
    return (cx - w//2, int(cy - h/2), cx + w//2, int(cy - h/2) + h)   # frames then shear (fatdan card, 2026-09-10)

def card_plate(hole, t, caption=None, caption_style="italic", in_dur=0.42, radius=20, dur=None):
    """The olive-glow card on the field with the media hole punched. `caption`: his oblique olive line under the
    card (AI PICTURE OF MYSELF WITH THE BODY I WANTED), typing on."""
    im = field().convert("RGBA"); d = ImageDraw.Draw(im)
    h = _hole_at(hole, t, in_dur)
    rrect(im, [h[0]-14, h[1]-14, h[2]+14, h[3]+14], 30, fill=CARD_OL+(255,), glow=26)
    if caption:
        fc = font(44, "ExtraBold"); k = clamp01((t-0.25)/0.9)
        lines = wrap(caption.upper(), fc, VW-2*MARGIN)
        lay = blank(); dd = ImageDraw.Draw(lay); y = hole[3] + 54
        for n, ln in enumerate(lines):
            draw_type(dd, ln, fc, (VW - text_size(ln, fc)[0])//2, y + n*int(fc.size*1.15), OLIVE+(255,), clamp01((k-n*0.2)*1.3))
        im.alpha_composite(oblique(lay, 9.0, pivot_y=y + len(lines)*int(fc.size*1.15)/2))
    return punch(im, h, radius)

def ai_chip(im, x_right, y_bottom, size=34, txt="AI-GENERATED"):
    """His AI-GENERATED chip: black rounded box, white Manrope, bottom-right of the media, never over a face."""
    fl = font(size, "SemiBold"); lw, lh = text_size(txt, fl)
    bx, by = int(x_right - lw - 34), int(y_bottom - lh - 22)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx+lw+34, by+lh+22], radius=9, fill=(0, 0, 0, 215))
    d.text((bx+17, by+11), txt, font=fl, fill=INK+(255,), anchor="lt")

def ai_chip_bleed(im, y=None, size=54):
    """His full-frame label: top-left, larger. Placed just under the top safe area."""
    fl = font(size, "SemiBold"); lw, lh = text_size("AI-GENERATED", fl)
    bx, by = 44, (y if y is not None else TOP_SAFE + 10)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx+lw+40, by+lh+26], radius=10, fill=(0, 0, 0, 215))
    d.text((bx+20, by+13), "AI-GENERATED", font=fl, fill=INK+(255,), anchor="lt")

# ------------------------------------------------------------------ overlays on the talking head
def lower_third(lines, t, dur, y_bottom=1600, weights=None, sizes=None):
    """His olive tab + black bar + white type, letter by letter. Line 0 regular, line 1 bold (his pattern), or as given."""
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
    o = 1.0 - ease_in_out(clamp01((t-(dur-0.12))/0.12)); gw = ease_out_cubic(clamp01(t/0.34))   # his bars hold to the end; a 3-frame out
    d.rounded_rectangle([bx-TAB-14, by, bx-14, by+bh], radius=8, fill=OLIVE+(int(235*o*gw),))
    d.rounded_rectangle([bx, by, bx+int(bw*gw), by+bh], radius=8, fill=(0, 0, 0, int(232*o)))
    yy = by + 17
    for n, (s, f, lh) in enumerate(zip(lines, fs, lhs)):
        k = clamp01((t - 0.20 - n*0.55)/0.80)
        draw_type(d, s, f, bx + (bw - text_size(s, f)[0])//2, yy, INK+(int(255*o),), k); yy += lh
    return im

def day_chip(label, text, t, dur, y_bottom=1600):
    """His 'Day 1 | You're motivated' device: olive chip with the day, black bar with the line typing on."""
    fl, ft = font(50, "ExtraBold"), font(46, "SemiBold")
    lw = text_size(label, fl)[0] + 64; tw = min(text_size(text, ft)[0] + 90, VW - 2*40 - lw - 12)
    h = 96; total = lw + 12 + tw; x0 = (VW-total)//2; y0 = y_bottom - h
    im = blank(); d = ImageDraw.Draw(im)
    o = 1.0 - ease_in_out(clamp01((t-(dur-0.12))/0.12)); g = ease_out_cubic(clamp01(t/0.30))
    d.rounded_rectangle([x0, y0, x0+lw, y0+h], radius=10, fill=OLIVE+(int(245*o*g),))
    d.text((x0+lw//2, y0+h//2), label, font=fl, fill=INK+(int(255*o*g),), anchor="mm")
    d.rounded_rectangle([x0+lw+12, y0, x0+lw+12+int(tw*g), y0+h], radius=10, fill=(0, 0, 0, int(232*o)))
    k = clamp01((t-0.15)/min(0.75, max(0.25, dur-0.40)))          # the line always finishes typing before the chip goes (audit: Day 3's second line never did)
    draw_type(d, text, ft, x0+lw+12+45, y0 + (h - ft.size)//2 - 4, INK+(int(255*o),), k)
    return im

def cta_pill(top, big, t, dur, y=None, big_size=70):
    ft, fb = font(40, "SemiBold"), font(big_size, "ExtraBold")
    tl = wrap(top, ft, VW-2*MARGIN-80) if top else []; bl = wrap(big, fb, VW-2*MARGIN-80)
    w = min(max([text_size(x, ft)[0] for x in tl] + [text_size(x, fb)[0] for x in bl]) + 96, VW-2*46)
    h = len(tl)*int(ft.size*1.2) + len(bl)*int(fb.size*1.12) + 62
    y = y if y is not None else CAP_Y - h//2
    k = ease_out_back(clamp01(t/0.40)); o = 1.0 - ease_in_out(clamp01((t-(dur-0.30))/0.30))
    im = blank(); ww, hh = int(w*(0.94+0.06*k)), int(h*(0.94+0.06*k)); bx, by = (VW-ww)//2, y+(h-hh)//2
    rrect(im, [bx, by, bx+ww, by+hh], 26, fill=OLIVE+(int(255*o),), glow=16)
    d = ImageDraw.Draw(im); yy = by+30
    if tl: yy = draw_lines(d, tl, ft, bx, yy, (255, 255, 255, int(255*o)), lead=1.2, align="c", w=ww) + 6
    draw_lines(d, bl, fb, bx, yy, (255, 255, 255, int(255*o)), lead=1.12, align="c", w=ww)
    return im

# ------------------------------------------------------------------ the hook's note + title
DIETS = ["Keto", "Intermittent Fasting", "Paleo", "Calorie Counting", "Carnivore"]
def note_title(t, strike_times, dur, x=MARGIN, y=1040):
    """His skip-stopper: a pinned paper note listing five diets, each struck through in red at its cue, and the
    heavy oblique 'WHY ARE DIETS / FAILING YOU?' with an olive rule. Drawn on the field under Dan's window."""
    im = blank(); d = ImageDraw.Draw(im)
    a = fade(t, dur, tin=0.25, tout=0.16)
    # the note
    fn = font(32, "SemiBold"); nw, nh = 430, 48 + len(DIETS)*44
    note = Image.new("RGBA", (nw, nh), (0, 0, 0, 0)); dn = ImageDraw.Draw(note)
    dn.rounded_rectangle([0, 0, nw-1, nh-1], radius=6, fill=(246, 244, 236, int(255*a)))
    for i, s in enumerate(DIETS):
        yy = 30 + i*44
        dn.rectangle([26, yy+12, 34, yy+20], fill=(20, 20, 20, int(255*a)))
        dn.text((48, yy), s, font=fn, fill=(24, 24, 24, int(255*a)), anchor="lt")
        k = clamp01((t - strike_times[i])/0.22)
        if k > 0:
            tw = text_size(s, fn)[0]
            dn.line([(44, yy+19), (44+int((tw+12)*k), yy+15)], fill=RED+(int(255*a),), width=6)
    note = note.rotate(3.5, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", note.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, int(120*a)), [0, 0, note.width, note.height], note.getchannel("A"))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x+6, y+14)); im.alpha_composite(note, (x, y))
    # the pin
    d.ellipse([x+nw//2-12, y-8, x+nw//2+12, y+16], fill=(190, 40, 40, int(255*a)))
    # the title, right of the note
    ft = font(64, "ExtraBold"); lay = blank(); dt = ImageDraw.Draw(lay)
    tx, ty = x + nw + 40, y + 40
    k = clamp01((t-0.15)/0.7)
    for n, ln in enumerate(["WHY ARE DIETS", "FAILING YOU?"]):
        draw_type(dt, ln, ft, tx, ty + n*int(ft.size*1.05), INK+(int(255*a),), clamp01((k-n*0.3)*1.4))
    im.alpha_composite(oblique(lay, 9.0, pivot_y=ty+ft.size))
    d = ImageDraw.Draw(im)
    d.rectangle([tx, ty + 2*int(ft.size*1.05) + 12, tx + int(430*clamp01(k*1.2)), ty + 2*int(ft.size*1.05) + 18], fill=OLIVE+(int(255*a),))
    return im

# ------------------------------------------------------------------ title cards
def title_card(headline, sub, t, dur=None):
    """His 'THERE'S A SECOND REASON' beat: olive card on the field, heavy oblique caps typing on, subtitle under."""
    fh, fs = font(96, "ExtraBold"), font(46, "SemiBold")
    hl = wrap(headline.upper(), fh, VW-2*150); sl = wrap(sub, fs, VW-2*150) if sub else []
    lh, ls = int(fh.size*1.06), int(fs.size*1.20)
    inner = len(hl)*lh + (40+len(sl)*ls if sl else 0); ch = inner + 150
    box = (72, (VH-ch)//2 - 120, VW-72, (VH-ch)//2 - 120 + ch)
    im = field().convert("RGBA")
    k0 = ease_out_back(clamp01(t/0.40)); o = fade(t, dur, tin=0.01, tout=0.2) if dur else 1.0
    cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
    hw, hh = (box[2]-box[0])/2*(0.94+0.06*k0), (box[3]-box[1])/2*(0.94+0.06*k0)
    rrect(im, [cx-hw, cy-hh, cx+hw, cy+hh], 30, fill=CARD_OL+(int(255*o),), glow=26)
    lay = blank(); d = ImageDraw.Draw(lay); y = box[1] + 75
    for n, ln in enumerate(hl):
        draw_type(d, ln, fh, (VW - text_size(ln, fh)[0])//2, y, INK+(int(255*o),), clamp01((t-0.18-n*0.26)/0.62)); y += lh
    im.alpha_composite(oblique(lay, 9.0, pivot_y=box[1]+75+len(hl)*lh/2))
    if sl:
        y += 40; d2 = ImageDraw.Draw(im)
        for n, ln in enumerate(sl):
            draw_type(d2, ln, fs, (VW - text_size(ln, fs)[0])//2, y, INK+(int(255*o),), clamp01((t-0.55-n*0.18)/0.55)); y += ls
    return im

def why_card(photo, t, headline=("WHY DIETS HAVE", "FAILED YOU"), sub="Even though you're trying your hardest to eat healthy"):
    """His 34.5-39.8 card: the deckchair photo and the oblique headline share one olive card. Vertical: photo on top,
    the headline + sub under it, all inside the card."""
    fh, fs = font(72, "ExtraBold"), font(42, "SemiBold")
    box = (60, 150, VW-60, 1330)
    im = field().convert("RGBA")
    k0 = ease_out_back(clamp01(t/0.40)); cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
    hw, hh = (box[2]-box[0])/2*(0.94+0.06*k0), (box[3]-box[1])/2*(0.94+0.06*k0)
    rrect(im, [cx-hw, cy-hh, cx+hw, cy+hh], 30, fill=CARD_OL+(255,), glow=26)
    # photo (portrait) in the upper part of the card, his blur-in
    ph = 640; pw = int(ph*photo.width/photo.height)
    p = cover(photo, pw, ph); bl = 18*(1-ease_out_cubic(clamp01((t-0.05)/0.55)))
    if bl > 0.5: p = p.filter(ImageFilter.GaussianBlur(bl))
    px0, py0 = int(cx - pw/2), box[1] + 60
    im.paste(p, (px0, py0))
    lay = blank(); d = ImageDraw.Draw(lay); y = py0 + ph + 60
    for n, ln in enumerate(headline):
        draw_type(d, ln, fh, (VW - text_size(ln, fh)[0])//2, y + n*int(fh.size*1.04), INK+(255,), clamp01((t-0.2-n*0.3)/0.7))
    im.alpha_composite(oblique(lay, 9.0, pivot_y=y+fh.size))
    d2 = ImageDraw.Draw(im); y2 = y + 2*int(fh.size*1.04) + 26
    for n, ln in enumerate(wrap(sub, fs, box[2]-box[0]-120)):
        draw_type(d2, ln, fs, (VW - text_size(ln, fs)[0])//2, y2 + n*int(fs.size*1.2), INK+(255,), clamp01((t-0.9-n*0.25)/0.7))
    return im

# ------------------------------------------------------------------ phones
def phone_frame(screen, w=620, notch=True):
    """A phone mockup: black rounded bezel, the screen image cover-fitted inside, a pill notch. Returns RGBA."""
    r = 19.5/9; h = int(w*r); bz = 14
    im = Image.new("RGBA", (w+2*bz, h+2*bz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w+2*bz-1, h+2*bz-1], radius=int(w*0.15), fill=(18, 18, 20, 255))
    sc = cover(screen, w, h); m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w-1, h-1], radius=int(w*0.12), fill=255)
    im.paste(sc, (bz, bz), m)
    if notch: d.rounded_rectangle([bz+w//2-70, bz+16, bz+w//2+70, bz+50], radius=17, fill=(10, 10, 12, 255))
    return im

def lockscreen(goal, t, w=560):
    """His lock-screen phone: the goal image as wallpaper, 'Tue Apr 1' and a big thin clock, the two bottom controls."""
    r = 19.5/9; h = int(w*r); sc = cover(goal, w, h).convert("RGBA"); d = ImageDraw.Draw(sc)
    fd, fc = font(26, "SemiBold"), font(150, "ExtraLight")
    d.text((w//2, 96), "Tue Apr 1", font=fd, fill=(255, 255, 255, 235), anchor="mt")
    d.text((w//2, 128), "9:41", font=fc, fill=(255, 255, 255, 225), anchor="mt")
    for cx in (w*0.2, w*0.8):
        d.ellipse([cx-32, h-110, cx+32, h-46], fill=(40, 40, 44, 200))
    d.rounded_rectangle([w//2-80, h-22, w//2+80, h-14], radius=4, fill=(255, 255, 255, 220))
    return phone_frame(sc, w)

def flash(frame_rgb, k):
    """A screen blend toward white (k = 1 is pure white). Applied per frame from his measured envelope."""
    import numpy as np
    a = np.asarray(frame_rgb, dtype=np.float32)/255.0
    return ((1 - (1-a)*(1-k))*255).clip(0, 255).astype("uint8")
