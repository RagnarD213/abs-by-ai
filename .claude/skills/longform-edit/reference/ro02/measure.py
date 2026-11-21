"""Where Dan is in every kept piece: source frames at 2 fps (960x540), Apple Vision person mask, then per sample the
hair top, head centre x, body left/right edge (1080-scale source px). Writes measure.json {piece: [[t, top, hx, x0, x1], ...]}."""
import json, os, glob, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl as E
W = E.W; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
P = json.load(open(f"{W}/edl.json")); out = {}
for p in P:
    d = f"{W}/tmp/meas/{p['id']}"; os.makedirs(d, exist_ok=True)
    if not glob.glob(f"{d}/f_*.jpg"):
        subprocess.run(["nice", "-n", "10", FF, "-v", "error", "-y", "-ss", f"{p['in']:.3f}", "-t", f"{p['out']-p['in']:.3f}", "-i", E.src(p["roll"]),
                        "-vf", "fps=2,scale=960:540:in_color_matrix=bt709:in_range=tv", "-q:v", "3", f"{d}/f_%05d.jpg"], check=True)
    fs = sorted(glob.glob(f"{d}/f_*.jpg"))
    if not glob.glob(f"{d}/m/*.mask.png"):
        os.makedirs(f"{d}/m", exist_ok=True)
        for i in range(0, len(fs), 200): subprocess.run([PM, f"{d}/m"]+fs[i:i+200], check=True, capture_output=True)
    rows = []
    for k, f in enumerate(fs):
        mp = f"{d}/m/"+os.path.basename(f)[:-4]+".mask.png"
        if not os.path.exists(mp): continue
        m = np.asarray(Image.open(mp).convert("L")) > 127
        if m.shape != (540, 960): m = np.asarray(Image.open(mp).convert("L").resize((960, 540))) > 127
        lab, n = ndimage.label(m)                      # largest connected blob only (a stray blob sits on the chimney cap)
        if not n: continue
        m = lab == (1+int(np.argmax(ndimage.sum(m, lab, range(1, n+1)))))
        ys = np.where(m.sum(1) >= 3)[0]
        if not len(ys): continue
        top = int(ys[0]); bot = int(ys[-1])
        h = max(20, int((bot-top)*0.09))
        xs = np.where(m[top:top+h].sum(0) > 0)[0]; ax = np.where(m.sum(0) >= 3)[0]
        rows.append([round(p["in"]+(k+0.5)/2, 2), top*2, int(xs.mean())*2, int(ax[0])*2, int(ax[-1])*2, bot*2])
    out[p["id"]] = rows
    a = np.array(rows)
    print(f"{p['id']:8s} n={len(rows):3d} top {a[:,1].min():4.0f}-{a[:,1].max():4.0f} head x {a[:,2].min():4.0f}-{a[:,2].max():4.0f} body x {a[:,3].min():4.0f}-{a[:,4].max():4.0f} bottom {a[:,5].max():4.0f}", flush=True)
json.dump(out, open(f"{W}/measure.json", "w"))
