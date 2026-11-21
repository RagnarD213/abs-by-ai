#!/usr/bin/env python3
"""Watch pass. The QC gate measures the container and the audio; it never LOOKS at the
picture. Two sheets per short, both pulled from the DELIVERED file:

  sheet_<id>.jpg      every 2 s - the whole short, read like a storyboard
  bounds_<id>.jpg     three consecutive frames either side of every shot join

The boundary strip is the one that earns its keep: a black frame, a flash bloom or a shot
that opens on the wrong content is invisible in a 2 s sample and obvious in consecutive frames.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000 / 1001
F = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)

segs = json.loads(subprocess.check_output(
    ['node', '-e', """const {SEGMENTS}=require('./segments.js');const {loadShots}=require('./plan.js');
console.log(JSON.stringify(SEGMENTS.map(s=>({id:s.id,slug:s.slug,
  shots:loadShots().filter(x=>x.seg===s.id).map(x=>({name:x.name,dur:x.dur,t:x.t}))}))))"""],
    cwd=HERE, stderr=subprocess.DEVNULL).decode())

def frames(src, times, w=200):
    out = []
    for t in times:
        o = f'/tmp/_w{abs(hash((src,t)))%10**9}.jpg'
        r = subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{max(0,t):.3f}", "-i", src,
                            "-frames:v", "1", "-vf", f"scale={w}:-1", o], capture_output=True)
        out.append((t, Image.open(o) if os.path.exists(o) else None))
    return out

def grid(items, cols, w, path, label=lambda t: f"{t:.2f}s"):
    h = round(w * 16 / 9)
    rows = (len(items) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * (h + 20)), (14, 14, 14))
    d = ImageDraw.Draw(sh)
    for i, (t, im) in enumerate(items):
        x, y = (i % cols) * w, (i // cols) * (h + 20)
        if im: sh.paste(im.resize((w, h)), (x, y + 20))
        d.text((x + 3, y + 3), label(t), fill=(255, 220, 120), font=F)
    sh.save(path, quality=86)
    return sh.size

for s in segs:
    src = os.path.join(HERE, 'out', f"{s['id'].lower()}_{s['slug']}.mp4")
    dur = float(subprocess.check_output([FF.replace('ffmpeg','ffprobe'), '-v','error','-show_entries',
        'format=duration','-of','csv=p=0', src]).decode().strip())
    ts = [round(t, 2) for t in [i * 2.0 + 0.5 for i in range(int(dur / 2.0))]]
    print(s['id'], 'sheet', grid(frames(src, ts), 12, 190, os.path.join(HERE, 'shots', f"sheet_{s['id']}.jpg")))
    # boundaries
    joins, acc = [], 0.0
    for sh in s['shots'][:-1]:
        acc += sh['dur']; joins.append(round(acc, 3))
    items = []
    for j in joins:
        for k in (-3, -2, -1, 0, 1, 2):
            items.append((round(j + k / FPS, 3), None))
    got = frames(src, [t for t, _ in items], w=190)
    print(s['id'], 'bounds', grid(got, 6, 190, os.path.join(HERE, 'shots', f"bounds_{s['id']}.jpg")))
