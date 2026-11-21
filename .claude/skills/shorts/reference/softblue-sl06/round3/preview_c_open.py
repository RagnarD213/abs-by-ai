#!/usr/bin/env python3
"""Card reasons: the clinical clip fills only as a square (a fill crop loses the thigh and shows only gown and glove); Karli Sine is a vertical video whose injection sits low in her frame, under our captions, with her own captions on her chest and her midriff above the thigh, so it is a card on the thigh and hands.
SL-06 R3 stage 1: short C's new opening as a playable preview (0 to 13 s): the AI flex intro as stills (no motion yet,
title band off), then the title band back with two real YouTube thigh injections (montage), then Karli Sine's pinch and
inject as a card, each with its credit chip lower right; captions are C's own caption images; audio is round 2's C.
Also writes each trimmed, colour-corrected clip to clips/ and the sources to clips/youtube_sources.json."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/sl06"); import batch as Bt, lib
from PIL import Image
R = "/Volumes/Extreme/_edit_work/sl06/round3"; FF = lib.FF; W, H, DROP = 1080, 1920, 310; FPS = 30000 / 1001
HD = R + "/yt/hd/"
CL = [  # id, file, in, out (file seconds), output a, b, fit, crop param, eq, credit, source
 dict(id="yt_nursescott", f="Pz49hyOla6s_nursescott.mp4", i=12.0, a=2.84, b=4.305, fx=0.49, eq="", credit="Video: Nurse Scott / YouTube",
      src=dict(url="https://www.youtube.com/watch?v=Pz49hyOla6s", channel="Nurse Scott", title="Painless Self Injection", t0="6:20.0", t1="6:21.5", what="syringe needle going into his own front thigh")),
 dict(id="yt_clinical", f="4v3kQNFLID8_clinical.mp4", i=4.6, a=4.305, b=5.77, card=(640, 0, 1080, 1080), y=330, z=1.0, eq="eq=gamma=1.35:brightness=0.02:saturation=1.05", credit="Video: Clinical Skills Training / YouTube",
      src=dict(url="https://www.youtube.com/watch?v=4v3kQNFLID8", channel="CLINICAL SKILLS TRAINING Medical Assistant Skills", title="Injection vastus lateralis intramuscular and subcutaneous", t0="0:42.6", t1="0:44.1", what="gloved hand puts an insulin syringe into the outer thigh")),
 dict(id="yt_karli", f="HcAsUbiFJyw_karli.mp4", i=14.6, a=5.77, b=9.56, card=(100, 1200, 900, 720), y=380, z=1.2, eq="eq=brightness=-0.03", credit="Video: Karli Sine / YouTube",
      src=dict(url="https://www.youtube.com/watch?v=HcAsUbiFJyw", channel="Karli Sine", title="Take my Semaglutide shot with me!", t0="2:28.6", t1="2:32.4", what="she pinches her front thigh and puts the insulin syringe in")),
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
