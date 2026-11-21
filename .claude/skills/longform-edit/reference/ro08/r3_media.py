"""RO-08 round 3 review media (folder round3/; nothing in round2/ is touched).
usage: r3_media.py context [names...]
context: each of the three changed spots moving in the film with speech either side; voice sliced from the whole-film chain render (no bed in these).
  A4-out: 1:50 to 2:08, the AI clip is gone and the middle shot of the take is the camera frame (the one named framing change)
  A5:     the new two-shot donut clip with 3 s either side
  A3-out: the pancake stock clip, Dan on camera where the AI clip was, then A1"""
import sys, os, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro08/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro08"; OUT = f"{W}/round3"; FF = Bd.FF; BY = {r["id"]: r for r in Bd.R}
CTX = {"A4-out": (110.35, 127.42), "A5": (BY["A5"]["t0"] - 3.0, BY["A5"]["t1"] + 3.0), "A3-out": (BY["C23"]["t0"] - 3.0, BY["A1"]["t1"] + 3.0)}
def review_copy(path, poster_t):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base + ".jpg"], check=True)
if __name__ == "__main__" and sys.argv[1] == "context":
    os.makedirs(f"{OUT}/context", exist_ok=True); only = set(sys.argv[2:])
    for name, (a, b) in CTX.items():
        if only and name not in only: continue
        out = f"{OUT}/context/{name}-context.mp4"
        Bd.render_range(a, b, out, audio="slice"); review_copy(out, 4.5)
        for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4"):
            try: os.remove(out + ext)
            except OSError: pass
        os.replace(out, out[:-4] + " - 1080p.mp4"); print("context", name, round(a, 2), round(b, 2), flush=True)
def one(name, a, b):
    out = f"{OUT}/context/{name}-context.mp4"; Bd.render_range(a, b, out, audio="slice"); review_copy(out, 4.5)
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4"):
        try: os.remove(out + ext)
        except OSError: pass
    os.replace(out, out[:-4] + " - 1080p.mp4"); print("context", name, round(a, 2), round(b, 2), flush=True)
if __name__ == "__main__" and sys.argv[1] == "alts":
    # the two clips Dan did not name that the three questions caught: each as the film now has it (cut down to the part that works) and as it
    # was in the round 2 film, so he can overrule either change in one look
    os.makedirs(f"{OUT}/context", exist_ok=True); FPS = Bd.FPS; MO2 = f"{W}/round2/motion"
    a6 = (BY["A6"]["t0"] - 3.0, 736.37 + 3.0); a8 = (295.131 - 3.0, BY["A8"]["t1"] + 3.0)
    one("A6-now", *a6); one("A8-now", *a8)
    BY["A6"]["t1"] = 736.3701; Bd._SEGS = None; print("A6 as in round 2: jumps", Bd.jumps(), flush=True); one("A6-round2", *a6)
    BY["A8"]["src"] = [f"{MO2}/A8-t1.mp4@0.0"]; BY["A8"]["t0"] = 295.131; BY["A8"].pop("subcuts", None); Bd._SEGS = None; print("A8 as in round 2: jumps", Bd.jumps(), flush=True); one("A8-round2", *a8)
