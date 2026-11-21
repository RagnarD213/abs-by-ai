"""Key numbers, approved vs refined, read in lockstep over one key range (key16 --variant both):
  interior   share of pixels deep inside the head (25 px erosion of alpha > .5, top 700 rows) with alpha below 0.99
  green edge mean green excess G - (R+B)/2 (only where positive) of the foreground colour in the edge band 0.15 < alpha < 0.98
  leftover   pixels with alpha > 0.02 more than 30 px from Dan (screen left behind)
  steadiness mean frame-to-frame alpha change on the SAME pixels for both variants (approved key's semitransparent band, and the
             head interior); lower = steadier. Motion dominates the band figure, so compare the two columns, not the value.
usage: keynum.py <K.mkv> <every_n> [out.json]"""
import sys, os, json, subprocess
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp16 as C
key, step = sys.argv[1], int(sys.argv[2]); out = sys.argv[3] if len(sys.argv) > 3 else None
def rd(path): return subprocess.Popen([C.FF + '.real', '-v', 'error', '-i', path, '-an', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
pa, pr = rd(key), rd(key.replace('.mkv', '_refined.mkv'))
acc = {n: dict(inter=[], green=[], far=[], band=[], head=[]) for n in ('approved', 'refined')}
prev = None; i = 0
while True:
    fa, fr = C.read_frame(pa), C.read_frame(pr)
    if fa is None or fr is None: break
    cur = {'approved': fa, 'refined': fr}
    Aa = fa[1]; m = (Aa > .5).astype(np.uint8)
    if i % step == 0:
        core = cv2.erode(m, np.ones((25, 25), np.uint8)) > 0; core[700:] = False
        farm = cv2.dilate(m, np.ones((61, 61), np.uint8)) == 0
        for n, (F, A) in cur.items():
            acc[n]['inter'].append(float((A[core] < .99).mean()) if core.any() else 0)
            e = (A > .15) & (A < .98); g = np.maximum(F[..., 1] - .5 * (F[..., 0] + F[..., 2]), 0)
            acc[n]['green'].append(float(g[e].mean()) if e.any() else 0)
            acc[n]['far'].append(int((A[farm] > .02).sum()))
    if prev is not None and i % step == 1:
        band = (prev['approved'][1] > .05) & (prev['approved'][1] < .95)
        inner = cv2.erode(m, np.ones((9, 9), np.uint8)) > 0; inner[700:] = False
        for n in cur:
            d = np.abs(cur[n][1] - prev[n][1]); acc[n]['band'].append(float(d[band].mean())); acc[n]['head'].append(float(d[inner].mean()))
    prev = {n: (None, v[1]) for n, v in cur.items()}; i += 1
for q in (pa, pr): q.stdout.close(); q.wait()
res = {n: dict(frames=i, sampled=len(v['inter']), interior_below_099_pct=round(100 * float(np.mean(v['inter'])), 2), edge_green=round(float(np.mean(v['green'])), 4),
               leftover_screen_px_max=int(np.max(v['far'])), edge_band_change=round(float(np.mean(v['band'])), 4), head_interior_change=round(float(np.mean(v['head'])), 5))
       for n, v in acc.items()}
print(json.dumps(res, indent=1))
if out: json.dump(res, open(out, 'w'), indent=1)
