#!/usr/bin/env python3
"""Build Ad 10's 9:16 YouTube ad thumbnail from the approved dark-studio design.
Run from the full project checkout, where the photo library and clean builder are available.
"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__)); THUMBS = os.path.dirname(HERE)
AD5 = THUMBS + "/Ad 5 Every Diet You've Tried Failed For The Same Reason/_build-2026-09-10/build_clean.py"
spec = importlib.util.spec_from_file_location('clean', AD5); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

W, H = 1080, 1920
PHOTO, WAIST, LINES = 'studio-gray-26', 0.705, ['THE DAD BOD', 'PROBLEM']
FOLDER = THUMBS + '/Ad 10 My Dad Bod'
FIT, ASSERT = 45, 25


def build():
    m.LINES = LINES
    lx, ly, barw, gap = 60, 60, 10, 30
    lg = m.logo_img(330)
    tx = lx + barw + gap
    band_top = ly + lg.height + 70
    size = min(m.fit(t, W - tx - 60, 170) for t in LINES)
    f = m.font(size); hs = [f.getbbox(t)[3] - f.getbbox(t)[1] for t in LINES]; lead = int(size * 0.40)
    total = sum(hs) + lead * (len(LINES) - 1)
    # Figure width = 94 % of the frame: solve the head-top position that gives it, then check the type clears it.
    bb = m.src(PHOTO)['bb']; bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    s = 0.94 * W / bw; top = H - WAIST * bh * s
    top = max(top, band_top + total + FIT)                           # never let him rise into the type band
    canvas, mask = m.o1(PHOTO, W, H, 0.5, top, WAIST)
    d = ImageDraw.Draw(canvas); canvas.paste(lg, (lx, ly), lg)
    ty = band_top
    d.rectangle([lx, ty - 14, lx + barw, ty + total + 14], fill=m.RED)
    yy = ty; boxes = []
    for t, hh in zip(LINES, hs):
        b = f.getbbox(t); d.text((tx, yy - b[1]), t, font=f, fill=m.WHITE)
        boxes.append((tx, yy, tx + b[2] - b[0], yy + hh)); yy += hh + lead
    # Clearance: the lowest pixel of the type block to the highest pixel of his mask in the type's columns.
    x0, x1 = min(b[0] for b in boxes), max(b[2] for b in boxes)
    rows = np.where(mask[:, x0:x1 + 1].any(1))[0]
    type_bottom = max(b[3] for b in boxes)
    overlap = rows[(rows >= ty) & (rows <= type_bottom)] if len(rows) else rows
    clear = -1 if len(overlap) else (9999 if not len(rows) else int(rows[rows > type_bottom].min() - type_bottom))
    ok = clear >= ASSERT
    # The waistband must stay in frame (shorts visible = the crop is at the waist, not the navel).
    p = f"{FOLDER}/ad10-claude-9x16_O1-dark-studio-{PHOTO}-FINAL.jpg"; canvas.save(p, quality=93)
    print(f"  ad10 9x16 O1 {PHOTO}  font {size}  head top {int(top)}  clearance {clear} px  {'PASS' if ok else 'FAIL'}  {os.path.getsize(p)//1024} KB")
    return dict(ad='ad10', aspect='9x16', opt='O1', photo=PHOTO, font=size, head_top=int(top), clearance=clear, ok=ok, file=p)


def sheet(r):
    im = Image.open(r['file']); sh = Image.new('RGB', (540 + 3 * 24 + 180, 960 + 48), (242, 242, 244))
    sh.paste(im.resize((540, 960), Image.LANCZOS), (24, 24))
    sh.paste(im.resize((180, 320), Image.LANCZOS), (24 + 540 + 24, 24))
    ImageDraw.Draw(sh).text((24 + 540 + 24, 360), 'feed size', font=m.font(18), fill=(40, 40, 48))
    p = HERE + '/REVIEW_ad10_9x16.jpg'; sh.save(p, quality=88); print('  sheet', p)


if __name__ == '__main__':
    r = build(); json.dump(r, open(HERE + '/qc.json', 'w'), indent=1); sheet(r)
    print('ALL PASS' if r['ok'] else 'QC FAIL'); sys.exit(0 if r['ok'] else 1)
