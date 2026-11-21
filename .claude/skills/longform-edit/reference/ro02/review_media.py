"""Round-1 review media: the finished first minute, and a moving context clip for every HyperFrames graphic (3 s of
speech either side), each with a 540p review copy and a poster. Then the verification: checks.py (clearance, face,
card fill) on every context clip, and base fidelity (PSNR of the render against its own graded base on frames with no
graphic) on the first minute.
usage: review_media.py first|context [IDS...]|verify"""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro02/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro02"; OUT = f"{W}/round2"; FF = Bd.FF
HFD = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes"
FIRST_END = None
def review_copy(path):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.5", "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base + ".jpg"], check=True)

def fidelity(render, base, t0):
    """PSNR of the render against its own graded base (the pre-graphics picture) on every frame no plan item touches,
    plus above y 740 on lower-third frames (the strip lives below): the untouched picture must survive the RGB
    compositing round trip (round 2: 43 dB or better)."""
    import numpy as np
    sys.path.insert(0, HFD); import composite as HC
    R = json.load(open(f"{W}/plan_resolved.json"))
    act = lambda g: [it for it in R if it["t1"] and Bd.fr(it["t0"]) <= g < Bd.fr(it["t1"])]
    clean, lt = [], []
    for i, (x, y) in enumerate(zip(HC.reader(render), HC.reader(base))):
        g = Bd.fr(t0) + i; a = act(g)
        if not a: rows = slice(0, 1080)
        elif all(it["kind"] == "lt" for it in a): rows = slice(0, 740)
        else: continue
        d = (x[rows].astype(np.float32) - y[rows].astype(np.float32)); mse = float((d * d).mean())
        (clean if not a else lt).append(99.0 if mse == 0 else 10 * np.log10(255 * 255 / mse))
    f = lambda v: dict(frames=len(v), min=round(min(v), 1), mean=round(sum(v) / len(v), 1)) if v else None
    return dict(untouched_frames=f(clean), above_lower_thirds=f(lt))

def first_end():
    """End the first minute on the first shot join at or after 60 s and after every graphic that started before 60 s."""
    R = json.load(open(f"{W}/plan_resolved.json"))
    lim = max([60.0] + [it["t1"] + 0.3 for it in R if it["t1"] and it["t0"] < 60.0])
    return min((s["out_f0"] for s in Bd.S if s["out_f0"] / Bd.FPS >= lim)) / Bd.FPS

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "first":
        os.makedirs(f"{OUT}/first-minute", exist_ok=True)
        e = first_end(); out = f"{OUT}/first-minute/DRAFT - RO-02 round 2 - first minute.mp4"
        Bd.render_range(0.0, e, out); review_copy(out); print("first minute to", round(e, 2))
        json.dump(dict(end=e), open(f"{OUT}/first-minute/end.json", "w"))
        fd = fidelity(out, out+".base.mp4", 0.0); json.dump(fd, open(f"{OUT}/first-minute/fidelity.json", "w")); print(json.dumps(fd))
    elif what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True)
        man = json.load(open(Bd.MANIFEST)); only = set(sys.argv[2:])
        man = man + [dict(id=it["id"], a=it["t0"], b=it["t1"]) for it in Bd.R if it["kind"] in ("anat", "count")]     # the two new moving kinds
        for m in man:
            if only and m["id"] not in only: continue
            a, b = max(0.0, m["a"] - 3.0), min(Bd.S[-1]["out_f1"] / Bd.FPS, m["b"] + 3.0)
            out = f"{OUT}/context/{m['id']}-context.mp4"
            Bd.render_range(a, b, out); review_copy(out)
            json.dump(dict(id=m["id"], t0=a), open(out + ".t0.json", "w"))
    elif what == "verify":
        res = {}
        man = json.load(open(Bd.MANIFEST))
        for m in man:
            out = f"{OUT}/context/{m['id']}-context.mp4"
            if not os.path.exists(out): continue
            t0 = json.load(open(out + ".t0.json"))["t0"]
            json.dump([m], open(f"{OUT}/checks/_m_{m['id']}.json", "w")) if os.path.isdir(f"{OUT}/checks") else (os.makedirs(f"{OUT}/checks"), json.dump([m], open(f"{OUT}/checks/_m_{m['id']}.json", "w")))
            r = subprocess.run(["python3", f"{HFD}/checks.py", f"{OUT}/checks/_m_{m['id']}.json", "--film", out, "--film-t0", str(t0),
                                "--out", f"{OUT}/checks/{m['id']}"], capture_output=True, text=True)
            res[m["id"]] = json.load(open(f"{OUT}/checks/{m['id']}/checks.json"))
            print(m["id"], r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:], flush=True)
        json.dump(res, open(f"{OUT}/checks/all.json", "w"), indent=1)
