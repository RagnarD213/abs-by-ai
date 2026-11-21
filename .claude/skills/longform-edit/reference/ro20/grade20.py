"""RO-20 (8/3 kitchen doorway roll C1511, S-Cinetone 10-bit, new set under the round method): masks + skin stats over the whole
roll, then the look candidates. Reuses grade.py's skin-anchored curve. Writes grades.json {C1511: {stats, <option>: vf}}.
usage: grade20.py masks | stats"""
import json, glob, os, subprocess, sys, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade as G0
W = "/Volumes/Extreme/_edit_work/ro20"; FF = G0.FF; PM = G0.PM
SRC = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1511.MP4"; ROLL = "C1511"
OPT = {  # target skin Y90, mid, low (shadow depth, 1 = straight line), saturation, hue turn, pre (denoise), post
 # a steep per-channel curve alone pushed skin to hue 31 / saturation 0.58 (yellow-orange arms on the stills); saturation < 1 and
 # hue -6 bring it back to the camera's own skin hue 25 and RO-07 look D's saturation (0.53)
 "A": dict(t90=0.46, mid=0.97, low=0.90, sat=0.96, hue=-6, pre="hqdn3d=2.5:2:5:4,", name="Rich"),
 "F": dict(t90=0.52, mid=0.98, low=0.92, sat=0.94, hue=-6, pre="hqdn3d=2.5:2:5:4,", name="Between rich and bright"),
 "D": dict(t90=0.57, mid=0.98, low=0.95, sat=0.92, hue=-6, pre="hqdn3d=2.5:2:5:4,", name="Bright and natural (the RO-07 target Dan approved)"),
 "E": dict(t90=0.57, mid=0.96, low=0.82, sat=0.96, hue=-6, pre="hqdn3d=2.5:2:5:4,", post=",unsharp=lx=13:ly=13:la=0.45:cx=13:cy=13:ca=0", name="Bright, more contrast"),
}
def curve20(st, o):
    """This roll's blacks sit at 0.084 and the tank top at 0.10, so grade.py's fixed control at x=0.10 lands 0.016 from the black
    point and the spline rings (posterised, false colour: seen on the first stills). Controls here: black point, one shadow
    control HALFWAY to the skin median (o['low'] deepens it), skin median, skin Y90, the top."""
    k = o["t90"]/st["skinY90"]; bp = st["black"] - 0.006; ym = st["skinY"]*k*o["mid"]; xm = (bp + st["skinY"])/2
    pts = [(0, 0), (bp, 0.004), (xm, (0.004 + ym)/2*o["low"]), (st["skinY"], ym), (st["skinY90"], o["t90"])]
    top = min(0.985, st["p995"]+0.10); pts.append((top, min(0.975, o["t90"] + (top-st["skinY90"])*min(k, 1.6)*0.62))); pts.append((1, 1))
    pts = [(round(x, 4), round(min(max(y, 0), 1), 4)) for x, y in pts]
    assert all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(pts, pts[1:])), pts
    return ("curves=all='" + " ".join(f"{x}/{y}" for x, y in pts) + "'" + (f",eq=saturation={o['sat']}" if o["sat"] != 1 else "")
            + (f",hue=h={o['hue']}" if o.get("hue") else ""))
def masks():
    d = f"{W}/mask/{ROLL}_grade"; os.makedirs(d + "/m", exist_ok=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", SRC, "-vf", "fps=1/30,scale=960:540:in_color_matrix=bt709:in_range=tv", "-q:v", "3", f"{d}/f_%05d.jpg"], check=True)
    fs = sorted(glob.glob(f"{d}/f_*.jpg")); subprocess.run([PM, d + "/m"] + fs, check=True, capture_output=True)
    json.dump(dict(n=len(fs)), open(d + "/done", "w")); print(len(fs), "frames masked")
def tank():
    """black tank top RGB (person mask, dark, low saturation): is there a colour veil in the shadows?"""
    out = []
    for f in sorted(glob.glob(f"{W}/mask/{ROLL}_grade/f_*.jpg"))[::6]:
        mp = f.replace("/f_", "/m/f_").replace(".jpg", ".mask.png")
        if not os.path.exists(mp): continue
        im = np.asarray(Image.open(f).convert("RGB"), np.float32)/255; m = np.asarray(Image.open(mp).convert("L").resize((960, 540)), np.float32)/255 > 0.5
        y = im @ np.array([0.2126, 0.7152, 0.0722]); t = m & (y < 0.12) & (np.arange(540)[:, None] > 250)
        if t.sum() > 2000: out.append(np.median(im[t], 0))
    return np.median(out, 0)
if __name__ == "__main__":
    if sys.argv[1] == "masks": masks()
    else:
        G0.W = W; st = G0.roll_stats(ROLL + "_grade", 1); tk = tank(); print("stats", {k: round(v, 3) for k, v in st.items()}, "tank RGB", np.round(tk, 3))
        G = {ROLL: dict(stats=st, tank=[float(x) for x in tk])}
        for k, o in OPT.items(): G[ROLL][k] = o.get("pre", "") + curve20(st, o) + o.get("post", "")
        json.dump(G, open(f"{W}/grades.json", "w"), indent=1)
        for k in OPT: print(k, G[ROLL][k])
