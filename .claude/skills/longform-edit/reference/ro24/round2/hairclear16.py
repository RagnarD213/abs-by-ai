"""Head/hair clearance on a RENDERED keyed export (VIDEO-RULES 2026-10-20, RO-27): the background behind Dan is drawn by us, so for
every checked frame the exact expected background (the shot's crop of comp16.background, resized like the picture) is subtracted
from the decoded export, and the hair top is the first row from the top where at least 3 pixels differ from the background by more
than 14/255 in luma. Independent of the key's own alpha measurement that placed the crops. Checks every 0.25 s of picture plus the
two frames either side of every segment boundary. Requires >= 20 px of clearance at 1080p on every checked frame.

  hairclear16.py <export.mp4> <export.mp4.build.json> [--out report.json] [--proof proof.jpg]
"""
import sys, os, json, subprocess, argparse
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp16 as C
FFR = C.FF + '.real'
ap = argparse.ArgumentParser(); ap.add_argument('mp4'); ap.add_argument('build'); ap.add_argument('--out'); ap.add_argument('--proof'); ap.add_argument('--min', type=int, default=20); ap.add_argument('--upscale', action='store_true')
ap.add_argument('--skip-opaque', help='film manifest: frames under a full-screen (opaque) graphic or photo show no presenter and are skipped')
A = ap.parse_args(); B = json.load(open(A.build)); segs = B['segments']; g0 = B.get('g0', 0)
N = (B['g1'] if B.get('g1') else B['frames']) - g0
step = 7                                                     # 7 frames = 0.234 s
check = set(range(0, N, step))
for s in segs:
    for d in (-2, -1, 0, 1):
        f = s['o0'] - g0 + d
        if 0 <= f < N: check.add(f)
if A.skip_opaque:                                            # round 2: full-screen photo scenes and cards cover Dan entirely
    FPS = 30000 / 1001
    cov = [(int(round(m['a'] * FPS)), int(round(m['b'] * FPS))) for m in json.load(open(A.skip_opaque)) if m['kind'] == 'opaque']
    skipped = {f for f in check if any(a <= f + g0 < b for a, b in cov)}; check -= skipped
    print('skipped (under a full-screen graphic):', len(skipped))
bgfull = C.background(B['bg'])
cache = {}
def expected(seg):
    k = tuple(seg['crop'])
    if k not in cache:
        x, y, w = seg['crop']; h = int(round(w * 9 / 16))
        cache[k] = cv2.resize(bgfull[y:y + h, x:x + w], (1920, 1080), interpolation=cv2.INTER_AREA)
    return cache[k]
p = subprocess.Popen([FFR, '-v', 'error', '-i', A.mp4, '-an', '-vf', 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc' + (',scale=1920:1080:flags=bicubic' if A.upscale else '') + ',format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
res = []; worst = []
for i in range(N):
    raw = p.stdout.read(1920 * 1080 * 3)
    if len(raw) < 1920 * 1080 * 3: break
    if i not in check: continue
    g = i + g0; seg = next(s for s in segs if s['o0'] <= g < s['o1'])
    fr = np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3).astype(np.float32) / 255
    d = np.abs(fr - expected(seg)).max(-1)
    rows = np.where((d[:400] > 14 / 255).sum(1) >= 3)[0]
    top = int(rows[0]) if len(rows) else None
    res.append(dict(frame=i, t=round(i / C.FPS, 3), framing=seg['framing'], top=top))
    worst.append((top if top is not None else -1, i, fr))
    worst = sorted(worst, key=lambda x: x[0])[:6]
p.stdout.close(); p.wait()
valid = [r for r in res if r['top'] is not None]
fails = [r for r in res if r['top'] is None or r['top'] < A.min]
rep = dict(file=A.mp4, frames_checked=len(res), min_required=A.min, none_detected=sum(1 for r in res if r['top'] is None),
           min_top=min(r['top'] for r in valid) if valid else None,
           by_framing={f: min(r['top'] for r in valid if r['framing'] == f) for f in set(r['framing'] for r in valid)},
           worst=[dict(frame=w[1], t=round(w[1] / C.FPS, 2), top=w[0]) for w in worst], fails=fails[:50], verdict='PASS' if not fails else 'FAIL')
if A.out: json.dump(rep, open(A.out, 'w'), indent=1)
if A.proof:
    tiles = []
    for top, i, fr in worst:
        t = (fr[:300, 560:1360] * 255).astype(np.uint8).copy()
        cv2.line(t, (0, A.min), (799, A.min), (255, 0, 0), 1)
        cv2.putText(t, f'{i / C.FPS:.2f}s top {top}px', (8, 290), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2)
        tiles.append(t)
    cv2.imwrite(A.proof, np.concatenate(tiles, 0)[:, :, ::-1])
print(json.dumps({k: v for k, v in rep.items() if k != 'fails'}, indent=1))
