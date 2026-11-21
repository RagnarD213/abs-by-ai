#!/usr/bin/env python3
"""LABEL PLACEMENT BY MEASUREMENT (Dan 2026-09-12: never over his face or his abs; above his head or off to one side).
For every labelled picture of Dan: render the beat's first and last frame WITHOUT the chip (stills push, so frame 0 is the
loosest framing), person-mask both (Apple Vision, rc/personmask), union + 16 px dilation, then search the safe area for
a box the mask never touches -- BIGGER TYPE before fewer lines, highest clear position first. A group of pictures that
flip quickly (the four after shots) takes ONE size, the smallest any of them needs (skill A12.11).
Writes label_place.json: {"<aspect>:<n0>": {x, y, lines, size, kind}}; --verify re-checks a delivered file.
  python3 zlabel9.py --aspect 9x16|1x1"""
import json, os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw
import cv2
args = sys.argv[1:]
def arg(k, d): return args[args.index(k)+1] if k in args else d
ASPECT = arg('--aspect', '9x16'); SQ = ASPECT == '1x1'
sys.argv = [sys.argv[0], '--aspect', ASPECT, '--nolabel']
import render9 as R
VW, VH = R.VW, R.VH
TOP, LEFT, RIGHT = (30, 30, VW-30) if SQ else (R.G5.TOP_SAFE + 8, 40, VW - 120)      # 9:16: Shorts takes the right ~120 px
BOT = R.CAP_Y - 34
GROUPS = [[4723, 4741, 4759, 4777]]
MANUAL = {   # the robot clip (no person to mask): top-left, clear of the robot's head, hand and the bottle (checked on stills)
    '9x16:85':  dict(x=44, y=160, lines=1, size=44, kind='ai'), '9x16:262': dict(x=44, y=160, lines=1, size=44, kind='ai'),
    '1x1:85':   dict(x=268, y=46, lines=1, size=30, kind='ai'), '1x1:262':  dict(x=30, y=30, lines=1, size=38, kind='ai')}
beats = [b for b in R.tl if (b.get('label') or b['kind'] == 'shot')]
out = json.load(open('label_place.json')) if os.path.exists('label_place.json') else {}
os.makedirs(f'lp{R.SFX}', exist_ok=True)
def frames_of(b):
    # a beat that blurs in is masked after the blur has settled (0.4 s): Vision reads a blurred frame as 80 % person
    ns = [b['n0'] + (14 if R.sp_of(b).get('blur') else 0), b['n1']-1]; d = f'lp{R.SFX}/fr'; R.stills(ns, d)
    return [f'{d}/f{n:05d}.png' for n in ns]
def mask_of(paths):
    small = []
    for p in paths:
        q = p.replace('.png', '_s.png'); Image.open(p).resize((VW//2, VH//2), Image.BILINEAR).save(q); small.append(q)
    os.makedirs(f'lp{R.SFX}/m', exist_ok=True)
    subprocess.run(['./rc/personmask', f'lp{R.SFX}/m'] + small, check=True, capture_output=True)
    m = np.zeros((VH, VW), bool)
    for q in small:
        mm = np.asarray(Image.open(f'lp{R.SFX}/m/' + os.path.basename(q).replace('.png', '.mask.png')).convert('L').resize((VW, VH), Image.BILINEAR)) > 127
        m |= mm
    return cv2.dilate(m.astype(np.uint8), np.ones((33, 33), np.uint8)) > 0
def place(mask, kind, max_size=48, only=None, LEFT=LEFT, RIGHT=RIGHT):
    I = np.pad(mask.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    for size in [s for s in (48, 44, 40, 36, 34, 32, 30, 28) if s <= max_size]:
        for lines in ((1, 2, 3) if kind == 'real' else (1,)):
            if only and (size, lines) != only: continue
            w, h = R.chip_size(kind, lines, size)
            if w > RIGHT - LEFT: continue
            for y in range(TOP, BOT - h, 6):
                xs = np.arange(LEFT, RIGHT - w + 1, 6)
                tot = I[y+h, xs+w] - I[y, xs+w] - I[y+h, xs] + I[y, xs]
                ok = xs[tot == 0]
                if len(ok):
                    ys, xm = np.nonzero(mask[: y+h+200]) if mask.any() else (None, None)
                    hx = float(np.median(np.nonzero(mask[:max(1, np.nonzero(mask.any(1))[0].min()+120)])[1])) if mask.any() else VW/2
                    x = int(ok[np.argmin(np.abs(ok + w/2 - hx))])          # the clear box nearest his head's column
                    return dict(x=x, y=int(y), lines=lines, size=size, kind=kind)
    return None
masks = {}; BND = {}
for b in beats:
    key = f"{ASPECT}:{b['n0']}"
    if key in MANUAL: out[key] = MANUAL[key]; continue
    kind = b.get('label') or 'real'
    masks[b['n0']] = (mask_of(frames_of(b)), kind)
    sp = R.sp_of(b); BND[b['n0']] = {}
    if sp.get('fit') == 'fith':                       # a full-height photo on the field: the chip stays inside the photo's own width (skill S1 A.1)
        pil = R.still(sp['media']); w = int(VH*pil.width/pil.height)//2*2
        BND[b['n0']] = dict(LEFT=(VW - w)//2 + 14, RIGHT=(VW + w)//2 - 14)
    out[key] = place(*masks[b['n0']], **BND[b['n0']])
    if out[key] is None and BND[b['n0']]:             # a photo filled edge to edge by his body has no clear box inside its own width:
        BND[b['n0']] = {}                             # the chip takes the top corner beside his head, overlapping the photo's edge (S1 A.4)
        out[key] = place(*masks[b['n0']])
        if out[key]: out[key]['why'] = 'no clear box inside the photo; top corner beside his head, overlapping the photo edge'
    assert out[key], f'no clear box for {key}'
for g in GROUPS:
    ks = [f'{ASPECT}:{n}' for n in g if f'{ASPECT}:{n}' in out and n in masks]
    if len(ks) > 1:
        # ONE size and ONE line count for the run (they flip every ~0.6 s): the biggest type every picture can take
        done = False
        for size in (48, 44, 40, 36, 34, 32, 30, 28):
            for lines in (1, 2, 3):
                ps = [place(masks[n][0], masks[n][1], only=(size, lines), **BND[n]) for n in g]
                if all(ps):
                    for n, p in zip(g, ps): out[f'{ASPECT}:{n}'] = p
                    # ...and ONE position if a box exists that is clear on all of them (no hop between flips)
                    w, h = R.chip_size('real', lines, size); y = max(p['y'] for p in ps)
                    for x in sorted(range(max([LEFT] + [BND[n].get('LEFT', LEFT) for n in g]), min([RIGHT] + [BND[n].get('RIGHT', RIGHT) for n in g]) - w + 1, 6), key=lambda x: abs(x - np.mean([p['x'] for p in ps]))):
                        if not any(masks[n][0][y:y+h, x:x+w].any() for n in g):
                            for n in g: out[f'{ASPECT}:{n}'] = dict(x=int(x), y=int(y), lines=lines, size=size, kind='real')
                            break
                    done = True; break
            if done: break
        assert done, 'no common label size for the group'
json.dump(out, open('label_place.json', 'w'), indent=1)
for b in beats:
    key = f"{ASPECT}:{b['n0']}"; p = out.get(key)
    if not p or b['n0'] not in masks: print(key, p); continue
    im = Image.open(f"lp{R.SFX}/fr/f{b['n1']-1:05d}.png").convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); R.chip_at(ov, p['kind'], p['x'], p['y'], p['lines'], p['size'])
    edge = cv2.Canny((masks[b['n0']][0]*255).astype(np.uint8), 50, 150) > 0
    a = np.asarray(Image.alpha_composite(im, ov).convert('RGB')).copy(); a[edge] = (255, 0, 255)
    Image.fromarray(a).resize((VW//2, VH//2)).save(f"lp{R.SFX}/proof_{b['n0']}.jpg", quality=88)
    print(key, p)
