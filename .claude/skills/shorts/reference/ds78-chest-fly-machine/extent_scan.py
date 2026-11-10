"""Per-frame person-mask extent of a whole library clip (native px): top of hair, left/right of body+arms. Used to pick
crops that keep both hands at the stretch and >= 20 px head room. usage: extent_scan.py LIB_ID"""
import sys, subprocess, json, shutil, numpy as np, cv2
from pathlib import Path
from PIL import Image
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = str(R/'Media/video_edit/bin/ffmpeg')
PM = str(R/'.claude/skills/shorts/reference/recentre/personmask'); L = json.load(open(W/'records/library.json')); lib = sys.argv[1]
d = Path(f'/tmp/absbyai-scratch/DS-78/ext-{lib}'); shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
subprocess.run([F, '-v', 'error', '-i', L[lib]['path'], '-vf', 'scale=960:540:in_color_matrix=bt709:in_range=tv', '-q:v', '3', str(d/'f-%04d.jpg')], check=True)
ps = sorted(d.glob('f-*.jpg'))
for j in range(0, len(ps), 150): subprocess.run([PM, str(d)]+[str(p) for p in ps[j:j+150]], check=True, stdout=subprocess.PIPE)
rows = []
for i, p in enumerate(ps):
    m = np.array(Image.open(d/(p.stem+'.mask.png')).convert('L')); n, lab, st, _ = cv2.connectedComponentsWithStats((m > 127).astype('uint8'), 8)
    if n < 2: rows.append(dict(t=round(i/29.97, 3), top=None)); continue
    big = 1+int(np.argmax(st[1:, cv2.CC_STAT_AREA])); keep = [k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] > 0.08*st[big, cv2.CC_STAT_AREA]]
    mm = np.isin(lab, keep); ys = np.where(mm.sum(1) >= 2)[0]; xs = np.where(mm.sum(0) >= 2)[0]
    rows.append(dict(t=round(i/29.97, 3), top=int(ys[0])*4, left=int(xs[0])*4, right=int(xs[-1])*4+3))
json.dump(dict(lib=lib, scale='native 3840x2160 px', rows=rows), open(W/f'evidence/broll/extent-{lib}.json', 'w'))
print(lib, len(rows), 'frames', flush=True)
