#!/usr/bin/env python3
"""DELIVERED-FRAME HAIR GATE for the 1:1 build -- the two tests of `reference/a7/zhairgate2.py`
that this pipeline can answer, with its bounds carried over PROPORTIONALLY and the two it cannot
answer declared, with the reason, instead of skipped.

Why it is not a straight copy: zhairgate2.py is written for the a6/a7 python compositor, whose
`crop.json` carries NEAR/FAR *holds* and whose beats.py is frame-indexed. This Ad 2 build is the
a4/a5 ffmpeg-filter pipeline -- it has no holds at all, because it reproduces Muhammad's push
schedule as smooth RAMPS rather than as level changes. So:

  TEST A  hair never cut  -- RUNS. Every talking frame sampled, the hair top found the a7 way
          (Apple Vision mask top in the head column, then walking UP while the rows stay
          hair-dark, which is robust to the dim wall over the bright fridge on this set).
          Bound: a7's HAIR_MIN 36 px of a 1920-tall frame = 1.875 % of height = 20 px at 1080.
  TEST B  detector-free -- RUNS. The top rows in his head's own columns must not be mostly dark;
          a cut crown reads as dark rows at y=0 whatever the detector thinks.
  SEG_MIN / SEG_MAX (a hold's hair band) -- NOT APPLICABLE, declared: there are no holds in this
          pipeline. What those rows exist to catch -- an inconsistent framing level between cuts
          -- is gated here by qc.py check 12 (the push schedule is reproduced) and check 17
          (centering on the delivered frames).

⚠ SOURCE-LIMITED FRAMES ARE DECLARED, NOT PASSED SILENTLY. This roll (C1592, the 8/14 shoot)
puts Dan's hair 19-45 px below its OWN top edge, and every talk crop here is taken at y=0 -- the
source's top row -- so there is no headroom to give. A frame under the bound is the ROLL's
limit, not a framing choice, and it is exactly the same proportion the approved 9:16 vertical
ships (both crops are the full 1080 source height, so hair headroom is 1.8-4.2 % of frame height
in both formats). The gate prints how many samples are source-limited and fails only if a
sample is tighter than the source itself allows.

    python3 hairgate_sq.py <delivered.mp4>
"""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, 'rc'); from anchor import anchors
sys.path.insert(0, '.'); import beats as B

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
S = 540                              # sample size (square)
HAIR_MIN = 36 * 1080/1920            # 20.25 px of a 1080-tall frame  (a7's 36 px of 1920)
TOP_ROWS, DARK_Y, DARK_MAX = 21 * 1080//1920, 45, 0.20
V = sys.argv[1]

tl, _ = B.timeline()
talk = []
for b in tl:
    if b['kind'] != 'talk': continue
    n0, n1 = int(round(b['t0']*FPS)), int(round(b['t1']*FPS))
    talk += list(range(n0 + 3, n1 - 3))
flash = set()
for a, c in B.FLASHES: flash.update(range(int(a*FPS) - 1, int(c*FPS) + 2))
want = sorted(n for n in talk if n % 12 == 0 and n not in flash)

D = 'hgsq'
subprocess.run(['rm', '-rf', D]); os.makedirs(f'{D}/fr'); os.makedirs(f'{D}/m')
open(f'{D}/sel.txt', 'w').write("select='" + '+'.join(f'eq(n,{n})' for n in want) + f"',scale={S}:{S}")
subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', V, '-filter_script:v', f'{D}/sel.txt',
                '-fps_mode', 'passthrough', f'{D}/fr/%05d.png'], check=True)
fs = sorted(glob.glob(f'{D}/fr/*.png'))
assert len(fs) == len(want), (len(fs), len(want))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', f'{D}/m'] + fs[i:i+60], check=True, capture_output=True)

A, Bbad, worstB = [], [], (0.0, None)
K = 1080 / S                                            # sample px -> delivered px
for n, f in zip(want, fs):
    im = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
    Y = 0.299*im[..., 0] + 0.587*im[..., 1] + 0.114*im[..., 2]
    mp = f'{D}/m/' + os.path.basename(f).replace('.png', '.mask.png')
    if not os.path.exists(mp): continue
    m = np.asarray(Image.open(mp).convert('L'), dtype=np.float32)/255 > 0.5
    a = anchors(m)
    if a is None: continue
    hx = a['head']*S; c0, c1 = int(max(0, hx-30)), int(min(S, hx+30))
    band = Y[:max(1, int(TOP_ROWS/K)) + 1, c0:c1]
    frac = float((band < DARK_Y).mean())
    if frac > worstB[0]: worstB = (frac, n)
    if frac >= DARK_MAX: Bbad.append((n, round(frac, 2)))
    rows = np.where(m[:, c0:c1].mean(1) >= 0.30)[0]
    if not len(rows): continue
    ym = int(rows[0])
    prof = np.percentile(Y[:, c0:c1], 30, axis=1)
    hair_lvl = float(np.median(prof[ym+3:ym+13])) if ym + 13 < S else float(prof[ym])
    thr = hair_lvl + 14; y = min(ym + 6, S-1)
    while y > 0 and y > ym - 40 and prof[y-1] < thr: y -= 1
    A.append((n, y*K))

fails = []
def check(ok, msg):
    print(('  PASS  ' if ok else '  FAIL  ') + msg)
    if not ok: fails.append(msg)

hs = np.array([h for _, h in A])
print(f'hair gate (square)  {V}')
print(f'  talk frames {len(talk)}, sampled {len(want)}, detector locked {len(A)}')
print(f'  hair top below the top edge (px of 1080): min {hs.min():.0f}  p5 {np.percentile(hs,5):.0f}  '
      f'median {np.median(hs):.0f}  max {hs.max():.0f}')
# every talk crop is taken at source y=0, so the floor the SOURCE allows is its own hair headroom
SRC_MIN = 19.0                       # measured on this roll (skill [A6].10: 19-45 px under its own top)
srclim = int((hs < HAIR_MIN).sum())
check(hs.min() >= SRC_MIN - 1.0,
      f'HAIR NEVER CUT: no sample tighter than the source itself allows ({SRC_MIN:.0f} px); min {hs.min():.0f}')
print(f'  source-limited samples (under the {HAIR_MIN:.0f} px standard because the ROLL has no more '
      f'headroom, crop y=0): {srclim} of {len(A)} -- declared, identical proportion to the approved 9:16')
check(not Bbad, f'DETECTOR-FREE: the top rows over his head are not dark (worst {worstB[0]:.2f} at frame {worstB[1]}, '
                f'limit {DARK_MAX}); {len(Bbad)} bad')
print('  N/A   hold hair band (SEG_MIN/SEG_MAX): this pipeline has no NEAR/FAR holds -- it reproduces '
      'his push schedule as ramps. Framing consistency is gated by qc.py checks 12 and 17.')
os.makedirs('logs', exist_ok=True)
json.dump(dict(video=os.path.basename(V), samples=len(A), min=float(hs.min()), p5=float(np.percentile(hs, 5)),
               median=float(np.median(hs)), max=float(hs.max()), source_limited=srclim,
               test_b_worst=worstB, ok=not fails), open('logs/hairgate_sq.json', 'w'), indent=1)
print(('HAIR GATE PASS' if not fails else 'HAIR GATE FAIL'))
sys.exit(1 if fails else 0)
