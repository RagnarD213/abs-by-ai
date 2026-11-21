"""RO-19 round 3: scene-content check on the exact master (CUT-CONTINUITY-QC section 5). Every full-screen item of the plan (clip, photo scene, phone scene) is
compared at its entrance, interior and exit with its INDEPENDENT component: the component's own file decoded at the matching offset through the build's own
filter (and lift), never a crop of the master. Compared on the picture above the lower-third band and away from the label chip (rows 110 to 700), as the
correlation of the two frames at 480x270. Also reports whether each scene moves (mean frame change over its first second in the master).
Writes scene_checklist.json beside the master. usage: scene_check19.py MASTER.mp4"""
import sys, os, json, subprocess, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import build as Bd, gfx as G, frames as F
master = os.path.abspath(sys.argv[1]); FPS = Bd.FPS; FF = Bd.FF
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def mframe(f):                                           # the master's frame f, decoded sequentially from 1 s before (never a bare seek)
    t = f/FPS; ss = max(0, t - 1.0)
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{ss:.4f}", "-i", master, "-ss", f"{t-ss-0.4/FPS:.4f}" if t > ss else "0", "-frames:v", "1", "-vf", "scale=1920:1080:in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1920, 1080), raw)
def small(im): return np.asarray(im.convert("L").resize((480, 270), Image.BILINEAR), np.float32)[28:175]
def corr(a, b): a = a - a.mean(); b = b - b.mean(); return float((a*b).sum()/max(1e-6, np.sqrt((a*a).sum()*(b*b).sum())))
out = []; hashes = {}
for it in Bd.R:
    if it["kind"] != "clip": continue
    f0, f1 = Bd.fr(it["t0"]), Bd.fr(it["t1"]); n = f1 - f0; comp = list(Bd.clip_frames(it))          # the component frames exactly as the build reads them
    assert len(comp) == n, (it["id"], len(comp), n)
    rows = []
    for nm, k in (("entrance", 1), ("interior", n//2), ("exit", n - 2)):
        rows.append(dict(at=nm, frame=f0 + k, t=round((f0 + k)/FPS, 3), corr=round(corr(small(mframe(f0 + k)), small(comp[k])), 4)))
    mv = float(np.mean([np.abs(small(comp[k + 1]) - small(comp[k])).mean() for k in range(0, min(n - 1, 30))]))
    srcs = []
    for sp in it["src"]:
        p = G.src_path(sp); hashes.setdefault(p, sha(p)); srcs.append(dict(path=p, sha256=hashes[p], start=G.src_start(sp)))
    still = bool(it.get("pair") or it.get("photo") or it.get("portraits"))
    out.append(dict(id=it["id"], t0=round(f0/FPS, 3), t1=round(f1/FPS, 3), frames=n, intended=it.get("note", ""), components=srcs, label=it.get("label"),
                    intentional_still=still, moves=round(mv, 3), checks=rows, ok=min(r["corr"] for r in rows) >= 0.90))
    print(it["id"], [r["corr"] for r in rows], "moves", round(mv, 2), "" if out[-1]["ok"] else "  <-- LOW", flush=True)
json.dump(dict(master=master, sha256=sha(master), scenes=out), open(os.path.join(os.path.dirname(master), "scene_checklist.json"), "w"), indent=1)
print(len(out), "scenes;", sum(o["ok"] for o in out), "match their component at entrance, interior and exit; low:", [o["id"] for o in out if not o["ok"]])
