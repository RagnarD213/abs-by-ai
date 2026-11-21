"""Every clip source against its RESOLVED slot (resolve.py snaps clip edges to shot joins after resolve_part.py checked the
part, so a slot can grow past its source): prints each clip that is too short, with the largest start offset that fits."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx as G
FPS = 30000/1001; FP = G.FF.replace("ffmpeg", "ffprobe"); bad = 0
def fr(t): return int(round(t*FPS))
for it in json.load(open("/Volumes/Extreme/_edit_work/ro20/plan_resolved.json")):
    if it["kind"] != "clip" or it.get("frames"): continue
    n = fr(it["t1"]) - fr(it["t0"]); s = it["src"]; per = n // len(s)
    for k, sp in enumerate(s):
        m = per if k < len(s)-1 else n - per*(len(s)-1)
        dur = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", G.src_path(sp)], capture_output=True, text=True).stdout or 0)
        if dur - G.src_start(sp) < m/FPS + 0.15:      # 0.15 s spare: a source that ends within a frame or two of its slot gives a short read (Cd30)
            bad += 1; print(f"{it['id']} src {k+1}/{len(s)} {os.path.basename(G.src_path(sp))[:44]}: has {dur-G.src_start(sp):.2f}s from {G.src_start(sp)}, slot {m/FPS:.2f}s; fits from <= {dur-m/FPS:.2f}")
print("too short:", bad)
