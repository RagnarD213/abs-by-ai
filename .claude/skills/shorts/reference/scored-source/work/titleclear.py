#!/usr/bin/env python3
"""STANDING RULE CHECK: the title must not sit on his face or his abs.

Measured on the DELIVERED file, during the title window only. Vision gives the person mask;
the face+abs band is taken as the top 55% of the subject's own height (head through navel).
The title's ink bbox comes from the rendered title PNG. If the two rectangles intersect on
BOTH axes, the rule is broken.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
L = json.load(open(os.path.join(HERE, 'layout.json')))
# The title now HOLDS for the whole short, so the check runs across the whole duration
# rather than a 3.2s window - and it also asserts the picture never reaches above dropTop,
# which is the structural guarantee behind the rule.
DROP = L['dropTop']
segs = json.loads(subprocess.check_output(
    ['node', '-e', "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS.map(s=>[s.id,s.slug])))"],
    cwd=HERE, stderr=subprocess.DEVNULL).decode())
tmp = '/tmp/_tc'; os.makedirs(tmp, exist_ok=True)
bad = 0
for sid, slug in segs:
    src = os.path.join(HERE, 'out', f'{sid.lower()}_{slug}.mp4')
    # title ink rectangle, excluding the scrim (which is transparent-ish and not "blocking")
    a = np.array(Image.open(os.path.join(HERE, 'assets', f'title-{sid}.png')).split()[-1])
    ink = a > 200                       # solid glyph pixels only
    ys, xs = np.nonzero(ink)
    tx0, tx1, ty0, ty1 = xs.min(), xs.max(), ys.min(), ys.max()
    dur = float(subprocess.check_output(
        [FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', src]).decode().strip())
    worst = None; ref = None
    for i in range(10):
        t = 0.25 + i * (dur - 0.6) / 9
        f = f'{tmp}/{sid}_{i}.png'
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', src,
                        '-frames:v', '1', f], check=True)
        subprocess.run([os.path.join(HERE, 'recentre', 'personmask'), tmp, f],
                       check=True, capture_output=True)
        # Structural check: above dropTop the frame must be EXACTLY the J2 field plus the
        # title. Measuring "is anything there" fails immediately - the title is there by
        # design - so compare against the intended composite and look for picture leaking in.
        im = cv2.imread(f)
        if ref is None:
            bg = Image.open(os.path.join(HERE, 'assets', 'j2-bg.png')).convert('RGBA')
            ttl = Image.open(os.path.join(HERE, 'assets', f'title-{sid}.png')).convert('RGBA')
            comp = Image.alpha_composite(bg, ttl).convert('RGB')
            ref = cv2.cvtColor(np.array(comp), cv2.COLOR_RGB2BGR)[:DROP - 6].astype(int)
        d = np.abs(im[:DROP - 6].astype(int) - ref).mean()
        if d > 3.0:
            print(f'  {sid}: PICTURE LEAKS ABOVE dropTop at {t:.2f}s (mean diff {d:.1f})')
            bad += 1
        m = cv2.imread(f'{tmp}/{sid}_{i}.mask.png', cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        mm = m > 127
        ys2, xs2 = np.nonzero(mm)
        if len(ys2) < 500: continue
        y0, y1 = ys2.min(), ys2.max()
        band = y0 + 0.55 * (y1 - y0)            # head through navel
        sel = ys2 <= band
        fx0, fx1 = xs2[sel].min(), xs2[sel].max()
        ov_y = min(ty1, band) - max(ty0, y0)
        ov_x = min(tx1, fx1) - max(tx0, fx0)
        overlap = ov_y > 0 and ov_x > 0
        area = (ov_y * ov_x) if overlap else 0
        if worst is None or area > worst[0]:
            worst = (area, t, (fx0, fx1, y0, int(band)))
    if worst is None:
        print(f'  {sid}: no person detected in any sample - picture-position check only'); continue
    area, t, (fx0, fx1, y0, band) = worst
    ok = area == 0
    if not ok: bad += 1
    print(f'  {sid}: title ink x{tx0}-{tx1} y{ty0}-{ty1} | face+abs x{fx0}-{fx1} y{y0}-{band} '
          f'@{t:.2f}s -> {"CLEAR" if ok else f"BLOCKED ({area}px2)"}')
print(f'\ntitle-clearance: {"PASS" if bad == 0 else f"{bad} short(s) BLOCKED"}')
sys.exit(0 if bad == 0 else 1)
