#!/usr/bin/env python3
"""Check the rendered covers: size, title safe areas, text off every face and hair, YouTube JPEG size. Face sheet for the eye check."""
from pathlib import Path
import json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from build import BUILT, OUT, PM, W, H, SHORTS, LETTERS
rows = []; sheet_faces = []
for s in SHORTS:
    m = json.loads((BUILT/s/'manifest.json').read_text())
    for row in m['outputs']:
        d = BUILT/s/row['letter']; pf = row['platform']; p = d/f'{pf}.png'; pic = d/f'{pf}.picture.png'; mask = d/f'{pf}.person-mask.png'
        r = subprocess.run([str(PM), str(pic), str(mask)], capture_output=True, text=True, check=True); faces = json.loads(r.stdout)['faces']
        tm = np.array(Image.open(d/f'{pf}.text-mask.png')) > 0; im = Image.open(p)
        hits = []
        for f in faces:
            x0, y0, x1, y1 = map(int, f); fw, fh = x1-x0, y1-y0
            a, b, c, e = max(0, x0-fw//4), max(0, y0-fh//2), min(W, x1+fw//4), min(H, y1+fh//5)
            hits.append(int(tm[b:e, a:c].sum()))
            if pf == 'youtube' and fw*fh > 16000: sheet_faces.append((f"{s}{row['letter']}", ImageOps.contain(im.crop((a, b, c, e)), (170, 200))))
        miny, maxy = (240, 1680) if pf == 'instagram' else (50, 1850)
        safe = all(25 <= q[0] < q[2] <= W-25 and miny <= q[1] < q[3] <= maxy for q in row['text_bounds'])
        ok = safe and im.size == (W, H) and bool(faces) and not any(hits)
        if pf == 'youtube': ok = ok and p.with_suffix('.jpg').stat().st_size < 2_000_000
        rows.append(dict(s=s, letter=row['letter'], platform=pf, safe=safe, faces=len(faces), hits=hits, passed=ok))
bad = [r for r in rows if not r['passed']]
(OUT/'cover-checks.json').write_text(json.dumps(dict(all_passed=not bad, rows=rows), indent=1))
print(len(rows), 'checked;', len(bad), 'failed'); print(*bad, sep='\n')
n = len(sheet_faces); cols = 10; sh = Image.new('RGB', (cols*180, (n//cols+1)*230), '#253044'); dr = ImageDraw.Draw(sh)
for i, (t, f) in enumerate(sheet_faces):
    x, y = (i % cols)*180, (i//cols)*230; sh.paste(f, (x+5, y+22)); dr.text((x+5, y+5), t, fill='white')
sh.save(OUT/'face-check.jpg', quality=92)
