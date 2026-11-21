"""Per-clip midtone lift for the Oct 23 gym library masters (Color C, measured darker than the bright pool presenter), the
DS-76 method: a curve that keeps the black point (no gamma-only lift, no crushed blacks), stepped until the clip's window
reaches median luma >= 55 with black share (<16) <= 20 %. Target range: DS-84/DS-76 approved gym cutaways (median 46-72,
black 7-22 %), upper half because the presenter is a sunny pool. Writes broll/grade.json {clip_id@start: vf}."""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"; W = "/Volumes/Expansion/_edit_work/RO-37/round1"; FF = f"{P}/Media/video_edit/bin/ffmpeg"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed"
def path(cid):
    import glob; return glob.glob(f"{LIB}/{cid}_*")[0]
def curve(k): return f"curves=all='0/0 0.12/{0.12+0.55*k:.3f} 0.35/{0.35+0.45*k:.3f} 0.7/{0.7+0.18*k:.3f} 1/1',eq=saturation={1+0.25*k:.3f}"
def stats(p, t0, d, vf):
    out = []
    for t in np.linspace(t0 + 0.2, t0 + max(0.4, min(d, 6)) - 0.2, 5):
        raw = subprocess.check_output([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1", "-vf",
              f"{vf+',' if vf else ''}scale=360:-2:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,format=gray", "-f", "rawvideo", "-"])
        out.append(np.frombuffer(raw, np.uint8))
    a = np.concatenate(out).astype(float) * 255 / 219 - 16 * 255 / 219
    return float(np.median(a)), float((a < 16).mean())
def tune(items):
    os.makedirs(f"{W}/broll", exist_ok=True); fp = f"{W}/broll/grade.json"
    res = json.load(open(fp)) if os.path.exists(fp) else {}
    for cid, t0, d in items:
        key = f"{cid}@{t0}"
        if key in res: continue
        p = path(cid); m0, b0 = stats(p, t0, d, ""); pick = (0.0, m0, b0)
        for k in np.arange(0.1, 1.01, 0.1):
            if pick[1] >= 55 and pick[2] <= 0.20: break
            m, b = stats(p, t0, d, curve(k)); pick = (round(float(k), 2), m, b)
        res[key] = dict(path=p, before=[round(m0, 1), round(b0, 3)], k=pick[0], after=[round(pick[1], 1), round(pick[2], 3)], vf=curve(pick[0]) if pick[0] else "")
        print(key, res[key]["before"], "->", res[key]["k"], res[key]["after"], flush=True)
        json.dump(res, open(fp, "w"), indent=1)
    return res
if __name__ == "__main__":
    items = [(a.split("@")[0], float(a.split("@")[1]), float(a.split("@")[2])) for a in sys.argv[1:]]
    tune(items)
