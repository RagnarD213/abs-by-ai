#!/usr/bin/env python3
"""SL-19: head and hair clearance on the DELIVERED short (VIDEO-RULES 2026-10-20): every 0.25 s of presenter picture plus the first and
last frame of every talking shot, the Vision person mask's top (largest component, rows with >= 20 px of mask) against the picture's
top edge (canvas y 310). Fails under 20 px or on a frame with no detection. Writes build/S/gate/haircheck.json."""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image
from scipy import ndimage
import importlib.util as _iu
import batch as Bt
_sp = _iu.spec_from_file_location('sl19_deliver', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deliver.py')); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
PM = Bt.PM; FF = Bt.lib.FF; FPS = Bt.FPS
def run(S):
    V = Dl.dname(S); shots = json.load(open(f"{Bt.D(S)}/shots.json")); out = []
    td = f"/private/tmp/claude-501/sl19hair/{S}"; os.makedirs(td, exist_ok=True)
    for f in glob.glob(td + "/*"): 
        if os.path.isfile(f): os.remove(f)
    ts = []
    for sh in shots:
        if sh["kind"] != "talk": continue
        a, b = sh["f0"] / FPS, (sh["f1"] - 1) / FPS
        ts += [a + 0.01] + list(np.arange(a + 0.25, b, 0.25)) + [b - 0.01]
    paths = []
    for k, t in enumerate(ts):
        p = f"{td}/h_{k:04d}.png"
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", V, "-frames:v", "1", "-vf", "crop=1080:1610:0:310,scale=540:805", p], check=True, env=dict(os.environ, GATE_OFF="1"))
        paths.append(p)
    os.makedirs(td + "/m", exist_ok=True)
    subprocess.run([PM, td + "/m"] + paths, check=True, capture_output=True)
    for t, p in zip(ts, paths):
        mp = f"{td}/m/{os.path.basename(p)[:-4]}.mask.png"
        m = np.array(Image.open(mp)) > 127 if os.path.exists(mp) else None
        top = None
        if m is not None and m.any():
            lab, n = ndimage.label(m); bb = lab == (int(np.argmax(ndimage.sum(m, lab, range(1, n + 1)))) + 1)
            rows = np.where(bb.sum(1) >= 10)[0]
            if len(rows): top = int(rows[0]) * 2           # back to 1080-wide picture pixels
        out.append(dict(t=round(t, 2), clearance=top))
    bad = [r for r in out if r["clearance"] is None or r["clearance"] < 20]
    res = dict(file=os.path.basename(V), samples=len(out), min=min((r["clearance"] for r in out if r["clearance"] is not None), default=None),
               worst=sorted([r for r in out if r["clearance"] is not None], key=lambda r: r["clearance"])[:5], failing=bad)
    json.dump(res, open(f"{Bt.D(S)}/gate/haircheck.json", "w"), indent=1)
    print(S, "samples", res["samples"], "min clearance px", res["min"], "failing", len(bad), "worst", res["worst"][:3])
for S in sys.argv[1:]: run(S)
