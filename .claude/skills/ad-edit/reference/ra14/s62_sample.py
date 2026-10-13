#!/usr/bin/env python3
"""RA-14 round 1: the LOOK sample, the opening of the ad up to the "Step one" seam, finished 9:16.

  s62_sample.py            -> round1/RA-14 round 1 - look sample (opening).mp4  (+ the more-bass audio alternative)

Same stage-1 as the approved RA-01 renderer (s10_render.py): ONE decode of the roll, frame-indexed trims, crop (the
hair-anchored level) -> BT.709 decode -> the approved 8/28 daylight grade -> lanczos. Then the G1 card (softblue.scene_photo)
and the burned captions. It starts on speech (frame 0 is the head edge, 0.12 s before the first word).
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
from ra01lib import Aspect
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB

KEY = "9x16"; A = Aspect(KEY)
CUT = json.load(open("cut.json")); B = json.load(open("beats.json"))
G = json.load(open("grade.json")); GRADE = G["filter"]
FPS = L.FPS; fr = lambda t: int(round(t*FPS))
OUT = "round1"; SEG = "sample_seg"; os.makedirs(SEG, exist_ok=True); os.makedirs(OUT, exist_ok=True)
END = next(o["t0"] for o in B["overlays"] if o["id"] == "L1")          # the R1|R2 seam: "Step one" starts here
ENDF = fr(END)
byname = {c["name"]: c for c in B["cards"]}
punchby = {f"dan{i:02d}": p for i, p in enumerate(B["punch"])}
items = [dict(it) for it in B["timeline"] if it["f0"] < ENDF]
for it in items:
    it["f1"] = min(it["f1"], ENDF); it["n"] = it["f1"] - it["f0"]
    it["b"] = it["f1"]/FPS
PIECES = CUT["pieces"]


def src_spans(a, b):
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        out.append((fr(p["src_in"] + (lo - p["t_in"])), fr(p["src_in"] + (hi - p["t_in"]))))
    return out


dan = [it for it in items if it["kind"] == "dan"]
import numpy as np
from PIL import Image
# STAGE 1: one decode of the roll -> one LOSSLESS graded strip per hold, wide enough for the crop's whole travel.
# STAGE 1b: the land-then-hold crop (beats.json punch[].track, one centre per frame, from _shared/cut/landing.py) is cut
# out of the strip per frame with a sub-pixel window and scaled to 1080x1920 (a whole-pixel window steps 2 px at 2.1x).
chains, outs = [], []
nb = sum(len(src_spans(it["a"], it["b"])) for it in dan)
chains.append(f"[0:v]split={nb}" + "".join(f"[b{i}]" for i in range(nb)))
bi = 0
for it in dan:
    pu = punchby[it["name"]]; cw, ch = A.levels[pu["level"]]
    y = int(round(pu["hair_min"] - 0.04*ch)); y = max(0, min(3840-ch, y - y % 2))
    tr = np.array(pu["track"][:it["n"]], float)
    if len(tr) < it["n"]: tr = np.concatenate([tr, np.full(it["n"]-len(tr), tr[-1])])
    x0s = int(max(0, np.floor(tr.min() - cw/2) - 4)); x0s -= x0s % 2
    x1s = int(min(2160, np.ceil(tr.max() + cw/2) + 4)); x1s += x1s % 2
    it["strip"] = [x1s - x0s, ch, x0s, y]; it["track"] = tr; it["cw"] = cw
    spans = src_spans(it["a"], it["b"])
    tot = sum(b_-a_ for a_, b_ in spans)
    if tot != it["n"]:
        a_, b_ = spans[-1]; spans[-1] = (a_, b_ + (it["n"] - tot))
    labs = []
    for a_, b_ in spans:
        chains.append(f"[b{bi}]trim=start_frame={a_}:end_frame={b_},setpts=PTS-STARTPTS,crop={x1s-x0s}:{ch}:{x0s}:{y},"
                      f"{L.DECODE},{GRADE},format=bgr0[p{bi}]")
        labs.append(f"[p{bi}]"); bi += 1
    chains.append(("".join(labs) + f"concat=n={len(labs)}:v=1:a=0[{it['name']}]") if len(labs) > 1 else f"{labs[0]}null[{it['name']}]")
    outs.append(it)
cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-i", L.ROLL, "-filter_complex", ";".join(chains)]
for it in outs:
    cmd += ["-map", f"[{it['name']}]", "-frames:v", str(it["n"]), "-c:v", "ffv1", "-r", "30000/1001", f"{SEG}/{it['name']}_strip.mkv"]
for it in outs:
    print(f"   {it['name']}  {it['a']:6.2f}->{it['b']:6.2f}  {it['n']:4d}f  {punchby[it['name']]['level']:<4} strip {it['strip']}  "
          f"crop centre {it['track'].min():.0f}..{it['track'].max():.0f}")
if os.environ.get("SKIP1") != "1":
    subprocess.run(cmd, check=True)
for it in outs:
    sw, sh, sx0, _ = it["strip"]; cw = it["cw"]
    dec = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-i", f"{SEG}/{it['name']}_strip.mkv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{A.VW}x{A.VH}",
                            "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-r", "30000/1001", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                            "-x264-params", "keyint=30:min-keyint=1:scenecut=0", f"{SEG}/{it['name']}.mp4"], stdin=subprocess.PIPE)
    for k in range(it["n"]):
        buf = dec.stdout.read(sw*sh*3)
        assert len(buf) == sw*sh*3, (it["name"], k)
        im = Image.frombuffer("RGB", (sw, sh), buf, "raw", "RGB", 0, 1)
        xl = float(it["track"][k]) - cw/2 - sx0
        xl = max(0.0, min(sw - cw, xl))
        enc.stdin.write(im.resize((A.VW, A.VH), Image.LANCZOS, box=(xl, 0, xl + cw, sh)).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    it["track"] = [round(float(v), 2) for v in it["track"]]

# the G1 card: one photo on the Soft Blue field, exact frame count
for it in items:
    if it["kind"] != "card": continue
    assert it["name"] == "G1", it
    n = it["n"]; p = f"{SEG}/G1.mp4"
    goal = f"{L.REPO}/Media/example pictures/dan by pool.png"
    frames = (SB.scene_photo(i/FPS, A.VW, A.VH, goal, "AI-GENERATED") for i in range(n))
    L.encode_h264(frames, p, A.size, crf=15)
lst = f"{SEG}/timeline.txt"
with open(lst, "w") as f:
    for it in items: f.write(f"file '{os.path.abspath(SEG)}/{it['name']}.mp4'\n")
pic = f"{SEG}/picture.mp4"
subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", "cap_9x16/captions.mov",
                "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-frames:v", str(ENDF),
                "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", pic], check=True)
dur = ENDF/FPS
for wav, name in (("mix.wav", "RA-14 round 1 - look sample (opening).mp4"),
                  ("mix_bass.wav", "RA-14 round 1 - look sample (opening) - more bass.mp4")):
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", pic, "-i", wav, "-map", "0:v", "-map", "1:a", "-t", f"{dur:.4f}",
                    "-af", f"afade=t=out:st={dur-0.25:.3f}:d=0.25", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                    f"{OUT}/{name}"], check=True)
    print("wrote", f"{OUT}/{name}", f"{dur:.2f}s")
json.dump({"end": END, "frames": ENDF, "items": items}, open(f"{SEG}/sample.json", "w"), indent=1)
