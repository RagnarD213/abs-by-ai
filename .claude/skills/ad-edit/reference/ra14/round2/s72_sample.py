#!/usr/bin/env python3
"""RA-14 round 2: the opening, finished 9:16, WITHOUT the AI picture, in the two best colour candidates.

  s72_sample.py   -> round2/RA-14 round 2 - opening - *.mp4

What changed against round 1's s62_sample.py:
  * the framing pair comes from framing_choice.json (ra01lib.Aspect), the holds from beats_camopen.json (the superset plan:
    it also holds the camera-scene opening, which is what plays if no opener clip is approved);
  * every hold is graded in EVERY look of LOOKS in the same decode (split after the crop), so candidates cost one pass;
  * the roll is NOT decoded from frame 0. An input seek to half a frame before a known frame lands on exactly that frame
    (verified against round 1's full-decode strip: difference 0.0 at offset 0, 4.5 one frame either side), so the decode is
    the 18 s that are used, not 6.5 minutes;
  * where the opener clip will go, the recommended idea's START and END frames play as a LABELLED PLACEHOLDER (VIDEO-RULES
    "Future contextual previews"). No motion exists yet.
It ends on the R1|R2 take seam (10.58 s), where "Step one" starts.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
from ra01lib import Aspect
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB
import s71_opener_frames as OF

A = Aspect("9x16"); FPS = L.FPS; fr = lambda t: int(round(t*FPS))
CUT = json.load(open("cut.json")); B = json.load(open("beats_camopen.json"))
LOOKS = json.load(open("round2/colour/looks.json"))
USE = ["C2_brighter_gold", "C1_approved_level"]                      # the best two, by eye beside the approved videos
OPENER = os.environ.get("OPENER_ID", "O1")                     # the placeholder shows the recommended idea
OUT = "round2"; SEG = "round2/sample_seg"; os.makedirs(SEG, exist_ok=True)
ENDF = next(it["f0"] for it in B["timeline"] if it["kind"] == "dan" and it["a"] > 10.5)
punchby = {f"dan{i:02d}": p for i, p in enumerate(B["punch"])}
items = [dict(it) for it in B["timeline"] if it["f0"] < ENDF]
for it in items:
    it["f1"] = min(it["f1"], ENDF); it["n"] = it["f1"] - it["f0"]; it["b"] = it["f1"]/FPS
PIECES = CUT["pieces"]


def src_spans(a, b):
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        out.append((fr(p["src_in"] + (lo - p["t_in"])), fr(p["src_in"] + (hi - p["t_in"]))))
    return out


dan = [it for it in items if it["kind"] == "dan"]
N0 = min(a for it in dan for a, _ in src_spans(it["a"], it["b"])) - 60       # seek point: 2 s of pre-roll
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
    it["strip"] = [x1s - x0s, ch, x0s, y]; it["track"] = tr; it["cw"] = cw; it["level"] = pu["level"]
    spans = src_spans(it["a"], it["b"]); tot = sum(b_-a_ for a_, b_ in spans)
    if tot != it["n"]:
        a_, b_ = spans[-1]; spans[-1] = (a_, b_ + (it["n"] - tot))
    labs = {k: [] for k in USE}
    for a_, b_ in spans:
        chains.append(f"[b{bi}]trim=start_frame={a_-N0}:end_frame={b_-N0},setpts=PTS-STARTPTS,crop={x1s-x0s}:{ch}:{x0s}:{y},"
                      f"{L.DECODE},split={len(USE)}" + "".join(f"[c{bi}_{j}]" for j in range(len(USE))))
        for j, k in enumerate(USE):
            chains.append(f"[c{bi}_{j}]{LOOKS[k]['filter']},format=bgr0[p{bi}_{j}]"); labs[k].append(f"[p{bi}_{j}]")
        bi += 1
    for j, k in enumerate(USE):
        chains.append(("".join(labs[k]) + f"concat=n={len(labs[k])}:v=1:a=0[{it['name']}_{j}]") if len(labs[k]) > 1 else f"{labs[k][0]}null[{it['name']}_{j}]")
    outs.append(it)
cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{(N0-0.5)/FPS:.5f}", "-i", L.ROLL, "-filter_complex", ";".join(chains)]
for it in outs:
    for j, k in enumerate(USE):
        cmd += ["-map", f"[{it['name']}_{j}]", "-frames:v", str(it["n"]), "-c:v", "ffv1", "-r", "30000/1001", f"{SEG}/{it['name']}_{k}_strip.mkv"]
for it in outs:
    print(f"   {it['name']}  {it['a']:6.2f}->{it['b']:6.2f}  {it['n']:4d}f  {it['level']:<4} crop {it['cw']}x{it['strip'][1]} y {it['strip'][3]}  "
          f"centre {it['track'].min():.0f}..{it['track'].max():.0f}")
if os.environ.get("SKIP1") != "1":
    subprocess.run(cmd, check=True)
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
for it in outs:
    sw, sh, sx0, _ = it["strip"]; cw = it["cw"]
    for k in USE:
        dec = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-i", f"{SEG}/{it['name']}_{k}_strip.mkv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{A.VW}x{A.VH}", "-framerate", "30000/1001",
                                "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + X264 + [f"{SEG}/{it['name']}_{k}.mp4"], stdin=subprocess.PIPE)
        for q in range(it["n"]):
            buf = dec.stdout.read(sw*sh*3); assert len(buf) == sw*sh*3, (it["name"], k, q)
            im = Image.frombuffer("RGB", (sw, sh), buf, "raw", "RGB", 0, 1)
            xl = max(0.0, min(sw - cw, float(it["track"][q]) - cw/2 - sx0))
            enc.stdin.write(im.resize((A.VW, A.VH), Image.LANCZOS, box=(xl, 0, xl + cw, sh)).tobytes())
        enc.stdin.close(); enc.wait(); dec.wait()
    it["track"] = [round(float(v), 2) for v in it["track"]]

# the opener PLACEHOLDER: the recommended idea's START frame, a hard cut, its END frame; a banner says what it is
first = next(it for it in items if it["name"] == "dan00"); n = first["n"]; half = n//2
k = OPENER.lower()
def ph(which):
    im = Image.open(f"round2/frames/{OPENER}-{which}.png").convert("RGBA")
    if k == "o1": OF.slider(im, 0.0 if which == "start" else 1.0)
    if k == "o2": OF.pixel_text(im, "ABS X0" if which == "start" else "ABS X6", 70, 216)
    SB.disclosure(im, "AI-GENERATED", xy=(60, 1296), anchor="lt")
    d = ImageDraw.Draw(im); d.rectangle((0, 0, 1080, 150), fill=(250, 204, 21))
    d.text((540, 42), "PLACEHOLDER: AI opener, frames only", font=SB.font(40, True), fill=(20, 20, 20), anchor="mm")
    d.text((540, 104), f"{which.upper()} frame. No motion is made until you approve the frames.", font=SB.font(28, False), fill=(20, 20, 20), anchor="mm")
    return im.convert("RGB")
a_, b_ = ph("start"), ph("end")
L.encode_h264((a_ if i < half else b_ for i in range(n)), f"{SEG}/placeholder_{OPENER}.mp4", A.size, crf=15)

def build(look, opener, wav, name):
    lst = f"{SEG}/tl_{look}_{int(opener)}.txt"
    with open(lst, "w") as f:
        for it in items:
            p = f"placeholder_{OPENER}.mp4" if (opener and it["name"] == "dan00") else f"{it['name']}_{look}.mp4"
            f.write(f"file '{os.path.abspath(SEG)}/{p}'\n")
    pic = f"{SEG}/picture_{look}_{int(opener)}.mp4"
    if not os.path.exists(pic) or os.environ.get("REPIC", "1") == "1":
        subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", "cap_9x16/captions.mov",
                        "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-frames:v", str(ENDF),
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30000/1001",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", pic], check=True)
    dur = ENDF/FPS
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error", "-i", pic, "-i", wav, "-map", "0:v", "-map", "1:a", "-t", f"{dur:.4f}",
                    "-af", f"afade=t=out:st={dur-0.12:.3f}:d=0.12", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", f"{OUT}/{name}"], check=True)
    print("wrote", f"{OUT}/{name}", f"{dur:.2f}s")

T = "RA-14 round 2 - opening - "
build("C2_brighter_gold", True,  "mix.wav",      T + "brighter gold colour - opener placeholder.mp4")
build("C2_brighter_gold", True,  "mix_bass.wav", T + "brighter gold colour - opener placeholder - more bass.mp4")
build("C1_approved_level", True, "mix.wav",      T + "RA-01 level colour - opener placeholder.mp4")
build("C2_brighter_gold", False, "mix.wav",      T + "brighter gold colour - camera opening.mp4")
json.dump({"end_frame": ENDF, "dur": ENDF/FPS, "seek_frame": N0, "looks": USE, "opener": OPENER, "items": items}, open(f"{SEG}/sample.json", "w"), indent=1, default=str)
