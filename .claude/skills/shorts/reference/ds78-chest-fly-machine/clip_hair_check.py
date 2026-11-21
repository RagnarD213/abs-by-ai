"""Hair/head room on every delivered frame of each gym clip (except the low-angle B04): distance from the clip's own top edge
(window top y=388+border for windowed clips, frame top for full screen) to the top of the person mask."""
import json, subprocess, shutil, hashlib, numpy as np, cv2
from pathlib import Path
from PIL import Image
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = str(R/'Media/video_edit/bin/ffmpeg'); PM = str(R/'.claude/skills/shorts/reference/recentre/personmask')
m = json.load(open(W/'records/assembly.json')); v = m['master']; sha = hashlib.sha256(open(v, 'rb').read()).hexdigest()
d = Path('/tmp/absbyai-scratch/DS-78/cliphair'); shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True); out = {}
for u in m['assets']:
    if u['id'] == 'B04': continue   # low angle from below: his head sits mid-frame under his outstretched arms
    top = 0 if u.get('fullscreen') else 388; bot = 1920 if u.get('fullscreen') else u['box'][3]
    sd = d/u['id']; sd.mkdir()
    subprocess.run([F, '-v', 'error', '-i', v, '-vf', f"select='between(n\\,{u['fa']}\\,{u['fb']-1})',crop=1080:{bot-top}:0:{top},scale=540:-2:in_color_matrix=bt709:in_range=tv", '-vsync', '0', str(sd/'f-%04d.jpg')], check=True)
    ps = sorted(sd.glob('f-*.jpg'))
    for j in range(0, len(ps), 150): subprocess.run([PM, str(sd)]+[str(p) for p in ps[j:j+150]], check=True, stdout=subprocess.PIPE)
    rows = []
    for p in ps:
        mk = np.array(Image.open(sd/(p.stem+'.mask.png')).convert('L')); n, lab, st, _ = cv2.connectedComponentsWithStats((mk > 127).astype('uint8'), 8)
        if n < 2: rows.append(None); continue
        c = 1+int(np.argmax(st[1:, cv2.CC_STAT_AREA])); ys = np.where((lab == c).sum(1) >= 3)[0]
        rows.append(int(ys[0])*2 if len(ys) else None)
    good = [r for r in rows if r is not None]
    out[u['id']] = dict(frames=len(rows), expected=u['frames'], missed=rows.count(None), min_px=min(good), under20=sum(r < 20 for r in good))
    print(u['id'], out[u['id']], flush=True)
json.dump(dict(video_sha256=sha, method='person mask on every delivered clip frame, top of largest component vs the clip top edge, 1080p px', clips=out), open(W/'evidence/clip-hair.json', 'w'), indent=2)
