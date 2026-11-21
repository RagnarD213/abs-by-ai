#!/usr/bin/env python3
"""RA-12 round 1: the hook and story clip cards, 9:16, each exactly its plan frame count -> round1/cards/<name>.mp4 + clips.json

  W1  A0151 (16:9) heavyset man doing slow crunches, "isn't a workout". He lies across the frame, so a full-screen window cuts him
      in half and a centre square loses his head or feet: the card keeps the full height and trims the sides to 1400 px (x 290).
  D1  A0069 (16:9) a man pushes away a plate of pizza, "and it's not a diet". Source 0.55-1.47 s only: the file cuts to a push-up
      shot at about 1.9 s. The plate, his raised hand and the salad need 1300 px (x 460, which also drops the clip's own burned
      AI chip at x 90-450).
  G1  his AI goal picture (dan by pool), Soft Blue photo scene, AI-GENERATED, "It's a picture." (softblue.scene_photo, as P1's result)
  K1  A0074 (9:16) a hand holds a phone with the AI goal picture on the lock screen, fills the frame, chip top left (RA-15's spot).
  Q1  A0172 (16:9) a worn-out beginner flat on a gym floor beside a tiny pink dumbbell, "when everyone else quits". Source 0.40 s
      on, before he rolls over to get up (2.5 s). He and the dumbbell span x 150-1830: 1680 px wide.
Every 16:9 card keeps the source's full height (VIDEO-RULES 2026-10-01); the width trim is the reason written above.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Expansion/_edit_work/ra12")
import ra01lib as L
SH = f"{L.REPO}/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes")
import softblue as SB
import composite as CP
import vertical as V

FPS = L.FPS; FPSS = "30000/1001"; W, H = 1080, 1920
PL = json.load(open("beats.json")); CB = {c["name"]: c for c in PL["cards"]}
P = json.load(open("clip_paths.json"))
GOAL = f"{L.REPO}/Media/example pictures/dan by pool.png"
OUT = "round1/cards"; PLT = os.path.abspath("round1/plates"); os.makedirs(OUT, exist_ok=True); os.makedirs("round1/media", exist_ok=True)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"

PLATES = {  # name -> (asset, source in, crop w, crop h, crop x)
    "W1": ("A0151", 0.90, 1400, 1080, 290),
    "D1": ("A0069", 0.55, 1300, 1080, 460),
    "Q1": ("A0172", 0.40, 1680, 1080, 150),
}


def media(name, path, t0, n, vf, wh):
    out = f"round1/media/{name}.mp4"
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{n / FPS + 0.3:.3f}", "-i", path,
                    "-vf", f"fps={FPSS},{vf},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1", "-frames:v", str(n)] + ENC + [out], check=True)
    return out


def frames(path, wh, n):
    p = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-i", path, "-vf", f"{D709},format=rgb24", "-frames:v", str(n),
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    sz = wh[0] * wh[1] * 3
    for k in range(n):
        b = p.stdout.read(sz); assert len(b) == sz, (path, k, n)
        yield np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3)
    p.stdout.close(); p.wait()


def writer(out):
    return subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-framerate", FPSS, "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + ENC + [out],
                            stdin=subprocess.PIPE)


meta = {}
only = set(sys.argv[1:]); want = lambda k: not only or k in only

for name, (asset, t0, cw, ch, cx) in PLATES.items():
    if not want(name): continue
    n = CB[name]["frames"]
    scene, hole = V.media_card_scene("P_" + name, n / FPS + 0.2, cw / ch, label="AI-GENERATED")
    V.build([scene], PLT, render=True, snap=1.0)
    x0, y0, x1, y1 = hole; wh = (x1 - x0, y1 - y0)
    m = media(name, P[asset], t0, n, f"crop={cw}:{ch}:{cx}:0", wh)
    e = writer(f"{OUT}/{name}.mp4")
    for f, ov in zip(frames(m, wh, n), CP.reader(f"{PLT}/renders/P_{name}.mov", 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes())
    e.stdin.close(); e.wait()
    meta[name] = dict(asset=asset, src=P[asset], src_in=t0, frames=n, crop=[cw, ch, cx, 0], hole=hole, chip=scene[1].get("chip"))
    print(name, n, "frames, hole", hole, "chip", scene[1].get("chip"), flush=True)

if want("K1"):
    # RA-12 re-review N3: A0074 animates the photo on its screen (he tilts his head and squints). K1 is now built in code: the goal
    # picture as the wallpaper of the approved iPhone shell (s63_stills.phone_card), a slow 4 % push over the shot, chip under the phone.
    import s63_stills as S63
    from PIL import ImageOps
    n = CB["K1"]["frames"]; e = writer(f"{OUT}/K1.mp4")
    # the visible screen = what is white in the shell around a pure red screen (the shell draws a white screen bigger than the content box);
    # the wallpaper fills all of it, edge to edge, like a lock screen; the island and status icons stay drawn on top
    red, _ = S63.phone_card(0.0, Image.new("RGB", (518, 982), (255, 0, 0)))
    ra = np.asarray(red).astype(int)
    scr = ((ra[..., 0] > 245) & (ra[..., 1] < 15) & (ra[..., 2] < 15)) | ((ra.min(2) > 240) & (np.arange(W)[None, :] > 240) & (np.arange(W)[None, :] < 840) & (np.arange(H)[:, None] > 100) & (np.arange(H)[:, None] < 1380))
    ys, xs = np.nonzero(scr); bx = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    wall_full = ImageOps.fit(Image.open(GOAL).convert("RGB"), (bx[2] - bx[0], bx[3] - bx[1]), Image.LANCZOS, centering=(0.5, 0.3))
    canvas = np.zeros((H, W, 3), np.uint8); canvas[bx[1]:bx[3], bx[0]:bx[2]] = np.asarray(wall_full)
    m3 = scr[..., None]
    print("K1 screen box", bx, flush=True)
    for i in range(n):
        im, box = S63.phone_card(CB["K1"]["beat"][0] + i / FPS, Image.new("RGB", (518, 982), (255, 0, 0)))
        im = Image.fromarray(np.where(m3, canvas, np.asarray(im.convert("RGB"))).astype(np.uint8))
        z = 1.0 + 0.04 * i / max(1, n - 1)
        if z > 1.0:
            cw, ch = W / z, H / z; x0, y0 = (W - cw) / 2, (H - ch) * 0.35
            im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
        im = im.convert("RGBA"); SB.disclosure(im, "AI-GENERATED", xy=(W // 2, 1580), anchor="mt")   # fixed, after the push
        e.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    e.stdin.close(); e.wait()
    meta["K1"] = dict(asset="goal on phone (code)", src=GOAL, frames=n, phone_box=box, push="4 %", chip="AI-GENERATED at (540, 1580), drawn after the push")
    print("K1", n, "frames (code-built phone wallpaper)", flush=True)

if want("G1"):
    n = CB["G1"]["frames"]; e = writer(f"{OUT}/G1.mp4")
    for i in range(n):
        im = SB.scene_photo(1.0 + 4 * i / FPS, W, H, GOAL, "AI-GENERATED").convert("RGB")   # review D4: 4x the push rate, visible over the 1.1 s shot
        e.stdin.write(np.asarray(im).tobytes())
    e.stdin.close(); e.wait()
    meta["G1"] = dict(asset="goal", src=GOAL, frames=n, chip="AI-GENERATED under the photo (softblue.scene_photo)")
    print("G1", n, "frames", flush=True)

old = json.load(open(f"{OUT}/clips.json")) if os.path.exists(f"{OUT}/clips.json") else {}
old.update(meta); json.dump(old, open(f"{OUT}/clips.json", "w"), indent=1, default=str)
print("CLIPS DONE", sorted(meta))
