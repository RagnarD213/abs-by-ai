#!/usr/bin/env python3
"""SL-06 R4 stage 1: short C's new opening as a playable preview (0 to 13 s): the AI flex intro as stills (no motion yet,
title band off), then the title band back with the Seattle Children's front-thigh self-injection (Dan's R4 pick for the opening),
then SynergenX's pinch and inject, both filling the frame, each with its credit chip lower right; captions are C's own
caption images; audio is round 2's C. Also writes each trimmed, colour-corrected clip to clips/ and clips/youtube_sources.json."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl06"); import batch as Bt, lib
from PIL import Image
R = "/Volumes/Extreme/_edit_work/sl06/round3"; FF = lib.FF; W, H, DROP = 1080, 1920, 310; FPS = 30000 / 1001
HD = R + "/yt/hd/"
CL = [  # id, file, in (file seconds), output a, b, fill crop position fx, eq, credit, source
 dict(id="yt_seattle", f="7TP0rTlQVao_seattle.mp4", i=4.5, a=2.84, b=5.77, fx=0.53, eq="eq=gamma=1.08", credit="Video: Seattle Children's / YouTube",
      src=dict(url="https://www.youtube.com/watch?v=7TP0rTlQVao", channel="Seattle Children's", title="Giving Yourself Subcutaneous Hormone Shots", t0="6:59.5", t1="7:02.4", what="a man pinches the front of his own thigh and puts an insulin syringe in")),
 dict(id="yt_synergenx", f="FeweDb3Xfxg_synergenx.mp4", i=5.5, a=5.77, b=9.56, fx=0.45, eq="eq=saturation=0.85:brightness=-0.02", credit="Video: SynergenX / YouTube",
      src=dict(url="https://www.youtube.com/watch?v=FeweDb3Xfxg", channel="SynergenX - Testosterone & Weight Loss", title="How to Self Inject Testosterone in the Thigh", t0="1:39.5", t1="1:43.3", what="he pinches the front of his mid thigh and puts the insulin syringe in")),
]
def frames(path, vf, w, h, t0, n):
    p = subprocess.run([FF, "-v", "error", "-ss", f"{t0:.3f}", "-i", path, "-frames:v", str(n), "-vf", f"fps={FPS},{vf},format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, h, w, 3)
for c in CL:
    n = round((c["b"] - c["a"]) * FPS) + 1
    if "card" in c:
        x, y, w, h = c["card"]; w2, h2 = round(w * c["z"]), round(h * c["z"]); vf = f"crop={w}:{h}:{x}:{y},scale={w2}:{h2}:flags=lanczos" + ("," + c["eq"] if c["eq"] else ""); c["box"] = (0, c["y"], w2, h2); w, h = w2, h2
    else:
        w, h = W, H - DROP; vf = (f"scale=-2:{h}:flags=lanczos,crop={w}:{h}:(iw-{w})*{c['fx']}:0" + ("," + c["eq"] if c["eq"] else "")); c["box"] = (0, DROP, w, h)
    c["fr"] = frames(HD + c["f"], vf, w, h, c["i"], n)
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{c['i']:.3f}", "-t", f"{c['b'] - c['a']:.3f}", "-i", HD + c["f"], "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f"{R}/clips/{c['id']}.mp4"], check=True)
    c["chip"] = Bt.chip_png(c["credit"], (0, 0), size=20, u=1.5)
json.dump([dict(id=c["id"], file=f"clips/{c['id']}.mp4", output_s=[c["a"], c["b"]], credit=c["credit"], eq=c["eq"], **c["src"]) for c in CL], open(f"{R}/clips/youtube_sources.json", "w"), indent=1)
# field + band background for the card (the film's Soft Blue canvas)
bg = lib.canvas(0); lib.band(bg, "GLP-1 Tips", ["How To Inject", "In 10 Seconds"]); bg = np.asarray(bg.convert("RGB"))
cues = json.load(open("/Volumes/Extreme/_edit_work/sl06/build/C/cues.json"))
caps = [(q["a"], q["b"], np.asarray(Image.open(f"/Volumes/Extreme/_edit_work/sl06/build/C/cap/cue{k:03d}.png"))) for k, q in enumerate(cues) if q["a"] < 10]
st = np.asarray(Image.open(f"{R}/preview/C_start_chip.png").convert("RGB")); en = np.asarray(Image.open(f"{R}/preview/C_end_chip.png").convert("RGB"))
T = 13.0; N = round(T * FPS); base = frames(f"{R}/../round2/media/C - 1080x1920.mp4", "null", W, H, 0, N)
def over(fr, rgba, x, y):
    h, w = rgba.shape[:2]; a = rgba[..., 3:4].astype(np.float32) / 255; reg = fr[y:y + h, x:x + w].astype(np.float32)
    fr[y:y + h, x:x + w] = (reg * (1 - a) + rgba[..., :3].astype(np.float32) * a + .5).astype(np.uint8)
out = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-ss", "0", "-t", f"{T}", "-i", f"{R}/../round2/media/C - 1080x1920.mp4",
                        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", f"{R}/preview/C_open_context.mp4"], stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS; fr = base[i].copy()
    if t < 2.84: fr = (st if t < 1.42 else en).copy()
    else:
        for c in CL:
            if c["a"] <= t < c["b"]:
                if "card" in c: fr[:1796] = bg[:1796]
                x, y, w, h = c["box"]; k = min(int((t - c["a"]) * FPS), len(c["fr"]) - 1); hh = min(h, 1796 - y); fr[y:y + hh, x:x + w] = c["fr"][k][:hh]
                rgba, bb = c["chip"]; chip = rgba[bb[1]:bb[3], bb[0]:bb[2]]; over(fr, chip, W - 34 - chip.shape[1], 1716)
        if t < 9.56:
            for a, b, im in caps:
                if a <= t < b: over(fr, im, 0, 0)
    out.stdin.write(fr.tobytes())
out.stdin.close(); out.wait(); print("ok", N)
