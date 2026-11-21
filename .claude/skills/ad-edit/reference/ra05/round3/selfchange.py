"""Self-change map (VIDEO-RULES 2026-10-13, question 1 measured): per shot, first frame against the 10th and the last, over the whole
picture, tolerant of 2 px of drift, with the person masked out (Apple Vision person mask, dilated 25 px). Every region left is listed
with its box and area and drawn on a sheet for a look frame by frame.  usage: selfchange.py <clip.mp4> <name> <shot ranges json>"""
import json, os, subprocess, sys, numpy as np, cv2
from PIL import Image
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
clip, name, shots = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
D = f"check3/selfchange/{name}"; os.makedirs(D, exist_ok=True)
def grab(n):
    p = f"{D}/f{n:04d}.png"
    if not os.path.exists(p):
        subprocess.run([FF, "-v", "error", "-y", "-i", clip, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1", "-update", "1", p], check=True)
    return p
rep = []
for a, b in shots:
    ids = sorted(set([a, min(a + 9, b), b]))
    paths = [grab(n) for n in ids]
    subprocess.run([PM, f"{D}/masks"] + paths, check=True, capture_output=True)
    F = {n: cv2.imread(p) for n, p in zip(ids, paths)}
    M = {n: cv2.resize(cv2.imread(f"{D}/masks/{os.path.basename(p)[:-4]}.mask.png", 0), (F[n].shape[1], F[n].shape[0])) for n, p in zip(ids, paths)}
    for n in ids[1:]:
        f0, f1 = F[a].astype(np.int16), F[n].astype(np.int16)
        # tolerant of 2 px drift: the smallest difference over shifts of -2..2
        best = None
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                d = np.abs(f1 - np.roll(np.roll(f0, dy, 0), dx, 1)).max(2)
                best = d if best is None else np.minimum(best, d)
        best = cv2.GaussianBlur(best.astype(np.float32), (7, 7), 2)
        pm = cv2.dilate(np.maximum(M[a], M[n]), np.ones((51, 51), np.uint8)) > 60
        ch = (best > 22) & ~pm
        nlab, lab, st, _ = cv2.connectedComponentsWithStats(ch.astype(np.uint8))
        regs = [dict(box=[int(v) for v in st[i][:4]], area=int(st[i][4])) for i in range(1, nlab) if st[i][4] >= 150]
        rep.append(dict(shot=[a, b], vs=n, regions=sorted(regs, key=lambda r: -r["area"])[:12]))
        vis = F[n].copy(); vis[pm] = (vis[pm] * 0.35).astype(np.uint8); vis[ch] = (0, 0, 255)
        for r in regs:
            x, y, w, h = r["box"]; cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 255), 3)
        cv2.imwrite(f"{D}/map_{a}_{n}.jpg", cv2.resize(vis, (540, 960)))
json.dump(rep, open(f"{D}/report.json", "w"), indent=1)
for r in rep: print(r["shot"], "vs", r["vs"], [(x["box"], x["area"]) for x in r["regions"]])
