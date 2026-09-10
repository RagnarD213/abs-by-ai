#!/usr/bin/env python3
"""The delivered-frame HAIR gate for this build (the website-video hairgate.py's two tests, in this geometry).

That gate is bound to the 8/28 set: a door-panel column profile, a 4K base, a 16:9 1080p master. Here the master is
1080x1920 and the room above Dan's head is the bright wall and fridge, so the same two tests are rebuilt:
  A  DETECTOR on the delivered frames, every talk frame on a 6-frame grid: in the head band (the crop is centred on his
     torso, so columns 430-650), the per-row 30th-percentile luma drops from the bright room to near-black hair; the
     hair top is the first row below the midpoint of the two levels. FAIL if any sample is < HAIR_MIN px from the top
     edge; per hold the minimum must be >= SEG_MIN (not tighter than the standard) and <= SEG_MAX (anchored, not loose).
     DECLARED EXCEPTION, auditable: a hold whose crop already starts at the TOP OF THE SOURCE (y0 = 0) cannot gain
     headroom by cropping -- this 8/14 roll puts his hair 19-45 px from its own top edge -- so SEG_MIN does not apply
     there; HAIR_MIN still does, on every frame.
  B  DETECTOR-FREE, every talk frame: the top TOP_ROWS rows of the head band must not be hair-dark (luma < DARK_Y) on
     more than DARK_MAX of their pixels. Hair against the edge reads 0.5+.
Bounds are the standard's 1080p numbers scaled to the 1920-tall frame (x 1920/1080): 20 -> 36, 30 -> 53, 70 -> 124,
12 rows -> 21. Proof: the six tightest frames at native resolution in logs/hairgate_sheet.jpg -- LOOK at them.
  python3 zhairgate.py <delivered.mp4>"""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
HAIR_MIN, SEG_MIN, SEG_MAX, TOP_ROWS, DARK_Y, DARK_MAX = 36, 53, 124, 21, 45, 0.20
sys.path.insert(0, '.')
import beats as B
V = sys.argv[1]
C = json.load(open('crop.json')); CROP = {int(k): v for k, v in C['frames'].items()}; HOLDS = C['holds']
tl, _ = B.timeline()
talk = set()
for b in tl:
    if b['kind'] == 'talk': talk.update(range(b['n0'], b['n1']))
talk -= set(B.FLASHES)
p = subprocess.Popen([FF, '-v', 'error', '-i', V, '-vf', 'crop=1080:420:0:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                     stdout=subprocess.PIPE)
A, Bbad, worstB, n = [], [], (0.0, None), 0
keep = {}
while True:
    buf = p.stdout.read(1080*420*3)
    if len(buf) < 1080*420*3: break
    if n in talk:
        fr = np.frombuffer(buf, np.uint8).reshape(420, 1080, 3).astype(np.float32)
        Y = 0.299*fr[..., 0] + 0.587*fr[..., 1] + 0.114*fr[..., 2]
        band = Y[:, 430:650]
        frac = float((band[:TOP_ROWS] < DARK_Y).mean())
        if frac > worstB[0]: worstB = (frac, n)
        if frac >= DARK_MAX: Bbad.append((n, round(frac, 2)))
        if n % 6 == 0:
            prof = np.percentile(band, 30, axis=1)
            lo, hi = np.percentile(prof[:400], 8), np.percentile(prof[:400], 92)
            thr = (lo + hi)/2
            y = next((y for y in range(0, 397) if prof[y] < thr and prof[y+1] < thr and prof[y+2] < thr), None)
            if hi - lo >= 25 and y is not None:
                A.append((n, y)); keep[n] = fr.astype(np.uint8)
                if len(keep) > 400: keep = dict(sorted(keep.items(), key=lambda kv: dict(A)[kv[0]])[:40])
    n += 1
p.wait()
fails = []
def check(ok, msg):
    print(('  PASS  ' if ok else '  FAIL  ') + msg)
    if not ok: fails.append(msg)
hs = np.array([h for _, h in A])
print(f'hair gate  {V}  {n} frames, {len(talk)} talk frames; detector samples {len(A)}')
print(f'  hair top below the top edge (px of 1920): min {hs.min()}  p5 {np.percentile(hs,5):.0f}  median {np.median(hs):.0f}  max {hs.max()}')
check(hs.min() >= HAIR_MIN, f'HAIR NEVER CUT: every sample >= {HAIR_MIN} px below the top edge (min {hs.min()})')
seg = []
for h in HOLDS:
    v = [y for m, y in A if h['n0'] <= m < h['n1']]
    if not v: continue
    seg.append((h['n0'], h['level'], min(v), h['y0']))
tight = [s for s in seg if s[2] < SEG_MIN and s[3] > 0.5]
limited = [s for s in seg if s[2] < SEG_MIN and s[3] <= 0.5]
loose = [s for s in seg if s[2] > SEG_MAX]
print(f'  per-hold minimum: {[s[2] for s in seg]}')
print(f'  declared: {len(limited)} hold(s) below {SEG_MIN} px sit at the TOP OF THE SOURCE (y0=0), headroom is the roll\'s own: '
      f'{[(s[0], s[1], s[2]) for s in limited]}')
check(not tight, f'no hold anchors the hair closer than {SEG_MIN} px where the crop had room to give it (y0 > 0): {tight[:5]}')
check(not loose, f'every hold brings the hair within {SEG_MAX} px of the top edge (anchored, not loose): {loose[:5]}')
check(not Bbad, f'INDEPENDENT TEST: no talk frame has hair-dark pixels in the top {TOP_ROWS} rows of the head band '
                f'(>= {DARK_MAX}); worst {worstB[0]:.3f} at frame {worstB[1]}: {Bbad[:6]}')
tight6 = sorted(A, key=lambda a: a[1])[:6]
sheet = Image.new('RGB', (6*360, 420), (0, 0, 0)); d = ImageDraw.Draw(sheet)
for i, (m, y) in enumerate(tight6):
    if m not in keep: continue
    im = Image.fromarray(keep[m][:, 360:720]); dd = ImageDraw.Draw(im)
    dd.line([(0, y), (359, y)], fill=(0, 255, 0), width=2); dd.text((6, 396), f'f{m}  hair {y}px', fill=(255, 255, 0))
    sheet.paste(im, (i*360, 0))
sheet.save('logs/hairgate_sheet.jpg', quality=90)
json.dump(dict(video=V, samples=len(A), min=int(hs.min()), median=float(np.median(hs)), per_hold=seg, limited=limited,
               top_rows_worst=worstB, fails=fails), open('logs/hairgate.json', 'w'), indent=1, default=str)
print('\n' + ('HAIR GATE PASSED' if not fails else f'HAIR GATE FAILED -- {len(fails)} check(s)'))
sys.exit(1 if fails else 0)
