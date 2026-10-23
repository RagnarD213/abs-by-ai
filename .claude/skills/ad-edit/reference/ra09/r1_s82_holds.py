#!/usr/bin/env python3
"""RA-14 round 3: every Dan hold of the plan, finished 9:16 picture (approved F2 framing, approved C2 colour), one mp4 each.

  PLAN=beats.json python3 s82_holds.py [dan04 dan06 ...]     -> r1/seg/<name>.mp4  (+ r1/seg/holds.json)

Same method as round 2's s72_sample.py (one input-seeked decode of the roll, frame-indexed trims, crop of the land-then-hold
track strip, the one LUT in grade.json, lanczos to 1080x1920), for the whole film instead of the opening, in the one
approved look. Picture only: captions, graphics and audio are laid on in s86_assemble.py.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09")
import ra01lib as L
from ra01lib import Aspect
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")

A = Aspect("9x16"); FPS = L.FPS; fr = lambda t: int(round(t*FPS))
CUT = json.load(open("cut.json")); B = json.load(open(os.environ.get("PLAN", "beats.json")))
LUT = json.load(open("grade.json"))["filter"]
SEG = "r1/seg"; os.makedirs(SEG, exist_ok=True)
ONLY = set(sys.argv[1:])
punchby = {f"dan{i:02d}": p for i, p in enumerate(B["punch"])}
PIECES = CUT["pieces"]


SP = CUT.get("speed") or 1.0     # RA-09: the talk plays at 1.06x (Dan's RA-05 rule, 2026-10-14); the end hold at 1.0x


def src_spans(a, b):
    """source frame spans for film [a, b): talk pieces at SP (film span x SP of source), then the end hold at 1.0x"""
    out = []
    for p in PIECES:
        lo, hi = max(a, p["t_in"]), min(b, p["t_out"])
        if hi - lo <= 1e-6: continue
        out.append((fr(p["src_in"] + (lo - p["t_in"])*SP), fr(p["src_in"] + (hi - p["t_in"])*SP)))
    return out


def tail_span(a, b):
    """the end hold after the last word: source continues from the last piece at normal speed"""
    lp = PIECES[-1]; lo = max(a, lp["t_out"])
    if b - lo <= 1e-6: return None
    return (fr(lp["src_out"] + (lo - lp["t_out"])), fr(lp["src_out"] + (b - lp["t_out"])))


dan = []
for it in B["timeline"]:
    if it["kind"] != "dan" or (ONLY and it["name"] not in ONLY): continue
    it = dict(it); it["b"] = it["f1"]/FPS
    dan.append(it)
N0 = min([a for it in dan for a, _ in src_spans(it["a"], it["b"])] + [t[0] for it in dan for t in [tail_span(it["a"], it["b"])] if t]) - 60       # seek point: 2 s of pre-roll
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
    spans = src_spans(it["a"], it["b"]); tail = tail_span(it["a"], it["b"])
    # film frames of the talk part and of the end-hold part of this hold
    n_tail = 0 if tail is None else it["n"] - max(0, int(round((min(it["b"], PIECES[-1]["t_out"]) - it["a"]) * FPS)))
    n_talk = it["n"] - n_tail
    it["n_talk"], it["n_tail"] = n_talk, n_tail
    if tail is not None:
        tail = (tail[0], tail[0] + n_tail)
    it["tail"] = tail
    if spans and it["n_talk"] > 0:
        # rounding at the span edges can leave the 1.06x retime a frame short of n_talk: read 2 spare source frames after the last
        # talk span (trimmed off again by end_frame when not needed)
        a_, b_ = spans[-1]; spans[-1] = (a_, b_ + 2)
    if pu.get("picture_slip") == "lead_in":
        raise SystemExit("picture_slip is not wired for the 1.06x speed-up")
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
    parts = []
    if labs and it["n_talk"] > 0:
        # RA-09 speed-up: the talk spans are concatenated, played at SP (setpts), re-gridded to 29.97 and cut to n_talk frames
        chains.append(("".join(labs) + f"concat=n={len(labs)}:v=1:a=0," if len(labs) > 1 else f"{labs[0]}") +
                      f"setpts=(PTS-STARTPTS)/{SP},fps=30000/1001,trim=end_frame={it['n_talk']},setpts=PTS-STARTPTS[{it['name']}_t]")
        parts.append(f"[{it['name']}_t]")
    if it["tail"] is not None:
        ta, tb = it["tail"]
        chains.append(f"[b{bi}]trim=start_frame={ta-N0}:end_frame={tb-N0},setpts=PTS-STARTPTS,crop={x1s-x0s}:{ch}:{x0s}:{y},"
                      f"{L.DECODE},{LUT},format=bgr0[{it['name']}_e]")
        bi += 1; parts.append(f"[{it['name']}_e]")
    chains.append(("".join(parts) + f"concat=n={len(parts)}:v=1:a=0[{it['name']}]") if len(parts) > 1 else f"{parts[0]}null[{it['name']}]")
chains.insert(0, f"[0:v]split={bi}" + "".join(f"[b{i}]" for i in range(bi)))      # one branch per final span (after any slip)
cmd = [L.FF, "-nostdin", "-y", "-v", "error", "-ss", f"{(N0-0.5)/FPS:.5f}", "-i", L.ROLL, "-filter_complex", ";".join(chains)]
for it in dan:
    cmd += ["-map", f"[{it['name']}]", "-frames:v", str(it["n"]), "-c:v", "ffv1", "-r", "30000/1001", f"{SEG}/{it['name']}_strip.mkv"]
for it in dan:
    print(f"   {it['name']}  {it['a']:6.2f}->{it['b']:6.2f}  {it['n']:4d}f  {it['level']:<4} crop {it['cw']}x{it['strip'][1]} y {it['strip'][3]}  "
          f"centre {it['track'].min():.0f}..{it['track'].max():.0f}  spans {it['spans']}", flush=True)
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
