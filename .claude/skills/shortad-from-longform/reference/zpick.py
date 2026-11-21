#!/usr/bin/env python3
"""Contact-sheet candidate AFTER pictures as the RENDERED 9:16 full-bleed crop -- skill rule 12 says verify the push
windows ON THE ASSET before rendering, and the standing rule says contact-sheet the RENDERED crop, never the file.

Each tile is push_cover() at the START of the beat (z=1.00) with the TIGHTEST push window (z=1.05) drawn in red, so
"hairline >= 10 % from the top and the shorts line inside the tightest window, subject centred" is checkable by eye,
plus the real-picture chip composited where it will actually sit. Run it FROM the build dir (it imports that build's
g5). Built for Ad 5 round 1 (2026-09-11), where six after pictures had to be chosen out of 46 pool-shoot and 130
studio finals.

    python3 zpick.py "<glob of candidates>" out.jpg [--cols 8] [--oy 0.30] [--start 0] [--n 24]

It filters to PORTRAIT sources automatically: a landscape still cannot be full-bleed in 9:16 at all (a 1.22:1 frame
crops to a head), which is the whole reason this round existed.
"""
import sys, os, glob, numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw
sys.path.insert(0, os.getcwd())          # run it from the BUILD dir so it picks up that build's g5/g8
try: import g5 as G                      # optional: draws the real-picture chip where it will actually sit
except Exception: G = None
VW, VH = 1080, 1920

def still(p): return ImageOps.exif_transpose(Image.open(p)).convert('RGB')

def warp_crop(img, x0, y0, w, h, W=VW, H=VH):
    sx, sy = W/w, H/h
    M = np.float32([[sx, 0, -x0*sx], [0, sy, -y0*sy]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

def rendered(pil, ox=0.5, oy=0.5, z=1.0):
    W0, H0 = pil.size; s = max(VW/W0, VH/H0)*z; cw, ch = VW/s, VH/s
    return warp_crop(np.asarray(pil), (W0-cw)*ox, (H0-ch)*oy, cw, ch)

def tile(path, ox=0.5, oy=0.5, tw=270):
    pil = still(path)
    a = rendered(pil, ox, oy, 1.0)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    # tightest push window (z=1.05 of the same crop), drawn in the rendered frame's own coordinates
    m = 1 - 1/1.05
    d.rectangle([VW*m/2, VH*m/2, VW*(1-m/2), VH*(1-m/2)], outline=(255, 0, 0), width=6)
    if G is not None and hasattr(G, 'real_chip'):
        lay = G.blank(); G.real_chip(lay)
        im = Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB')
    im = im.resize((tw, int(tw*VH/VW)), Image.LANCZOS)
    d2 = ImageDraw.Draw(im); d2.rectangle([0, 0, tw-1, im.height-1], outline=(90, 100, 58), width=3)
    d2.text((8, 6), os.path.basename(path)[:34], fill=(255, 255, 0))
    d2.text((8, 20), f'{pil.size[0]}x{pil.size[1]} ar={pil.size[0]/pil.size[1]:.2f} oy={oy}', fill=(255, 255, 0))
    return im

def sheet(paths, out, cols=6, ox=0.5, oy=0.5):
    ts = [tile(p, ox, oy) for p in paths]
    if not ts: return
    tw, th = ts[0].size; rows = (len(ts)+cols-1)//cols
    S = Image.new('RGB', (cols*tw, rows*th), (20, 20, 20))
    for i, t in enumerate(ts): S.paste(t, ((i % cols)*tw, (i//cols)*th))
    S.save(out); print(out, S.size, len(ts))

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('glob'); ap.add_argument('out')
    ap.add_argument('--cols', type=int, default=6); ap.add_argument('--oy', type=float, default=0.5)
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--n', type=int, default=36)
    a = ap.parse_args()
    ps = sorted(glob.glob(a.glob))
    ps = [p for p in ps if Image.open(p).size[0] < Image.open(p).size[1]][a.start:a.start+a.n]
    sheet(ps, a.out, a.cols, oy=a.oy)
