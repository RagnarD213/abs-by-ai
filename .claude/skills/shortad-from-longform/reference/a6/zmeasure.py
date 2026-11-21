#!/usr/bin/env python3
"""Torso centre + HAIR TOP on the base, at exact frame indices (skill A5.18: never fps= sampling).
Frames: every 6th inside each picture segment + its first and last frame. Apple Vision person mask (rc/personmask) on
960x540 frames: torso = anchor.py's tall-column midpoint (hands cannot drag it). Hair top = the mask's top row in the
head band, refined on the full-resolution frame by walking up over DARK-HAIR pixels (luma < 70) against the bright
fridge/wall -- the standard is the measured top of the hair (memory framing-standard-hair-anchored). Writes measure.json."""
import glob, json, os, subprocess, sys, numpy as np
from PIL import Image
sys.path.insert(0, 'rc'); from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
E = json.load(open('edl_picture.json'))
want = set()
for s in E:
    want.update(range(s['n0'], s['n1'], 6)); want.update([s['n0'], s['n1']-1])
want = sorted(want)
subprocess.run(['rm', '-rf', 'rc/fr', 'rc/m'], check=False); os.makedirs('rc/fr'); os.makedirs('rc/m')
open('rc/sel.txt', 'w').write("select='" + '+'.join(f'eq(n,{n})' for n in want) + "'")
subprocess.run([FF,'-nostdin','-v','error','-y','-i','base.mp4','-filter_script:v','rc/sel.txt','-fps_mode','passthrough',
                'rc/fr/%05d.png'], check=True)
fs = sorted(glob.glob('rc/fr/*.png')); assert len(fs) == len(want), (len(fs), len(want))
small = []
for f in fs:
    p = f.replace('.png', '_s.png'); Image.open(f).resize((960, 540), Image.BILINEAR).save(p); small.append(p)
for i in range(0, len(small), 60):
    subprocess.run(['./rc/personmask', 'rc/m'] + small[i:i+60], check=True, capture_output=True)
rows = []
for n, f, p in zip(want, fs, small):
    mp = 'rc/m/' + os.path.basename(p).replace('.png', '.mask.png')
    if not os.path.exists(mp): rows.append(dict(n=n, ok=False)); continue
    m = np.asarray(Image.open(mp).convert('L'), dtype=np.float32)/255 > 0.5
    a = anchors(m)
    if a is None: rows.append(dict(n=n, ok=False)); continue
    tx, hx = a['torso']*1920, a['head']*1920
    im = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
    Y = 0.299*im[..., 0] + 0.587*im[..., 1] + 0.114*im[..., 2]
    c0, c1 = int(hx - 70), int(hx + 70)
    band = m[:, max(0, c0//2):c1//2]
    rs = np.where(band.mean(1) >= 0.30)[0]
    ymask = int(rs[0])*2 if len(rs) else None
    # dark-hair walk on the full-res frame: highest row (<= mask top + 30) with >= 20% dark pixels in the head band,
    # contiguous down to the mask top (a dark door groove above the head is not contiguous with the hair)
    yl = None
    if ymask is not None:
        dark = (Y[:, max(0, c0):c1] < 70).mean(1)
        y = min(1079, ymask + 30); last = None; gap = 0
        while y >= 0:
            if dark[y] >= 0.20: last = y; gap = 0
            else:
                gap += 1
                if gap > 4 and last is not None: break
            y -= 1
        yl = last
    rows.append(dict(n=n, ok=True, torso=round(tx, 1), head=round(hx, 1), hair_mask=ymask, hair=yl if yl is not None else ymask))
json.dump(rows, open('measure.json', 'w'))
ok = [r for r in rows if r['ok']]
h = np.array([r['hair'] for r in ok if r['hair'] is not None])
print(f"{len(rows)} frames, {len(ok)} with a person; hair top (1080 px): min {h.min()} p5 {np.percentile(h,5):.0f} median {np.median(h):.0f} max {h.max()}")
d = np.array([r['hair'] - r['hair_mask'] for r in ok if r['hair'] is not None and r['hair_mask'] is not None])
print(f"luma refinement vs Vision mask top: median {np.median(d):+.0f} px, p5 {np.percentile(d,5):+.0f}, p95 {np.percentile(d,95):+.0f}")
