#!/usr/bin/env python3
"""SQUARE (1080x1080) rebuild of Muhammad's design system, re-laid out from the APPROVED
9:16 vertical (`vlib_9x16_orig.py` beside this file is that file, untouched, for diffing).

A 1:1 frame is not a short 9:16 and not a cropped 16:9. Three things change and nothing else:

  * THE TALKING HEAD IS 1.00x. A 1080x1080 window of the 1920x1080 conform is a pure crop --
    no upscale at all, where the vertical is forced into 1.78x. Nothing here is sharpened.
  * THE WINDOW BEATS LOSE HEIGHT, SO THE TYPE COMES DOWN AND THE WINDOW CLAMP COMES DOWN with
    it (470-720 px against the vertical's 820-1220). Measured per beat, never one compromise.
  * MEDIA THAT CANNOT SURVIVE A 1:1 CROP GOES IN HIS CARD INSTEAD OF FULL-BLEED. A 1:1 crop of
    a 3:4 photo of a person takes 25 % of its height, and what it takes is his head (verified
    on rendered frames: sqtest/_sheet_stills.png).

Every token below is still MEASURED off his finished 16:9 cut (see gradefit2.py / the
palette probe), not guessed: field #0D0E0B, sage accent #8C995B, card olive #5A643A, black
bars, white ink, a ~4% grid on the field, rounded cards with a soft glow.

His frame puts text LEFT and Dan RIGHT. A 1:1 frame has the width for that, but not at a
readable type size: his text pane is 51 % of 1920 = 975 px, which in a 1080-wide frame is
549 px, and his 44 px bullets become 25 px. So the TEXT beats keep the vertical's stacked
form (Dan above, text below, the window sized to the beat's text), while the PORTRAIT-MEDIA
beat keeps HIS OWN left/right arrangement -- phone left, Dan right, exactly as his 3:22
split has it -- because there a 1:1 frame really does have the width for it.
"""
import sys, os, math
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import motionlib as M
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, wrap, text_size, text_bbox, oblique, drop_shadow, nframes, encode
from motionlib import ease_out_cubic, ease_out_expo, ease_out_back, ease_in_out, clamp01

VW, VH = 1080, 1080
FPS = 30000/1001

FIELD    = (13, 14, 11)
FIELD_HI = (23, 25, 19)
OLIVE    = (140, 153, 91)
CARD_OL  = (90, 100, 58)
INK      = (255, 255, 255)
INK_SOFT = (176, 184, 158)
BAR      = (0, 0, 0)

# --- square safe area ---------------------------------------------------------
# A 1:1 unit in a feed carries the platform's own furniture: YouTube in-feed and Discover put
# their title/channel row under the thumbnail rather than over it, Gmail and Meta feed crop
# nothing, but every one of them can overlay the right-hand ~100 px with a menu affordance.
# So: nothing that must be READ below y=980 or above y=80, and nothing readable in the
# right-hand 100 px. The caption band sits at 880 -- its own bottom edge lands at ~952, clear
# of 980, and it leaves the cards 848 px of height above it.
TOP_SAFE, BOT_SAFE = 80, 980
RIGHT_SAFE = 100                 # nothing that must be read to the right of VW-100
CAP_Y = 880
# ⚠ 100, NOT THE VERTICAL'S 76, AND SYMMETRIC. The in-feed reserve is on the right only, but an
# asymmetric text column in a 1:1 frame reads as mis-centred type, so the margin is 100 on BOTH
# sides and the right-hand reserve is satisfied by construction. Measured cost of going 76 -> 100
# across all five window beats: ONE extra wrapped line, on one bullet, at 50.4 s. Rightmost text
# pixel 951 against the 980 line (at 76 it was 992, and at the vertical's own bullet-wrap width,
# which forgets the 38 px bullet indent, 1051 -- 29 px from the frame edge).
MARGIN = 100

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
        P = 46                                   # ~4.3% of width == his 73px at 1920 (frame width is unchanged)
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
WIN_Y0   = 30          # the window's top edge; his own screens sit hard against the top
WIN_GAP  = 56          # window bottom -> first line of type
WIN_MIN, WIN_MAX = 470, 720
TEXT_BOT = BOT_SAFE - 10

def window_rect(text_h):
    """Dan's window on a STACKED (text) beat: as tall as the beat's text will allow.

    The square's whole budget is 1080 px of height, so this clamp is the vertical's
    (820-1220) brought down by the 840 px the format does not have. 720 is his own 16:9
    framing exactly (see window_crop); below 608 the window is a letterbox slice of the
    source and he starts losing his chest, so 470 is the floor and `beats.py` is sized so
    that no beat asks for less."""
    h = TEXT_BOT - WIN_GAP - WIN_Y0 - text_h
    h = max(WIN_MIN, min(WIN_MAX, int(h)))
    return (0, WIN_Y0, VW, WIN_Y0 + h)

def window_crop(win_h, win_w=VW, cx=None):
    """Source crop (in the 1920x1080 conform) that fills a window of win_w x win_h.

    ⚠ THE MAGNIFICATION IS win_w / crop_w, AND AT A FULL-WIDTH WINDOW OF 608 PX IT IS EXACTLY
    0.5625 -- which is HIS OWN 16:9 FRAMING, pixel for pixel. That is the number to keep in
    mind when reading these windows: the square's talking head is never blown up, it is either
    his framing (a wide short window) or tighter than it (a taller or narrower one).

      win_h >= 608 : height-limited -- the crop is 1080 tall and narrower than 1920, centred
                     on the face track, so the window is TIGHTER than his cut.
      win_h <  608 : width-limited  -- the crop is the full 1920 wide and shorter than 1080.
                     It is anchored at y=0 because this roll puts his hair 19-45 px below its
                     own top edge (skill [A6].10): there is no headroom to give away, and the
                     height comes off the bottom of frame, below his chest."""
    from grade import SUBJECT_CX
    A = win_w / win_h
    if A <= 1920/1080:                       # crop is 1080 tall
        w = int(round(1080 * A)); w = min(w, 1920) - (min(w, 1920) % 2)
        h = 1080
    else:                                    # crop is 1920 wide
        w = 1920
        h = int(round(1920 / A)); h = min(h, 1080) - (min(h, 1080) % 2)
    x = int(round((SUBJECT_CX if cx is None else cx) - w/2))
    x = max(0, min(x, 1920 - w))
    return (w, h, x, 0)

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

# ⚠ The 1080x1920 build carried TWO `plate_window` definitions, the second silently
# overriding the first. The dead one is deleted here rather than ported: an unused layout
# function that looks live is exactly the kind of thing a later session edits by mistake.
# `vlib_9x16_orig.py` still has both, byte for byte, if it is ever needed.

CARD_TOP, CARD_BOT = 64, 848      # the card must end ABOVE the caption band (CAP_Y 880)
CARD_BOT_TEXT = 790               # ... and above its own caption, when it carries one

def card_hole(media_ar, has_text):
    """Biggest card that fits the media's OWN aspect ratio.

    A fixed 16:9 hole cover-crops a portrait photo, and the thing it crops off a photo of
    a person is their head. Size the hole from the media, never the other way round.

    ⚠ THE CARD ENDS ABOVE THE CAPTION BAND. A card sized to the full frame height puts its
    bottom third under the captions, and a white app screen behind white captions is
    unreadable. In a 1:1 frame that costs real height -- 784 px against the vertical's 1180 --
    so a phone recording comes out ~360 px wide here. That is not a loss against the
    reference: HIS OWN 16:9 card runs the phone at ~445 px of 1920, which is 250 px at a
    1080-wide display. The square is 44 % more generous than his cut, the vertical was 117 %."""
    maxw = VW - 2*40
    top, bot = CARD_TOP, (CARD_BOT if not has_text else CARD_BOT_TEXT)
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
        if label:                                     # label chip, inside the card
            # ⚠ FIT THE CHIP TO THE CARD, NEVER THE OTHER WAY ROUND. "Real picture of me --
            # not AI-generated" is 37 characters against "AI-GENERATED"'s 12, and at a fixed
            # 30 px it runs past a 566 px portrait card on both sides (Dan, 2026-09-11).
            fl_ = fl
            while fl_.size > 18 and text_size(label, fl_)[0] + 34 > (h[2]-h[0]) - 28:
                fl_ = font(fl_.size - 2, "SemiBold")
            lw, lh_ = text_size(label, fl_)
            lay = Image.new("RGBA", (VW, VH), (0,0,0,0))
            bx = (VW-(lw+34))//2
            by = int(h[3]) - lh_ - 40
            ImageDraw.Draw(lay).rounded_rectangle([bx, by, bx+lw+34, by+lh_+22], radius=9,
                                                  fill=(0,0,0,215))
            ImageDraw.Draw(lay).text((bx+17, by+11), label, font=fl_, fill=INK, anchor="lt")
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

def overlay_cta(top, big, dur, fps=FPS, y=None, big_size=70):
    """His sage CTA pill. RGBA overlay -- it sits ON Dan, it does not replace him.

    `top` may be empty: his second CTA is a SINGLE line, "Get access to the AI nutrition
    plan", not a two-line pill."""
    ft = font(40, "SemiBold"); fb = font(big_size, "ExtraBold")
    tl = wrap(top, ft, VW-2*MARGIN-48) if top else []
    bl = wrap(big, fb, VW-2*MARGIN-48)
    w = max([text_size(x, ft)[0] for x in tl] + [text_size(x, fb)[0] for x in bl]) + 96
    w = min(w, VW-2*MARGIN)
    h = len(tl)*int(ft.size*1.2) + len(bl)*int(fb.size*1.12) + 62
    # ⚠ THE PILL IS TALLER THAN THE CAPTION BAND IT REPLACES. Centred on CAP_Y the two-line pill
    # runs to y 1019 in a 1080 frame -- 39 px from the edge and 39 px past the bottom safe line.
    # It is centred on the band and then pushed up until its bottom clears BOT_SAFE.
    y = y if y is not None else min(CAP_Y - h//2, BOT_SAFE - 10 - h)
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
        if tl:
            yy = draw_lines(d, tl, ft, bx, yy, (255,255,255,int(255*o)), lead=1.2, align="c", w=ww)
            yy += 6
        draw_lines(d, bl, fb, bx, yy, (255,255,255,int(255*o)), lead=1.12, align="c", w=ww)
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

def draw_type(d, txt, f, x, y, fill, k, tail=5, spread=0.75, anchor_w=None, cols=None):
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
        base = fill if cols is None else cols[i]
        col = tuple(int(v * a) for v in base[:3]) + ((int(base[3]*a),) if len(base) > 3 else ())
        d.text((ax, y), ch, font=f, fill=col, anchor="ls")
        ax += w + extra
    return ax - x

def type_lines(d, lines, f, x, y, fill, k, lead=1.14, align="l", w=None, stagger=0.55, cols_lines=None):
    """Several wrapped lines revealed one after another."""
    lh = int(f.size * lead)
    for i, ln in enumerate(lines):
        kk = clamp01((k - i * stagger * (1.0 / max(1, len(lines)))) * (1 + stagger))
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0]) // 2
        draw_type(d, ln, f, xx, y + i * lh, fill, kk,
                  cols=(cols_lines[i] if cols_lines else None))
    return y + lh * len(lines)

# ------------------------------------------------------------------ split layouts
#  His frame is TEXT LEFT / DAN RIGHT. A 9:16 frame has no left and right to give, so the
#  same relationship becomes DAN ABOVE / TEXT BELOW. The window height adapts to how much
#  the beat has to say, which is what keeps him large on short beats.

def wrap_runs(runs, f, maxw):
    """Wrap [(text, colour), ...] and return [(line, [colour per character]), ...].

    His bullets colour individual phrases olive -- "a 38 year old dad running a successful
    ad agency" -- and a phrase can straddle a line break, so the colour has to travel with
    the words through the wrap rather than being applied to whole lines afterwards."""
    toks = []
    for txt, col in runs:
        for wd in txt.split():
            toks.append((wd, col))
    lines, cur = [], []
    for wd, col in toks:
        trial = ' '.join(w for w, _ in cur + [(wd, col)])
        if cur and text_size(trial, f)[0] > maxw:
            lines.append(cur); cur = [(wd, col)]
        else:
            cur.append((wd, col))
    if cur: lines.append(cur)
    out = []
    for ln in lines:
        s_, cs = '', []
        for j, (wd, col) in enumerate(ln):
            if j: s_ += ' '; cs.append(col)
            s_ += wd; cs.extend([col]*len(wd))
        out.append((s_, cs))
    return out

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
    """Dan ABOVE, olive eyebrow + white bullets BELOW -- his bullet screen.
    A bullet is a string, or a list of (text, colour) runs for his olive highlights."""
    # ⚠ SIZED SO NO BEAT EVER CLAMPS. At the vertical's 46/50 the four-bullet beat
    # ("It builds your meal plan") asks for 440 px of type and leaves Dan 444 -- under the
    # 470 floor, i.e. a silent 26 px overflow past the bottom safe line. At 40/44 the worst
    # beat asks 410 and every window lands in 474..626 with nothing clamped. 44 px in a
    # 1080-wide frame is still 1.76x his own bullets (44 px of 1920 = 25 px at 1080).
    fh, fb = font(40, "ExtraBold"), font(44, "SemiBold")
    maxw = VW - MARGIN*2
    items = []
    BUL_IND = 38                      # the olive marker's indent -- the wrap must allow for it
    for b in bullets:
        runs = [(b, INK)] if isinstance(b, str) else [(t, c) for t, c in b]
        items.append(wrap_runs(runs, fb, maxw - BUL_IND))
    # ⚠ THE HEADER MUST WRAP. Two of his headers are long -- "1) WHY AI IS BETTER THAN
    # HUMAN NUTRITIONISTS." and "3) AI GIVES YOU A SCIENCE-BASED NUTRITION PLAN." -- and he
    # sets both on two lines. Drawn as one line they run straight off the right edge of a
    # 1080-wide frame, which is what the first render did.
    hlines = wrap(header.upper(), fh, maxw) if header else []
    hlh = int(fh.size*1.10)
    lh = int(fb.size*1.14)
    text_h = (len(hlines)*hlh + 30 if header else 0) + sum(len(it)*lh + 34 for it in items)
    def body(d, im, t, ty):
        if header:
            k = clamp01((t-0.08)/0.42)
            wdt = 0
            for n_, hl in enumerate(hlines):
                kk = clamp01((k - n_*0.25) * 1.4)
                wdt = max(wdt, draw_type(d, hl, fh, MARGIN, ty + n_*hlh, OLIVE+(255,), kk))
            yb = ty + (len(hlines)-1)*hlh + fh.size + 16
            d.rectangle([MARGIN, yb, MARGIN+int(wdt*clamp01(k*1.2)), yb+6], fill=OLIVE)
            ty += len(hlines)*hlh + 46
        for n, wrapped in enumerate(items):
            k = clamp01((t - (0.30 + n*stagger)) / reveal)
            if k <= 0: break
            d.rectangle([MARGIN, ty+18, MARGIN+14, ty+32],
                        fill=tuple(int(v*clamp01(k*4)) for v in OLIVE))
            type_lines(d, [l for l, _ in wrapped], fb, MARGIN+38, ty, INK+(255,), k, lead=1.14,
                       cols_lines=[[tuple(c)+(255,) for c in cs] for _, cs in wrapped])
            ty += len(wrapped)*lh + 34
    return _win_plate(dur, body, fps, text_h, radius)

def plate_stmt_window(parts, dur, fps=FPS, radius=0, reveal=1.15):
    """Dan ABOVE, mixed-weight statement BELOW -- his 'Chat GPT / General Purpose AI'
    screen, which is the same split as the bullets, not a bare field."""
    fbig, fmid = font(58, "ExtraBold"), font(46, "SemiBold")
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

# --- the split beat (his phone-left / Dan-right product screen) -------------------
# ⚠ A FULL-HEIGHT WINDOW IN A 1080-TALL FRAME IS ALWAYS 1.00x, WHATEVER ITS WIDTH. The crop is
# 1080 tall and the window is 1080 tall, so the magnification is fixed and a narrow window just
# shows LESS of him. His own 16:9 split gets away with it because his window is 945 px wide of
# 1920 -- 49 % of his frame -- and his head lands at 40 % of the window. The square has 1080 px
# of width to share with the phone, so a full-height window is 496 px and his head fills 81 %
# of it: a face close-up nobody asked for, and a magnification at which a 20 px lean is visible.
# So Dan's window here is SHORTER than the frame and sized to the magnification the APPROVED
# VERTICAL used on this same beat (0.611; here 0.60), vertically centred against the phone.
SPLIT_M_X, SPLIT_M_W, SPLIT_M_H = 30, 520, 886     # the media card's box: left edge, w, h
SPLIT_M_Y = 88
SPLIT_GAP = 26
SPLIT_D_W = 496                                    # Dan's window width
SPLIT_D_MAG = 0.60                                 # window px per source px (vertical: 0.611)

def plate_window_media(dur, media_ar, fps=FPS, radius=0, gap=SPLIT_GAP):
    """HIS OWN SPLIT, kept as his: MEDIA LEFT, DAN RIGHT.

    This is the one beat where a 1:1 frame can reproduce his 16:9 arrangement rather than
    translate it -- his 3:22 screen is the phone at x 0.16-0.38 of the frame and Dan in a
    window from x 0.51 to the right edge (`ref/_v_winmedia_2025.png`). The vertical had to
    stack them; the square does not. Returns (frames, dan_rect, media_hole): TWO holes, so
    render.py feeds two sources."""
    mh = SPLIT_M_H
    mw = mh * media_ar
    if mw > SPLIT_M_W:                       # a wide media shrinks its own box, never Dan's
        mw = SPLIT_M_W; mh = mw/media_ar
    mx = SPLIT_M_X + (SPLIT_M_W - mw)/2
    my = SPLIT_M_Y + (SPLIT_M_H - mh)/2
    hole = (int(mx), int(my), int(mx+mw), int(my+mh))
    dh = int(round(SPLIT_D_W * 1080 / (SPLIT_D_W / SPLIT_D_MAG)))   # == SPLIT_D_W*1080/crop_w
    dh -= dh % 2
    dx = SPLIT_M_X + SPLIT_M_W + gap
    dy = int(SPLIT_M_Y + (SPLIT_M_H - dh)/2)
    rect = (int(dx), dy, int(dx + SPLIT_D_W), dy + dh)
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
def overlay_lower_third(lines, dur, fps=FPS, y_bottom=950, in_dur=0.55):
    """Olive tab + black bar + white type, revealed letter by letter. Seven of these
    carry his cut; captions are suppressed for their duration because the line they
    print IS the sentence being spoken.

    `y_bottom` is the bar's BOTTOM edge. The square default 950 puts it in the caption
    band's own space -- legitimate, because a lower third mutes the captions -- and inside
    the 980 safe line. A beat whose picture needs the band clear passes its own value."""
    # Each line is fitted to the bar, not assumed to fit it: his longest lower third is
    # 48 characters and at a fixed 52 px it overflowed the bar on both sides.
    AVAIL = VW - 2*MARGIN - 96
    fs = []
    for n, t in enumerate(lines):
        sz = 52 if n == 0 else 40
        w8 = "ExtraBold" if n == 0 else "SemiBold"
        while sz > 24 and text_size(t, font(sz, w8))[0] > AVAIL: sz -= 2
        fs.append(font(sz, w8))
    ws = [text_size(t, f)[0] for t, f in zip(lines, fs)]
    lhs = [int(f.size*1.30) for f in fs]
    bw = max(ws) + 96
    bw = min(bw, VW - 2*MARGIN - 44)      # the bar is drawn at +22 and the olive tab hangs 40 px left of it
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
        # His content cut lands ON the flash peak (measured on V2: onset, peak two frames
        # later, then a long tail). The window is placed 0.10 s before the cut and 0.30 s
        # after it, so the peak sits at 25% of the window -- fast attack, slow decay.
        q = p/0.5 if p < 0.25 else 0.5 + (p-0.25)/1.5
        a = np.sin(np.pi * q) ** 0.75
        alpha = (_FLASH * a * 255).astype("uint8")
        im = Image.new("RGBA", (VW, VH), (255, 253, 246, 0))
        im.putalpha(Image.fromarray(alpha))
        out.append(im)
    return out, None
