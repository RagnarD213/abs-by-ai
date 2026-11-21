#!/usr/bin/env python3
"""Build a Reel/Short COVER (grid thumbnail) in the locked J2 tactical system.

Why a cover at all: Instagram's uploader defaults the cover to frame 0, which on
our shorts is the black opening frame — an empty tile in the profile grid.

Grid-safe by construction. Instagram's profile grid centre-crops a 1080x1920
cover to 3:4, keeping only y 240-1680, so every text element lives inside that
window and the asserts at the bottom of build() enforce it. The Reels player
additionally paints its caption row over roughly the bottom 15% (y>1630) and the
action buttons over the right ~15%; the wordmark therefore sits at y=1540 and
bottom-RIGHT, because the grid tile paints its play count bottom-LEFT.

Layout is a text band over a photo panel, NOT full-bleed. Full-bleed was tried
and rejected: a 9:16 crop of the 1920x1080 source puts the subject's head exactly
where the headline goes, so the scrim swallows his face. The panel keeps face and
abs both visible under the type.

Usage: adapt SRC/PANEL_Y/lines per short; frames come from the ORIGINAL longform,
never from the finished short — the short has burned-in word captions across the
abs and there is no caption-free frame to steal.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (13, 14, 11); OLIVE = (140, 152, 88); GRID = (27, 30, 19); INSET = 28
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'

TILE_TOP, TILE_BOT = 240, 1680   # what Instagram's 3:4 profile tile keeps
PANEL_Y = 560                    # photo starts here; text band is above it
SRC_OVERLAY_RIGHT = 693          # V4 source carries its own teal pills left of this


def spaced(d, xy, text, font, fill, gap=5):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + gap
    return x


def tactical(im):
    d = ImageDraw.Draw(im)
    for x in range(0, W, 90):
        d.line([(x, 0), (x, H)], fill=GRID)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=GRID)
    return im


def frame(im):
    d = ImageDraw.Draw(im)
    d.rectangle([INSET, INSET, W - INSET - 1, H - INSET - 1], outline=OLIVE, width=3)
    for x in range(INSET + 60, W - INSET - 40, 60):
        n = 18 if (x // 60) % 3 == 0 else 9
        d.line([(x, INSET + 3), (x, INSET + 3 + n)], fill=OLIVE, width=2)
        d.line([(x, H - INSET - 4), (x, H - INSET - 4 - n)], fill=OLIVE, width=2)
    for y in range(INSET + 60, H - INSET - 40, 60):
        n = 18 if (y // 60) % 3 == 0 else 9
        d.line([(INSET + 3, y), (INSET + 3 + n, y)], fill=OLIVE, width=2)
        d.line([(W - INSET - 4, y), (W - INSET - 4 - n, y)], fill=OLIVE, width=2)
    for (cx, cy, sx, sy) in [(INSET, INSET, 1, 1), (W - INSET, INSET, -1, 1),
                             (INSET, H - INSET, 1, -1), (W - INSET, H - INSET, -1, -1)]:
        d.rectangle([min(cx, cx + sx * 74), min(cy, cy + sy * 6),
                     max(cx, cx + sx * 74), max(cy, cy + sy * 6)], fill=(255, 255, 255))
        d.rectangle([min(cx, cx + sx * 6), min(cy, cy + sy * 74),
                     max(cx, cx + sx * 6), max(cy, cy + sy * 74)], fill=(255, 255, 255))
    return im


def panel(src_path, cx=1152, ytop=40, hfrac=0.85):
    """Crop the subject out of the 16:9 source and scale to fill the photo panel."""
    src = Image.open(src_path).convert('RGB'); sw, sh = src.size
    ph = H - PANEL_Y
    ch = int(sh * hfrac); cw = int(ch * W / ph)
    x0 = max(SRC_OVERLAY_RIGHT, min(cx - cw // 2, sw - cw))
    assert x0 >= SRC_OVERLAY_RIGHT, f'crop would include the source overlay: x0={x0}'
    assert ytop + ch <= sh, 'crop runs past the bottom of the source'
    return src.crop((x0, ytop, x0 + cw, ytop + ch)).resize((W, ph), Image.LANCZOS)


def build(out, src_path, line1, line2, eyebrow='AB ANATOMY', **kw):
    im = tactical(Image.new('RGB', (W, H), BG))
    im.paste(panel(src_path, **kw), (0, PANEL_Y))

    # Feather the photo's top edge into the black so it isn't a hard seam.
    ramp = Image.new('L', (1, 170))
    for i in range(170):
        ramp.putpixel((0, i), int(255 * (1 - i / 170) ** 0.9))
    im.paste(Image.new('RGB', (W, 170), BG), (0, PANEL_Y), ramp.resize((W, 170)))

    d = ImageDraw.Draw(im)
    ys = {'eyebrow': 268, 'line1': 326, 'line2': 510, 'wordmark': 1540}
    spaced(d, (60, ys['eyebrow']), eyebrow, ImageFont.truetype(COPPER, 36), OLIVE, 7)
    f1 = ImageFont.truetype(IMPACT, 162); f2 = ImageFont.truetype(IMPACT, 84)
    assert f1.getlength(line1) <= W - 116, f'line1 overflows: {line1}'
    assert f2.getlength(line2) <= W - 116, f'line2 overflows: {line2}'
    d.text((56, ys['line1']), line1, font=f1, fill=(255, 255, 255))
    d.text((60, ys['line2']), line2, font=f2, fill=OLIVE)

    wm = ImageFont.truetype(COPPER, 30); t = 'AbsByAI.com'
    d.text((W - 66 - d.textlength(t, font=wm), ys['wordmark']), t, font=wm,
           fill=(238, 238, 232))

    frame(im)
    for name, y in ys.items():
        assert TILE_TOP <= y <= TILE_BOT - 60, f'{name} at y={y} is cut by the 3:4 tile'
    im.save(out)
    return out


if __name__ == '__main__':
    S = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(S, 'cover-A.png'), os.path.join(S, 'frame.png'),
          '4 AB MUSCLES', 'NOT JUST A SIX-PACK')
