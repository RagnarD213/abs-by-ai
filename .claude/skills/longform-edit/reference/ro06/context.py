"""Moving context clips for the review page: an item with ~3 s of speech either side. usage: context.py ID..."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro06/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; OUT = f"{W}/round1/context"; os.makedirs(OUT, exist_ok=True)
end = Bd.S[-1]["out_f1"]/Bd.FPS
for i in sys.argv[1:]:
    it = next(r for r in Bd.R if r["id"] == i); a, b = max(0.0, it["t0"]-3.0), min(end, it["t1"]+3.0)
    out = f"{OUT}/{i}-context.mp4"; Bd.render_range(a, b, out)
    subprocess.run([Bd.FF, "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    f"{OUT}/{i}-context - REVIEW 540p.mp4"], check=True)
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4", ".untreated.wav"):
        try: os.remove(out + ext)
        except OSError: pass
    print("context", i, round(a, 1), round(b, 1), flush=True)
