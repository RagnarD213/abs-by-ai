#!/usr/bin/env python3
"""Delivered-frame HAIR gate, detector rebuilt for this set: the luma-profile detector of zhairgate.py (bright wall ->
dark hair) reads 0 px on Muhammad's C1595 frames where the wall above Dan's head is DIM (30th-pct luma 40-70 -- below
the hair/forehead midpoint), so half the samples fail on a detector fault, not a framing fault (2026-09-10).
Here the hair top is found the way the build measures it (zmeasure/zhair): Apple Vision person mask on the DELIVERED
frame -> mask top in the head band -> refined RELATIVE to what is above (wall level vs hair level, midpoint, walking
down). Same bounds as zhairgate.py (the standard's 1080p numbers x 1920/1080): HAIR_MIN 36, SEG_MIN 53, SEG_MAX 124;
plus the detector-free test B. Proof sheet: logs/hairgate2_sheet.jpg.   python3 zhairgate2.py <delivered.mp4>"""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, 'rc'); from anchor import anchors
sys.path.insert(0, '.'); import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
HAIR_MIN, SEG_MIN, SEG_MAX, TOP_ROWS, DARK_Y, DARK_MAX = 36, 53, 124, 21, 45, 0.20
V = sys.argv[1]
C = json.load(open('crop.json')); HOLDS = C['holds']
tl, _ = B.timeline()
talk = set()
for b in tl:
    if b['kind'] == 'talk': talk.update(range(b['n0'], b['n1']))
talk -= set(B.FLASHES)
want = sorted(n for n in talk if n % 6 == 0)
D = 'hg2'; subprocess.run(['rm', '-rf', D]); os.makedirs(f'{D}/fr'); os.makedirs(f'{D}/m')
open(f'{D}/sel.txt', 'w').write("select='" + '+'.join(f'eq(n,{n})' for n in want) + "',scale=540:960")
subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', V, '-filter_script:v', f'{D}/sel.txt', '-fps_mode', 'passthrough', f'{D}/fr/%05d.png'], check=True)
fs = sorted(glob.glob(f'{D}/fr/*.png')); assert len(fs) == len(want), (len(fs), len(want))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', f'{D}/m'] + fs[i:i+60], check=True, capture_output=True)
A, Bbad, worstB = [], [], (0.0, None)
for n, f in zip(want, fs):
    im = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32); Y = 0.299*im[..., 0] + 0.587*im[..., 1] + 0.114*im[..., 2]
    mp = f'{D}/m/' + os.path.basename(f).replace('.png', '.mask.png')
    band = Y[:TOP_ROWS//2 + 1, 215:325]; frac = float((band < DARK_Y).mean())          # test B, at 540x960 (rows /2)
    if frac > worstB[0]: worstB = (frac, n)
    if frac >= DARK_MAX: Bbad.append((n, round(frac, 2)))
    if not os.path.exists(mp): continue
    m = np.asarray(Image.open(mp).convert('L'), dtype=np.float32)/255 > 0.5
    a = anchors(m)
    if a is None: continue
    hx = a['head']*540; c0, c1 = int(max(0, hx-30)), int(min(540, hx+30))
    rows = np.where(m[:, c0:c1].mean(1) >= 0.30)[0]
    if not len(rows): continue
    ym = int(rows[0])
    prof = np.percentile(Y[:, c0:c1], 30, axis=1)
    hair_lvl = float(np.median(prof[ym+3:ym+13])) if ym + 13 < 960 else float(prof[ym])
    # walk UP from inside the hair while the rows stay hair-dark (hair level + 14): robust to whatever sits above the
    # head -- a dim wall over a bright fridge fooled a top-down midpoint search into y = 0 (2026-09-10)
    thr = hair_lvl + 14; y = min(ym + 6, 959)
    while y > 0 and y > ym - 40 and prof[y-1] < thr: y -= 1
    A.append((n, int(y*2)))                                                      # back to 1920-tall px
fails = []
def check(ok, msg):
    print(('  PASS  ' if ok else '  FAIL  ') + msg)
    if not ok: fails.append(msg)
hs = np.array([h for _, h in A])
print(f'hair gate 2  {V}  {len(talk)} talk frames; detector samples {len(A)} of {len(want)}')
print(f'  hair top below the top edge (px of 1920): min {hs.min()}  p5 {np.percentile(hs,5):.0f}  median {np.median(hs):.0f}  max {hs.max()}')
check(hs.min() >= HAIR_MIN, f'HAIR NEVER CUT: every sample >= {HAIR_MIN} px below the top edge (min {hs.min()})')
seg = []
for h in HOLDS:
    v = [y for m_, y in A if h['n0'] <= m_ < h['n1']]
    if v: seg.append((h['n0'], h['level'], min(v), h['y0']))
tight = [s for s in seg if s[2] < SEG_MIN and s[3] > 0.5]; limited = [s for s in seg if s[2] < SEG_MIN and s[3] <= 0.5]; loose = [s for s in seg if s[2] > SEG_MAX]
print(f'  per-hold minimum: {[s[2] for s in seg]}')
print(f'  declared: {len(limited)} hold(s) below {SEG_MIN} px sit at the TOP OF THE SOURCE (y0=0): {[(s[0], s[1], s[2]) for s in limited]}')
check(not tight, f'no hold anchors the hair closer than {SEG_MIN} px where the crop had room to give it (y0 > 0): {tight[:5]}')
check(not loose, f'every hold brings the hair within {SEG_MAX} px of the top edge (anchored, not loose): {loose[:5]}')
check(not Bbad, f'INDEPENDENT TEST: no talk frame has hair-dark pixels in the top {TOP_ROWS} rows of the head band (>= {DARK_MAX}); worst {worstB[0]:.3f} at frame {worstB[1]}: {Bbad[:6]}')
tight6 = sorted(A, key=lambda a: a[1])[:6]
sheet = Image.new('RGB', (6*360, 420), (0, 0, 0))
for i, (m_, y) in enumerate(tight6):
    im = Image.open(fs[want.index(m_)]).convert('RGB').resize((1080, 1920)).crop((360, 0, 720, 420)); dd = ImageDraw.Draw(im)
    dd.line([(0, y), (359, y)], fill=(0, 255, 0), width=2); dd.text((6, 396), f'f{m_}  hair {y}px', fill=(255, 255, 0))
    sheet.paste(im, (i*360, 0))
sheet.save('logs/hairgate2_sheet.jpg', quality=90)
json.dump(dict(video=V, samples=len(A), min=int(hs.min()), median=float(np.median(hs)), per_hold=seg, limited=limited, top_rows_worst=worstB, fails=fails), open('logs/hairgate2.json', 'w'), indent=1, default=str)
print('\n' + ('HAIR GATE PASSED' if not fails else f'HAIR GATE FAILED -- {len(fails)} check(s)'))
sys.exit(1 if fails else 0)
