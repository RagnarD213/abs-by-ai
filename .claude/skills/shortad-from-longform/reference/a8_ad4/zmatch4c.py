#!/usr/bin/env python3
"""The two audit phones beside Dan's head (results 6041-6206, safety 6282-6391), matched on FULL-RES crops of his frames
(mf/phone_hd2.rgb: x 1340-1720, y 120-800 of his 1920x1080, every 2nd frame 6036-6394) by multi-scale template search --
his phone screen is ~100 px wide at 640, too small for the 640 matcher. Updates media_map.json."""
import json, subprocess, numpy as np, cv2
import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def src_frames(src, w, h):
    b = subprocess.run([FF, '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}:flags=area,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w).astype(np.float32)
OUT = json.load(open('media_map.json'))
PH = np.memmap('mf/phone_hd2.rgb', np.uint8, 'r').reshape(-1, 680, 380, 3); pidx = list(range(6036, 6396, 2)); X0, Y0 = 1340, 120
def screen(im):
    a = im.astype(np.int16); m = (a.min(-1) > 190) & ((a.max(-1) - a.min(-1)) < 45); m[:, :25] = False
    ys, xs = np.nonzero(m)
    if len(xs) < 3000: return None
    return int(np.percentile(xs, 1)), int(np.percentile(ys, 1)), int(np.percentile(xs, 99))+1, int(np.percentile(ys, 99))+1
for name, src, n0, n1 in (('results', B.RESULTS, 6041, 6206), ('safety', B.SAFETY, 6282, 6391)):
    SW, SH = 90, 160; S = src_frames(src, SW, SH)
    res = []
    for k, n in enumerate(pidx):
        if not (n0 <= n < n1) or n in B.FLASH: continue
        im = np.asarray(PH[k]); bx = screen(im)
        if bx is None: res.append([n, None, 0.0, None, 0]); continue
        x0, y0, x1, y1 = bx; g = cv2.cvtColor(np.ascontiguousarray(im[y0:y1, x0:x1]), cv2.COLOR_RGB2GRAY).astype(np.float32)
        best = (-2, 0, 0, 0)
        for sc in (0.70, 0.78, 0.86, 0.94, 1.0):
            tw = int(SW*sc); th = int(round(tw*(y1-y0)/(x1-x0)))
            if th > SH: th = SH; tw = int(round(th*(x1-x0)/(y1-y0)))
            t = cv2.resize(g, (tw, th), interpolation=cv2.INTER_AREA)
            for j in range(len(S)):
                r = cv2.matchTemplate(S[j], t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
                if mv > best[0]: best = (float(mv), j, sc, ml[1])
        res.append([n, round(best[1]/30, 3), round(best[0], 3), [X0+x0, Y0+y0, X0+x1, Y0+y1], best[2], best[3]])
    OUT[name] = dict(src=src, n0=n0, n1=n1, map=res)
    ok = [r for r in res if r[1] is not None]
    print(f'{name}: {len(ok)}/{len(res)}  r median {np.median([r[2] for r in ok]):.2f}  box {ok[len(ok)//2][3]}')
    print('   ', ' '.join(f'{r[0]}->{r[1]}({r[2]:.2f},s{r[4]})' for r in ok[::2]))
json.dump(OUT, open('media_map.json', 'w'))
