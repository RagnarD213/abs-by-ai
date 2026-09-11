#!/usr/bin/env python3
"""Re-match the two beats zmatch4 could not see: the robot clip (his label sits beside it, so the hole box is FIXED at
his clip's measured position) and the two audit-results phones (100 px wide at 640 -- matched on full-res crops,
mf/phone_hd.rgb, by template search so his phone's crop/scale of the recording does not matter). Updates media_map.json."""
import json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw
import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
def src_frames(src, w, h):
    b = subprocess.run([FF, '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}:flags=area,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w)
def z(a): a = a.astype(np.float32); a = a - a.mean(); return a/max(float(np.sqrt((a*a).sum())), 1e-6)
OUT = json.load(open('media_map.json'))
idx = list(map(int, open('mf/index.txt').read().split())); pos = {n: i for i, n in enumerate(idx)}
HIS = np.memmap('mf/frames640.rgb', np.uint8, 'r').reshape(-1, 360, 640, 3)
# ---- robot: fixed box (his clip at x 233-407, y 42-350 of 640x360, measured off f00150/f00300)
BX = (236, 45, 404, 347)
S = src_frames(B.ROBOT, 54, 96); SZ = np.stack([z(s) for s in S]).reshape(len(S), -1)
res = []
for n in range(96, 437):
    if n not in pos or n in B.FLASH: continue
    g = cv2.cvtColor(np.ascontiguousarray(HIS[pos[n]][BX[1]:BX[3], BX[0]:BX[2]]), cv2.COLOR_RGB2GRAY)
    t = cv2.resize(g, (54, 96), interpolation=cv2.INTER_AREA); v = SZ @ z(t).reshape(-1); j = int(np.argmax(v))
    res.append([n, round(j/24, 3), round(float(v[j]), 3), list(BX)])
OUT['robot'] = dict(src=B.ROBOT, n0=85, n1=437, map=res)
print('robot:', ' '.join(f'{n}->{t}({r:.2f})' for n, t, r, _ in res[::4]))
# ---- results / safety on full-res crops (x 1620-1920, y 0-400 of his frame)
PH = np.memmap('mf/phone_hd.rgb', np.uint8, 'r').reshape(-1, 400, 300, 3); pidx = list(range(6036, 6396, 2))
def screen(im):
    a = im.astype(np.int16); m = (a.min(-1) > 200) & ((a.max(-1) - a.min(-1)) < 40); m[:, :90] = False
    ys, xs = np.nonzero(m)
    if len(xs) < 1500: return None
    return int(np.percentile(xs, 1)), int(np.percentile(ys, 1)), int(np.percentile(xs, 99))+1, int(np.percentile(ys, 99))+1
for name, src, n0, n1 in (('results', B.RESULTS, 6041, 6206), ('safety', B.SAFETY, 6282, 6391)):
    SW = 72; S = src_frames(src, SW, 128).astype(np.float32)
    res = []
    for k, n in enumerate(pidx):
        if not (n0 <= n < n1) or n in B.FLASH: continue
        im = np.asarray(PH[k]); bx = screen(im)
        if bx is None: res.append([n, None, 0.0, None]); continue
        x0, y0, x1, y1 = bx; g = cv2.cvtColor(np.ascontiguousarray(im[y0:y1, x0:x1]), cv2.COLOR_RGB2GRAY).astype(np.float32)
        th = int(round(SW*(y1-y0)/(x1-x0)))
        t = cv2.resize(g, (SW, th), interpolation=cv2.INTER_AREA)
        if th > 128: t = t[(th-128)//2:(th-128)//2+128]; th = 128
        best = (-2, 0, 0)
        for j in range(len(S)):
            r = cv2.matchTemplate(S[j], t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
            if mv > best[0]: best = (float(mv), j, ml[1])
        res.append([n, round(best[1]/30, 3), round(best[0], 3), [1620+x0, y0, 1620+x1, y1], best[2]])
    OUT[name] = dict(src=src, n0=n0, n1=n1, map=res)
    ok = [r for r in res if r[1] is not None]
    print(f'{name}: r median {np.median([r[2] for r in ok]):.2f}  ', ' '.join(f'{r[0]}->{r[1]}({r[2]:.2f},y{r[4]})' for r in ok[::3]))
json.dump(OUT, open('media_map.json', 'w'))
