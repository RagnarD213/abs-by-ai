"""DS-31 R2 colour options (Dan, R1: "not warm enough. The colors aren't vivid and saturated enough. Give me some better
color correction options"). Varies warmth and saturation only, at Color A's brightness (VIDEO-RULES: vary the requested
property). Same camera chain as picture.py (Pair B crop + land-then-hold x, lanczos to 1080x1920, then the grade).

Out: col/<opt>-<frame>.png stills, col/options.json (filters + measured numbers), col/<opt>-sample.mp4 (6.3 s, sound).
  python3 recipe/col_options.py stills      build + measure the stills (brightness matched to A by an eq=brightness term)
  python3 recipe/col_options.py samples     moving samples with sound for every option
"""
from pathlib import Path
import subprocess, sys, os, json
import numpy as np
from PIL import Image
W = Path(__file__).resolve().parents[1]; O = W/'col'; O.mkdir(exist_ok=True)
argv = sys.argv; sys.argv = [argv[0]]
src = (W/'recipe/picture.py').read_text().split('def probe(f):')[0]
G = {'__file__': str(W/'recipe/picture.py'), '__name__': 'picture_head'}; exec(compile(src, 'picture_head', 'exec'), G)
sys.argv = argv
ff, F, S, FPS, COLOR_A, shots, source_t, ENC = G['ff'], G['F'], G['S'], G['FPS'], G['COLOR_A'], G['shots'], G['source_t'], G['ENC']
rows = {r['n']: r for r in json.load(open(W/'source-measurements.json'))}

DEN = "hqdn3d=1.5:1.5:3:3"; CURVE = "curves=all='0/0 0.06/0.045 0.15/0.19 0.25/0.35 0.5/0.61 0.8/0.87 1/1'"; SHARP = "unsharp=5:5:0.3:5:5:0"
assert COLOR_A.startswith(DEN + ',' + CURVE) and COLOR_A.endswith(SHARP)
# Round 2 grade method (third pass; the first two are in git history and the R2 notes): a global warm white balance
# (colorbalance red up / blue down) grays the teal backdrop, so the backdrop could not get more vivid however much
# saturation went on top, and global saturation turned skin orange. So both warmth and saturation live in one
# luma-preserving 3D LUT (col/<opt>.cube) applied after A's denoise + contrast curve, in BT.709 Y'CbCr:
#   warmth: a small chroma push toward skin tone, applied to warm hues and near-neutrals only (the cool band is masked
#           out), scaled up with brightness so shadows do not go muddy;
#   saturation: a base factor (A runs eq=saturation=0.90), an extra lift for the cool band (backdrop, tubes: hue
#           130-230) with a few degrees of rotation toward blue there, and a smaller lift on skin hues.
# E keeps A's own (cool) colour balance and only adds the saturation, for comparison.
A_CB = 'rs=0.006:gs=-0.008:bs=0.014:rm=0.005:gm=-0.018:bm=0.045:pl=0'
OPTS = {
    'A': dict(name='Color A (Round 1, Meal Prep)', warm=None),
    'B': dict(name='Warm natural', cb=None, tint=0.010, base=1.00, cool=0.30, skin=0.04, rot=3),
    'C': dict(name='Warm vivid', cb=None, tint=0.016, base=1.04, cool=0.55, skin=0.08, rot=5),
    'D': dict(name='Golden bold', cb=None, tint=0.024, base=1.08, cool=0.80, skin=0.12, rot=6),
    'E': dict(name='Vivid, same warmth as A', cb=A_CB, tint=0.0, base=1.04, cool=0.55, skin=0.08, rot=0),
}
def build_lut(k, o, N=33):
    g = np.linspace(0, 1, N); r, gg, bb = np.meshgrid(g, g, g, indexing='ij'); rgb = np.stack([r, gg, bb], -1)
    Y = rgb @ np.array([.2126, .7152, .0722]); mx, mn = rgb.max(-1), rgb.min(-1); d = mx - mn + 1e-9
    h = np.where(mx == r, ((gg - bb)/d) % 6, np.where(mx == gg, (bb - r)/d + 2, (r - gg)/d + 4))*60
    def bump(c, w): x = np.abs((h - c + 180) % 360 - 180); return np.clip(1 - x/w, 0, 1)**1.5
    chroma = np.clip(d*6, 0, 1); cool = bump(180, 50)*chroma; skin = bump(22, 28)*chroma
    gain = 0.90*o['base']*(1 + o['cool']*cool + o['skin']*skin)
    cb_, cr = (bb - Y)/1.8556, (r - Y)/1.5748
    ang = np.deg2rad(o['rot'])*cool   # + = counter-clockwise in (Cb, Cr): cyan turns toward blue
    cb2 = gain*(cb_*np.cos(ang) - cr*np.sin(ang)); cr2 = gain*(cb_*np.sin(ang) + cr*np.cos(ang))
    keep = np.clip(1 - np.abs((h - 180 + 180) % 360 - 180)/95, 0, 1)**0.4*np.clip(d*10, 0, 1)   # the cool band, hard-edged (a soft mask let the push turn the teal green)
    wt = o['tint']*(1 - keep)*np.clip(Y*2.2, 0, 1)   # warm push: not on the cool band, eased in the shadows
    cb2 -= wt*0.55; cr2 += wt*0.83
    R2 = Y + 1.5748*cr2; B2 = Y + 1.8556*cb2; G2 = (Y - .2126*R2 - .0722*B2)/.7152
    out = np.clip(np.stack([R2, G2, B2], -1), 0, 1)
    f = O/f'{k}.cube'
    with open(f, 'w') as fh:
        fh.write(f'LUT_3D_SIZE {N}\n')
        for bi in range(N):
            for gi in range(N):
                for ri in range(N): fh.write('%.6f %.6f %.6f\n' % tuple(out[ri, gi, bi]))
    return f
def grade(o, gamma=1.0, k=None):
    if o.get('warm', 1) is None: return COLOR_A
    lut = build_lut(k, o)
    return ','.join([DEN, CURVE] + ([f"colorbalance={o['cb']}"] if o['cb'] else []) + [f"lut3d=file='{lut}'", f"eq=gamma={gamma:.4f}", SHARP])

FRAMES = {'tight': ('S0084', 4.00), 'wide': ('S0484', 17.00), 'closing': ('S1756', 60.00)}
def cam_vf(s, n, g):
    cw, ch, y = s['crop']; x = dict(s['tracking'])[n]
    return f"crop={cw}:{ch}:{x}:{y},scale=1080:1920:flags=lanczos,{g},setsar=1"
def grab(sid, t, g, out):
    s = next(x for x in shots if x['id'] == sid); n = int(round(t*FPS))
    ff(['-ss', f'{source_t(n):.5f}', '-i', S, '-frames:v', 1, '-vf', cam_vf(s, n, g) + ',format=rgb24', out]); return s, n

def measure(png, s, n):
    im = np.asarray(Image.open(png).convert('RGB')).astype(np.float32)/255
    y = im @ np.array([.2126, .7152, .0722]); mx, mn = im.max(2), im.min(2); sat = np.where(mx > 0, (mx - mn)/np.maximum(mx, 1e-6), 0)
    # skin: inner cheek/forehead patch of the measured face box, mapped from source to the 1080x1920 frame
    cw, ch, cy = s['crop']; x = dict(s['tracking'])[n]; k = 1080/cw
    r = min(rows, key=lambda m: abs(m - n)); fx0, fy0, fx1, fy1 = rows[r]['face']
    X0, X1 = (fx0 - x)*k, (fx1 - x)*k; Y0, Y1 = (fy0 - cy)*k, (fy1 - cy)*k
    px = im[int(Y0 + .45*(Y1 - Y0)):int(Y0 + .70*(Y1 - Y0)), int(X0 + .22*(X1 - X0)):int(X0 + .78*(X1 - X0))].reshape(-1, 3)
    import colorsys
    hs = np.array([colorsys.rgb_to_hsv(*p) for p in px[::7]]); skin = hs[(hs[:, 1] > .15) & (hs[:, 2] > .2)]
    # tubes: brightest saturated column band in the wide frames (hue of pixels with value > 0.8 and sat > 0.25)
    bright = (mx > .8) & (sat > .25); th = None
    if bright.sum() > 2000:
        tp = im[bright][::23]; th = float(np.median([colorsys.rgb_to_hsv(*p)[0] for p in tp])*360)
    bg = im[60:420, 40:300].reshape(-1, 3); bgh = float(np.median([colorsys.rgb_to_hsv(*p)[0] for p in bg[::11]])*360)
    bgs = sat[60:420, 40:300]
    return dict(luma=round(float(np.median(y)), 4), mean_luma=round(float(y.mean()), 4), sat=round(float(np.median(sat)), 4),
                backdrop_sat=round(float(np.median(bgs)), 3),
                skin_hue=round(float(np.median(skin[:, 0])*360), 1), skin_sat=round(float(np.median(skin[:, 1])), 3),
                tube_hue=None if th is None else round(th, 1), backdrop_hue=round(bgh, 1))

if 'stills' in argv:
    res = {}
    for k, o in OPTS.items():
        # Brightness is matched on MEAN luma with a gamma term (bisection): the median sits inside the black tank top's
        # cluster and jumps, and eq=brightness clips the blacks non-linearly; median luma is still reported.
        gm = 1.0
        if k != 'A':
            target = np.mean([res['A']['frames'][f]['mean_luma'] for f in ('tight', 'wide')])
            def ml(gg_):
                v = []
                for fk in ('tight', 'wide'):
                    sid, t = FRAMES[fk]; p = O/'_probe.png'; s_, n_ = grab(sid, t, grade(o, gg_, k), p); v.append(measure(p, s_, n_)['mean_luma'])
                return np.mean(v) - target
            lo, hi = 0.85, 1.25
            for it in range(8):
                gm = (lo + hi)/2; e = ml(gm)
                if abs(e) < 0.0008: break
                if e < 0: lo = gm
                else: hi = gm
        res[k] = dict(name=o['name'], filter=grade(o, gm, k), gamma=round(gm, 4), frames={})
        for fk, (sid, t) in FRAMES.items():
            p = O/f'{k}-{fk}.png'; s, n = grab(sid, t, res[k]['filter'], p); res[k]['frames'][fk] = measure(p, s, n)
        print(k, o['name'], json.dumps(res[k]['frames']), flush=True)
    (O/'options.json').write_text(json.dumps(res, indent=1))

if 'samples' in argv:
    res = json.load(open(O/'options.json')); a = 25.66; b = 31.93   # wide S0769 then tight S0863, speech from the first second
    for k, o in res.items():
        parts = []
        for sid in ('S0769', 'S0863'):
            s = next(x for x in shots if x['id'] == sid); cw, ch, y = s['crop']
            import cv2
            pts = cv2.approxPolyDP(np.array([[(n - s['n0'])/FPS, x] for n, x in s['tracking']], np.float32), .1, False).reshape(-1, 2).tolist()
            expr = str(pts[0][1]) + ''.join(f'+({bb[1]-aa[1]:.4f})*clip((t-{aa[0]:.5f})/{bb[0]-aa[0]:.5f},0,1)' for aa, bb in zip(pts, pts[1:]) if bb[0] > aa[0])
            out = O/f'_{k}-{sid}.mp4'; parts.append(out)
            ff(['-ss', f"{source_t(s['n0']):.5f}", '-i', S, '-an', '-vf', f"setpts=PTS-STARTPTS,crop={cw}:{ch}:'{expr}':{y},scale=1080:1920:flags=lanczos,{o['filter']},setsar=1,format=yuv420p",
                '-frames:v', s['n1'] - s['n0']] + ENC + [out])
        cat = O/f'_{k}.txt'; cat.write_text(''.join(f"file '{p}'\n" for p in parts))
        ff(['-f', 'concat', '-safe', 0, '-i', cat, '-ss', f'{a:.3f}', '-i', W/'voice.wav', '-t', f'{b - a:.3f}', '-map', '0:v', '-map', '1:a',
            '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 19, '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', O/f'{k}-sample.mp4'])
        print('SAMPLE', k, flush=True)

if 'pick' in argv:   # python3 recipe/col_options.py pick C  -> col/pick.json, read by picture.py
    k = argv[argv.index('pick') + 1]; res = json.load(open(O/'options.json'))
    (O/'pick.json').write_text(json.dumps(dict(option=k, name=res[k]['name'], filter=res[k]['filter'], measured=res[k]['frames'],
                                               why='recommended in R2; Dan picks on the page'), indent=1)); print('PICK', k, res[k]['name'])

if 'broll' in argv:   # each B-roll clip (its R2 grade, unchanged from R1) beside the camera frames before and after it, per option
    res = json.load(open(O/'options.json')); B2 = W.parent/'round1/build'   # B-roll parts are graded exactly as R1 (read only)
    def mid(sid):
        s = next(x for x in shots if x['id'] == sid); p = O/f'_br_{sid}.png'
        if not p.exists(): ff(['-ss', f"{(s['n1'] - s['n0'])/2/FPS:.3f}", '-i', B2/f'{sid}.mp4', '-frames:v', 1, p])
        return Image.open(p).convert('RGB').resize((270, 480))
    brs = [s for s in shots if s['kind'] == 'broll' and not s.get('ai') and s['f'] != 'aichat.mp4']
    for k in res:
        tight = Image.open(O/f'{k}-tight.png').convert('RGB').resize((270, 480)); wide = Image.open(O/f'{k}-wide.png').convert('RGB').resize((270, 480))
        sheet = Image.new('RGB', (270*(len(brs) + 2), 480), (10, 14, 20)); sheet.paste(tight, (0, 0)); sheet.paste(wide, (270, 0))
        for i, s in enumerate(brs): sheet.paste(mid(s['id']), (270*(i + 2), 0))
        sheet.save(O/f'broll-{k}.jpg', quality=86)
    print('BROLL SHEETS', [s['id'] for s in brs])
