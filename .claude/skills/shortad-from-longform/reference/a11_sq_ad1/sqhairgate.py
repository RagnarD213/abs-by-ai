#!/usr/bin/env python3
"""Delivered-frame HAIR gate for the SQUARE cut.

The framing standard is hair-anchored (memory `framing-standard-hair-anchored`): the top of
his hair must never be cut and must never sit so close to the top edge that the frame reads
as a crop. The standard's numbers were set on a 1920-tall delivered frame (HAIR_MIN 36 px);
here the frame is 1080 tall, so the bound is the same FRACTION of frame height:
36/1920 = 1.875 %  ->  20 px of 1080. That is a scaling of the standard, not a loosening of
it -- the fraction is what the eye sees.

Detector: Apple Vision person mask on the DELIVERED frame -> mask top in the head band ->
refined RELATIVE to what is above it (walk UP from inside the hair while rows stay
hair-dark). A fixed luma threshold climbs to y=0 on a dim wall, which is how a correct crop
once FAILED this gate (A7.11).

  python3 sqhairgate.py <delivered.mp4>
"""
import json, os, subprocess, sys, glob
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, 'rc'); from anchor import anchors
sys.path.insert(0, '.'); import beats as B

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
S = 540                                   # sample size; delivered px = sample px * 1080/540
HAIR_MIN = 20                             # = 36 px of 1920, the standard, as a fraction
TOP_ROWS, DARK_Y, DARK_MAX = 12, 45, 0.20 # test B: a dark band hard against the top edge
V = sys.argv[1]

# ⚠ CLASSIFY BY THE CUMULATIVE FRAME PLAN, NOT BY SECONDS. The renderer lays beats out on
# cumulative rounded frame counts; converting each beat's seconds independently disagrees
# with it by a frame at a boundary, and the gate then grades a PHOTO as a talking-head frame.
# On the cutdown that put the detector on the towel picture, whose dark trees above his head
# read 0.89 on the detector-free test against a 0.20 bound -- a FAIL on a frame the gate
# should never have looked at. A 2-frame guard either side of every edge on top of that.
tl, _ = B.timeline()
talk, prev = [], 0
for b in tl:
    cum = round(b['t1']*FPS)
    if b['kind'] == 'talk': talk += list(range(prev + 2, cum - 2))
    prev = cum
flash = set()
for a, c in B.FLASHES: flash.update(range(int(a*FPS)-2, int(c*FPS)+3))
want = sorted(n for n in talk if n % 6 == 0 and n not in flash)

D = 'hg'; subprocess.run(['rm', '-rf', D]); os.makedirs(f'{D}/fr'); os.makedirs(f'{D}/m')
open(f'{D}/sel.txt', 'w').write("select='" + '+'.join(f'eq(n,{n})' for n in want) + f"',scale={S}:{S}")
subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', V, '-filter_script:v', f'{D}/sel.txt',
                '-fps_mode', 'passthrough', f'{D}/fr/%05d.png'], check=True)
fs = sorted(glob.glob(f'{D}/fr/*.png')); assert len(fs) == len(want), (len(fs), len(want))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', f'{D}/m'] + fs[i:i+60], check=True, capture_output=True)

A, Bbad, worstB = [], [], (0.0, None)
for n, f in zip(want, fs):
    im = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
    Y = 0.299*im[..., 0] + 0.587*im[..., 1] + 0.114*im[..., 2]
    mp = f'{D}/m/' + os.path.basename(f).replace('.png', '.mask.png')
    if not os.path.exists(mp): continue
    m = np.asarray(Image.open(mp).convert('L'), dtype=np.float32)/255 > 0.5
    a = anchors(m)
    if a is None: continue
    hx = a['head']*S; c0, c1 = int(max(0, hx-30)), int(min(S, hx+30))
    # test B, detector-free: a dark band right at the top edge over his head means hair in it
    band = Y[:TOP_ROWS, c0:c1]; frac = float((band < DARK_Y).mean())
    if frac > worstB[0]: worstB = (frac, n)
    if frac >= DARK_MAX: Bbad.append((n, round(frac, 2)))
    rows = np.where(m[:, c0:c1].mean(1) >= 0.30)[0]
    if not len(rows): continue
    ym = int(rows[0])
    prof = np.percentile(Y[:, c0:c1], 30, axis=1)
    hair_lvl = float(np.median(prof[ym+3:ym+13])) if ym + 13 < S else float(prof[ym])
    thr = hair_lvl + 14; y = min(ym + 6, S-1)
    while y > 0 and y > ym - 40 and prof[y-1] < thr: y -= 1
    A.append((n, int(round(y*1080/S))))

fails = []
def check(ok, msg):
    print(('  PASS  ' if ok else '  FAIL  ') + msg)
    if not ok: fails.append(msg)

assert A, 'NOT MEASURED: the detector found no usable talking-head frame'
hs = np.array([h for _, h in A])
print(f'hair gate (square)  {V}   {len(talk)} talk frames; detector samples {len(A)} of {len(want)}')
print(f'  hair top below the top edge (px of 1080): min {hs.min()}  p5 {np.percentile(hs,5):.0f}  '
      f'median {np.median(hs):.0f}  max {hs.max()}   (= {100*hs.min()/1080:.2f}% .. {100*hs.max()/1080:.2f}% of frame height)')
check(hs.min() >= HAIR_MIN, f'HAIR NEVER CUT: every sample >= {HAIR_MIN} px (= the standard 36/1920) below the top edge (min {hs.min()})')
check(not Bbad, f'test B (detector-free): no dark band hard against the top edge over his head '
                f'(worst {worstB[0]:.2f} at frame {worstB[1]}, bound {DARK_MAX})')
worst = sorted(A, key=lambda r: r[1])[:8]
os.makedirs('logs', exist_ok=True)
json.dump(dict(video=os.path.basename(V), n=len(A), min=int(hs.min()), p5=float(np.percentile(hs,5)),
               median=float(np.median(hs)), max=int(hs.max()), hair_min=HAIR_MIN,
               testB_worst=worstB, fails=fails, worst_frames=worst),
          open('logs/hairgate.json','w'), indent=1)
# proof sheet of the eight tightest frames
tiles = []
for n, h in worst:
    f = f'{D}/fr/{want.index(n)+1:05d}.png'
    im = Image.open(f).convert('RGB').resize((360, 360))
    d = ImageDraw.Draw(im); yy = h*360/1080
    d.line([0, yy, 360, yy], fill=(255, 60, 60), width=2)
    d.text((6, 6), f'n={n} hair {h}px', fill=(255, 220, 0))
    tiles.append(im)
sh = Image.new('RGB', (4*364, 2*364), (25, 25, 25))
for i, t in enumerate(tiles): sh.paste(t, ((i % 4)*364, (i//4)*364))
sh.save('logs/hairgate_sheet.jpg', quality=90)
print(f'  proof sheet: logs/hairgate_sheet.jpg (the eight tightest frames)')
sys.exit(1 if fails else 0)
