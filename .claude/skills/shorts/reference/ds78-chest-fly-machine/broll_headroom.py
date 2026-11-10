"""Head/hair room on every frame of a library clip at a given crop, in output-window pixels (person mask, largest component).
usage: broll_headroom.py LIB_ID X W WINDOW_W OUT.json [START END]   (full height always kept)"""
import sys, subprocess, json, shutil, numpy as np, cv2
from pathlib import Path
from PIL import Image
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); F = str(R/'Media/video_edit/bin/ffmpeg'); PM = str(R/'.claude/skills/shorts/reference/recentre/personmask')
L = json.load(open('/Users/danielrose/Projects/_edit_work/DS-78/round1/records/library.json'))
lib, x, w, ww, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
a = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0; b = float(sys.argv[7]) if len(sys.argv) > 7 else L[lib]['duration']
wh = round(ww*2160/w); half = (ww//2, wh//2)
d = Path(f'/tmp/absbyai-scratch/DS-78/head-{lib}-{x}-{w}'); shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
subprocess.run([F, '-v', 'error', '-ss', str(a), '-i', L[lib]['path'], '-t', str(b-a), '-vf', f"crop={w}:2160:{x}:0,curves=all='0/0 0.12/0.230 0.35/0.440 0.7/0.736 1/1',scale={half[0]}:{half[1]}:in_color_matrix=bt709:in_range=tv", str(d/'f-%04d.jpg')], check=True)
ps = sorted(d.glob('f-*.jpg'))
for j in range(0, len(ps), 150): subprocess.run([PM, str(d)]+[str(p) for p in ps[j:j+150]], check=True, stdout=subprocess.PIPE)
rows = []
for i, p in enumerate(ps):
    m = np.array(Image.open(d/(p.stem+'.mask.png')).convert('L')); n, lab, st, _ = cv2.connectedComponentsWithStats((m > 127).astype('uint8'), 8)
    if n < 2: rows.append((round(a+i/29.97, 3), None)); continue
    c = 1+int(np.argmax(st[1:, cv2.CC_STAT_AREA])); ys = np.where((lab == c).sum(1) >= 3)[0]
    if not len(ys): ys = np.where(lab == c)[0]
    rows.append((round(a+i/29.97, 3), int(ys[0])*2))
json.dump(dict(lib=lib, crop=[x, 0, w, 2160], window=[ww, wh], rows=rows), open(out, 'w'))
v = [r for _, r in rows if r is not None]
print(lib, x, w, 'frames', len(rows), 'missed', sum(r is None for _, r in rows), 'min', min(v), flush=True)
# runs where room >= 24 px (margin over 20)
ok = [t for t, r in rows if r is not None and r >= 24]; runs = []; s = None; prev = None
for t, r in rows:
    good = r is not None and r >= 24
    if good and s is None: s = t
    if not good and s is not None: runs.append((s, prev)); s = None
    prev = t
if s is not None: runs.append((s, prev))
print('  clear runs (>=24 px):', [(round(p, 2), round(q, 2)) for p, q in runs if q-p >= 1.0])
