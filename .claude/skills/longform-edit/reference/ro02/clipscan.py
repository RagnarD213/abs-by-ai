"""Pre-check every cutaway's used range: source long enough, no fade from/to black at the edges, no internal scene cut."""
import json, subprocess, sys, re
sys.path.insert(0, "recipe"); import gfx as G
FF = G.FF if hasattr(G, "FF") else "ffmpeg"; FP = FF.replace("ffmpeg", "ffprobe"); FPS = 30000/1001
R = json.load(open("plan_resolved.json")); out = []
for it in R:
    if it["kind"] not in ("clip", "phone"): continue
    n = round(it["t1"]*FPS) - round(it["t0"]*FPS); per = n // len(it["src"])
    for k, sp in enumerate(it["src"]):
        m = per if k < len(it["src"]) - 1 else n - per*(len(it["src"]) - 1)
        path = G.src_path(sp); st = G.src_start(sp); d = m/FPS
        dur = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
        r = subprocess.run([FF, "-v", "info", "-ss", f"{st:.3f}", "-t", f"{d:.3f}", "-i", path, "-vf", "scale=320:180,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"], capture_output=True, text=True)
        ys = [float(x) for x in re.findall(r"YAVG=([\d.]+)", r.stdout)]
        r2 = subprocess.run([FF, "-v", "info", "-ss", f"{st:.3f}", "-t", f"{d:.3f}", "-i", path, "-vf", "scale=320:180,select='gt(scene,0.3)',metadata=print:file=-", "-f", "null", "-"], capture_output=True, text=True)
        sc = re.findall(r"pts_time:([\d.]+)", r2.stdout)
        row = dict(id=it["id"], src=path.split("/")[-1], start=st, need=round(d, 2), have=round(dur - st, 2), y_first=ys[:3], y_last=ys[-3:], y_med=sorted(ys)[len(ys)//2] if ys else None, scene_cuts=sc)
        out.append(row); print(row, flush=True)
json.dump(out, open("round3/logs/clipscan.json", "w"), indent=1)
