#!/usr/bin/env python3
"""ROUND 1 (Dan, 2026-09-13): place every label on a picture of Dan by MEASURING him.

  "put that above my head or somewhere it doesn't block my face or abs ... this is supposed to
   be proof, and this is kind of blocking the proof."

For each labelled full-bleed / full-height beat: render the beat WITHOUT a chip, run Apple Vision
person segmentation (rc/personmask) on every 3rd frame + the last, take the union mask over the
whole beat (the stills push, so frame 0 is not enough -- [A10].4), dilate it by CLEAR px, and
search chip placements in preference order:
   A  one line, fully ABOVE his head          (Dan's first choice)
   B  beside his head, one or two lines, top of frame
   C  anywhere else clear of him, above the caption band
Inside the safe area (y >= 80, x <= 980 for the in-feed strip) and, for a full-HEIGHT photo, inside
the photo itself (never straddling the photo's edge and the field). Writes label_place.json; the
numbers are then copied into sqassets.py so the placement is auditable in the treatment table.

  python3 sqlabelplace.py            # measure + choose
  python3 sqlabelplace.py --verify <delivered.mp4> [--boxes boxes.json]   # gate: no chip touches him (8 px)
"""
import json, os, subprocess, sys, glob, shutil
sys.path.insert(0, '.')
import numpy as np
from PIL import Image
import sqlib as V, beats, sqassets as SA
import render as R

FF = R.FF
CLEAR = 16                  # px of clearance between the chip and any pixel of him
CHIP_BOTTOM_MAX = 800       # above the caption band (captions ~848..912 + scrim)
D = '_r1/place'

def plan():
    tl, _ = beats.timeline(); prev, out = 0, []
    for b in tl:
        cum = round(b['t1']*R.FPS); out.append((b, prev, cum-prev)); prev = cum
    return out

def masks_for(video, idxs, tag):
    d = f'{D}/{tag}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + '/m')
    sel = '+'.join(f'eq(n,{i})' for i in idxs)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', video, '-vf', f"select='{sel}'",
                    '-fps_mode', 'passthrough', f'{d}/%04d.png'], check=True)
    fs = sorted(glob.glob(f'{d}/*.png'))
    subprocess.run(['./rc/personmask', f'{d}/m'] + fs, check=True, capture_output=True)
    ms = []
    for f in fs:
        mf = f'{d}/m/' + os.path.basename(f).replace('.png', '.mask.png')
        m = np.array(Image.open(mf).convert('L').resize((V.VW, V.VH))) > 127
        ms.append(m)
    return fs, ms

def dilate(m, r):
    from scipy.ndimage import binary_dilation
    return binary_dilation(m, iterations=r)

def head_box(m):
    ys, xs = np.nonzero(m)
    y0, y1 = ys.min(), ys.max()
    hs = xs[ys <= y0 + 0.12*(V.VH)]            # the top ~130 px of him = head
    return int(hs.min()), int(y0), int(hs.max()), int(y0 + 0.12*V.VH)

def choose(label, union, hbox, xr):
    x_lo, x_hi = xr
    hx0, hy0, hx1, hy1 = hbox; hcx = (hx0+hx1)/2
    dil = dilate(union, CLEAR)
    ii = np.pad(dil.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    def clear(x, y, w, h):
        return ii[y+h, x+w] - ii[y, x+w] - ii[y+h, x] + ii[y, x] == 0
    opts = []
    lines_opts = (1, 2, 3) if label == V.REAL_LABEL else (1,)
    for cls in ('A', 'B', 'C'):
        for size in (34, 32, 30, 28, 26, 24):      # bigger type first, then fewer lines
            for lines in lines_opts:
                w, h = V.chip_dims(label, lines, size)
                best = None
                for y in range(V.TOP_SAFE, CHIP_BOTTOM_MAX - h + 1, 4):
                    for x in range(max(x_lo, 40), min(x_hi, 980) - w + 1, 4):
                        if not clear(x, y, w, h): continue
                        above = y + h <= hy0
                        beside = (not above) and y < hy1
                        if cls == 'A' and not above: continue
                        if cls == 'B' and not beside: continue
                        cx = x + w/2
                        # A: centred over his head; B/C: as close to his head as clear space allows, high
                        cost = abs(cx - hcx) + (0 if cls == 'A' else 0.5*y)
                        if best is None or cost < best[0]: best = (cost, x, y)
                if best:
                    return dict(cls=cls, lines=lines, size=size, x=best[1], y=best[2], w=w, h=h)
    return None

def main():
    os.makedirs(D, exist_ok=True)
    res = {}
    for b, n0, nfr in plan():
        key = b.get('media')
        if not key: continue
        T = SA.treat(key)
        if not T['label'] or T['mode'] not in ('cover', 'fith'): continue
        label = V.REAL_LABEL if T['label'] == 'real' else V.AI_LABEL
        SA.SQ[key] = dict(SA.SQ[key], label=None)          # render the beat with no chip
        vid = f'{D}/{key}.mp4'
        R._render(vid, b, nfr, b['t0'])
        idxs = sorted(set(list(range(0, nfr, 3)) + [nfr-1]))
        fs, ms = masks_for(vid, idxs, key)
        union = np.any(ms, axis=0)
        hb = head_box(union)
        # A full-HEIGHT photo's chip stays INSIDE the photo -- except photoshop_gag: a 0.56:1 photo whose
        # arms fill it leaves 164 px beside his head, and the AI chip is 205 px even at 24 px type. The
        # round-1 audit flagged the straddle (finding 3); measured, nothing inside the photo clears his
        # head, so the chip keeps the photo's top corner beside his head. Reported to Dan as a trade-off.
        if T['mode'] == 'fith' and key != 'photoshop_gag':
            ar = R.media_ar(key); w = int(round(V.VH*ar)); w -= w % 2; px = (V.VW-w)//2
            xr = (px + 16, px + w - 16)
        else:
            xr = (0, V.VW)
        c = choose(label, union, hb, xr)
        assert c, f'{key}: no clear placement at any size'
        res[key] = dict(c, beat=[b['t0'], b['t1']], head=hb, xr=xr,
                        body=[int(v) for v in (np.nonzero(union)[1].min(), np.nonzero(union)[0].min(),
                                               np.nonzero(union)[1].max(), np.nonzero(union)[0].max())])
        print(key, res[key], flush=True)
        # proof tile: first + last frame, union outline, chip
        lay = V.chip_at(label, c['x'], c['y'], c['lines'], c['size'])
        tiles = []
        for f in (fs[0], fs[-1]):
            im = Image.open(f).convert('RGBA'); im.alpha_composite(lay)
            a = np.array(im); edge = dilate(union, 2) & ~union; a[edge] = [255, 0, 0, 255]
            tiles.append(Image.fromarray(a).convert('RGB').resize((540, 540)))
        sheet = Image.new('RGB', (1080, 540)); sheet.paste(tiles[0], (0, 0)); sheet.paste(tiles[1], (540, 0))
        sheet.save(f'{D}/{key}_proof.jpg')
    json.dump(res, open('label_place.json', 'w'), indent=1)

def verify(video, override=None):
    """On the DELIVERED file: every labelled beat, every 3rd frame + last, person mask, and the chip box from
    sqassets (or `override` {key: (x, y, w, h)}) must not touch him (8 px). Exit 1 on any contact."""
    bad = 0; out = {}
    for b, n0, nfr in plan():
        key = b.get('media')
        if not key: continue
        T = SA.treat(key)
        if not T['label'] or T['mode'] not in ('cover', 'fith'): continue
        if override and key in override:
            x, y, w, h = override[key]
        else:
            c = T['chip']; label = V.REAL_LABEL if T['label'] == 'real' else V.AI_LABEL
            w, h = V.chip_dims(label, c['lines'], c['size']); x, y = c['x'], c['y']
        idxs = sorted(set([n0 + k for k in range(0, nfr, 3)] + [n0 + nfr - 1]))
        fs, ms = masks_for(video, idxs, 'verify_' + key)
        worst = 0
        for m in ms:
            worst = max(worst, int(dilate(m, 8)[y:y+h, x:x+w].sum()))
        ok = worst == 0; bad += not ok
        out[key] = dict(box=[x, y, w, h], frames=len(ms), contact_px=worst, ok=ok)
        print(f"{'PASS' if ok else 'FAIL'}  {key:15s} box {x},{y} {w}x{h}  {len(ms)} frames  contact {worst} px")
    json.dump(out, open(video + '.labelcheck.json', 'w'), indent=1)
    print('LABELS OFF HIS BODY', 'PASS' if not bad else f'FAIL ({bad})')
    return bad

if __name__ == '__main__':
    if '--verify' in sys.argv:
        v = sys.argv[sys.argv.index('--verify') + 1]
        ov = json.load(open(sys.argv[sys.argv.index('--boxes') + 1])) if '--boxes' in sys.argv else None
        sys.exit(1 if verify(v, ov) else 0)
    main()
