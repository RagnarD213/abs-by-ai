import os
#!/usr/bin/env python3
"""Ad 3 "Stop Paying Human Trainers" -- the vertical rebuild of MUHAMMAD's v6 HD design, on top of g5 (his J2 tokens,
measured on Ads 2 and 5 and re-checked on this render: field 13,14,11 + grid, olive 140,153,91, card olive 90,100,58).

What Ad 3 adds (read off his frames at full resolution, 2026-09-11):
  * his NUMBERED lower third -- a wide olive tab carrying a big white numeral (1-4) beside the black bar;
  * his text-left screens as BLOCKS of elements that BLUR IN at their cue (not type on): white bullets with an olive
    square, olive phrases inside a bullet ("personal trainer", "38 year old"), heavy oblique olive lines that continue a
    bullet ("NEXT FEW MINUTES", "SIX-PACK ABS.", "TEN YEARS AGO."), underlined olive caps headers ("HOW DO I KNOW ALL
    THIS?"); a block swap clears the old text on one frame and the new one blurs in;
  * the full-frame AI chip for a native 9:16 AI clip -- LOW, over the waistline, never a face (Dan, 2026-08-27);
  * his rapid photo-shoot stills on the field (4 stills, ~7 frames each, soft shadow, no card).
"""
from g5 import *                      # noqa: F401,F403 -- every g5 token and function
import g5 as _g5
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, wrap, text_size, oblique, ease_out_cubic, ease_out_back, ease_in_out, clamp01

# ------------------------------------------------------------------ lower thirds (plain + his numbered tab)
def lower_third(lines, t, dur, y_bottom=1600, weights=None, sizes=None, num=None):
    """His olive tab + black bar + white type, letter by letter. Both lines ExtraBold at one size (his Ad 3 bars).
    num: his numbered tab -- a wide olive tab with a big white numeral, the bar starting right of it."""
    if num is None:
        return _g5.lower_third(lines, t, dur, y_bottom=y_bottom, weights=weights or ["ExtraBold"]*len(lines),
                               sizes=sizes or [48]*len(lines))
    TABW, GAP = 104, 12
    AVAIL = VW - 2*36 - TABW - GAP - 60
    fs = []
    for n_, s in enumerate(lines):
        sz = sizes[n_] if sizes else 48; w8 = weights[n_] if weights else "ExtraBold"
        while sz > 24 and text_size(s, font(sz, w8))[0] > AVAIL: sz -= 2
        fs.append(font(sz, w8))
    ws = [text_size(s, f)[0] for s, f in zip(lines, fs)]; lhs = [int(f.size*1.30) for f in fs]
    bw = min(max(ws) + 70, VW - 2*36 - TABW - GAP); bh = sum(lhs) + 34
    total = TABW + GAP + bw; tx = (VW - total)//2; bx = tx + TABW + GAP; by = y_bottom - bh
    im = blank(); d = ImageDraw.Draw(im)
    o = 1.0 - ease_in_out(clamp01((t-(dur-0.12))/0.12)); gw = ease_out_cubic(clamp01(t/_g5.LT_GROW))
    th = bh + 24
    d.rounded_rectangle([tx, by - 12, tx + TABW, by - 12 + th], radius=12, fill=OLIVE+(int(240*o*gw),))
    fn = font(96, "ExtraBold")
    d.text((tx + TABW//2, by - 12 + th//2 + 2), str(num), font=fn, fill=INK+(int(255*o*gw),), anchor="mm")
    d.rounded_rectangle([bx, by, bx + int(bw*gw), by + bh], radius=8, fill=(0, 0, 0, int(232*o)))
    yy = by + 17
    for n_, (s, f, lh) in enumerate(zip(lines, fs, lhs)):
        k = clamp01((t - _g5.LT_LEAD - n_*_g5.LT_STAGGER)/_g5.LT_SPAN)
        draw_type(d, s, f, bx + (bw - text_size(s, f)[0])//2, yy, INK+(int(255*o),), k); yy += lh
    return im

# ------------------------------------------------------------------ his text-left screens, as blocks that blur in
FB = lambda: font(50, "SemiBold")
FOH = lambda: font(62, "ExtraBold")
def _fh(big=False): return font(58 if big else 46, "ExtraBold")
REVEAL = 0.40                       # his bullet blur-in: 12 frames soft->sharp, measured at FULL RES on the
                                    # bullets themselves (269->281, 439->451, 3100->3110, 3097->3109, 6649->6661,
                                    # 7635->7648; median 12, = 0.400 s). The old 0.27 was read off 1085->1093,
                                    # which is the WINDOW PANEL opening, not a bullet -- a different animation.
# His SECTION HEADERS do not blur -- they TYPE, fast: "H" at 3966, "HOW D" at 3967, "HOW DO" at 3968; "I T" / "IT DE"
# / "IT DESIG" at 6530-32; "I" / "IT A" at 7455-56 (independent audit, 2026-09-11, item 14 -- and the notes claimed
# we already did this). ~2.5 characters a frame, so a 23-character header lands in about 9 frames.
HDR_TYPE = 0.30
def _rev(el): return HDR_TYPE if el['kind'] == 'hdr' else REVEAL
IND = MARGIN + 38                   # the bullet text indent

def _colour_spans(text, olive):
    cols = [INK]*len(text)
    for ph in olive:
        i = text.find(ph)
        while i >= 0:
            for k in range(i, i+len(ph)): cols[k] = OLIVE
            i = text.find(ph, i+len(ph))
    return cols

def _layout(el, maxw):
    k = el['kind']
    if k == 'bullet':
        f = FB(); paras = el['text'].split('\n'); lines = []
        for p in paras: lines += wrap(p, f, maxw - 38)
        return f, lines, int(f.size*1.14)
    if k == 'ohdr':
        f = FOH(); return f, wrap(el['text'].upper(), f, maxw - (38 if el.get('indent', True) else 0)), int(f.size*1.04)
    if k == 'hdr':
        f = _fh(el.get('big')); return f, wrap(el['text'].upper(), f, maxw), int(f.size*1.10)
    raise ValueError(k)

GAP_AFTER = dict(bullet=34, ohdr=26, hdr=46)
def block_height(items, maxw=VW - 2*MARGIN):
    h = 0; prev = None
    for el in items:
        f, lines, lh = _layout(el, maxw)
        if prev == 'bullet' and el['kind'] == 'ohdr' and el.get('indent', True): h -= 26      # a continuation line sits tight
        h += len(lines)*lh + GAP_AFTER[el['kind']] + (22 if el['kind'] == 'hdr' else 0)
        prev = el['kind']
    return h

def _element_layer(el, ty, maxw, kt=1.0):
    """the element drawn on a transparent frame-sized layer; returns (layer, height).
    kt < 1 types the HEADER on (his headers type, they do not blur -- see HDR_TYPE)."""
    f, lines, lh = _layout(el, maxw); lay = blank(); d = ImageDraw.Draw(lay); k = el['kind']
    if k == 'bullet':
        d.rectangle([MARGIN, ty+18, MARGIN+14, ty+32], fill=OLIVE+(255,))
        cols = _colour_spans(el['text'].replace('\n', ' '), el.get('olive', ())); idx = 0; flat = el['text'].replace('\n', ' ')
        for n_, ln in enumerate(lines):
            i0 = flat.find(ln, idx); i0 = idx if i0 < 0 else i0
            draw_type(d, ln, f, IND, ty + n_*lh, INK+(255,), 1.0, cols=[c+(255,) for c in cols[i0:i0+len(ln)]])
            idx = i0 + len(ln)
        return lay, len(lines)*lh + GAP_AFTER[k]
    if k == 'ohdr':
        x = IND if el.get('indent', True) else MARGIN
        for n_, ln in enumerate(lines): draw_type(d, ln, f, x, ty + n_*lh, OLIVE+(255,), 1.0)
        return oblique(lay, 9.0, pivot_y=ty + len(lines)*lh/2), len(lines)*lh + GAP_AFTER[k]
    if k == 'hdr':
        wdt = 0
        # one k across the whole header, so a wrapped header types line after line rather than both at once
        tot = sum(len(ln) for ln in lines); done = kt*tot; seen = 0
        for n_, ln in enumerate(lines):
            kl = clamp01((done - seen)/max(1, len(ln))); seen += len(ln)
            wdt = max(wdt, draw_type(d, ln, f, MARGIN, ty + n_*lh, OLIVE+(255,), kl))
        yb = ty + (len(lines)-1)*lh + f.size + 16
        bw = max(wdt, 520) if kt >= 1.0 else wdt          # his rule grows with the type, then settles to the full bar
        if bw > 0: d.rectangle([MARGIN, yb, MARGIN + bw, yb + 6], fill=OLIVE+(255,))
        return lay, len(lines)*lh + GAP_AFTER[k] + 22
    raise ValueError(k)

_ELC = {}
def blocks_body(blocks, maxw=VW - 2*MARGIN):
    """blocks = [dict(t0=s, items=[dict(kind, text, t=s, olive=(...), indent=True, big=False)])] -- times relative to
    the beat. At a block's t0 the previous block is gone on that frame; each item blurs in over REVEAL from its t."""
    th = max(block_height(b['items'], maxw) for b in blocks)
    def active(tt):
        cur = 0
        for i, b in enumerate(blocks):
            if tt >= b['t0']: cur = i
        return cur
    def settled_key(tt):
        bi = active(tt); b = blocks[bi]
        pend = [el for el in b['items'] if el['t'] <= tt < el['t'] + _rev(el)]
        shown = tuple(i for i, el in enumerate(b['items']) if el['t'] <= tt)
        return (bi, shown) if not pend else None
    def body(d, im, tt, ty):
        bi = active(tt); b = blocks[bi]; y = ty; prev = None
        for i, el in enumerate(b['items']):
            if prev == 'bullet' and el['kind'] == 'ohdr' and el.get('indent', True): y -= 26
            key = (id(blocks), bi, i, y)
            if key not in _ELC:
                _ELC[key] = _element_layer(el, y, maxw)
            lay, h = _ELC[key]
            if tt >= el['t']:
                k = clamp01((tt - el['t'])/_rev(el))
                if k >= 1.0:
                    im.alpha_composite(lay)
                elif el['kind'] == 'hdr':                 # his headers TYPE on; only the bullets blur in
                    im.alpha_composite(_element_layer(el, y, maxw, kt=k)[0])
                else:
                    s = 12.0*(1 - ease_out_cubic(k)); L = lay.filter(ImageFilter.GaussianBlur(s)) if s > 0.4 else lay
                    a = L.getchannel('A').point(lambda v: int(v*ease_out_cubic(k)))
                    L = L.copy(); L.putalpha(a); im.alpha_composite(L)
            y += h; prev = el['kind']
    body.settled_key = settled_key
    return body, th

# ------------------------------------------------------------------ AI chips
def ai_chip_low(im, cy=1250, size=78, txt="AI-GENERATED"):
    """The full-frame AI label for a native 9:16 AI clip: big, centred, over the waistline and above the caption band --
    never over a face (Dan, 2026-08-27: 'don't cover my face with labels like this. Make that a rule')."""
    fl = font(size, "SemiBold"); lw, lh = text_size(txt, fl)
    bx, by = (VW - lw - 60)//2, int(cy - (lh + 34)/2)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx + lw + 60, by + lh + 34], radius=14, fill=(0, 0, 0, 205))
    d.text((bx + 30, by + 17), txt, font=fl, fill=INK+(255,), anchor="lt")

# ------------------------------------------------------------------ his rapid photo-shoot stills on the field
# ------------------------------------------------------------------ the standing real-picture label (Dan, 2026-09-11)
# "Throughout this video, whenever you're showing the after pictures, I want to start adding a label where we say,
# 'Real pictures of me, not AI-generated.'" -- now a standing rule in AGENTS.md and every video skill. Dan's BEFORE
# pictures stay unlabelled (the two fat-dad cards here); his AI goal image keeps AI-GENERATED. Chip copied from the
# Ad 4 session's committed reference/a8_ad4/g8.py so both ads carry the identical label.
REAL_TXT = "Real picture of me — not AI-generated"
def real_chip(im, x0, y0, w, h, size=38):
    """Black chip, white Manrope SemiBold, centred INSIDE the photo and bottom-aligned -- so it lands on the picture
    for a portrait still (waist line) and for a landscape one (which sits short of the field's bottom), never on the
    field below it, and never over a face.
    38 px is the largest size that fits the NARROWEST still in his sequence (the 778-wide portraits; the landscapes are
    960) -- one size for all four, so the label does not resize as his photos flip every 5-8 frames."""
    fl = font(size, "SemiBold")
    while text_size(REAL_TXT, fl)[0] + 36 > w - 24 and size > 26: size -= 2; fl = font(size, "SemiBold")
    lw, lh = text_size(REAL_TXT, fl)
    bw, bh = lw + 36, lh + 22
    bx, by = x0 + (w - bw)//2, y0 + h - bh - 22
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=10, fill=(0, 0, 0, 215))
    d.text((bx+18, by+11), REAL_TXT, font=fl, fill=INK+(255,), anchor="lt")

# ------------------------------------------------------------------ label placement OFF HIS BODY (Dan, 2026-09-12)
# "the label will not block my face or my abs... put it above my head, to the side, or somewhere that it doesn't block my
# face and my abs in all of these after pictures." The old rule put the chip bottom-centre on the photo -- on the 04_SHOT1
# still that sat across his lower abs. Placement is MEASURED: Apple Vision person mask of the still (assets/labelmask/,
# made by shorts/reference/recentre/personmask), dilated for breathing room, then every chip position inside the photo is
# scored and only positions touching NONE of him are allowed. One size for all four stills (they flip every 5-8 frames).
LABEL_MASKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'labelmask')
_SPLIT = ("Real picture of me \u2014", "not AI-generated")
def _chip_dims(size, two):
    fl = font(size, "SemiBold")
    lines = _SPLIT if two else (REAL_TXT,)
    lw = max(text_size(t, fl)[0] for t in lines); lh = text_size("Ag", fl)[1]
    return fl, lines, lw + 36, len(lines)*lh + (len(lines)-1)*8 + 22, lh
def label_candidates(photo_name, x0, y0, w, h, top_min=TOP_SAFE_Y if 'TOP_SAFE_Y' in globals() else 160, bot_max=1380):
    """every (size, two_line) layout that fits with ZERO overlap on his dilated silhouette -> {(size,two): best (bx,by)}"""
    import numpy as _np
    from scipy.ndimage import binary_dilation
    mp = os.path.join(LABEL_MASKS, os.path.splitext(photo_name)[0] + '.mask.png')
    if not os.path.exists(mp): return None
    m = _np.asarray(Image.open(mp).convert('L').resize((w, h), Image.BILINEAR)) > 100
    m = binary_dilation(m, iterations=max(8, int(0.025*h)))
    ii = _np.pad(m.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    rows = _np.nonzero(m.any(1))[0]; headx = float(_np.nonzero(m[rows[0]])[0].mean()) if len(rows) else w/2
    out = {}
    for size in (38, 36, 34, 32, 30, 28):
        for two in (False, True):
            _, _, bw, bh, _ = _chip_dims(size, two)
            if bw > w - 24 or bh > h - 24: continue
            best = None
            for by in range(max(12, top_min - y0), min(h - bh - 12, bot_max - y0 - bh) + 1, 6):
                for bx in range(12, w - bw - 12 + 1, 6):
                    if ii[by+bh, bx+bw] - ii[by, bx+bw] - ii[by+bh, bx] + ii[by, bx]: continue
                    score = by*0.05 + abs(bx + bw/2 - headx)*0.02
                    if best is None or score < best[0]: best = (score, bx, by)
            if best: out[(size, two)] = (x0 + best[1], y0 + best[2])
    return out

def real_chip_at(im, bx, by, size, two):
    fl, lines, bw, bh, lh = _chip_dims(size, two)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=10, fill=(0, 0, 0, 215))
    for i, t in enumerate(lines):
        d.text((bx + (bw - text_size(t, fl)[0])//2, by + 11 + i*(lh + 8)), t, font=fl, fill=INK+(255,), anchor="lt")

def photo_on_field(photo, box=(60, 170, VW-60, 1330), shadow=26, real_label=False, label=None):
    """a still centred on the field, contained in `box` at its own aspect, soft dark shadow, thin dark border (his look)"""
    im = field().convert("RGBA")
    bw, bh = box[2]-box[0], box[3]-box[1]; s = min(bw/photo.width, bh/photo.height)
    w, h = int(photo.width*s)//2*2, int(photo.height*s)//2*2
    x0, y0 = box[0] + (bw-w)//2, box[1] + (bh-h)//2
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([x0-4, y0+8, x0+w+4, y0+h+14], fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(shadow)))
    ImageDraw.Draw(im).rectangle([x0-3, y0-3, x0+w+2, y0+h+2], fill=(20, 22, 18, 255))
    im.paste(photo.resize((w, h), Image.LANCZOS), (x0, y0))
    if real_label and label is not None:
        # label = (size, two_line, fx, fy): position as a FRACTION of the photo, so it rides the flag still's pop-zoom
        size, two, fx, fy = label
        real_chip_at(im, x0 + int(round(fx*w)), y0 + int(round(fy*h)), size, two)
    elif real_label: real_chip(im, x0, y0, w, h)
    return im.convert("RGB")
