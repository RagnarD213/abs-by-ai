#!/usr/bin/env python3
"""Add the per-range `vf` extras to edl.json: 10% zoom cuts + the deodorant fix.

ZOOM CUTS (Dan's note 6). Alternating 10% punch-in so every join reads as a
deliberate zoom cut rather than a jump cut; crop anchored to the TOP (y=0)
because his head sits close to the frame edge. A join already hidden by a
full-frame cutaway keeps the SAME zoom state on both sides - a zoom nobody can
see is a wasted flip. Cards do NOT count as cover: they are left-side panels
and the cut is fully visible beside them.

DEODORANT FIX (Dan's note 7). The recipe is the handoff's measured one, NOT
re-derived:
    W     = box * clip((0.45-sat)/0.20,0,1) * clip((0.62-val)/0.15,0,1)
    r,g,b *= (1-0.28W), (1-0.45W), (1-0.63W)
which maps the residue colour (88,76,67) onto the neighbouring hair colour
(63,42,25) at full weight, so it re-tints rather than paints and the texture
survives.

TWO THINGS HAD TO CHANGE TO SHIP IT SAFELY:
 1. It is applied as an ALPHA-MASKED PATCH, not a full-frame geq. Measured
    end-to-end, `format=gbrp,geq,format=yuv420p` changed ~560,000 pixels
    OUTSIDE the box (max delta 199) - that is the yuv->rgb->yuv chroma round
    trip, not the edit, and it would have made these six beats visibly
    different from the other 38. Cropping to the armpit, computing alpha = W
    and overlaying means every pixel with W = 0 passes through untouched, and
    geq runs on ~30k pixels instead of 2M.
 2. The viewer-LEFT search band was DISCARDED. Every "left armpit" box it
    produced landed on the bright white DOOR FRAME at x 680-800 - confirmed by
    cropping each one and looking at it. Only boxes verified by eye are used.
usage: apply_vf.py
"""
import json, importlib.util
from pathlib import Path

B = Path("/Volumes/Seagate 4TB/_edit_work/spraytan")
edl = json.load(open(B / "edl.json"))
R = edl["ranges"]
spec = importlib.util.spec_from_file_location("i", B / "inserts.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

ZOOM = "crop=1728:972:96:0,scale=1920:1080:flags=lanczos"
FEATHER = 18

# (beat, local_start, local_end, [boxes]) -- local = seconds into that range.
#
# ONLY THREE WINDOWS SURVIVED. The recipe is sound but it needs a box locked to
# the armpit, and on this footage the armpit is on screen for well under a
# second at a time inside fast arm-spread gestures. Measured: at intro t=148.9
# the pit sits at x1150-1225, and by t=150.1 it has left that region of the
# frame entirely. So:
#   - a static box over a 2-3s window lands on his tank, forearm or palm and
#     does nothing (verified frame by frame - see DEO_VERIFY.png);
#   - a box generous enough to contain the whole gesture reaches past his arm
#     onto the white fridge, whose shadowed side reads val 0.55-0.62, inside
#     the filter's own gate, and the "fix" paints a grey smudge across it -
#     far worse than the residue, and exactly the failure the handoff warns of;
#   - per-frame tracking is what the handoff rules out.
# What DOES work is a short window (<=0.8s) with a tight box, which is the one
# regime where a static box is valid. Each of the three below was A/B'd
# losslessly at three frames: residue reduced, texture kept, zero pixels changed
# outside the box.
# The other three arms-spread moments (5:36, 14:19, 16:18 in the rev-0 render)
# are LEFT ALONE, and the real fix for them is at the shoot: clear/invisible-
# solid deodorant, or wipe the underarms down before rolling.
DEO = [
 ("intro",              12.90, 13.70, [(1145, 630, 1235, 775)]),
 ("how-long-it-lasts",   4.60,  5.30, [(1285, 682, 1355, 810)]),
 ("how-long-it-lasts",   5.90,  6.40, [(1325, 632, 1400, 770)]),
]
FEATHER = 14

def deo_graph_multi(wins, tag):
    """One split, one patch per (window, box) pair, chained overlays."""
    flat = [(a, b, box) for (a, b, boxes) in wins for box in boxes]
    n = len(flat)
    parts = ["split=" + str(n + 1) + f"[{tag}m0]" + "".join(f"[{tag}k{i}]" for i in range(n))]
    for i, (a, b, (x0, y0, x1, y1)) in enumerate(flat):
        w, h = x1 - x0, y1 - y0
        MX = "max(max(r(X,Y),g(X,Y)),b(X,Y))"
        MN = "min(min(r(X,Y),g(X,Y)),b(X,Y))"
        SAT = f"(({MX})-({MN}))/max({MX},1)"
        VAL = f"({MX})/255"
        BOX = f"clip(min(X\\,{w}-X)/{FEATHER}\\,0\\,1)*clip(min(Y\\,{h}-Y)/{FEATHER}\\,0\\,1)"
        SATW = f"clip((0.45-({SAT}))/0.20\\,0\\,1)"
        VALW = f"clip((0.62-({VAL}))/0.15\\,0\\,1)"
        W = f"({BOX})*{SATW}*{VALW}"
        parts.append(f"[{tag}k{i}]crop={w}:{h}:{x0}:{y0},format=gbrap,"
                     f"geq=r='r(X\\,Y)*(1-0.28*({W}))'"
                     f":g='g(X\\,Y)*(1-0.45*({W}))'"
                     f":b='b(X\\,Y)*(1-0.63*({W}))'"
                     f":a='255*({W})',format=yuva420p[{tag}p{i}]")
    main = f"{tag}m0"
    for i, (a, b, (x0, y0, x1, y1)) in enumerate(flat):
        nxt = f"{tag}m{i+1}"
        parts.append(f"[{main}][{tag}p{i}]overlay={x0}:{y0}:format=yuv420"
                     f":enable='between(t\\,{a}\\,{b})'[{nxt}]")
        main = nxt
    return ";".join(parts), main

by_beat = {r["beat"]: r for r in R}
windows = {}
for beat, a, b, boxes in DEO:
    assert beat in by_beat, beat
    d = by_beat[beat]["end"] - by_beat[beat]["start"]
    assert 0 <= a < b <= d + 0.1, f"{beat}: window {a}-{b} outside range 0-{d:.2f}"
    windows.setdefault(beat, []).append((a, b, boxes))
deo_vf, deo_out = {}, {}
for beat, wins in windows.items():
    tag = "".join(c for c in beat if c.isalpha())[:7]
    g, out = deo_graph_multi(wins, tag)
    deo_vf[beat], deo_out[beat] = g, out

# ---- which joins are hidden by a full-frame cutaway?
offs, acc = [], 0.0
for r in R: offs.append(acc); acc += round(r["end"] - r["start"], 3)
cover = [(a, a + d) for a, d, k, _, _ in m.INSERTS if k in ("clip", "photo")]
def hidden(t): return any(a - 0.15 <= t <= b + 0.15 for a, b in cover)

state, flips, kept = 0, 0, 0
for i, r in enumerate(R):
    if i > 0:
        if hidden(offs[i]): kept += 1
        else: state ^= 1; flips += 1
    deo = deo_vf.get(r["beat"])
    if deo and state:  r["vf"] = f"{deo};[{deo_out[r['beat']]}]{ZOOM}"
    elif deo:          r["vf"] = f"{deo};[{deo_out[r['beat']]}]null"
    elif state:        r["vf"] = ZOOM
    else:              r.pop("vf", None)

json.dump(edl, open(B / "edl.json", "w"), indent=1)
z = sum(1 for r in R if "lanczos" in r.get("vf", ""))
print(f"{len(R)} ranges: {z} zoomed, {len(R)-z} at native framing")
print(f"joins: {flips} flipped (zoom cut), {kept} left alone (already hidden by a cutaway)")
print(f"deodorant patch on {len(deo_vf)} ranges: {', '.join(deo_vf)}")
print(f"ranges carrying a vf: {sum(1 for r in R if r.get('vf'))} -> that many cache misses")
