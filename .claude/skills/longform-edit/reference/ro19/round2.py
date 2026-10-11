"""RO-19 round 2 media (Dan's round 1 notes, 2026-10-11). usage: round2.py first | context IDS... | stills
first: the first minute again (opens on the camera's wide frame, look F, voice W4 from audio/opts2), 540p review copy, poster.
context: the named items with 3 s of speech either side (voice = a slice of voice/film_voice_r2.wav, build.py filmvoice).
stills: one frame of each round 2 photo scene. Builds in round2/ only; round1/ is never touched."""
import sys, os, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro19/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro19"; OUT = f"{W}/round2"; FF = Bd.FF
FM = f"{OUT}/first-minute/DRAFT - RO-19 round 2 - first minute.mp4"
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
        Bd.render_range(0.0, e, FM); review_copy(FM, 1.5); clean(FM); print("first minute to", round(e, 2), flush=True)
    if what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True); end = Bd.S[-1]["out_f1"]/Bd.FPS
        for i in sys.argv[2:]:
            it = next(r for r in Bd.R if r["id"] == i); out = f"{OUT}/context/{i}-context.mp4"
            a, b = max(0.0, it["t0"]-3.0), min(end, it["t1"]+3.0)
            Bd.render_range(a, b, out, audio="slice"); review_copy(out, min(it["t0"]-a+1.2, b-a-0.5)); clean(out)
            os.remove(out); print("context", i, round(a, 1), round(b, 1), flush=True)
    if what == "stills":
        os.makedirs(f"{OUT}/stills", exist_ok=True)
        for i in ("P02", "P03", "P04", "P05"):
            subprocess.run([FF, "-v", "error", "-y", "-ss", "4.0", "-i", f"{W}/gfx/r2/{i}.mp4", "-frames:v", "1", "-q:v", "2", f"{OUT}/stills/{i}.jpg"], check=True)
