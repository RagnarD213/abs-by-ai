#!/usr/bin/env python3
"""The LAST frame of a full-bleed still beat, rendered exactly as render.py would.

⚠ WHY THIS EXISTS. `sqstills.py` renders frame 0, and `still_chain` starts at zoom 1.0 -- so a
frame-0 contact sheet shows the LOOSEST framing the beat ever has. The push then tightens it by
`amt` over the beat. The 2026-09-11 audit found the top of Dan's head cut on `fatdad_a` at the
beat's end while the frame-0 sheet had looked fine. Check BOTH ends, always.
    python3 sqstill_end.py <key>:<frames>[:ox[:oy[:amt]]] ...
"""
import os, subprocess, sys
sys.path.insert(0,'.'); sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import render as R
from assets import MEDIA
os.makedirs('sqtest/ends', exist_ok=True)
for arg in sys.argv[1:]:
    p = arg.split(':'); key = p[0]; nfr = int(p[1])
    o = dict(R.media_opts(key))
    if len(p) > 2 and p[2] != '': o['ox'] = float(p[2])
    if len(p) > 3 and p[3] != '': o['oy'] = float(p[3])
    amt = float(p[4]) if len(p) > 4 and p[4] != '' else o.pop('amt', 0.075)
    o.pop('amt', None)
    ch = R.still_chain(1080, 1080, nfr, amt=amt, **o)
    tag = f'{key}_ox{o.get("ox",0.5)}_oy{o.get("oy",0.5)}_amt{amt}'
    subprocess.run([R.FF,'-v','error','-y','-loop','1','-framerate','30000/1001','-t',f'{nfr/29.97+0.3:.3f}',
                    '-i', MEDIA[key][1], '-filter_complex', f'[0:v]{ch}[v]','-map','[v]',
                    '-r','30000/1001','-frames:v',str(nfr),
                    '-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p',
                    f'sqtest/ends/_{tag}.mp4'], check=True)
    subprocess.run([R.FF,'-v','error','-y','-i',f'sqtest/ends/_{tag}.mp4','-vf',f"select='eq(n,{nfr-1})'",
                    '-fps_mode','passthrough','-frames:v','1', f'sqtest/ends/{tag}_END.png'], check=True)
    subprocess.run([R.FF,'-v','error','-y','-i',f'sqtest/ends/_{tag}.mp4','-vf',"select='eq(n,0)'",
                    '-fps_mode','passthrough','-frames:v','1', f'sqtest/ends/{tag}_START.png'], check=True)
    os.remove(f'sqtest/ends/_{tag}.mp4')
    print(f'sqtest/ends/{tag}_START.png  +  _END.png  ({nfr} frames)')
