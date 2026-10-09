"""RO-07 round 1 media. usage: round1.py first | context [IDS] | budget
first: the finished first minute (ends on the first shot join at or after 60 s and after any item that started before it),
       540p review copy, poster, audio gate with the A/B clip. context: every item with 3 s of speech either side."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro07/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro07"; OUT = f"{W}/round1"; FF = Bd.FF
FM = f"{OUT}/first-minute/DRAFT - RO-07 round 1 - first minute.mp4"
def review_copy(path, poster_t=1.5):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base + ".jpg"], check=True)
def first_end():
    lim = max([60.0] + [it["t1"] + 0.3 for it in Bd.R if it["t0"] < 60.0])
    return min(s["out_f0"] for s in Bd.S if s["out_f0"]/Bd.FPS >= lim)/Bd.FPS
def clean(out):
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4"):
        try: os.remove(out + ext)
        except OSError: pass
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "first":
        os.makedirs(os.path.dirname(FM), exist_ok=True); e = first_end()
        Bd.render_range(0.0, e, FM); review_copy(FM, 5.0); clean(FM); print("first minute to", round(e, 2), flush=True)
    if what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True); end = Bd.S[-1]["out_f1"]/Bd.FPS; only = set(sys.argv[2:])
        for it in Bd.R:
            if only and it["id"] not in only: continue
            out = f"{OUT}/context/{it['id']}-context.mp4"
            if os.path.exists(out[:-4] + " - REVIEW 540p.mp4") and not only: continue
            a, b = max(0.0, it["t0"]-3.0), min(end, it["t1"]+3.0)
            Bd.render_range(a, b, out); review_copy(out, min(3.6, b-a-0.5)); clean(out)
            for ext in (".untreated.wav", ".build.json"):
                try: os.remove(out + ext)
                except OSError: pass
            os.remove(out); print("context", it["id"], round(a, 1), round(b, 1), flush=True)
