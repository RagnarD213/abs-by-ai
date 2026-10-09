"""RO-03 round-1 review media: the finished first minute, a moving context clip for every graphic outside it (3 s either
side), each with a 540p review copy and a poster. usage: media.py first | context [IDS...]"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro03"; OUT = f"{W}/round1"; FF = Bd.FF
FIRST = f"{OUT}/first-minute/DRAFT - RO-03 round 1 - first minute.mp4"
def review_copy(path):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base+" - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "1.5", "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base+".jpg"], check=True)
def first_end():
    lim = max([60.0]+[it["t1"]+0.3 for it in Bd.R if it["kind"] == "lt" and it["t0"] < 60.0])
    return min(s["out_f0"] for s in Bd.S if s["out_f0"]/Bd.FPS >= lim)/Bd.FPS
def contexts():
    MK = json.load(open(f"{W}/marks.json")); H, Bp = MK["holds"], MK["beeps"]; end = Bd.S[-1]["out_f1"]/Bd.FPS
    c = {it["id"]: (it["t0"]-3.0, it["t1"]+3.0) for it in Bd.R if it["kind"] == "lt"}
    c.update({"K00-rest1": (Bp[0]-4.0, Bp[0]+7.0), "K00-set2": (H[1]-8.5, H[1]+4.0), "K00-end": (Bp[2]-6.0, Bp[2]+6.0)})
    return {k: (max(0.0, a), min(end, b)) for k, (a, b) in c.items()}
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "first":
        os.makedirs(os.path.dirname(FIRST), exist_ok=True); e = first_end()
        Bd.render_range(0.0, e, FIRST); review_copy(FIRST); json.dump(dict(end=e), open(f"{OUT}/first-minute/end.json", "w")); print("first minute to", round(e, 2))
    elif what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True); only = set(sys.argv[2:]); e = json.load(open(f"{OUT}/first-minute/end.json"))["end"]
        for k, (a, b) in contexts().items():
            if (only and k not in only) or (not only and b <= e): continue      # already inside the first minute
            out = f"{OUT}/context/{k}-context.mp4"; Bd.render_range(a, b, out); review_copy(out); json.dump(dict(id=k, t0=a, t1=b), open(out+".t0.json", "w"))
