"""Per-roll, skin-anchored grade for the 8/3 pool rolls (sun dropping: sunlit skin Y90 0.65 -> 0.57, background into shade).
Each roll gets ONE tone curve (applied to R, G, B alike) that puts its measured skin highlight (Y90) on the option's target,
crushes its black point and shapes mids, then a saturation factor. Three options A/B/C for Dan's look round.
Writes grades.json {roll: {stats, A: vf, B: vf, C: vf}}. No white-balance change: the tan is the subject (skill Step 6)."""
import json, glob, os, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro06"
S = json.load(open(f"{W}/shots.json"))
OPT = {  # target skin Y90, mid factor (x linear), shadow factor at 0.10, saturation
 "A": dict(t90=0.70, mid=1.00, low=1.00, sat=1.00, name="Natural"),
 "B": dict(t90=0.76, mid=0.97, low=0.88, sat=1.12, name="Rich"),
 "C": dict(t90=0.80, mid=1.04, low=1.12, sat=1.18, name="Bright"),
}
def roll_stats(roll):
    ys, y90s, p995, bps = [], [], [], []
    for f in sorted(glob.glob(f"{W}/mask/{roll}/f_*.jpg"))[::3]:
        mp = f.replace("/f_", "/m/f_").replace(".jpg", ".mask.png")
        if not os.path.exists(mp): continue
        im = np.asarray(Image.open(f).convert("RGB"), np.float32)/255; m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
        r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(2); mn = im.min(2); d = mx-mn+1e-6
        h = np.where(mx == r, ((g-b)/d) % 6, np.where(mx == g, (b-r)/d+2, (r-g)/d+4))*60; s = d/(mx+1e-6)
        sk = m & (h > 8) & (h < 38) & (s > 0.25) & (s < 0.78) & (mx > 0.12)
        if sk.sum() < 800: continue
        y = 0.2126*r+0.7152*g+0.0722*b
        ys.append(np.median(y[sk])); y90s.append(np.percentile(y[sk], 90)); p995.append(np.percentile(y, 99.5)); bps.append(np.percentile(y, 1))
    return dict(skinY=float(np.median(ys)), skinY90=float(np.median(y90s)), p995=float(np.median(p995)), black=float(np.median(bps)), n=len(ys))
def curve(st, o):
    k = o["t90"]/st["skinY90"]; bp = max(0.012, st["black"])
    pts = [(0, 0), (bp, 0.004), (0.10, 0.10*k*o["low"]), (st["skinY"], st["skinY"]*k*o["mid"]), (st["skinY90"], o["t90"])]
    top = min(0.985, st["p995"]+0.10); pts.append((top, min(0.975, o["t90"] + (top-st["skinY90"])*k*0.62)))
    pts.append((1, 1))
    pts = [(round(x, 4), round(min(max(y, 0), 1), 4)) for x, y in pts]
    assert all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(pts, pts[1:])), pts
    return "curves=all='" + " ".join(f"{x}/{y}" for x, y in pts) + "'" + (f",eq=saturation={o['sat']}" if o["sat"] != 1 else "")
if __name__ == "__main__":
    G = {}
    for roll in sorted({s["roll"] for s in S}):
        st = roll_stats(roll); G[roll] = dict(stats=st, **{k: curve(st, o) for k, o in OPT.items()})
        print(roll, {k: round(v, 3) for k, v in st.items()}, "gain B x%.2f" % (OPT["B"]["t90"]/st["skinY90"]))
    json.dump(G, open(f"{W}/grades.json", "w"), indent=1)
