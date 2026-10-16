#!/usr/bin/env python3
"""RA-07 round 4 (from round 3's s86r3_assemble.py): the WHOLE 9:16 with G1 (gym closed) and O1 (leg press out of order) as labelled
placeholders from their START frames (their frames are on the round 4 page for Dan's yes; motion only after it).

  python3 s86r4_assemble.py work   -> round4/work/picture_9x16.mp4  (the working composite, 1579 frames)
  python3 s86r4_assemble.py cuts   -> round4/DRAFT - RA-07 round 4 - full film.mp4 (+ REVIEW 540p), round4/run - REVIEW 540p.mp4 (33-50 s),
                                      round4/context/<ID>-context - REVIEW 540p.mp4 + .jpg (about 3 s of speech either side), round4/stills/<ID>.jpg

Picture per film frame, in plan order: danNN = round4/seg/danNN.mp4 (every hold reused frame-for-frame from rounds 2 and 3: same plan time,
frame count, level and crop); H1 = round2/clips; A1 M1 H2 I5 = round4/clips; P1 K1 W1 = round2/cards; G1 O1 = placeholder.
Then hyperframes/composite.py's Compositor lays the lower thirds and the button, then the caption states (cap_9x16/captions.mov, unchanged).
Audio: round3/mix_bass_r3.wav (the approved voice with the bass lift and round 3's smoothed music tail).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/hyperframes")
import composite as CP
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB

FPS = L.FPS; W, H = 1080, 1920
PL = json.load(open(os.environ.get("PLAN", "beats_r4.json")))
MAN = json.load(open("round2/gfx/manifest.json"))
WORK = os.environ.get("WORK", "round4/work"); os.makedirs(WORK, exist_ok=True)
PIC = f"{WORK}/picture_9x16.mp4"
WAV = os.environ.get("WAV", "round3/mix_bass_r3.wav")
CAPS = "cap_9x16/captions.mov"
SRC = {k: f"round2/clips/{k}.mp4" for k in ("H1",)}
SRC.update({k: f"round4/clips/{k}.mp4" for k in ("A1", "M1", "H2", "I5")})
SRC.update({k: f"round2/cards/{k}.mp4" for k in ("P1", "K1", "W1")})
PENDING = {"G1", "O1"}
PLACE = {"G1": ("round4/frames/GC-start_v2.png", "Gym closed"), "O1": ("round4/frames/LP-start_v1.png", "Leg press out of order")}
END30 = next(it["f0"] for it in PL["timeline"] if it["kind"] == "dan" and it["a"] > 30.0)     # "you'll get far better results"
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
TITLE = "DRAFT - RA-07 round 4 - full film"


def placeholder(cid):
    fn, label = PLACE[cid]
    im = Image.open(fn).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 760, W, 1000), fill=(10, 20, 34, 225))
    d.text((W // 2, 800), "PLACEHOLDER", font=SB.font(64), fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 890), f"{label}: frames on this page; motion next round", font=SB.font(34, False), fill=(200, 225, 255), anchor="mt")
    return np.asarray(im.convert("RGB"))


def work():
    C = CP.Compositor(MAN, wh=(W, H))
    caps = CP.reader(CAPS, rgba=True, wh=(W, H))
    enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-r", "30000/1001"] + X264 + [PIC], stdin=subprocess.PIPE)
    g = 0; log = []
    for it in PL["timeline"]:
        name = it["name"]
        if name in PENDING:
            ph = placeholder(name); rd = None; src = "placeholder"
        else:
            src = SRC.get(name, f"{os.environ.get('SEG', 'round4/seg')}/{name}.mp4"); rd = CP.reader(src, wh=(W, H))
        for k in range(it["n"]):
            base = ph if rd is None else next(rd)
            fr = C.apply(base, g)
            fr = CP.over(np.ascontiguousarray(fr), next(caps))
            enc.stdin.write(np.ascontiguousarray(fr).tobytes()); g += 1
        if rd is not None:
            left = next(rd, None)
            assert left is None, f"{name}: segment longer than its slot"
            rd.close()
        log.append((name, it["f0"], it["f1"], src))
    enc.stdin.close(); enc.wait()
    assert g == PL["total_frames"], (g, PL["total_frames"])
    json.dump(dict(frames=g, timeline=log, manifest=MAN, captions=CAPS, pending=sorted(PENDING)),
              open(f"{WORK}/picture_9x16.json", "w"), indent=1)
    print("wrote", PIC, g, "frames")


def cut(out, f0, f1, review=True, fade=True):
    t0, d = f0 / FPS, (f1 - f0) / FPS
    af = f"atrim=start={t0:.5f}:duration={d:.5f},asetpts=PTS-STARTPTS"
    if fade: af += f",afade=t=in:d=0.04,afade=t=out:st={max(0, d - 0.12):.4f}:d=0.12"
    vf = f"trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS" + (",scale=540:960:flags=lanczos" if review else "")
    enc = [x if x != "14" else ("22" if review else "16") for x in X264]
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", PIC, "-i", WAV, "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]",
                    "-map", "[v]", "-map", "[a]"] + enc + ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)


def grab(t, out):
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.4f}", "-i", PIC, "-frames:v", "1",
                    "-vf", "scale=in_color_matrix=bt709:in_range=tv", "-q:v", "3", out], check=True)


def cuts():
    os.makedirs("round4/context", exist_ok=True); os.makedirs("round4/stills", exist_ok=True)
    T = f"round4/{TITLE}"
    tot = PL["total_frames"]
    cut(T + ".mp4", 0, tot, review=False, fade=False)
    cut(T + " - REVIEW 540p.mp4", 0, tot, review=True, fade=False)
    cut("round4/run - REVIEW 540p.mp4", int(round(33.0 * FPS)), int(round(50.0 * FPS)), review=True, fade=True)
    items = {c["name"]: tuple(c["beat"]) for c in PL["cards"]}
    for g in PL["overlays"]: items[g["id"]] = (g["t0"], g["t1"])
    meta = {}
    for k, (a, b) in sorted(items.items(), key=lambda x: x[1][0]):
        f0 = max(0, int(round((a - 3.0) * FPS))); f1 = min(tot, int(round((b + 3.0) * FPS)))
        out = f"round4/context/{k}-context - REVIEW 540p.mp4"
        cut(out, f0, f1, review=True, fade=f0 > 0)
        settle = a + min(b - a - 0.4, max(0.8, (b - a) * 0.75))
        grab(settle, f"round4/stills/{k}.jpg")
        Image.open(f"round4/stills/{k}.jpg").resize((540, 960)).save(f"round4/context/{k}-context - REVIEW 540p.jpg", quality=88)
        meta[k] = dict(a=round(a, 3), b=round(b, 3), clip=out, clip_in=round(f0 / FPS, 3), clip_out=round(f1 / FPS, 3),
                       still=f"round4/stills/{k}.jpg", still_t=round(settle, 3))
        print("context", k, f"{f0/FPS:.2f}-{f1/FPS:.2f}", flush=True)
    json.dump(dict(full=dict(file=T + ".mp4", frames=tot, dur=round(tot / FPS, 3)), items=meta), open("round4/cuts.json", "w"), indent=1)


if __name__ == "__main__":
    {"work": work, "cuts": cuts}[sys.argv[1]]()
