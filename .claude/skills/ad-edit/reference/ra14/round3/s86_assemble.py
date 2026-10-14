#!/usr/bin/env python3
"""RA-14 round 3: lay the picture, the HyperFrames graphics and the captions together, then cut what Dan reviews.

  python3 s86_assemble.py work      -> round3/work/picture_9x16.mp4  (the working composite, never shown whole: graphics and
                                       clips are not all approved, PRE-RENDER-APPROVAL "Forbidden")
  python3 s86_assemble.py cuts      -> round3/DRAFT - RA-14 round 3 - first 30 seconds.mp4 (+ REVIEW 540p)
                                       round3/context/<ID>-context - REVIEW 540p.mp4 + .jpg   (about 3 s of speech either side)
                                       round3/stills/<ID>.jpg                                  (each item settled, on its frame)

Picture per film frame g, in plan order: O0 = round3/opener/O2.mp4, danNN = round3/seg/danNN.mp4, P1 / T1 = round3/cards,
A1 = the HyperFrames analysis card (opaque). Then hyperframes/composite.py's Compositor lays the lower thirds (glass), the
recap card and the CTA in RGB, each file decoded by its own matrix, then the caption states (round3/cap_9x16/captions.mov).
Audio: mix_bass_r3.wav (Dan's pick, frame-locked to 1512 frames).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared/hyperframes")
import composite as CP

FPS = L.FPS; W, H = 1080, 1920
PL = json.load(open("beats_r3.json"))
MAN = json.load(open("round3/gfx/manifest.json"))
WORK = "round3/work"; os.makedirs(WORK, exist_ok=True)
PIC = f"{WORK}/picture_9x16.mp4"
WAV = "mix_bass_r3.wav"
SRC = {"O0": "round3/opener/O2.mp4", "P1": "round3/cards/P1.mp4", "T1": "round3/cards/T1.mp4"}
END30 = next(it["f0"] for it in PL["timeline"] if it["kind"] == "dan" and it["a"] > 30.0)   # "Step three" starts: 30.30 s
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]


def work():
    C = CP.Compositor(MAN, wh=(W, H))
    caps = CP.reader("round3/cap_9x16/captions.mov", rgba=True, wh=(W, H))
    enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-r", "30000/1001"] + X264 + [PIC], stdin=subprocess.PIPE)
    g = 0; log = []
    for it in PL["timeline"]:
        name = it["name"]
        if name == "A1":
            src = None
        else:
            src = SRC.get(name, f"round3/seg/{name}.mp4")
            rd = CP.reader(src, wh=(W, H))
        for k in range(it["n"]):
            base = None if src is None else next(rd)
            if base is None and not C.opaque(g): raise SystemExit(f"{name}: no picture at film frame {g}")
            fr = C.apply(base if base is not None else np.zeros((H, W, 3), np.uint8), g)
            fr = CP.over(np.ascontiguousarray(fr), next(caps))
            enc.stdin.write(np.ascontiguousarray(fr).tobytes()); g += 1
        if src is not None:
            assert next(rd, None) is None or name in SRC, f"{name}: segment longer than its slot"
            rd.close()
        log.append((name, it["f0"], it["f1"], src))
    enc.stdin.close(); enc.wait()
    assert g == PL["total_frames"], (g, PL["total_frames"])
    json.dump(dict(frames=g, timeline=log, manifest=MAN, captions="round3/cap_9x16/captions.mov"), open(f"{WORK}/picture_9x16.json", "w"), indent=1)
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


ITEMS = {   # id -> (in, out, settled moment) film seconds, from the plan
    "O2": (0.0, 3.637, 2.6),
}


def cuts():
    os.makedirs("round3/context", exist_ok=True); os.makedirs("round3/stills", exist_ok=True)
    T = "round3/DRAFT - RA-14 round 3 - first 30 seconds"
    cut(T + ".mp4", 0, END30, review=False)
    cut(T + " - REVIEW 540p.mp4", 0, END30, review=True)
    tot = PL["total_frames"]
    items = {"O2": (0.0, PL["cards"][0]["beat"][1])}
    for c in PL["cards"]:
        if c["name"] != "O0": items[c["name"]] = tuple(c["beat"])
    for g in PL["overlays"]: items[g["id"]] = (g["t0"], g["t1"])
    meta = {}
    for k, (a, b) in sorted(items.items(), key=lambda x: x[1][0]):
        f0 = max(0, int(round((a - 3.0) * FPS))); f1 = min(tot, int(round((b + 3.0) * FPS)))
        out = f"round3/context/{k}-context - REVIEW 540p.mp4"
        cut(out, f0, f1, review=True)
        settle = a + min(b - a - 0.4, max(0.8, (b - a) * 0.75))
        grab(settle, f"round3/stills/{k}.jpg")
        Image.open(f"round3/stills/{k}.jpg").resize((540, 960)).save(f"round3/context/{k}-context - REVIEW 540p.jpg", quality=88)
        meta[k] = dict(a=round(a, 3), b=round(b, 3), clip=out, clip_in=round(f0 / FPS, 3), clip_out=round(f1 / FPS, 3), still=f"round3/stills/{k}.jpg", still_t=round(settle, 3))
        print("context", k, f"{f0/FPS:.2f}-{f1/FPS:.2f}")
    json.dump(dict(first30=dict(file=T + ".mp4", frames=END30, dur=round(END30 / FPS, 3)), items=meta), open("round3/cuts.json", "w"), indent=1)


if __name__ == "__main__":
    {"work": work, "cuts": cuts}[sys.argv[1]]()
