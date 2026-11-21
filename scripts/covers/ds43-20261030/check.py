#!/usr/bin/env python3
"""Check rendered covers: size, safe zones, text off every detected face and its hair. Writes the faces sheet."""
from pathlib import Path
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw
OUT = Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/ds43-terry-crews-20261030'
ROOT = Path(__file__).resolve().parents[3]
PM = Path.home()/'.cache/absbyai/personmask/personmask'
rows = json.loads((OUT/'built/manifest.json').read_text()); res = []; crops = []
for r in rows:
    p = ROOT/r['path']; pic = p.with_name(p.stem+'.picture.png'); mk = p.with_name(p.stem+'.person-mask.png')
    faces = json.loads(subprocess.run([str(PM), str(pic), str(mk)], capture_output=True, text=True, check=True).stdout)['faces']
    tm = np.array(Image.open(p.with_name(p.stem+'.text-mask.png'))) > 0; im = Image.open(p); hit = []
    for f in faces:
        x0, y0, x1, y1 = map(int, f); fw, fh = x1-x0, y1-y0
        b = (max(0, x0-fw//4), max(0, y0-fh//2), min(1080, x1+fw//4), min(1920, y1+fh//5))
        hit.append(int(tm[b[1]:b[3], b[0]:b[2]].sum()))
        if r['platform'] == 'youtube': crops.append((r['letter'], ImageOps.contain(im.crop(b), (200, 230))))
    miny, maxy = (240, 1680) if r['platform'] == 'instagram' else (50, 1850)
    safe = all(25 <= b[0] < b[2] <= 1055 and miny <= b[1] < b[3] <= maxy for b in r['text_bounds'])
    ok = safe and im.size == (1080, 1920) and len(faces) >= 1 and not any(hit)
    res.append(dict(letter=r['letter'], platform=r['platform'], safe=safe, faces=len(faces), text_on_face=hit, ok=ok))
    print(r['letter'], r['platform'], 'OK' if ok else 'FAIL', len(faces), hit, safe)
s = Image.new('RGB', (210*len(crops), 260), '#253044'); d = ImageDraw.Draw(s)
for i, (l, c) in enumerate(crops): s.paste(c, (i*210+5, 25)); d.text((i*210+5, 5), l, fill='white')
s.save(OUT/'built/face-check.jpg', quality=92); (OUT/'built/cover-checks.json').write_text(json.dumps(res, indent=1))
