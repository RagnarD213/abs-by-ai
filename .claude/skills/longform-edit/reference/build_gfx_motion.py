#!/usr/bin/env python3
"""Render every graphic in spec.G to an alpha QTRLE .mov.

Alpha MOVs rather than PNGs because these are ANIMATED -- the whole point of the
rebuild. QTRLE is used because libx264 cannot carry an alpha channel and
pre-multiplying against a guessed background is how graphics get grey fringes.
"""
import os, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
os.environ["MOTIONLIB_FFMPEG"] = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
import motionlib as M
import spec
from concurrent.futures import ThreadPoolExecutor

OUT = "gfx"; os.makedirs(OUT, exist_ok=True)
P = M.MIL

def build(g):
    start, dur, kind, key, pl = g
    dst = f"{OUT}/{key}.mov"
    if os.path.exists(dst) and os.path.getsize(dst) > 5000: return key + " [cached]"
    if kind == "title":
        M.title_plate(dst, pl["h"], pl.get("sub"), dur, pal=P)
    elif kind == "section":
        M.section_label(dst, pl["n"], pl["t"], dur, pal=P)
    elif kind == "stack":
        M.stack_build(dst, pl["items"], dur, pal=P, head=pl.get("head"))
    elif kind == "lower":
        M.lower_third_bar(dst, pl["lines"], dur, pal=P, size=46, lead_size=52,
                          bar_color=P.accent, plate=(10, 11, 9))
    elif kind == "number":
        M.number_pop(dst, pl["text"], dur, pal=P, size=230, xy=(M.W // 2, int(M.H * 0.46)))
    elif kind == "endcard":
        return key + " [built with the inserts -- it carries video]"
    else:
        raise SystemExit("unknown graphic kind " + kind)
    return key

if __name__ == "__main__":
    todo = [g for g in spec.G if g[2] != "endcard"]
    with ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(build, todo): print(" ", r)
    print(f"{len(todo)} graphics -> {OUT}/")
