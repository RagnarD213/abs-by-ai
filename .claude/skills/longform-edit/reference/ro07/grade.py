"""Per-roll, skin-anchored grade for the 7/8 kitchen rolls (S-Cinetone, 10-bit, about 1.5 stops under: skin Y90 0.28) and the
7/8 poolside B-roll. Each roll gets ONE tone curve (R, G, B alike) that puts its measured skin highlight (Y90) on the option's
target, crushes its black point and shapes the mids, then saturation. The kitchen rolls first lose the blue veil in their
shadows (window glare: the black tank top reads R .067 G .075 B .098; the fridge mid-tone is neutral, so mids and skin are
left alone). Three options A/B/C for Dan's look round. Writes grades.json {roll: {stats, A: vf, B: vf, C: vf}}."""
import json, glob, os, subprocess, numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro07"; FPS = 30000/1001
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PM = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
SHOOT = "/Volumes/Extreme/abs by ai 7:8 Jeff Chagrin shoot/main camera"
OPT = {  # target skin Y90, mid factor, shadow factor at 0.10, saturation, hue turn (degrees, toward yellow)
 "A": dict(t90=0.46, mid=0.97, low=0.86, sat=1.22, hue=0, name="Rich"),
 "B": dict(t90=0.53, mid=0.98, low=0.90, sat=1.25, hue=0, name="Brighter"),
 "C": dict(t90=0.46, mid=0.97, low=0.86, sat=1.22, hue=7, name="Rich, warmer skin"),
}
POOL = dict(t90=0.74, mid=0.98, low=0.90, sat=1.15, hue=0)          # outdoor sun (RO-06's approved pool target, option B Rich: 0.76)
VEIL = "curves=g='0/0 0.075/0.067 0.26/0.258 1/1':b='0/0 0.098/0.067 0.28/0.272 1/1',"
BROLL = {"C1490": [(15, 20), (45, 50), (76, 120)], "C1491": [(1, 27)], "C1493": [(2, 46), (60, 80)], "C1494": [(2, 36), (60, 86)]}
def ensure_masks(roll, spans):
    d = f"{W}/mask/{roll}"
    if os.path.exists(d + "/done"): return
    os.makedirs(d + "/m", exist_ok=True); k = 0
    for a, b in spans:
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(a), "-t", str(b-a), "-i", f"{SHOOT}/{roll}.MP4", "-vf", "fps=1/2,scale=960:540", "-q:v", "4",
                        "-start_number", str(k+1), f"{d}/f_%05d.jpg"], check=True); k = len(glob.glob(f"{d}/f_*.jpg"))
    fs = sorted(glob.glob(f"{d}/f_*.jpg")); subprocess.run([PM, d + "/m"] + fs, check=True, capture_output=True)
    json.dump(dict(spans=spans, n=len(fs)), open(d + "/done", "w"))
def roll_stats(roll, step=3):
    ys, y90s, p995, bps = [], [], [], []
    for f in sorted(glob.glob(f"{W}/mask/{roll}/f_*.jpg"))[::step]:
        mp = f.replace("/f_", "/m/f_").replace(".jpg", ".mask.png")
        if not os.path.exists(mp): continue
        im = np.asarray(Image.open(f).convert("RGB"), np.float32)/255; m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
        r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(2); mn = im.min(2); d = mx-mn+1e-6
        h = np.where(mx == r, ((g-b)/d) % 6, np.where(mx == g, (b-r)/d+2, (r-g)/d+4))*60; s = d/(mx+1e-6)
        sk = m & (h > 4) & (h < 38) & (s > 0.22) & (s < 0.78) & (mx > 0.10)
        if sk.sum() < 800: continue
        y = 0.2126*r+0.7152*g+0.0722*b
        ys.append(np.median(y[sk])); y90s.append(np.percentile(y[sk], 90)); p995.append(np.percentile(y, 99.5)); bps.append(np.percentile(y, 1))
    return dict(skinY=float(np.median(ys)), skinY90=float(np.median(y90s)), p995=float(np.median(p995)), black=float(np.median(bps)), n=len(ys))
def curve(st, o, veil=""):
    k = o["t90"]/st["skinY90"]; bp = max(0.012, st["black"])
    pts = [(0, 0), (bp, 0.004), (0.10, 0.10*k*o["low"]), (st["skinY"], st["skinY"]*k*o["mid"]), (st["skinY90"], o["t90"])]
    pts = [p for i, p in enumerate(pts) if i == 0 or p[0] > pts[i-1][0] + 0.01]
    top = min(0.985, st["p995"]+0.10); pts.append((top, min(0.975, o["t90"] + (top-st["skinY90"])*min(k, 1.6)*0.62)))
    pts.append((1, 1))
    pts = [(round(x, 4), round(min(max(y, 0), 1), 4)) for x, y in pts]
    assert all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(pts, pts[1:])), pts
    return (veil + "curves=all='" + " ".join(f"{x}/{y}" for x, y in pts) + "'" + (f",eq=saturation={o['sat']}" if o["sat"] != 1 else "")
            + (f",hue=h={o['hue']}" if o.get("hue") else ""))
if __name__ == "__main__":
    G = json.load(open(f"{W}/grades.json")) if os.path.exists(f"{W}/grades.json") else {}
    for roll in ("C1484", "C1485"):
        if not os.path.exists(f"{W}/mask/{roll}/done"): print(roll, "masks not ready"); continue
        st = roll_stats(roll, 9); G[roll] = dict(stats=st, **{k: curve(st, o, VEIL) for k, o in OPT.items()})
        print(roll, {k: round(v, 3) for k, v in st.items()})
    for roll, spans in BROLL.items():
        ensure_masks(roll, spans); st = roll_stats(roll, 1); c = curve(st, POOL); G[roll] = dict(stats=st, A=c, B=c, C=c)
        print(roll, {k: round(v, 3) for k, v in st.items()}, c)
    json.dump(G, open(f"{W}/grades.json", "w"), indent=1)
