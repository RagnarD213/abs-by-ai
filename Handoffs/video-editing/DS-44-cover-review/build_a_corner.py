#!/usr/bin/env python3
"""DS-44 cover round 3 (Dan, 2026-10-23): "I like design A, but I want you to add me back into the corner like I appear in
the video. Shift the fat guy on the bottom to the right slightly to accommodate this."

Design A from build_split.py (Hormozi on top, black centre band, caller below), plus the small keyed Dan exactly as the
approved R2 opening shows him: film frame 12 (0.4 s), exported by corner_dan.py, 432 x 768 at (0, 1152), lower left,
flush with the left and bottom edges, laptop visible. The caller's face moves from x 540 to the right of Dan.
Instagram: built on the full 1920 canvas with the band inside the 3:4 grid window (y 240-1680), so Dan sits where he
sits in the film in both layouts.

Round 4 (Dan, 2026-10-23): "Change me in the corner to a shot of me looking at the camera, making it an attention-getting
facial expression. Two variations with different gestures or facial expressions. Don't use one of me looking down."
Variants use keyed talking frames of the approved R2 (same roll, same key and grade): A394 shocked, mouth open, both hands
out; A206 "ohh", eyebrows up, head tilted, hand raised. Same 0.2667 scale, flush left and bottom.
usage: build_a_corner.py [VARIANT ...]   (default: film12, i.e. round 3)
"""
import sys
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFilter
import build_split as S

VARIANTS = {   # name: (corner png, face box inside it [hair top to chin], output round folder, label)
    'film12': ('corner-dan-film-frame12.png', [110, 150, 300, 370], 'round3', 'Looking Down (Round 3)'),
    'A394': ('corner-dan-A394-shocked.png', None, 'round4', 'Shocked, Hands Out'),
    'A206': ('corner-dan-A206-oh.png', None, 'round4', 'Ohh, Hand Raised'),
}
CALLER_X = 720                   # caller face centre (was 540)
W, H = S.W, S.H


def face_box(dan):
    """Hair top to chin, measured on the keyed alpha: the head's rows are the first 32% of the visible figure."""
    a = dan.getchannel('A').point(lambda v: 255 if v > 128 else 0)
    x0, y0, x1, y1 = a.getbbox()
    head = a.crop((0, y0, dan.width, y0 + 150)).getbbox()   # hair and face only, above the shoulders
    return [head[0] - 10, y0, head[2] + 10, y0 + round((y1 - y0) * 0.36)]


def design(ig, variant):
    png, face, _, _ = VARIANTS[variant]
    dan = Image.open(S.ASSETS / png).convert('RGBA')
    CORNER_XY = (0, H - dan.height)   # flush left and bottom, as in the film
    DAN_FACE = face or face_box(dan)
    top = 240 if ig else 0
    span = 1440 if ig else 1920
    im = Image.new('RGB', (W, H), S.INK)
    band_h = 290
    band_y = top + round(span * 0.43)
    ph = band_y - top
    p1, f1 = S.crop_src(S.HORMOZI, ph / 1080 * 1.02, 560, 40, S.FACE_H, (W, ph))
    im.paste(p1, (0, top))
    f1 = S.shift(f1, 0, top)
    if top:  # above the Instagram grid window (not shown in the grid): a soft stretch of the picture's top rows
        im.paste(p1.crop((0, 0, W, 24)).resize((W, top)).filter(ImageFilter.GaussianBlur(20)), (0, 0))
    y2 = band_y + band_h
    hc = H - y2
    p2, f2 = S.crop_src(S.CALLER, max(hc / 925, 1.0) * 1.02, CALLER_X, 30, S.FACE_C, (W, hc), S.BANNER_BOTTOM)
    im.paste(p2, (0, y2))
    d = ImageDraw.Draw(im)
    d.rectangle((0, band_y, W, y2), fill=S.INK)
    d.rectangle((0, band_y, W, band_y + 10), fill=S.YELLOW)
    d.rectangle((0, y2 - 10, W, y2), fill=S.YELLOW)
    b1 = S.text(im, "ALEX HORMOZI'S", 540, band_y + 40, 'Impact.ttf', 110, S.YELLOW, 1000, 'center')
    b2 = S.text(im, 'WEIGHT LOSS MENTAL SHIFT', 540, b1[3] + 22, 'Impact.ttf', 100, S.WHITE, 1010, 'center')
    # the small keyed Dan, with the film's soft shadowless composite (light wrap is in the export's grade only)
    base = im.convert('RGBA')
    base.alpha_composite(dan, CORNER_XY)
    im = base.convert('RGB')
    df = S.shift(DAN_FACE, *CORNER_XY)
    fc = S.shift(f2, 0, y2)
    assert df[1] > y2 + 20, ('Dan overlaps the band', df, y2)
    assert fc[0] > df[2] + 20, ('caller face not clear of Dan', fc, df)
    return im, [b1, b2], [f1, fc, df]


def main():
    names = sys.argv[1:] or ['film12']
    all_finals, records = {}, []
    for v in names:
        all_finals[v] = one(v, records)
    rnd = VARIANTS[names[0]][2]
    OUT = S.PROJECT / f'Short-form video content/Hormozi Fat Guy - DS-44/covers/{rnd}'
    n = len(names)
    sheet = Image.new('RGB', (40 + n * 900, 900), (238, 237, 233))
    d = ImageDraw.Draw(sheet)
    d.text((24, 18), 'Hormozi Fat Guy | Design A, You In The Corner Looking At Camera', font=S.font('Manrope', 31), fill=(14, 26, 33))
    d.text((24, 64), 'Each option: YouTube Shorts full cover, then Instagram grid (3:4 crop)', font=S.font('Arial.ttf', 22), fill=(65, 75, 79))
    for k, v in enumerate(names):
        x = 24 + k * 900
        d.text((x, 100), f'{k + 1}. {VARIANTS[v][3]}', font=S.font('Arial Bold.ttf', 24), fill=(14, 26, 33))
        sheet.paste(all_finals[v]['youtube'].resize((420, 747), Image.Resampling.LANCZOS), (x, 140))
        sheet.paste(all_finals[v]['instagram'].crop((0, 240, W, 1680)).resize((420, 560), Image.Resampling.LANCZOS), (x + 440, 140))
    sheet.save(OUT / f'REVIEW-hormozi-design-A-corner-{rnd}.jpg', quality=94, subsampling=0)
    (S.HERE / f'cover-manifest-{rnd}.json').write_text(json.dumps({
        'job': 'DS-44', 'round': rnd, 'status': 'awaiting-dan-approval (revised pick: show before install)',
        'variants': {v: VARIANTS[v][0] for v in names}, 'outputs': records}, indent=2) + '\n')


def one(variant, records):
    finals = {}
    OUT = S.PROJECT / f'Short-form video content/Hormozi Fat Guy - DS-44/covers/{VARIANTS[variant][2]}'
    for layout in ('youtube', 'instagram'):
        ig = layout == 'instagram'
        im, boxes, faces = design(ig, variant)
        lo, hi = (240, 1680) if ig else (0, 1920)
        for b in boxes:
            assert b[1] >= lo + 30 and b[3] <= hi - 30, (layout, b)
            for f in faces:
                assert b[2] < f[0] - 20 or b[0] > f[2] + 20 or b[3] < f[1] - 20 or b[1] > f[3] + 20, (layout, b, f)
        path = OUT / layout / f'A-{variant}-hormozi-mental-shift-corner-cover.jpg'
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path, quality=93, subsampling=0)
        assert path.stat().st_size < 2_000_000, path
        finals[layout] = im
        records.append({'variant': variant, 'layout': layout, 'file': str(path), 'bytes': path.stat().st_size,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'text_boxes': boxes, 'faces': faces})
    return finals


if __name__ == '__main__':
    main()
