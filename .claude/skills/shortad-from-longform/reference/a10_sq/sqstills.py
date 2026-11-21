#!/usr/bin/env python3
"""Square framing probe: render ONE frame of a media key at 1080x1080 exactly as render.py
would (cover crop / still push at t=0), with optional ox/oy overrides, for eyeballing at full
resolution before a build. Usage: python3 sqstills.py <key>[:ox[:oy]] ..."""
import os, subprocess, sys
sys.path.insert(0,'.'); sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import render as R
from assets import MEDIA
FF = R.FF
os.makedirs('sqtest', exist_ok=True)
for arg in sys.argv[1:]:
    p = arg.split(':'); key = p[0]
    o = dict(R.media_opts(key))
    if len(p) > 1 and p[1] != '': o['ox'] = float(p[1])
    if len(p) > 2 and p[2] != '': o['oy'] = float(p[2])
    o.pop('amt', None)
    spec = MEDIA[key]
    t = float(p[3]) if len(p) > 3 else 0.0
    if spec[0] == 'img':
        ch = R.still_chain(1080, 1080, 2, **o)
        ins = ['-loop','1','-framerate','30','-t','0.2','-i',spec[1]]
    else:
        ch = R.media_prefix(key) + R.cover_chain(1080, 1080, **o) + R.bleed_sharpen(key)
        ins = ['-ss', f'{spec[2]+t:.3f}', '-i', spec[1]]
    out = f'sqtest/{key}_{o.get("ox",0.5)}_{o.get("oy",0.5)}_{t:g}.png'
    subprocess.run([FF,'-v','error','-y'] + ins + ['-filter_complex', f'[0:v]{ch}[v]','-map','[v]','-frames:v','1', out], check=True)
    print(out)
