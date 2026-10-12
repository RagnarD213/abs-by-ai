"""Round 2 context clips: a film range with the same treated voice the film carries. usage: context2.py NAME T0 T1 [--bare] ...
--bare = presenter only, no graphics or clips (the on-camera opening option for video 2)."""
import sys, os, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/recipe")
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro20"; OUT = f"{W}/round3/context"; os.makedirs(OUT, exist_ok=True)
a = sys.argv[1:]; jobs = []
while a:
    n, t0, t1 = a[0], float(a[1]), float(a[2]); a = a[3:]; bare = bool(a and a[0] == "--bare")
    if bare: a = a[1:]
    jobs.append((n, t0, t1, bare))
R0 = Bd.R; M0 = Bd.MANIFEST
for n, t0, t1, bare in jobs:
    out = f"{OUT}/{n}-context.mp4"; Bd.R = [] if bare else R0      # the framing solve is already cached from the full plan
    if bare: open(f"{OUT}/_empty_manifest.json", "w").write("[]"); Bd.MANIFEST = f"{OUT}/_empty_manifest.json"     # lower thirds come from the manifest, not the plan
    else: Bd.MANIFEST = M0
    Bd.all_segments(); Bd.render_range(t0, t1, out, audio="slice")
    subprocess.run([Bd.FF, "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{OUT}/{n}-context - REVIEW 540p.mp4"], check=True)
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4"):
        try: os.remove(out + ext)
        except OSError: pass
    print("context", n, t0, t1, flush=True)
