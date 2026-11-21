"""DS-107: frames for the person-judged negative-events scan (compliance:negative_events): 32 evenly spaced frames of the delivered
file plus every cutaway/photo midpoint, as one contact sheet with times; the judgment is written to main/negative-events.json."""
import subprocess, json, hashlib, sys
from pathlib import Path
from PIL import Image, ImageDraw
W = Path(__file__).resolve().parents[1]; O = W/'main'; F = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
M = O/'review'/'Metabolism Not The Reason SFC R1.mp4'; sha = hashlib.sha256(M.read_bytes()).hexdigest()
shots = json.load(open(O/'shots.json')); END = json.load(open(O/'edl.json'))['total_seconds']
ts = sorted(set([round(i*END/32 + END/64, 2) for i in range(32)] + [round((s['a'] + s['b'])/2, 2) for s in shots if s['kind'] in ('broll', 'still')]))
d = O/'negscan'; d.mkdir(exist_ok=True); ims = []
for t in ts:
    p = d/f'{t:06.2f}.jpg'; subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-i', str(M), '-frames:v', '1', '-vf', 'scale=216:384', str(p)], check=True)
    im = Image.open(p); ImageDraw.Draw(im).text((4, 370), f'{t:.2f}s', fill='yellow'); ims.append(im)
cols = 9; rows = (len(ims) + cols - 1)//cols; c = Image.new('RGB', (216*cols, 384*rows))
for k, im in enumerate(ims): c.paste(im, ((k % cols)*216, (k//cols)*384))
c.save(d/'sheet.jpg', quality=88); json.dump(dict(sha256=sha, times=ts), open(d/'frames.json', 'w')); print(len(ts), 'frames', sha[:12])
