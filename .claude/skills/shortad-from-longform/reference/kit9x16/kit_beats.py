#!/usr/bin/env python3
"""THE KIT'S BEATS MODULE -- the shim `render.py`, `captions.py`, `mux.py` and the plan builder import
as `beats`. It exposes exactly what the hand-written beats.py files exposed (timeline(), PUSHES,
PUSH_Z, FLASHES, LOWER_THIRDS, CTAS, INSETS, DUR, FPS, NO_CAPS_KINDS, BASE_KINDS, SEAMS, push_at,
at/end phrase anchors) but reads everything from `beats.json`, which `build_kit.py` writes from the
template + the content list + the recovered cut. Nothing in a build is typed by hand any more; the
beat sheet is data the kit generated, and this file is copied into the build dir as `beats.py`.
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_J = json.load(open(os.path.join(_HERE, "beats.json")))

FPS = 30000 / 1001
DUR = float(_J["dur"])
PUSH_Z = float(_J.get("push_z", 1.20))
BEATS = _J["beats"]                       # base-layer beats (kind, t0, t1, ...)
LOWER_THIRDS = _J.get("lower_thirds", [])
CTAS = _J.get("ctas", [])
INSETS = _J.get("insets", [])
PUSHES = [tuple(p) for p in _J.get("pushes", [])]
FLASHES = [tuple(f) for f in _J.get("flashes", [])]
NO_CAPS_KINDS = set(_J.get("no_caps_kinds", ["window", "title", "stmt", "cta"]))
NO_CAPS_BODIES = set(_J.get("no_caps_bodies", []))
BASE_KINDS = set(_J.get("base_kinds", ["talk", "window", "card", "title", "stmt", "bleed", "bleed2", "winmedia"]))
SEAMS = list(_J.get("seams", []))
DEVIATIONS = _J.get("deviations", [])
CTA_TOP, CTA_BIG = _J.get("cta_top", "Get A FREE AI Image Of Yourself"), _J.get("cta_big", "With Abs")

# phrase anchors, from the words file the kit was built against (the delivered mix's word timings)
_n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
WORDS = [(_n(w["w"]), float(w["t"]), float(w["e"])) for w in _J.get("words", []) if _n(w["w"])]


def _seq(phrase, after=0.0):
    toks = [_n(t) for t in phrase.split() if _n(t)]
    for i in range(len(WORDS)):
        if WORDS[i][1] < after:
            continue
        if [w[0] for w in WORDS[i:i + len(toks)]] == toks:
            return i, len(toks)
    raise ValueError(f"phrase not found after {after}: {phrase!r}")


def at(phrase, after=0.0):
    i, _ = _seq(phrase, after)
    return WORDS[i][1]


def end(phrase, after=0.0):
    i, n = _seq(phrase, after)
    return WORDS[i + n - 1][2]


def timeline():
    """Base layer covering 0..DUR with `talk` filling every gap, exactly as the hand-written sheets
    built it (gap > 0.40 s becomes a talk beat; a smaller gap is absorbed by the next beat)."""
    base = sorted([dict(b) for b in BEATS if b["kind"] in BASE_KINDS], key=lambda b: b["t0"])
    fixed, t = [], 0.0
    for b in base:
        b["t0"] = max(b["t0"], t)
        if b["t1"] - b["t0"] < 0.20:
            continue
        gap = b["t0"] - t
        if gap > 0.40:
            fixed.append(dict(kind="talk", t0=round(t, 3), t1=round(b["t0"], 3)))
        elif gap > 0:
            b["t0"] = t
        fixed.append(b)
        t = b["t1"]
    if DUR - t > 0.10:
        fixed.append(dict(kind="talk", t0=round(t, 3), t1=DUR))
    return fixed, [dict(o) for o in LOWER_THIRDS + CTAS + INSETS]


def push_at(t):
    """Scale of the talking-head crop at time t (1.00 wide .. PUSH_Z punched), smoothstepped ramps."""
    best = 0.0
    for a1, a2, b1, b2 in PUSHES:
        k = 1.0 if a2 <= a1 else max(0.0, min(1.0, (t - a1) / (a2 - a1)))
        ko = 0.0 if b2 <= b1 else max(0.0, min(1.0, (t - b1) / (b2 - b1)))
        r = min(k, 1 - ko)
        if t < a1:
            r = 0.0
        best = max(best, r * r * (3 - 2 * r))
    return 1.0 + (PUSH_Z - 1.0) * best


if __name__ == "__main__":
    tl, ov = timeline()
    for b in tl:
        det = b.get("media") or b.get("header") or b.get("headline") or ""
        print(f'{b["kind"]:9s} {b["t0"]:8.2f} {b["t1"]:8.2f} {b["t1"] - b["t0"]:6.2f}  {det}')
    ins = sum(b["t1"] - b["t0"] for b in tl if b["kind"] != "talk")
    talk = sum(b["t1"] - b["t0"] for b in tl if b["kind"] == "talk")
    pushed = sum(1 for i in range(int(DUR * 10)) if push_at(i / 10) > 1.05) / 10
    print(f"\n{len(tl)} base beats; insert coverage {100 * ins / DUR:.0f}%; lower thirds {len(LOWER_THIRDS)}; "
          f"CTAs {len(CTAS)}; flashes {len(FLASHES)}; pushes {len(PUSHES)}; talk {talk:.1f}s of which pushed "
          f"{pushed:.1f}s = {100 * pushed / max(talk, 1e-6):.0f}%")
