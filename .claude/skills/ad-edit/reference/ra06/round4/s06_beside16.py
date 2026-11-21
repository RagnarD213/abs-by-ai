#!/usr/bin/env python3
"""RA-06 round 4: the four 16:9 APP cards (tour, flow_a, flow_b, tour2) as Dan on camera with the app beside him, left third
(VIDEO-RULES 2026-10-10, the RO-06 format Dan approved for reuse; ad-edit lesson 83: an app screen goes NEXT TO DAN, never a small
phone on an empty field). Replaces their s06_inserts16.py plates. The AI story clips (I3, I1, fired, I4) keep their plates.

Per card: Dan's own footage under that exact stretch (one continuous piece of the cut, asserted), the NEAR or FAR window (LEVEL, the
hair-anchored crops the 16:9 holds use), graded as the build grades it, then moved right by DX with softblue.shift_presenter (fixed,
never animated; the uncovered strip is the wall stretched, mostly hidden by the phone). The app recording sits in a rounded panel
on the left (the split-screen opener's panel style), same in-points and crops as the 9:16. DX and the panel width are measured per
card from his person mask so the phone never touches him. flow_b's AI-GENERATED chip sits under its panel.
Writes cards_16x9/<name>.mp4 (exact frame counts) and updates hf16/plates.json + cards_16x9/meta.json for the gate."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH)
import ra01lib as L, softblue as SB
FF = L.FF; FPS = L.FPS; W, H = 1920, 1080
B = json.load(open("beats.json")); CUT = json.load(open("cut.json")); P = json.load(open("clip_paths.json"))
by = {c["name"]: c for c in B["cards"]}
FR = json.load(open("framing.json"))["samples"] + (json.load(open("framing_holdstart.json"))["samples"] if os.path.exists("framing_holdstart.json") else [])
GRADE = L.grade(); A = L.Aspect("16x9")
# the size per card puts a size change on every source join beside it: fired|tour (card edge) and tour|dan04 FAR at 27.56;
# dan05 NEAR|flow_a at 32.67; flow_b|tour2 at 37.10. flow_a -> dan06 and dan06 -> flow_b are continuous footage (no join).
LEVEL = {"tour": "NEAR", "flow_a": "FAR", "dan06": "FAR", "flow_b": "FAR", "tour2": "NEAR"}
fr = lambda t: int(round(t * FPS))
TOP, PH_MAX, PW_MAX = 40, 852, 520     # PW_MAX: wider pushes him off the right edge (flow_b at 702 px: his reach to x 1961)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30000/1001", "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"
# the 9:16's media for each card: segments (path, t0, dur), crop, media aspect
dur = lambda k: by[k]["frames"] * 1001 / 30000
def tour2_segs():
    d = dur("tour2"); a = min(1.75, d * 0.42); return [(P["B0544"], 6.05, a), (P["B0544"], 5.2 - (d - a), d - a)]
MEDIA = {"tour": ([(P["B0034"], 0.0, dur("tour"))], "null", 780 / 1476, None),
         "flow_a": ([(P["B0049"], 13.0, dur("flow_a"))], "crop=1320:1600:0:170", 1320 / 1600, None),
         "flow_b": ([(P["B0049"], 28.0, dur("flow_b"))], "crop=1320:1600:0:170", 1320 / 1600, "AI-GENERATED"),
         "tour2": (tour2_segs(), "null", 432 / 920, None)}
# ROUND 4 re-review: flow_a, dan06 and flow_b are ONE continuous piece of his take at FAR; with the phone only on the cards his picture hopped
# 102 px left then 270 px right at the same size mid-sentence. dan06 is now part of the same beside composition (one offset for all three);
# the phone keeps playing the generating screen through it (B0049 continues from where flow_a ends), then the result screen.
_d6 = next(t for t in B["timeline"] if t["name"] == "dan06")
by["dan06"] = dict(name="dan06", beat=[_d6["a"], (_d6["f1"]) / FPS], frames=_d6["n"], kind="beside", asset="B0049")
MEDIA["dan06"] = ([(P["B0049"], 13.0 + dur("flow_a"), _d6["n"] * 1001 / 30000)], "crop=1320:1600:0:170", 1320 / 1600, None)
GROUPS = [["tour"], ["flow_a", "flow_b"], ["tour2"]]   # dan06 is Dan alone at NEAR between them (r4_16x9_overrides.json level16)
assert 28.0 >= 27.9   # B0049's banned "Meet the new you" BEFORE/AFTER screen runs to about 27.6 s

def src_piece(a, b):
    ps = [p for p in CUT["pieces"] if min(b, p["t_out"]) - max(a, p["t_in"]) > 0.5 / FPS]   # a sub-frame overlap at a card edge is not a join inside it
    assert len(ps) == 1, ("a join inside the card", a, b, [(p["t_in"], p["t_out"]) for p in ps])
    p = ps[0]; return p["src_in"] + (a - p["t_in"])

def raw(cmd, wh, n):
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE); sz = wh[0] * wh[1] * 3; out = []
    for _ in range(n):
        b = pr.stdout.read(sz); assert len(b) == sz, cmd[-1]
        out.append(np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3))
    pr.stdout.close(); pr.wait(); return out

def dan_frames(name, span=None):
    """span = (src0, src1) the hair is measured over: the whole group, so continuous pieces share one crop (no vertical hop)."""
    CW, CH = A.levels[LEVEL[name]]
    a, b = by[name]["beat"]; n = by[name]["frames"]; s0 = src_piece(a, b)
    h0, h1 = span or (s0, s0 + n / FPS)
    hm = min(s["hair"] for s in FR if h0 - 0.5 <= s["src"] <= h1 + 0.5)
    y = int(round(hm - 0.04 * CH)); y = max(0, min(3840 - CH, y - y % 2))
    x = int(round(1088 - CW / 2)); x = max(0, min(2160 - CW, x - x % 2))          # cx16 = 1088, the 16:9 holds' shared centre
    N0 = fr(s0)
    vf = f"crop={CW}:{CH}:{x}:{y}:exact=1,{L.DECODE},{GRADE},scale={W}:{H}:flags=lanczos,format=rgb24"
    return raw([FF, "-nostdin", "-v", "error", "-ss", f"{(N0 - 0.5) / FPS:.5f}", "-i", L.ROLL, "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-"], (W, H), n), [CW, CH, x, y]

def media_frames(name, wh):
    segs, vf, _ar, _l = MEDIA[name]; n = by[name]["frames"]; ins, ch = [], []
    for i, (p, t0, d) in enumerate(segs):
        ins += ["-ss", f"{t0:.3f}", "-t", f"{d + 0.2:.3f}", "-i", p]
        ch.append(f"[{i}:v]fps=30000/1001,{vf},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1,trim=end_frame={round(d * 30000 / 1001)},setpts=PTS-STARTPTS[v{i}]")
    ch.append("".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=1,{D709},format=rgb24[v]")
    return raw([FF, "-nostdin", "-v", "error"] + ins + ["-filter_complex", ";".join(ch), "-map", "[v]", "-frames:v", str(n), "-f", "rawvideo", "-"], wh, n)

PL = json.load(open("hf16/plates.json")); META = json.load(open("cards_16x9/meta.json")); report = {}
only = set(sys.argv[1:])
u = SB.unit(W, H); RAD = round(22 * u)
for grp in GROUPS:
    if only and not (set(grp) & only): continue
    _sp = [(src_piece(*by[nm]["beat"]), by[nm]["frames"]) for nm in grp]
    span = (min(a for a, _ in _sp), max(a + k / FPS for a, k in _sp))
    D = {nm: dan_frames(nm, span) for nm in grp}
    assert len({tuple(D[nm][1]) for nm in grp}) == 1, ("one crop per group", {nm: D[nm][1] for nm in grp})
    # where he is: the union of his person mask over the whole group (one fixed offset for all of it)
    un = np.zeros((H, W), bool)
    for nm in grp:
        dan = D[nm][0]
        for f in dan[::max(1, len(dan) // 10)] + [dan[-1]]:
            m = L.person_mask(Image.fromarray(f)); un |= m if m is not None else False
    cols = np.where(un[TOP:900].any(0))[0]; left0, right0 = int(cols.min()), int(cols.max())
    ar = MEDIA[grp[0]][2]; anylabel = any(MEDIA[nm][3] for nm in grp)
    ph = PH_MAX - (92 if anylabel else 0)
    if ph * ar > PW_MAX: ph = int(PW_MAX / ar) // 2 * 2                 # the wide app screens (B0049 crop) get a shorter panel, never a wider one
    pw = int(ph * ar) // 2 * 2; px = 60
    c0 = max(40, left0 - 40)                          # the moved picture starts just left of his widest reach
    dx = max(0, px + pw + 50 - left0)                 # his widest reach lands 50 px right of the panel
    assert right0 + dx <= W + 40, (grp, "his reach leaves the frame", right0 + dx)
    mask = Image.new("L", (pw, ph), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), RAD, fill=255)
    shadow = Image.new("L", (W, H), 0); ImageDraw.Draw(shadow).rounded_rectangle((px + 6, TOP + 10, px + pw + 6, TOP + ph + 10), RAD, fill=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    for name in grp:
        dan, crop = D[name]; n = by[name]["frames"]; label = MEDIA[name][3]
        med = media_frames(name, (pw, ph))
        e = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-",
                              "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + ENC + [f"cards_16x9/{name}.mp4"], stdin=subprocess.PIPE)
        chip = None
        for i in range(n):
            im = SB.shift_presenter(Image.fromarray(dan[i]), dx=dx, c0=c0, wall_w=c0) if dx else Image.fromarray(dan[i])
            im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, shadow)
            im.paste(Image.fromarray(med[i]), (px, TOP), mask)
            SB.rr(im, (px, TOP, px + pw, TOP + ph), None, RAD, SB.GLASS_LINE, u)
            if label: chip = SB.disclosure(im, label, (px, TOP + ph + 12))
            e.stdin.write(np.asarray(im).tobytes())
            if i in (0, n // 2): im.save(f"round4/look/beside_{name}_{i:03d}.png")
        e.stdin.close(); assert e.wait() == 0
        PL[name] = dict(frames=n, hole=[px, TOP, px + pw, TOP + ph], mov=None, layout="beside-dan",
                        chip=dict(x=round(chip[0]), y=round(chip[1]), s=label, w=round(chip[2] - chip[0])) if chip else None)
        META[name] = dict(chip=label, chip_box=[round(v) for v in chip] if chip else None, hole=PL[name]["hole"], layout="beside-dan", dan_crop=crop, dx=dx, c0=c0)
        report[name] = dict(level=LEVEL[name], group=grp, frames=n, panel=[px, TOP, pw, ph], dan_crop=crop, his_reach=[left0, right0], dx=dx, c0=c0, chip=META[name]["chip_box"])
        print(name, report[name], flush=True)
json.dump(PL, open("hf16/plates.json", "w"), indent=1); json.dump(META, open("cards_16x9/meta.json", "w"), indent=1)
json.dump(report, open("round4/beside16.json", "w"), indent=1)
print("BESIDE16_COMPLETE")
