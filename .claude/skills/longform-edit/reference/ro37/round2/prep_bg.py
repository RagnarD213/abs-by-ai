"""RO-37 round 2 background media: (1) every gym clip the plan puts behind Dan, graded with round 1's tune method (the
library's Color C master + a black-keeping midtone lift to median >= 55, VIDEO-RULES: all B-roll colour corrected) and
scaled to 1920x1080 once, so the compositor reads plain 1080p files; (2) 40 graded stills from different October 23 gym
clips for the cards and the photo wall (machines and cables first; nothing with a barbell or dumbbell).
  python3 prep_bg.py clips | photos"""
import glob, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
import numpy as np
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed"
GJ = f"{r2.W2}/bgclips/grade.json"
def path(cid): return glob.glob(f"{LIB}/{cid}_*")[0]
def curve(k): return f"curves=all='0/0 0.12/{0.12+0.55*k:.3f} 0.35/{0.35+0.45*k:.3f} 0.7/{0.7+0.18*k:.3f} 1/1',eq=saturation={1+0.25*k:.3f}"


def stats(p, t0, d, vf):
    out = []
    for t in np.linspace(t0 + 0.2, t0 + max(0.4, min(d, 6)) - 0.2, 5):
        raw = subprocess.check_output([r2.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-vf",
              f"{vf+',' if vf else ''}scale=360:-2:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,format=gray", "-f", "rawvideo", "-"])
        out.append(np.frombuffer(raw, np.uint8))
    a = np.concatenate(out).astype(float) * 255 / 219 - 16 * 255 / 219
    return float(np.median(a)), float((a < 16).mean())


def tune(cid, t0, d):
    """round 1's broll_tune, same curve and target; round 1's own values are reused where it already tuned the clip."""
    res = json.load(open(GJ)) if os.path.exists(GJ) else {}
    if cid in res: return res[cid]["vf"]
    r1 = json.load(open(f"{r2.R1}/broll/grade.json"))
    old = next((v for k, v in r1.items() if k.split("@")[0] == cid), None)
    if old: res[cid] = dict(old, source="round 1 tune")
    else:
        p = path(cid); m0, b0 = stats(p, t0, d, ""); pick = (0.0, m0, b0)
        for k in np.arange(0.1, 1.01, 0.1):
            if pick[1] >= 55 and pick[2] <= 0.20: break
            m, b = stats(p, t0, d, curve(k)); pick = (round(float(k), 2), m, b)
        res[cid] = dict(path=p, before=[round(m0, 1), round(b0, 3)], k=pick[0], after=[round(pick[1], 1), round(pick[2], 3)], vf=curve(pick[0]) if pick[0] else "")
    json.dump(res, open(GJ, "w"), indent=1); print(cid, res[cid].get("before"), "->", res[cid].get("k"), res[cid].get("after"), flush=True)
    return res[cid]["vf"]


def clips():
    plan = json.load(open(f"{r2.W2}/bg_plan.json"))["segments"]
    ids = sorted({s["clip"]["id"] for s in plan if s.get("clip")})
    D = json.load(open(f"{r2.W2}/bgclips/index.json"))
    for cid in ids:
        out = f"{r2.W2}/bgclips/{cid}.mp4"
        if os.path.exists(out): continue
        vf = tune(cid, max(0.0, D[cid] / 2 - 3), 6.0)
        subprocess.run([r2.FF, "-nostdin", "-v", "error", "-y", "-i", path(cid), "-an", "-vf",
                        f"{r2.F.DEC},{vf + ',' if vf else ''}scale=1920:1080:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-crf", "15",
                        "-preset", "fast", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", "30000/1001",
                        out + ".tmp.mp4"], check=True)
        os.rename(out + ".tmp.mp4", out); print("bg clip", cid, flush=True)


PHOTO_CLIPS = ["B0566", "B0620", "B0678", "B0648", "B0688", "B0682", "B0574", "B0624", "B0665", "B0673", "B0723", "B0631",
               "B0626", "B0651", "B0655", "B0669", "B0637", "B0579", "B0611", "B0720", "B0699", "B0567", "B0622", "B0630",
               "B0604", "B0612", "B0629", "B0632", "B0649", "B0654", "B0656", "B0662", "B0666", "B0668", "B0670", "B0674",
               "B0679", "B0689", "B0694", "B0702"]


def photos():
    os.makedirs(f"{r2.W2}/photos", exist_ok=True); names = []
    for n, cid in enumerate(PHOTO_CLIPS):
        p = path(cid); d = float(subprocess.check_output([r2.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
        t = d * 0.45; vf = tune(cid, max(0.0, t - 2), 4.0)
        out = f"{r2.W2}/photos/g{n:02d}.jpg"
        if not os.path.exists(out):
            subprocess.run([r2.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf",
                            f"{r2.F.DEC},{vf + ',' if vf else ''}scale=1920:1080:flags=lanczos", "-q:v", "2", out], check=True)
        names.append(os.path.basename(out))
    json.dump(names, open(f"{r2.W2}/photos/index.json", "w"), indent=1)
    json.dump(dict(zip(names, PHOTO_CLIPS)), open(f"{r2.W2}/photos/source.json", "w"), indent=1)
    print(len(names), "stills")


if __name__ == "__main__":
    {"clips": clips, "photos": photos}[sys.argv[1]]()
