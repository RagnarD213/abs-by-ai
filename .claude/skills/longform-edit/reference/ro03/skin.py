"""Raw torso-skin luma per 0.5 s sample of every kept piece (person mask, chest-to-waist rows), for the per-shot exposure
trim. Writes skin.json {piece: [[t, luma], ...]} (luma = Rec.709 on the 8-bit BT.709 decode, 0..1)."""
import json, os, glob, sys, numpy as np
from PIL import Image
from scipy import ndimage
W = "/Volumes/Extreme/_edit_work/ro03"; P = json.load(open(f"{W}/edl.json")); out = {}
for p in P:
    d = f"{W}/tmp/meas/{p['id']}"; rows = []
    for k, f in enumerate(sorted(glob.glob(f"{d}/f_*.jpg"))):
        mp = f"{d}/m/"+os.path.basename(f)[:-4]+".mask.png"
        if not os.path.exists(mp): continue
        m = np.asarray(Image.open(mp).convert("L").resize((960, 540))) > 127
        lab, n = ndimage.label(m)
        if not n: continue
        m = lab == (1+int(np.argmax(ndimage.sum(m, lab, range(1, n+1)))))
        ys = np.where(m.sum(1) >= 3)[0]; top, bot = ys[0], ys[-1]; h = bot-top
        t = m.copy(); t[:top+int(h*0.13)] = False; t[top+int(h*0.42):] = False
        a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)/255
        r, g, b = a[..., 0], a[..., 1], a[..., 2]; t &= (r > g) & (g > b)
        if t.sum() < 500: continue
        rows.append([round(p["in"]+(k+0.5)/2, 2), float(np.median((a @ np.array([.2126, .7152, .0722], np.float32))[t]))])
    out[p["id"]] = rows; v = np.array([r[1] for r in rows])
    print(f"{p['id']:8s} {p['roll']} n={len(v):3d} median {np.median(v):.3f}  p5 {np.percentile(v,5):.3f} p95 {np.percentile(v,95):.3f}")
json.dump(out, open(f"{W}/skin.json", "w"))
