#!/usr/bin/env python3
"""Plan the 'Real picture of me' chip for the four photoseq stills OFF HIS BODY (Dan 2026-09-12), one common size.
Writes label_place.json {still basename: [size, two_line, fx, fy]} and a preview sheet labelplace_preview.png."""
import json, os, sys
sys.path.insert(0, '.')
from PIL import Image, ImageOps
import beats as B, g3 as G
BOX = (60, 170, G.VW-60, 1330)
stills = [p for b in B.T if b[0] == 'photoseq' for _, p in b[3]['stills']]
def geom(photo):
    bw, bh = BOX[2]-BOX[0], BOX[3]-BOX[1]; s = min(bw/photo.width, bh/photo.height)
    w, h = int(photo.width*s)//2*2, int(photo.height*s)//2*2
    return BOX[0] + (bw-w)//2, BOX[1] + (bh-h)//2, w, h
cands = {}
for p in stills:
    ph = ImageOps.exif_transpose(Image.open(p)); x0, y0, w, h = geom(ph)
    c = G.label_candidates(os.path.basename(p), x0, y0, w, h)
    cands[p] = (c, (x0, y0, w, h))
    print(os.path.basename(p), 'fits:', sorted({k for k in c}, reverse=True)[:6] if c else c)
plan = None
for size in (38, 36, 34, 32, 30, 28):
    pick = {}
    for p, (c, g) in cands.items():
        opt = c.get((size, False)) and (size, False) or (c.get((size, True)) and (size, True))
        if not opt: break
        pick[p] = (opt, c[opt], g)
    if len(pick) == len(stills): plan = pick; break
if plan is None: sys.exit('NO common size keeps the label off him on all four -- shrink further or place in a corner')
out = {}
sheet = []
for p, ((size, two), (bx, by), (x0, y0, w, h)) in plan.items():
    out[os.path.basename(p)] = [size, two, (bx-x0)/w, (by-y0)/h]
    im = G.photo_on_field(ImageOps.exif_transpose(Image.open(p)), box=BOX, real_label=True, label=out[os.path.basename(p)])
    sheet.append(im.resize((360, 640)))
json.dump(out, open('label_place.json', 'w'), indent=1)
S = Image.new('RGB', (360*len(sheet), 640)); [S.paste(t, (i*360, 0)) for i, t in enumerate(sheet)]; S.save('labelplace_preview.png')
print(json.dumps(out, indent=1))
