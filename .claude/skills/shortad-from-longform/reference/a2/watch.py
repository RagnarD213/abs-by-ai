#!/usr/bin/env python3
"""THE WATCH PASS -- the delivery gate.

Attempt 1 passed 11/11 on a metric gate and Dan rejected it: every check measured format,
none ever looked at the moving picture. This does two things the metrics cannot:

  1. AUTOMATED, over every frame of the finished file: frozen runs, black frames, dropped
     frames, and hard discontinuities that are not at a boundary the beat sheet knows about.
  2. HUMAN, at every boundary: a 2 s clip AND a strip of CONSECUTIVE frames spanning the
     cut at full rate. Consecutive frames are what expose a jump cut, a frozen segment or
     a mistimed animation -- a contact sheet at 1 s intervals cannot.

Writes logs/watch_pass.json, which qc.py check 15 refuses to pass without.
"""
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '.')
import beats as BT

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V  = sys.argv[1] if len(sys.argv) > 1 else 'ad1_vertical_9x16.mp4'
OUT = 'watch'
FPS = 30000/1001

def boundaries():
    tl, ov = BT.timeline()
    b = set()
    for x in tl:  b.add(round(x['t0'], 2))
    for x in ov:  b.add(round(x['t0'], 2)); b.add(round(x['t1'], 2))
    for a, c in BT.FLASHES: b.add(round(a, 2))
    for a1, a2, c1, c2 in BT.PUSHES: b.add(round(a1, 2)); b.add(round(c2, 2))
    return sorted(t for t in b if 0.2 < t < BT.DUR-0.2)

def scan(video):
    """Every frame, small and grey: frozen runs, black frames, unexplained jumps."""
    os.makedirs(f'{OUT}/all', exist_ok=True)
    if len(glob.glob(f'{OUT}/all/*.png')) < 6000:
        subprocess.run([FF,'-v','error','-y','-i',video,'-vf','fps=30000/1001,scale=96:171',
                        f'{OUT}/all/%05d.png'], check=True)
    fs = sorted(glob.glob(f'{OUT}/all/*.png'))
    A = np.stack([np.asarray(Image.open(f).convert('L'), dtype=np.float32) for f in fs])
    d = np.abs(np.diff(A, axis=0)).mean(axis=(1,2))
    lum = A.mean(axis=(1,2))
    frozen, i = [], 0
    while i < len(d):
        if d[i] < 0.05:
            j = i
            while j < len(d) and d[j] < 0.05: j += 1
            if j-i >= 8: frozen.append((i/FPS, (j-i)/FPS))
            i = j
        else: i += 1
    black = [(k/FPS) for k, v in enumerate(lum) if v < 3.0]
    known = set()
    for t in boundaries(): known.update(range(int((t-0.25)*FPS), int((t+0.25)*FPS)+1))
    for a, c in BT.FLASHES: known.update(range(int(a*FPS), int(c*FPS)+2))
    med = float(np.median(d))
    jumps = [(k/FPS, float(d[k])) for k in np.argsort(d)[::-1][:120]
             if d[k] > med*8 and k not in known]
    return dict(frames=len(fs), frozen=frozen, black=black,
                jumps=sorted(jumps)[:30], median_diff=med)

def strips(video, ts):
    """Per boundary: a 2 s clip and a strip of consecutive frames across the cut."""
    os.makedirs(f'{OUT}/clip', exist_ok=True); os.makedirs(f'{OUT}/strip', exist_ok=True)
    try: fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
    except Exception: fnt = ImageFont.load_default()
    fs = sorted(glob.glob(f'{OUT}/all/*.png'))
    made = 0
    for t in ts:
        c = f'{OUT}/clip/b{t:07.2f}.mp4'
        if not os.path.exists(c):
            subprocess.run([FF,'-v','error','-y','-ss',f'{max(0,t-1.0):.3f}','-t','2.0','-i',video,
                            '-vf','scale=270:480','-an','-c:v','libx264','-preset','veryfast',
                            '-crf','22','-pix_fmt','yuv420p',c], check=True)
        s = f'{OUT}/strip/b{t:07.2f}.png'
        if not os.path.exists(s):
            k0 = int(round(t*FPS))
            idx = [k0-4, k0-2, k0-1, k0, k0+1, k0+2, k0+4, k0+8]
            idx = [max(0, min(len(fs)-1, i)) for i in idx]
            W = 172
            im = Image.new('RGB', (W*len(idx), 306+20), (18,18,18)); d = ImageDraw.Draw(im)
            for n, i in enumerate(idx):
                d.rectangle([n*W, 0, (n+1)*W, 20], fill=(200,30,30) if i < k0 else (30,120,200))
                d.text((n*W+3, 2), f'{(i-k0):+d}f', font=fnt, fill=(255,255,255))
                im.paste(Image.open(fs[i]).resize((W, 306)), (n*W, 20))
            im.save(s, quality=92)
        made += 1
    return made

if __name__ == '__main__':
    ts = boundaries()
    rep = scan(V)
    n = strips(V, ts)
    print(f'frames {rep["frames"]}   median frame diff {rep["median_diff"]:.2f}')
    print(f'frozen runs >=8 frames : {len(rep["frozen"])}  {rep["frozen"][:6]}')
    print(f'black frames           : {len(rep["black"])}')
    print(f'unexplained jumps      : {len(rep["jumps"])}')
    for t, v in rep['jumps'][:12]: print(f'    {t:7.2f}s  diff {v:.1f}')
    print(f'\n{n} boundaries -> watch/clip/*.mp4 and watch/strip/*.png')
    json.dump(dict(video=os.path.basename(V), boundaries=len(ts), reviewed=0,
                   listened=False, scan={k: (v if not isinstance(v, list) else v[:40])
                                         for k, v in rep.items()}),
              open('logs/watch_pass.json','w'), indent=1)
