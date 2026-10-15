#!/usr/bin/env python3
"""RA-15 round 3: the Soft Blue HyperFrames analysis card (Dan, 2026-10-14: the standard in every video; built for RA-14 round 3)
replaces round 1/2's recoloured adkit card, in both shapes. -> cards_9x16/analysis.mp4, cards_16x9/analysis.mp4 (+ analysis_hf.json).
Words under it: "and it measures(21.21) the exact gap(22.09) between where you are now and where(23.95) you want(24.39) to be."
Picture: media/after_man.png, the B0049 man's own AI result (the same man as the flow card before it), AI-GENERATED."""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
HF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes"
sys.path.insert(0, HF)
import vertical as V9
import composite as CP
import hv16
B = json.load(open("beats.json")); by = {c["name"]: c for c in B["cards"]}
c0 = by["analysis"]; n = c0["frames"]; dur = n * 1001 / 30000
cfg = dict(id="A1", a=0.0, b=round(dur, 4), photo=os.path.abspath("media/after_man.png"), label="AI-GENERATED",
           reveal=[round(t - c0["beat"][0], 3) for t in (21.21, 22.09, 23.95)], band=["YOUR NUTRITION PLAN", round(24.39 - c0["beat"][0], 3)])   # a nutrition ad (review, round 3)
FF = V9.B.FF; ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30000/1001", "-colorspace", "bt709",
                     "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
out = {}
for key, mod, wh in (("9x16", V9, (1080, 1920)), ("16x9", hv16.V, (1920, 1080))):
    sc, meta = mod.analysis_scenes(dict(cfg, id=f"A1_{key}"))
    od = f"hf_analysis_{key}"; movs = mod.build(sc, od, render=True, snap=dur - 0.4)
    mov = str(list(movs.values())[0])
    C = CP.Compositor([dict(id="A1", a=0.0, b=dur, mov=mov, **meta)], wh=wh)
    os.makedirs(f"cards_{key}", exist_ok=True)
    e = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{wh[0]}x{wh[1]}", "-framerate", "30000/1001",
                          "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + ENC + [f"cards_{key}/analysis.mp4"], stdin=subprocess.PIPE)
    z = np.zeros((wh[1], wh[0], 3), np.uint8)
    for g in range(n):
        assert C.opaque(g), g
        e.stdin.write(np.ascontiguousarray(C.apply(z, g)).tobytes())
    e.stdin.close(); assert e.wait() == 0
    out[key] = dict(mov=mov, meta={k: v for k, v in meta.items()}, frames=n, cfg=cfg)
    print(key, n, "frames", meta, flush=True)
json.dump(out, open("round3/analysis_hf.json", "w"), indent=1)
print("ANALYSIS_DONE")
