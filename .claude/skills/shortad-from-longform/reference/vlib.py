#!/usr/bin/env python3
"""Vertical (1080x1920) rebuild of Muhammad's design system.

Every token below was MEASURED off his finished 16:9 cut (see gradefit2.py / the palette
probe), not guessed: field #0D0E0B, sage accent #8C995B, card olive #5A643A, black bars,
white ink, a ~4% grid on the field, rounded cards with a soft glow.

The layouts are NOT his layouts scaled down. His frame puts text LEFT and Dan RIGHT; a
9:16 frame has no left/right to give, so the same relationship is rebuilt as Dan ABOVE
and text BELOW. The window height adapts to how much text a beat carries, which is what
keeps Dan large on short beats instead of locking one compromise size for all of them.
"""
import sys, os, math
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import motionlib as M
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, wrap, text_size, text_bbox, oblique, drop_shadow, nframes, encode
from motionlib import ease_out_cubic, ease_out_expo, ease_out_back, ease_in_out, clamp01

VW, VH = 1080, 1920
FPS = 30000/1001

FIELD    = (13, 14, 11)
FIELD_HI = (23, 25, 19)
OLIVE    = (140, 153, 91)
CARD_OL  = (90, 100, 58)
INK      = (255, 255, 255)
INK_SOFT = (176, 184, 158)
BAR      = (0, 0, 0)

# --- vertical safe area -------------------------------------------------------
# YouTube Shorts overlays the bottom ~230 px and the right ~120 px; IG Reels takes
# ~350 px of bottom. Nothing that must be READ goes below y=1660, and the caption band
# sits at y=1250 so it clears both. Graphics that carry their own words suppress the
# captions for their duration -- two text systems in a 1080-wide frame is unreadable.
TOP_SAFE, BOT_SAFE = 150, 1660
# The caption band sits LOW, not at mid-frame: at 1250 it forced every card to end by
# 1150 and a card that ends at 1150 leaves the bottom third of the phone empty. 1400 puts
# the caption's own bottom edge at ~1465 -- clear of both YouTube Shorts' bottom 230 px
# and IG Reels' 350 px -- and gives the cards 230 px more height.
CAP_Y = 1400
MARGIN = 76

# ------------------------------------------------------------------ background
_FIELD_CACHE = {}
def field(w=VW, h=VH, grid=True):
    """Dark field + radial lift + the fine grid he uses on every graphic screen."""
    key = (w, h, grid)
    if key in _FIELD_CACHE: return _FIELD_CACHE[key].copy()
    sm = Image.new("RGB", (54, 96)); px = sm.load()
    for y in range(96):
        for x in range(54):
            d = math.hypot((x-27)/27, (y-48)/48)
            k = clamp01(1 - d*0.8)
            px[x, y] = tuple(int(FIELD[i] + (FIELD_HI[i]-FIELD[i])*k) for i in range(3))
    im = sm.resize((w, h), Image.BICUBIC)
    if grid:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        P = 46                                   # ~4.3% of width == his 73px at 1920
        for x in range(0, w, P): d.line([(x, 0), (x, h)], fill=(255, 255, 255, 9))
        for y in range(0, h, P): d.line([(0, y), (w, y)], fill=(255, 255, 255, 9))
        im = Image.alpha_composite(im.convert("RGBA"), g).convert("RGB")
    _FIELD_CACHE[key] = im
    return im.copy()

def vignette_mask(w=VW, h=VH):
    """His radial falloff, remapped into the vertical frame's own coordinates."""
    from grade import VIGNETTE
    import numpy as np
    ys, xs = np.mgrid[0:h, 0:w]
    r = np.hypot((xs-w/2)/(w/2), (ys-h/2)/(h/2))
    rr = np.array([p[0] for p in VIGNETTE]); gg = np.array([p[1] for p in VIGNETTE])
    return np.interp(r, rr, gg).astype("float32")

# ------------------------------------------------------------------ helpers
def rrect(im, box, radius, fill=None, outline=None, width=0, glow=0):
    if glow:
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle(
            [box[0]-glow, box[1]-glow, box[2]+glow, box[3]+glow],
            radius=radius+glow, fill=OLIVE+(70,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(glow*0.9)))
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, fill=fill,
                                         outline=outline, width=width)

def block(lines, f, lead=1.12):
    """(height, line_height) for a wrapped block drawn with anchor='lt'."""
    lh = int(f.size * lead)
    return lh * len(lines), lh

def draw_lines(d, lines, f, x, y, fill, lead=1.12, align="l", w=None):
    lh = int(f.size*lead)
    for i, ln in enumerate(lines):
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0])//2
        d.text((xx, y + i*lh), ln, font=f, fill=fill, anchor="lt")
    return y + lh*len(lines)

def cover(img, w, h):
    """Fill (w,h), cropping the overflow -- never letterbox a photo onto the field."""
    img = M.oriented(img).convert("RGB")
    s = max(w/img.width, h/img.height)
    im = img.resize((max(1,int(img.width*s)), max(1,int(img.height*s))), Image.LANCZOS)
    return im.crop(((im.width-w)//2, (im.height-h)//2, (im.width-w)//2+w, (im.height-h)//2+h))

def contain(img, w, h):
    img = M.oriented(img).convert("RGB")
    s = min(w/img.width, h/img.height)
    return img.resize((max(1,int(img.width*s)), max(1,int(img.height*s))), Image.LANCZOS)

# ------------------------------------------------------------------ window sizing
def window_rect(text_h):
    """Dan's window: as tall as the beat's text will allow, clamped so he never shrinks
    into a talking postage stamp and never crowds the text off the safe area."""
    h = VH - TOP_SAFE//2 - text_h - 150
    h = max(820, min(1220, h))
    return (0, 60, VW, 60+h)

def window_crop(win_h):
    """Source crop (in the 1920x1080 conform) that fills a full-width window of win_h.
    Height is always the full 1080, so the window is a DOWNSCALE -- pixel-sharp, unlike
    the 1.78x upscale the full-bleed mode is forced into."""
    from grade import SUBJECT_CX
    w = int(round(1080 * (VW/win_h)))
    w = min(w, 1920) - (min(w,1920) % 2)
    x = int(round(SUBJECT_CX - w/2))
    x = max(0, min(x, 1920-w))
    return (w, 1080, x, 0)

# ==============================================================================
#  BEAT PLATES
#  Every beat renders ONE RGBA plate that is opaque everywhere except a rounded
#  "media hole". Whatever belongs in the hole -- Dan's window, a photo, a clip --
#  is composited UNDERNEATH at the hole's final size. Animating the hole instead of
#  the media means a card can grow open without ever rescaling the picture inside it.
# ==============================================================================

def _hole_at(rect, t, in_dur=0.42, grow=0.055):
    """Hole rect at time t: opens from `grow` smaller with an ease-out-back settle."""
    k = ease_out_back(clamp01(t/in_dur)) if in_dur > 0 else 1.0
    x0, y0, x1, y1 = rect
    cx, cy = (x0+x1)/2, (y0+y1)/2
    s = (1-grow) + grow*k
    hw, hh = (x1-x0)/2*s, (y1-y0)/2*s
    return (cx-hw, cy-hh, cx+hw, cy+hh)

def _punch(plate, hole, radius):
    """Cut the hole out of an opaque plate."""
    m = Image.new("L", plate.size, 255)
    ImageDraw.Draw(m).rounded_rectangle([int(v) for v in hole], radius=radius, fill=0)
    a = plate.getchannel("A").point(lambda v: v)
    plate.putalpha(Image.composite(a, Image.new("L", plate.size, 0), m))
    return plate

def plate_window(header, bullets, dur, fps=FPS, radius=0, stagger=0.55):
    """Dan ABOVE, olive eyebrow + white bullets BELOW -- the vertical form of his
    'bullets left / Dan right' screen. Returns (frames, hole_rect)."""
    fh   = font(46, "ExtraBold")
    fb   = font(50, "SemiBold")
    maxw = VW - MARGIN*2
    items = [wrap(b, fb, maxw) for b in bullets]
    lh    = int(fb.size*1.14)
    text_h = (36 + 30) + sum(len(it)*lh + 34 for it in items)
    rect = window_rect(text_h)
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        d  = ImageDraw.Draw(im)
        ty = rect[3] + 74
        if header:
            k = ease_out_expo(clamp01((t-0.10)/0.45))
            d.text((MARGIN, ty), header.upper(), font=fh, fill=OLIVE, anchor="lt")
            hw = text_size(header.upper(), fh)[0]
            d.rectangle([MARGIN, ty+fh.size+16, MARGIN+int(hw*k), ty+fh.size+22], fill=OLIVE)
            ty += fh.size + 56
        for n, lines in enumerate(items):
            a = ease_out_cubic(clamp01((t - (0.35 + n*stagger))/0.42))
            if a <= 0: break
            dy = int((1-a)*26)
            col = tuple(int(v*a) for v in INK)
            d.rectangle([MARGIN, ty+dy+18, MARGIN+14, ty+dy+32],
                        fill=tuple(int(v*a) for v in OLIVE))
            draw_lines(d, lines, fb, MARGIN+38, ty+dy, col, lead=1.14)
            ty += len(lines)*lh + 34
        out.append(_punch(im, _hole_at(rect, t), radius))
    return out, rect

def card_hole(media_ar, has_text):
    """Biggest card that fits the media's OWN aspect ratio.

    A fixed 16:9 hole cover-crops a portrait photo, and the thing it crops off a photo of
    a person is their head. Size the hole from the media, never the other way round."""
    # The card must END ABOVE THE CAPTION BAND. A card sized to the full frame height put
    # its bottom third under the captions, and a white app screen behind white captions is
    # unreadable. Cards that carry their OWN text get the extra room instead, and suppress
    # the captions for their duration.
    maxw = VW - 2*40
    top, bot = 150, (1330 if not has_text else 1240)
    maxh = bot - top
    w, h = maxw, maxw/media_ar
    if h > maxh: h, w = maxh, maxh*media_ar
    cx, cy = VW//2, top + maxh/2
    return (int(cx-w/2), int(cy-h/2), int(cx+w/2), int(cy+h/2))

def plate_card(dur, caption=None, label=None, portrait=False, fps=FPS,
               top_kicker=None, hole=None, media_ar=None):
    """A photo / clip / phone screen inside his olive-glow card on the field."""
    if hole is None:
        if media_ar is None: media_ar = 0.62 if portrait else 16/9
        hole = card_hole(media_ar, bool(caption or top_kicker))
    fc = font(44, "SemiBold"); fk = font(40, "ExtraBold"); fl = font(30, "SemiBold")
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        d  = ImageDraw.Draw(im)
        h  = _hole_at(hole, t)
        rrect(im, [h[0]-14, h[1]-14, h[2]+14, h[3]+14], 30, fill=CARD_OL+(255,), glow=26)
        ty = hole[3] + 54
        if top_kicker:
            k = ease_out_expo(clamp01((t-0.10)/0.42))
            kf = font(76, "ExtraBold")
            lay = Image.new("RGBA", (VW, VH), (0,0,0,0))
            lines = wrap(top_kicker.upper(), kf, VW-2*MARGIN)
            draw_lines(ImageDraw.Draw(lay), lines, kf, MARGIN, ty,
                       tuple(int(v*k) for v in OLIVE), lead=1.06, align="c", w=VW-2*MARGIN)
            hgt = len(lines)*int(kf.size*1.06)
            im.alpha_composite(oblique(lay, 9.0, pivot_y=ty+hgt/2))
            wdt = max(text_size(x, kf)[0] for x in lines)
            d.rectangle([(VW-wdt)//2, ty+hgt+10, (VW-wdt)//2+int(wdt*k), ty+hgt+17], fill=OLIVE)
            ty += hgt + 44
        if caption:
            k = ease_out_cubic(clamp01((t-0.30)/0.42))
            lines = wrap(caption, fc, VW-2*MARGIN)
            draw_lines(d, lines, fc, MARGIN, ty+int((1-k)*18),
                       tuple(int(v*k) for v in INK), lead=1.14, align="c", w=VW-2*MARGIN)
        out.append(_punch(im, h, 20))
        if label:                                     # AI-GENERATED chip, inside the card
            lw, lh_ = text_size(label, fl)
            lay = Image.new("RGBA", (VW, VH), (0,0,0,0))
            bx = (VW-(lw+34))//2
            by = int(h[3]) - lh_ - 40
            ImageDraw.Draw(lay).rounded_rectangle([bx, by, bx+lw+34, by+lh_+22], radius=9,
                                                  fill=(0,0,0,215))
            ImageDraw.Draw(lay).text((bx+17, by+11), label, font=fl, fill=INK, anchor="lt")
            out[-1].alpha_composite(lay)
    return out, hole

def plate_title(headline, sub=None, dur=3.0, fps=FPS, accent_words=()):
    """Full-field title card: heavy oblique caps, his 'VISUALIZING YOUR GOAL' screen."""
    fh = font(112, "ExtraBold"); fs = font(46, "SemiBold")
    lines = wrap(headline.upper(), fh, VW-2*54)
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        lay = Image.new("RGBA", (VW, VH), (0,0,0,0)); d = ImageDraw.Draw(lay)
        lh = int(fh.size*1.04)
        blk = len(lines)*lh + (0 if not sub else 40 + int(fs.size*1.15)*len(wrap(sub, fs, VW-2*MARGIN)))
        y0 = (VH - blk)//2 - 60
        for n, ln in enumerate(lines):
            a = ease_out_expo(clamp01((t - n*0.10)/0.5))
            x = 54 + (VW-108 - text_size(ln, fh)[0])//2 - int((1-a)*40)
            d.text((x, y0+n*lh), ln, font=fh, fill=tuple(int(v*a) for v in INK), anchor="lt")
        lay = oblique(lay, 9.0, pivot_y=y0 + len(lines)*lh/2)
        im.alpha_composite(lay)
        if sub:
            a = ease_out_cubic(clamp01((t-0.35)/0.45))
            sl = wrap(sub, fs, VW-2*MARGIN)
            draw_lines(ImageDraw.Draw(im), sl, fs, MARGIN, y0+len(lines)*lh+46+int((1-a)*16),
                       tuple(int(v*a) for v in INK_SOFT), lead=1.15, align="c", w=VW-2*MARGIN)
        out.append(im)
    return out, None

def plate_statement(parts, dur=3.0, fps=FPS):
    """Mixed-weight statement on the field -- his 'Chat GPT / General Purpose AI' screen.
    `parts` is a list of (text, 'ink'|'olive'|'big') runs, laid out as wrapped lines."""
    fbig = font(78, "ExtraBold"); fmid = font(60, "SemiBold")
    out = []
    lines = []
    for txt, kind in parts:
        f = fbig if kind in ("big", "olive") else fmid
        col = OLIVE if kind == "olive" else INK
        for ln in wrap(txt, f, VW-2*MARGIN):
            lines.append((ln, f, col))
    tot = sum(int(f.size*1.14) for _, f, _ in lines)
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA"); d = ImageDraw.Draw(im)
        y = (VH-tot)//2 - 40
        for n, (ln, f, col) in enumerate(lines):
            a = ease_out_expo(clamp01((t - n*0.09)/0.46))
            d.text((MARGIN - int((1-a)*30), y), ln, font=f,
                   fill=tuple(int(v*a) for v in col), anchor="lt")
            y += int(f.size*1.14)
        out.append(im)
    return out, None

def overlay_cta(top, big, dur, fps=FPS, y=None):
    """His sage CTA pill. RGBA overlay -- it sits ON Dan, it does not replace him."""
    ft = font(40, "SemiBold"); fb = font(70, "ExtraBold")
    tl = wrap(top, ft, VW-2*MARGIN-80); bl = wrap(big, fb, VW-2*MARGIN-80)
    w = max([text_size(x, ft)[0] for x in tl] + [text_size(x, fb)[0] for x in bl]) + 96
    w = min(w, VW-2*46)
    h = len(tl)*int(ft.size*1.2) + len(bl)*int(fb.size*1.12) + 62
    y = y if y is not None else CAP_Y - h//2
    x = (VW-w)//2
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        k = ease_out_back(clamp01(t/0.40))
        o = 1.0 - ease_in_out(clamp01((t-(dur-0.30))/0.30))
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        ww, hh = int(w*(0.94+0.06*k)), int(h*(0.94+0.06*k))
        bx, by = (VW-ww)//2, y+(h-hh)//2
        rrect(im, [bx, by, bx+ww, by+hh], 26, fill=OLIVE+(int(255*o),), glow=16)
        d = ImageDraw.Draw(im)
        yy = by+30
        yy = draw_lines(d, tl, ft, bx, yy, (255,255,255,int(255*o)), lead=1.2, align="c", w=ww)
        draw_lines(d, bl, fb, bx, yy+6, (255,255,255,int(255*o)), lead=1.12, align="c", w=ww)
        out.append(im)
    return out, None

def overlay_callout(rect, dur, fps=FPS, draw_dur=0.5):
    """Animated stroke box -- his highlight on the photo taped to the door."""
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        p = ease_out_cubic(clamp01(t/draw_dur))
        o = 1.0 - ease_in_out(clamp01((t-(dur-0.28))/0.28))
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        x0, y0, x1, y1 = rect
        cx, cy = (x0+x1)/2, (y0+y1)/2
        hw, hh = (x1-x0)/2*(1.10-0.10*p), (y1-y0)/2*(1.10-0.10*p)
        ImageDraw.Draw(im).rounded_rectangle(
            [cx-hw, cy-hh, cx+hw, cy+hh], radius=14, outline=OLIVE+(int(255*o),), width=7)
        out.append(im)
    return out, None


# ==============================================================================
#  ATTEMPT 2 ADDITIONS -- measured off his finished cut, not invented
#
#  Three things attempt 1 did not have, all visible in his render:
#   1. every piece of type ARRIVES LETTER BY LETTER, the unsettled tail spaced wide and
#      dim (his "IN TODAY'S EPISODE", "VISUALIZING YOUR GOAL" and all seven lower thirds
#      do this; attempt 1 slid whole lines up instead);
#   2. he carries SEVEN LOWER THIRDS on the talking head -- attempt 1 had none;
#   3. eight beat changes are covered by a WHITE LIGHT-LEAK FLASH, not a hard cut.
# ==============================================================================

def draw_type(d, txt, f, x, y, fill, k, tail=5, spread=0.75, anchor_w=None):
    """Type-on reveal. Returns the settled width.

    The settled prefix never moves -- only the tail is spaced out -- so the line does not
    crawl sideways as it lands. `anchor_w` centres on the FINAL width for the same reason.

    ⚠ EVERY CHARACTER IS DRAWN ON THE BASELINE (anchor="ls"), NOT anchor="lt".
    PIL's "t" anchor is the ascender line OF THE STRING IT IS GIVEN, so drawing one
    character at a time with "lt" aligns each glyph by its own top: periods ride up to
    cap height, commas turn into apostrophes, and every ascender-less letter drops. The
    first full-resolution frame of attempt 2 had "moțivation ... sįx-pack abs·" burned
    into the bullets, and nothing in the metric gate can see it. `y` still means the same
    thing it does for a whole-string "lt" draw -- the ascender line -- so the baseline is
    y + ascent.
    """
    n = len(txt)
    if n == 0: return 0
    y = y + f.getmetrics()[0]
    shown = k * (n + tail)
    ax = x
    for i, ch in enumerate(txt):
        lead = shown - i
        if lead <= 0: break
        w = text_size(ch, f)[0]
        if lead >= tail:                       # settled
            a = 1.0; extra = 0
        else:
            a = clamp01(lead / tail)
            extra = int(w * spread * (1 - a))
        col = tuple(int(v * a) for v in fill[:3]) + ((int(fill[3]*a),) if len(fill) > 3 else ())
        d.text((ax, y), ch, font=f, fill=col, anchor="ls")
        ax += w + extra
    return ax - x

def type_lines(d, lines, f, x, y, fill, k, lead=1.14, align="l", w=None, stagger=0.55):
    """Several wrapped lines revealed one after another."""
    lh = int(f.size * lead)
    for i, ln in enumerate(lines):
        kk = clamp01((k - i * stagger * (1.0 / max(1, len(lines)))) * (1 + stagger))
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0]) // 2
        draw_type(d, ln, f, xx, y + i * lh, fill, kk)
    return y + lh * len(lines)

# ------------------------------------------------------------------ split layouts
#  His frame is TEXT LEFT / DAN RIGHT. A 9:16 frame has no left and right to give, so the
#  same relationship becomes DAN ABOVE / TEXT BELOW. The window height adapts to how much
#  the beat has to say, which is what keeps him large on short beats.

def _win_plate(dur, body, fps=FPS, text_h=0, radius=0, grow=0.045, in_dur=0.42):
    """Shared frame loop for the split layouts. `body(draw, im, t, y0)` paints under the
    window; `text_h` sizes the window."""
    rect = window_rect(text_h)
    out = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = field().convert("RGBA")
        d = ImageDraw.Draw(im)
        body(d, im, t, rect[3] + 74)
        out.append(_punch(im, _hole_at(rect, t, in_dur, grow), radius))
    return out, rect

def plate_window(header, bullets, dur, fps=FPS, radius=0, stagger=0.62, reveal=1.05):
    """Dan ABOVE, olive eyebrow + white bullets BELOW -- his 'IN TODAY'S EPISODE' screen."""
    fh, fb = font(46, "ExtraBold"), font(50, "SemiBold")
    maxw = VW - MARGIN*2
    items = [wrap(b, fb, maxw) for b in bullets]
    lh = int(fb.size*1.14)
    text_h = ((36+30) if header else 0) + sum(len(it)*lh + 34 for it in items)
    def body(d, im, t, ty):
        if header:
            k = clamp01((t-0.08)/0.42)
            wdt = draw_type(d, header.upper(), fh, MARGIN, ty, OLIVE+(255,), k)
            d.rectangle([MARGIN, ty+fh.size+16, MARGIN+int(wdt*clamp01(k*1.2)), ty+fh.size+22], fill=OLIVE)
            ty += fh.size + 56
        for n, lines in enumerate(items):
            k = clamp01((t - (0.30 + n*stagger)) / reveal)
            if k <= 0: break
            d.rectangle([MARGIN, ty+18, MARGIN+14, ty+32],
                        fill=tuple(int(v*clamp01(k*4)) for v in OLIVE))
            type_lines(d, lines, fb, MARGIN+38, ty, INK+(255,), k, lead=1.14)
            ty += len(lines)*lh + 34
    return _win_plate(dur, body, fps, text_h, radius)

def plate_stmt_window(parts, dur, fps=FPS, radius=0, reveal=1.15):
    """Dan ABOVE, mixed-weight statement BELOW -- his 'Chat GPT / General Purpose AI'
    screen, which is the same split as the bullets, not a bare field."""
    fbig, fmid = font(66, "ExtraBold"), font(52, "SemiBold")
    lines = []
    for txt, kind in parts:
        f = fbig if kind in ("big", "olive") else fmid
        col = OLIVE if kind == "olive" else INK
        for ln in wrap(txt, f, VW-2*MARGIN): lines.append((ln, f, col))
    text_h = sum(int(f.size*1.16) for _, f, _ in lines)
    def body(d, im, t, ty):
        for n, (ln, f, col) in enumerate(lines):
            k = clamp01((t - 0.25 - n*0.22) / reveal)
            draw_type(d, ln, f, MARGIN, ty, col+(255,), k)
            ty += int(f.size*1.16)
    return _win_plate(dur, body, fps, text_h, radius)

def plate_window_media(dur, media_ar, fps=FPS, radius=0, gap=42):
    """Dan ABOVE, a media card BELOW -- his 'phone left / Dan right' product screen.
    Returns (frames, dan_rect, media_hole): TWO holes, so render.py feeds two sources."""
    win_h = 660          # Dan is the inset here, the product screen is the subject --
    rect = (0, 60, VW, 60+win_h)   # the same weighting his 'phone left / Dan right' has
    top = rect[3] + gap
    bot = BOT_SAFE - 20
    mh = bot - top
    mw = mh * media_ar
    if mw > VW - 2*120:
        mw = VW - 2*120; mh = mw/media_ar; top = rect[3] + gap + (bot-top-mh)/2
    hole = (int(VW/2 - mw/2), int(top), int(VW/2 + mw/2), int(top+mh))
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        h = _hole_at(hole, t, 0.42, 0.06)
        rrect(im, [h[0]-12, h[1]-12, h[2]+12, h[3]+12], 26, fill=CARD_OL+(255,), glow=22)
        im = _punch(im, h, 18)
        im = _punch(im, _hole_at(rect, t, 0.30, 0.03), radius)
        out.append(im)
    return out, rect, hole

def plate_title_card(headline, sub, dur, fps=FPS):
    """His 'VISUALIZING YOUR GOAL' beat: an olive card on the bare field, heavy oblique
    caps typing on, subtitle under. No Dan."""
    fh, fs = font(96, "ExtraBold"), font(46, "SemiBold")
    hl = wrap(headline.upper(), fh, VW-2*150)
    sl = wrap(sub, fs, VW-2*150) if sub else []
    lh, ls = int(fh.size*1.06), int(fs.size*1.20)
    inner = len(hl)*lh + (40+len(sl)*ls if sl else 0)
    ch = inner + 150
    box = (72, (VH-ch)//2, VW-72, (VH-ch)//2 + ch)
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        k0 = ease_out_back(clamp01(t/0.40))
        cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
        hw, hh = (box[2]-box[0])/2*(0.94+0.06*k0), (box[3]-box[1])/2*(0.94+0.06*k0)
        rrect(im, [cx-hw, cy-hh, cx+hw, cy+hh], 30, fill=CARD_OL+(255,), glow=26)
        lay = Image.new("RGBA", (VW, VH), (0,0,0,0)); d = ImageDraw.Draw(lay)
        y = box[1] + 75
        for n, ln in enumerate(hl):
            k = clamp01((t - 0.18 - n*0.26)/0.62)
            draw_type(d, ln, fh, (VW - text_size(ln, fh)[0])//2, y, INK+(255,), k)
            y += lh
        lay = oblique(lay, 9.0, pivot_y=box[1]+75+len(hl)*lh/2)
        im.alpha_composite(lay)
        if sl:
            y += 40
            d2 = ImageDraw.Draw(im)
            for n, ln in enumerate(sl):
                k = clamp01((t - 0.55 - n*0.18)/0.55)
                draw_type(d2, ln, fs, (VW - text_size(ln, fs)[0])//2, y, INK+(255,), k)
                y += ls
        out.append(im)
    return out, None

# ------------------------------------------------------------------ overlays
def overlay_lower_third(lines, dur, fps=FPS, y_bottom=1600, in_dur=0.55):
    """Olive tab + black bar + white type, revealed letter by letter. Seven of these
    carry his cut; captions are suppressed for their duration because the line they
    print IS the sentence being spoken."""
    # Each line is fitted to the bar, not assumed to fit it: his longest lower third is
    # 48 characters and at a fixed 52 px it overflowed the bar on both sides.
    AVAIL = VW - 2*40 - 96
    fs = []
    for n, t in enumerate(lines):
        sz = 52 if n == 0 else 40
        w8 = "ExtraBold" if n == 0 else "SemiBold"
        while sz > 24 and text_size(t, font(sz, w8))[0] > AVAIL: sz -= 2
        fs.append(font(sz, w8))
    ws = [text_size(t, f)[0] for t, f in zip(lines, fs)]
    lhs = [int(f.size*1.30) for f in fs]
    bw = max(ws) + 96
    bw = min(bw, VW - 2*40)
    bh = sum(lhs) + 34
    bx, by = (VW-bw)//2 + 22, y_bottom - bh
    TAB = 26
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        o = 1.0 - ease_in_out(clamp01((t-(dur-0.32))/0.32))
        gw = ease_out_cubic(clamp01(t/0.34))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([bx-TAB-14, by, bx-14, by+bh], radius=8,
                            fill=OLIVE+(int(235*o*gw),))
        d.rounded_rectangle([bx, by, bx+int(bw*gw), by+bh], radius=8, fill=(0,0,0,int(232*o)))
        yy = by + 17
        for n, (txt, f, lh) in enumerate(zip(lines, fs, lhs)):
            k = clamp01((t - 0.20 - n*0.55)/0.80)
            draw_type(d, txt, f, bx + (bw - text_size(txt, f)[0])//2, yy,
                      INK+(int(255*o),), k)
            yy += lh
        out.append(im)
    return out, None

_FLASH = None
def overlay_flash(dur, fps=FPS, peak=0.62):
    """His light-leak transition: a white bloom that blows out for ~4 frames. Eight beat
    changes in his cut use it instead of a hard cut."""
    global _FLASH
    if _FLASH is None:
        import numpy as np
        ys, xs = np.mgrid[0:VH, 0:VW]
        r = np.hypot((xs-VW*0.42)/(VW*0.95), (ys-VH*0.44)/(VH*0.62))
        _FLASH = np.clip(1.25 - r*0.75, 0, 1) ** 1.15
    import numpy as np
    out = []
    n = nframes(dur, fps)
    for i in range(n):
        p = i/max(1, n-1)
        a = np.sin(np.pi * p) ** 0.75
        alpha = (_FLASH * a * 255).astype("uint8")
        im = Image.new("RGBA", (VW, VH), (255, 253, 246, 0))
        im.putalpha(Image.fromarray(alpha))
        out.append(im)
    return out, None
