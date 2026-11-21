#!/usr/bin/env python3
"""RA-07 round 2 (from RA-14 round 3 s82_holds.py): every Dan hold of the plan, finished 9:16 picture (approved F2 framing, approved C2 colour), one mp4 each.

  PLAN=beats_r3.json python3 s82_holds.py [dan04 dan06 ...]     -> round3/seg/<name>.mp4  (+ round3/seg/holds.json)

Same method as round 2's s72_sample.py (one input-seeked decode of the roll, frame-indexed trims, crop of the land-then-hold
track strip, the one LUT in grade.json, lanczos to 1080x1920), for the whole film instead of the opening, in the one
approved look. Picture only: captions, graphics and audio are laid on in s86_assemble.py.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
from ra01lib import Aspect
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import buildcap

A = Aspect("9x16"); FPS = L.FPS; fr = lambda t: int(round(t*FPS))
CUT = json.load(open("cut.json")); B = json.load(open(os.environ.get("PLAN", "beats.json")))
LUT = json.load(open("grade.json"))["filter"]
SEG = os.environ.get("SEG", "round2/seg"); os.makedirs(SEG, exist_ok=True)
ONLY = set(sys.argv[1:])
punchby = {f"dan{i:02d}": p for i, p in enumerate(B["punch"])}
PIECES = CUT["pieces"]


def src_spans(a, b):
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        out.append((fr(p["src_in"] + (lo - p["t_in"])), fr(p["src_in"] + (hi - p["t_in"]))))
    return [s for s in out if s[1] > s[0]]      # RA-07: a piece edge can round to a zero-frame span; it would break the concat


dan = []
for it in B["timeline"]:
    if it["kind"] != "dan" or (ONLY and it["name"] not in ONLY): continue
    it = dict(it); it["b"] = it["f1"]/FPS
    dan.append(it)
N0 = min(a for it in dan for a, _ in src_spans(it["a"], it["b"])) - 60       # seek point: 2 s of pre-roll
chains = []
bi = 0
for it in dan:
    pu = punchby[it["name"]]; cw, ch = A.levels[pu["level"]]
    y = int(round(pu["hair_min"] - 0.04*ch)); y = max(0, min(3840-ch, y - y % 2))
    tr = np.array(pu["track"][:it["n"]], float)
    if len(tr) < it["n"]: tr = np.concatenate([tr, np.full(it["n"]-len(tr), tr[-1])])
    x0s = int(max(0, np.floor(tr.min() - cw/2) - 4)); x0s -= x0s % 2
    x1s = int(min(2160, np.ceil(tr.max() + cw/2) + 4)); x1s += x1s % 2
    it.update(strip=[x1s - x0s, ch, x0s, y], track=tr, cw=cw, level=pu["level"])
    spans = src_spans(it["a"], it["b"]); tot = sum(b_-a_ for a_, b_ in spans)
    if tot != it["n"]:
        a_, b_ = spans[-1]; spans[-1] = (a_, b_ + (it["n"] - tot))
    if pu.get("picture_slip") == "lead_in":
        # the short pieces before the hold's first long piece are replaced by the frames just before that piece (he is silent
        # in both: they sit in a pause), so the picture runs continuously and there is no join (s84_plan.py, PICTURE_SLIP)
        k = next(j for j, (a_, b_) in enumerate(spans) if b_ - a_ >= 10)
        lead = sum(b_ - a_ for a_, b_ in spans[:k])
        it["slip"] = dict(was=spans[:k], now=[(spans[k][0] - lead, spans[k][0])])
        spans = [(spans[k][0] - lead, spans[k][1])] + spans[k+1:]
    it["spans"] = spans
    labs = []
    for a_, b_ in spans:
        chains.append(f"[b{bi}]trim=start_frame={a_-N0}:end_frame={b_-N0},setpts=PTS-STARTPTS,crop={x1s-x0s}:{ch}:{x0s}:{y},"
                      f"{L.DECODE},{LUT},format=bgr0[p{bi}]")
        labs.append(f"[p{bi}]"); bi += 1
    chains.append(("".join(labs) + f"concat=n={len(labs)}:v=1:a=0[{it['name']}]") if len(labs) > 1 else f"{labs[0]}null[{it['name']}]")
chains.insert(0, f"[0:v]split={bi}" + "".join(f"[b{i}]" for i in range(bi)))      # one branch per final span (after any slip)
cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{(N0-0.5)/FPS:.5f}", "-i", L.ROLL, "-filter_complex", ";".join(chains)]
for it in dan:
    cmd += ["-map", f"[{it['name']}]", "-frames:v", str(it["n"]), "-c:v", "ffv1", "-r", "30000/1001", f"{SEG}/{it['name']}_strip.mkv"]
for it in dan:
    print(f"   {it['name']}  {it['a']:6.2f}->{it['b']:6.2f}  {it['n']:4d}f  {it['level']:<4} crop {it['cw']}x{it['strip'][1]} y {it['strip'][3]}  "
          f"centre {it['track'].min():.0f}..{it['track'].max():.0f}  spans {it['spans']}", flush=True)
buildcap.wait("ra07 r2 holds")
if os.environ.get("SKIP1") != "1":
    subprocess.run(cmd, check=True)
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-r", "30000/1001", "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
for it in dan:
    sw, sh, sx0, _ = it["strip"]; cw = it["cw"]
    dec = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-i", f"{SEG}/{it['name']}_strip.mkv", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{A.VW}x{A.VH}", "-framerate", "30000/1001",
                            "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + X264 + [f"{SEG}/{it['name']}.mp4"], stdin=subprocess.PIPE)
    for q in range(it["n"]):
        buf = dec.stdout.read(sw*sh*3); assert len(buf) == sw*sh*3, (it["name"], q)
        im = Image.frombuffer("RGB", (sw, sh), buf, "raw", "RGB", 0, 1)
        xl = max(0.0, min(sw - cw, float(it["track"][q]) - cw/2 - sx0))
        enc.stdin.write(im.resize((A.VW, A.VH), Image.LANCZOS, box=(xl, 0, xl + cw, sh)).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    os.remove(f"{SEG}/{it['name']}_strip.mkv")
    it["track"] = [round(float(v), 2) for v in it["track"]]
    print("wrote", f"{SEG}/{it['name']}.mp4", flush=True)
old = json.load(open(f"{SEG}/holds.json")) if os.path.exists(f"{SEG}/holds.json") else {}
old.update({it["name"]: dict(a=it["a"], b=it["b"], n=it["n"], level=it["level"], cw=it["cw"], strip=it["strip"], spans=it["spans"], slip=it.get("slip"),
                             plan=os.environ.get("PLAN", "beats.json")) for it in dan})
json.dump(old, open(f"{SEG}/holds.json", "w"), indent=1)
print("HOLDS DONE", len(dan))
