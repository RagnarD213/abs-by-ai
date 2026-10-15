#!/usr/bin/env python3
"""RA-06 round 3, Dan: "the close is looking a little off-center. Just center that close a little bit more."
Per-hold 9:16 crop centre for the land-then-hold track. Shared by s10_render06.py (import) and the dry run here.
NEAR holds: the land-then-hold track with a 1 % dead band and no 'fixed under' allowance (Dan's request for this video
overrides the 3.3 % default; the 3.3 % band let the close sit 10-24 source px off his head centre, up to 58).
FAR holds keep the standard vertical_dense preset.
  python3 round3/s10b_near_track.py      -> prints median / max offset per hold for both bands
"""
import json, os, sys
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import landing as LD
NEAR_TOL = float(os.environ.get("NEAR_TOL", "0.01"))


def centres(level, nn, rr, f0, n_, cw):
    """dense per-frame centre for one hold, plus the head track interpolated to every frame."""
    seg = [dict(n0=f0, n1=f0 + n_)]
    if level != "NEAR" or NEAR_TOL <= 0:
        dn, cen, heads, _ = LD.vertical_dense(nn, rr, seg, cw)
        return cen, heads
    tn, tx, _ = LD.track(nn, rr, seg, slope_px_s=170 * cw / 608, k=3, fixed_under=None, tolerance=NEAR_TOL * cw)
    q = np.arange(f0, f0 + n_)
    return np.interp(q, tn, tx), np.interp(q, nn, rr)


if __name__ == "__main__":
    os.chdir("/Volumes/Extreme/_edit_work/ra06")
    sys.path.insert(0, ".")
    import ra01lib as L
    A = L.Aspect("9x16"); FPS = L.FPS; fr = lambda t: int(round(t * FPS))
    B = json.load(open("beats.json"))
    S = json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"]
    for tol in (0.033, NEAR_TOL):
        NEAR_TOL = tol
        print(f"--- NEAR dead band {tol*100:.1f} % of the crop width")
        for i, p in enumerate(B["punch"]):
            it = next(x for x in B["timeline"] if x["name"] == f"dan{i:02d}")
            f0, n_ = it["f0"], it["n"]; cw = A.levels[p["level"]][0]
            sm = sorted({fr(s["t"]): s["cx"] for s in S if f0 <= fr(s["t"]) < f0 + n_}.items())
            nn = np.array([k for k, _ in sm]); rr = np.array([v for _, v in sm], float)
            cen, heads = centres(p["level"], nn, rr, f0, n_, cw)
            cen = np.clip(cen, cw / 2, 2160 - cw / 2); off = np.abs(heads - cen)
            trav = np.abs(np.diff(cen)).sum()
            print(f"  hold {i} {p['level']:<4} {p['beat'][0]:6.2f}-{p['beat'][1]:6.2f}  off median {np.median(off):5.1f} px "
                  f"({np.median(off)/cw*100:4.2f} %)  max {off.max():5.1f}  crop travel {trav:5.1f} px")
