"""RO-08 round 2 review media (folder round2/; nothing in round1/ is touched).
usage: round2.py first [O6] | context [names...]
first:   the first minute with the opener the plan carries (the time-lapse), or with the split screen opener in the same slot (O6). Voice 1a
         through the shared chain with the film's bed, 540p review copy, poster.
context: each AI clip moving in the film with 3 s of speech either side; voice sliced from the whole-film chain render (no bed in these)."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro08/recipe")
os.environ.setdefault("RO08_BED", "/Volumes/Extreme/_edit_work/ro08/bed/bed.wav"); os.environ.setdefault("RO08_BED_DB", "-30")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro08"; OUT = f"{W}/round2"; FF = Bd.FF; R = Bd.R; BY = {r["id"]: r for r in R}
FM = {"OT": f"{OUT}/first-minute/DRAFT - RO-08 round 2 - first minute - opener A time-lapse.mp4", "O6": f"{OUT}/first-minute/DRAFT - RO-08 round 2 - first minute - opener B split screen.mp4"}
CTX = {"A4": ["A4"], "A8": ["A8"], "A5": ["A5"], "A3-A1": ["C23", "A3", "A1"], "A2": ["C24", "A2"], "A6": ["A6"], "A7": ["C34", "A7"], "C21-no-C22": ["C21", "G22"]}
def review_copy(path, poster_t=1.5):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base + ".jpg"], check=True)
def first_end():
    lim = max([60.0] + [it["t1"] + 0.3 for it in R if it["t0"] < 60.0])
    return min(s["out_f0"] for s in Bd.S if s["out_f0"]/Bd.FPS >= lim)/Bd.FPS
def clean(out, more=()):
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4") + tuple(more):
        try: os.remove(out + ext)
        except OSError: pass
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "first":
        op = sys.argv[2] if len(sys.argv) > 2 else "OT"
        if op == "O6": BY["OT"]["src"] = [f"{OUT}/motion/O6-t2.mp4@0.0"]; BY["OT"]["chip_xy"] = (54, 1000)
        os.makedirs(os.path.dirname(FM[op]), exist_ok=True); e = first_end()
        Bd.render_range(0.0, e, FM[op]); review_copy(FM[op], 5.0); clean(FM[op]); print("first minute", op, "to", round(e, 2), flush=True)
    if what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True); end = Bd.S[-1]["out_f1"]/Bd.FPS; only = set(sys.argv[2:])
        for name, ids in CTX.items():
            if only and name not in only: continue
            out = f"{OUT}/context/{name}-context.mp4"
            if os.path.exists(out[:-4] + " - REVIEW 540p.mp4") and not only: continue
            a, b = max(0.0, min(BY[i]["t0"] for i in ids) - 3.0), min(end, max(BY[i]["t1"] for i in ids) + 3.0)
            Bd.render_range(a, b, out, audio="slice"); review_copy(out, 3.0 + 1.5); clean(out)
            os.replace(out, out[:-4] + " - 1080p.mp4"); print("context", name, round(a, 1), round(b, 1), flush=True)
