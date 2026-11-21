"""Per-shot framing from the Apple Vision person mask on the RAW frames (2 per second over every shot):
hair top (min, median), head centre x, body x-extent. Writes shot_framing.json with the T crop per shot:
T = 1/ZT of the frame, top edge 4 % of the crop above the lowest... highest hair top in the shot (0 where the camera
left no room), centred on the head and held still for the whole shot (16:9 rule: no camera motion)."""
import os, json, subprocess, glob, sys
import numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
R = json.load(open(f"{W}/rolls.json")); S = json.load(open(f"{W}/shots.json")); ZT = 1.32
used = sorted({s["roll"] for s in S})
for roll in used:
    d = f"{W}/mask/{roll}"
    if os.path.exists(d + "/done"): continue
    os.makedirs(d + "/m", exist_ok=True)
    spans = [(s["src_f0"]-R[roll]["f0"], s["src_f1"]-R[roll]["f0"]) for s in S if s["roll"] == roll]
    a = min(x for x, _ in spans)/FPS; b = max(y for _, y in spans)/FPS
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", R[roll]["path"], "-vf", "fps=2,scale=960:540", "-q:v", "4", f"{d}/f_%05d.jpg"], check=True)
    fs = sorted(glob.glob(f"{d}/f_*.jpg"))
    for i in range(0, len(fs), 200): subprocess.run([PM, d + "/m"] + fs[i:i+200], check=True, capture_output=True)
    json.dump(dict(t0=a, n=len(fs)), open(d + "/done", "w")); print(roll, len(fs), "frames", flush=True)
out = {}
for s in S:
    roll = s["roll"]; d = f"{W}/mask/{roll}"; t0 = json.load(open(d + "/done"))["t0"]
    a = (s["src_f0"]-R[roll]["f0"])/FPS; b = (s["src_f1"]-R[roll]["f0"])/FPS
    rows = []
    for k in range(int(max(0, (a-t0)*2)), int((b-t0)*2)+1):
        t = t0 + (k+0.5)/2
        if not (a <= t <= b): continue
        mp = f"{d}/m/f_{k+1:05d}.mask.png"
        if not os.path.exists(mp): continue
        m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
        ys = np.where(m.sum(1) >= 3)[0]
        if not len(ys): continue
        top = ys[0]; xs = np.where(m.any(0))[0]; h = max(8, int((ys[-1]-top)*0.12))
        hx = np.where(m[top:top+h].any(0))[0]
        rows.append((top*2, (hx[0]+hx[-1])/2*2 if len(hx) else None, xs[0]*2, xs[-1]*2, ys[-1]*2))
    if not rows: out[s["id"]] = None; continue
    tops = [r[0] for r in rows]; cx = float(np.median([r[1] for r in rows if r[1] is not None]))
    feet = float(np.median([r[4] for r in rows]))
    zt = 1.5 if feet < 1000 else 1.3          # full-body wide rolls: 1.5x lands the bottom edge mid-shin (1.32x cut him at the ankles); closer rolls 1.3x
    cw = int(round(1920/zt/2))*2; ch = int(round(cw*9/16/2))*2
    y0 = max(0, int(np.percentile(tops, 10) - 0.04*ch)); x0 = int(min(max(0, cx - cw/2), 1920-cw))
    hmed = float(np.median(tops)); hp10 = float(np.percentile(tops, 10)); hp90 = float(np.percentile(tops, 90))
    xw = [r[3]-r[2] for r in rows]; cxs = [r[1] for r in rows if r[1] is not None]
    # Dan's tight shot (round 1 note): slightly above the hair to a little below the shorts line = 62 % of hair-to-feet on the wide rolls
    th = int(round((0.62*(feet-hmed) + 0.05*0.62*(feet-hmed))/2))*2; tw = int(round(th*16/9/2))*2
    ty0 = max(0, int(hp10 - 0.045*th)); tx0 = int(min(max(0, cx - tw/2), 1920-tw))
    active = (hp90-hp10 > 70) or (hmed-min(tops) > 90) or (np.percentile(xw, 95) > 1.75*np.median(xw)) or (max(cxs)-min(cxs) > 0.55*tw - np.median(xw)/2 + 60)
    extra = dict(T2=[tw, th, tx0, ty0], zt2=round(1920/tw, 2), active=bool(active), hair_p10=hp10, hair_p90=hp90, xw_med=float(np.median(xw)), xw_p95=float(np.percentile(xw, 95)))
    out[s["id"]] = dict(extra, n=len(rows), hair_min=int(min(tops)), hair_med=float(np.median(tops)), cx=round(cx), cx_range=[int(min(r[1] for r in rows)), int(max(r[1] for r in rows))],
                        x_extent=[int(np.percentile([r[2] for r in rows], 2)), int(np.percentile([r[3] for r in rows], 98))], feet=int(np.median([r[4] for r in rows])),
                        T=[cw, ch, x0, y0], zt=zt, T_hair_px=round((float(np.median(tops))-y0)*zt), W_hair_px=float(np.median(tops)))
json.dump(out, open(f"{W}/shot_framing.json", "w"), indent=1)
for k, v in out.items():
    if v: print(f"{k:10s} hair min {v['hair_min']:4d} med {v['hair_med']:5.0f} cx {v['cx']:4d} ({v['cx_range'][0]}-{v['cx_range'][1]}) body x {v['x_extent']} feet {v['feet']} T {v['T']} hairT {v['T_hair_px']}")
    else: print(k, "NO MASK")
