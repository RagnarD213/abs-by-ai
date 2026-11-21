#!/usr/bin/env python3
"""raw_torso.npy for the CURRENT base: 4 fps frames -> Apple Vision person masks -> torso anchor (px of 1920)."""
import glob, os, subprocess, sys, numpy as np
from PIL import Image
sys.path.insert(0, 'rc'); from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
subprocess.run(['rm','-rf','rc/fr2','rc/masks2'], check=False); os.makedirs('rc/fr2'); os.makedirs('rc/masks2')
subprocess.run([FF,'-nostdin','-v','error','-y','-i','base.mp4','-vf','fps=4,scale=480:270','rc/fr2/%05d.png'], check=True)
fs = sorted(glob.glob('rc/fr2/*.png'))
for i in range(0, len(fs), 60):
    subprocess.run(['./rc/personmask', 'rc/masks2'] + fs[i:i+60], check=True, capture_output=True)
ms = sorted(glob.glob('rc/masks2/*.mask.png'))
xs = []
for f in ms:
    m = np.asarray(Image.open(f).convert('L'), dtype=np.float32)/255.0
    a = anchors(m > 0.5); xs.append(np.nan if a is None else a['torso']*1920)
x = np.array(xs); ok = ~np.isnan(x)
np.save('raw_torso.npy', x)
print(f'{len(fs)} frames, {len(ms)} masks, {ok.sum()} with a person ({100*ok.mean():.0f}%); torso {np.nanmin(x):.0f}..{np.nanmax(x):.0f}')
