#!/usr/bin/env python3
"""raw torso anchor at EXACT frames: every 7th frame (n = 7k) PLUS the last frame before and the first
frame of every picture segment, so the track knows exactly where he is either side of each cut.

⚠ `fps=4` sampling labels its output k/4 s but takes a frame ~0.2 s LATER, so the old track switched to
the incoming take's pose two frames BEFORE the picture cut (the re-audit's 726 px/s whip at 21.05 s).
Frame indices are the only honest time base."""
import glob, json, os, subprocess, sys, numpy as np
from PIL import Image
sys.path.insert(0, 'rc'); from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
P = json.load(open('edl_picture.json'))
want = set(range(0, P[-1]['n1'], 7))
for s in P[1:]: want.update([s['n0']-1, s['n0']])
want = sorted(n for n in want if 0 <= n < P[-1]['n1'])
subprocess.run(['rm','-rf','rc/fr3','rc/masks3'], check=False); os.makedirs('rc/fr3'); os.makedirs('rc/masks3')
# select every wanted frame by index; showinfo is not needed because the output order == sorted indices
expr = '+'.join(f'eq(n\\,{n})' for n in want)
open('rc/select3.txt','w').write("select='" + '+'.join(f'eq(n,{n})' for n in want) + "',scale=480:270")
subprocess.run([FF,'-nostdin','-v','error','-y','-i','base.mp4','-filter_script:v','rc/select3.txt','-fps_mode','passthrough',
                'rc/fr3/%05d.png'], check=True)
fs = sorted(glob.glob('rc/fr3/*.png'))
assert len(fs) == len(want), (len(fs), len(want))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', 'rc/masks3'] + fs[i:i+60], check=True, capture_output=True)
ms = sorted(glob.glob('rc/masks3/*.mask.png')); assert len(ms) == len(fs)
xs = []
for f in ms:
    m = np.asarray(Image.open(f).convert('L'), dtype=np.float32)/255.0
    a = anchors(m > 0.5); xs.append(np.nan if a is None else a['torso']*1920)
x = np.array(xs); n = np.array(want)
np.save('raw_torso.npy', x); np.save('raw_torso_n.npy', n)
ok = ~np.isnan(x)
print(f'{len(want)} exact frames ({len(want)-len(P)*2} on the 7-frame grid + cut frames), {ok.sum()} with a person ({100*ok.mean():.0f}%)')
