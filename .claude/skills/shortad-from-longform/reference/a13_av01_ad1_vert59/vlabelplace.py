#!/usr/bin/env python3
"""AV-01: place the labels this cutdown adds, by MEASURING him on the approved vertical's own frames.

Dan, 2026-09-12: "the label will not block my face or my abs ... put it above my head, to the side,
or somewhere that it doesn't block my face and my abs".

Ported from the square's `sqlabelplace.py`, with one deliberate change: the square RE-RENDERED each
beat without a chip and measured that; here the beats are not re-rendered at all -- the cutdown is a
selection out of the approved vertical -- so the mask is taken from the DELIVERED master's own pixels
(`picture.mp4`), which is the picture the chip will actually sit on.

  python3 vlabelplace.py                       # measure + choose + proof sheets
  python3 vlabelplace.py --verify <file.mp4>   # gate on the delivered cutdown: no chip touches him
"""
import glob, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, '.')
import chips as V, beats as BT

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
CLEAR = 16                    # px of clearance between the chip and any pixel of him
TOP_SAFE = 150                # vlib.TOP_SAFE
CHIP_BOTTOM_MAX = 1340        # clear of the caption band (vlib.CAP_Y = 1400)
SIDE_SAFE = 40
D = '_place'

# The labels this cutdown ADDS to the approved vertical, and why.
#   today_towel / today_trees  real after pictures of Dan; the approved vertical carries no chip
#                              on them (it predates Dan's 2026-09-11 rule). The square added them.
#   after_reveal               the app's "Download Your Future Self" screen -- the picture in it is
#                              a generated result, so it carries our AI chip (lesson A6.13). Also
#                              new in the square.
# NOT added: the hook's chip is already burned into `ai_goal_plain.mp4` and is measured below
# rather than moved (see notes-AV-01.md).
ADD = {'today_towel': 'real', 'today_trees': 'real', 'after_reveal': 'ai'}

# A per-beat floor on the chip's top edge. Only `after_reveal` needs one: its card's own top rim
# sits at y=152 and the app screen's grey nav line ("your future self") runs at y~148, so the
# search's first clear row (TOP_SAFE=150) put the chip STRADDLING the card's edge and printing
# over that nav line. 176 is the first row fully inside the white plate; the headline starts at
# y=240, so the chip lands in the plate's own top margin, clear of every element and of the man
# in the picture. Measured on frames 2209-2270, where the card does not move.
Y_MIN = {'after_reveal': 176}


def beat(media):
    tl, ov = BT.timeline()
    for b in tl + ov:
        if b.get('media') == media: return b
    raise SystemExit(f'no beat with media={media!r}')


def masks_for(video, idxs, tag):
    d = f'{D}/{tag}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d + '/m')
    sel = '+'.join(f'eq(n,{i})' for i in idxs)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', video, '-vf', f"select='{sel}'",
                    '-fps_mode', 'passthrough', f'{d}/%04d.png'], check=True)
    fs = sorted(glob.glob(f'{d}/*.png'))
    assert len(fs) == len(idxs), (len(fs), len(idxs))
    subprocess.run(['./rc/personmask', f'{d}/m'] + fs, check=True, capture_output=True)
    ms = []
    for f in fs:
        mf = f'{d}/m/' + os.path.basename(f).replace('.png', '.mask.png')
        ms.append(np.array(Image.open(mf).convert('L').resize((V.VW, V.VH))) > 127)
    return fs, ms


def dilate(m, r):
    from scipy.ndimage import binary_dilation
    return binary_dilation(m, iterations=r)


def head_box(m):
    ys, xs = np.nonzero(m)
    y0 = ys.min()
    hs = xs[ys <= y0 + 0.12*V.VH]
    return int(hs.min()), int(y0), int(hs.max()), int(y0 + 0.12*V.VH)


def choose(label, union, hbox, y_min=TOP_SAFE):
    hx0, hy0, hx1, hy1 = hbox; hcx = (hx0 + hx1)/2
    dil = dilate(union, CLEAR)
    ii = np.pad(dil.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    def clear(x, y, w, h):
        return ii[y+h, x+w] - ii[y, x+w] - ii[y+h, x] + ii[y, x] == 0
    lines_opts = (1, 2, 3) if label == V.REAL_LABEL else (1,)
    for cls in ('A', 'B', 'C'):
        for size in (34, 32, 30, 28, 26, 24):
            for lines in lines_opts:
                w, h = V.chip_dims(label, lines, size)
                best = None
                for y in range(max(TOP_SAFE, y_min), CHIP_BOTTOM_MAX - h + 1, 4):
                    for x in range(SIDE_SAFE, V.VW - SIDE_SAFE - w + 1, 4):
                        if not clear(x, y, w, h): continue
                        above = y + h <= hy0
                        beside = (not above) and y < hy1
                        if cls == 'A' and not above: continue
                        if cls == 'B' and not beside: continue
                        cx = x + w/2
                        cost = abs(cx - hcx) + (0 if cls == 'A' else 0.5*y)
                        if best is None or cost < best[0]: best = (cost, x, y)
                if best:
                    return dict(cls=cls, lines=lines, size=size, x=best[1], y=best[2], w=w, h=h)
    return None


def main():
    os.makedirs(D, exist_ok=True)
    res = {}
    for media, kind in ADD.items():
        b = beat(media)
        n0, n1 = int(round(b['t0']*FPS)), int(round(b['t1']*FPS))
        nfr = n1 - n0
        idxs = sorted(set([n0 + k for k in range(0, nfr, 3)] + [n1 - 1]))
        fs, ms = masks_for('picture.mp4', idxs, media)
        union = np.any(ms, axis=0)
        label = V.REAL_LABEL if kind == 'real' else V.AI_LABEL
        hb = head_box(union)
        c = choose(label, union, hb, Y_MIN.get(media, TOP_SAFE))
        assert c, f'{media}: no clear placement at any size'
        ys, xs = np.nonzero(union)
        res[media] = dict(c, kind=kind, beat=[b['t0'], b['t1']], frames=nfr, head=hb,
                          body=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
        print(media, res[media], flush=True)
        lay = V.chip_at(label, c['x'], c['y'], c['lines'], c['size'])
        tiles = []
        for f in (fs[0], fs[len(fs)//2], fs[-1]):
            im = Image.open(f).convert('RGBA'); im.alpha_composite(lay)
            a = np.array(im); edge = dilate(union, 2) & ~union; a[edge] = [255, 0, 0, 255]
            tiles.append(Image.fromarray(a).convert('RGB').resize((360, 640)))
        sheet = Image.new('RGB', (1080, 640))
        for i, t in enumerate(tiles): sheet.paste(t, (360*i, 0))
        sheet.save(f'proof/label_{media}.jpg')
    json.dump(res, open('label_place.json', 'w'), indent=1)
    print('wrote label_place.json')


def verify(video):
    """Gate the DELIVERED cutdown on two separate facts, measured separately.

    ⚠ THE PERSON MASK CANNOT BE RUN ON A FRAME THAT ALREADY CARRIES THE CHIP. Apple Vision
    absorbs the chip into the person: on this build the delivered towel frames mask from y=149 --
    exactly the chip's top edge -- while the same content without the chip masks from y=244, where
    the top of his hair actually is. Measured that way the whole 644x56 box reads as "contact"
    while the eye sees a 94 px gap above his head. That is the square's audit finding 5 again (a
    correct file failed because of the instrument, not the bound), so the instrument is split, not
    the bound relaxed:

      A  CLEARANCE is measured on the MASTER's own pixels at the same frames -- the picture the
         chip sits on -- dilated by 8 px, exactly as `_shared/deliver` measures it.
      B  PRESENCE is measured on the DELIVERED pixels: the chip box must correlate >= 0.99 with
         the chip drawn over that master frame, on every sampled frame.

    A negative control runs with every pass (`--verify ... ` prints it): the same box moved down
    onto his abs FAILS A, so A is not permissive.
    """
    import numpy as _np
    from PIL import Image as _I
    import chips as CH
    P = json.load(open('cut_plan.json'))['ranges']
    place = json.load(open('label_place.json'))

    def dstwin(t0, t1):
        for p in P:
            a, bb = max(t0, p['src0']), min(t1, p['src1'])
            if bb - a > 0.02:
                return (p['dst0'] + (a - p['src0']), p['dst0'] + (bb - p['src0']),
                        int(round(p['n0'] + (a - p['src0'])*FPS)))
        return None

    bad, out = 0, {}
    for media, c in place.items():
        w = dstwin(*c['beat'])
        if not w:
            out[media] = dict(skipped='not in the cutdown'); continue
        d0, d1, m0 = w
        n0, n1 = int(round(d0*FPS)), int(round(d1*FPS))
        k = sorted(set(list(range(0, n1 - n0, 3)) + [n1 - n0 - 1]))
        x, y, cw, ch = c['x'], c['y'], c['w'], c['h']

        # --- A clearance, on the master's own pixels (no chip in them) --------
        _, ms = masks_for('picture.mp4', [m0 + i for i in k], 'clr_' + media)
        contact = max(int(dilate(m, 8)[y:y+ch, x:x+cw].sum()) for m in ms)
        # negative control: the same box dropped onto his torso must NOT be clear
        ys = [int(_np.nonzero(m.any(axis=1))[0].mean()) for m in ms]
        yc = min(max(ys), 1920 - ch)
        ctrl = max(int(dilate(m, 8)[yc:yc+ch, x:x+cw].sum()) for m in ms)

        # --- B presence, on the delivered pixels ------------------------------
        label = V.REAL_LABEL if c['kind'] == 'real' else V.AI_LABEL
        lay = V.chip_at(label, x, y, c['lines'], c['size'])
        fs_d, _ = masks_for(video, [n0 + i for i in k], 'pres_' + media)
        fs_m = sorted(glob.glob(f'{D}/clr_{media}/*.png'))
        corrs = []
        for fd, fm in zip(fs_d, fs_m):
            want = _I.open(fm).convert('RGBA'); want.alpha_composite(lay)
            a = _np.asarray(want.convert('L'), _np.float32)[y:y+ch, x:x+cw]
            b = _np.asarray(_I.open(fd).convert('L'), _np.float32)[y:y+ch, x:x+cw]
            corrs.append(float(_np.corrcoef(a.ravel(), b.ravel())[0, 1]))
        ok = contact == 0 and min(corrs) >= 0.99 and ctrl > 0
        bad += not ok
        out[media] = dict(box=[x, y, cw, ch], window=[round(d0, 3), round(d1, 3)],
                          kind=c['kind'], frames=len(k), clearance_contact_px=contact,
                          negative_control_contact_px=ctrl, presence_min_corr=round(min(corrs), 5),
                          ok=ok)
        print(f"{'PASS' if ok else 'FAIL'}  {media:14s} {c['kind']:4s} box {x},{y} {cw}x{ch}  "
              f"{len(k)} frames  clearance {contact} px  presence r={min(corrs):.5f}  "
              f"(negative control at y={yc}: {ctrl} px)")
    json.dump(out, open(video + '.labelcheck.json', 'w'), indent=1)
    print('LABELS OFF HIS FACE AND ABS, AND ACTUALLY ON THE FILE:',
          'PASS' if not bad else f'FAIL ({bad})')
    return bad


if __name__ == '__main__':
    if '--verify' in sys.argv:
        sys.exit(1 if verify(sys.argv[sys.argv.index('--verify') + 1]) else 0)
    main()
