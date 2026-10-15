#!/usr/bin/env python3
"""RA-04 round 4: land, then hold (VIDEO-RULES 2026-10-03, locked 10-05) on the 9:16.
round4/landing_check.json measured his head 3.5-20.8 % of the crop width off the fixed centre in 11 of 14 holds, so the fixed
per-hold crops of rounds 1-3 are replaced by RA-15 round 3's track: _shared/cut/landing.py with the standard's 20 px band (3.3 % of 608) and RA-14's
170 px/s follow, plus RA-15's Gaussian ease (sigma 8 frames). RA-15's slower 70 px/s / 52 px left four holds 6.1-12 % off centre at
the median (gate framing:centering bound 6 %); 170/20 puts every hold at 5.3 % or under, the landing frame exactly on him. Samples: framing.json (5 Hz) + framing_holdstart.json
(exact first and last frame of every hold). Writes punch[i]["track"] (one centre per output frame) into beats.json; the 16:9 keeps
its fixed cx16 (horizontal stays static, 2026-09-17). Idempotent: reads round4/backup/beats.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
import landing, ra01lib as L
B = json.load(open("round4/beats_r4base.json"))   # round 3 plan + the r4_home.py re-timing
SAM = sorted(json.load(open("framing.json"))["samples"] + json.load(open("framing_holdstart.json"))["samples"], key=lambda x: x["t"])
FPSX = 30000/1001; frx = lambda t: int(round(t*FPSX))
CW = {k: v[0] for k, v in L.Aspect("9x16").levels.items()}
punch = B["punch"]; items = {it["name"]: it for it in B["timeline"]}
# 9:16 watch-pass judge 2 (round 4 b): dan03 and dan09 panned 326 / 178 output px from their first frame (he sways ~36 % of the NEAR
# width in 1.6 s). Both sit between two cards (no zoom cut either side), so they go FAR, followed at 140 px/s, 25 px band: ~19 % less
# pan, median off centre 4.0 / 4.9 %. Slower follows put him 6-10 % off centre (gate bound 6 %).
# per-hold level override "i:LEVEL,..." (env HOLD_LEVEL): only for a hold with a card on BOTH sides (no zoom cut to keep)
for k, v in (x.split(":") for x in os.environ.get("HOLD_LEVEL", "3:FAR,9:FAR").split(",") if x):
    i = int(k); tl = B["timeline"]; j = next(n for n, it in enumerate(tl) if it["name"] == f"dan{i:02d}")
    assert tl[j-1]["kind"] == "card" and tl[j+1]["kind"] == "card", (i, "a level change here would make a same-size join")
    print(f"dan{i:02d} level {punch[i]['level']} -> {v}"); punch[i]["level_r3"] = punch[i]["level"]; punch[i]["level"] = v
_sn = np.array([frx(x["t"]) for x in SAM]); _sx = np.array([x["cx"] for x in SAM], float)
_o = np.argsort(_sn, kind="stable"); _sn, _sx = _sn[_o], _sx[_o]
_u = np.concatenate([[True], np.diff(_sn) > 0]); _sn, _sx = _sn[_u], _sx[_u]
_SL, _TOL, _SIG = (float(v) for v in os.environ.get("TRACK", "170,20,8").split(","))
for lvl in ("NEAR", "FAR"):
    idx = [i for i, p in enumerate(punch) if p["level"] == lvl]
    segs_l = [{"n0": items[f"dan{i:02d}"]["f0"], "n1": items[f"dan{i:02d}"]["f1"]} for i in idx]
    n_all, x_all, _ = landing.track(_sn, _sx, segs_l, slope_px_s=_SL*CW[lvl]/608, k=3, fixed_under=_TOL*CW[lvl]/608,
                                    fps=FPSX, tolerance=_TOL*CW[lvl]/608)
    n_all, x_all = np.asarray(n_all), np.asarray(x_all)
    # per-hold override "i:slope,band,sigma;..." (env HOLD_TRACK). Default: the CTA hold (dan14) at 100 px/s, 35 px band, sigma 12: the
    # 9:16 watch-pass judge called its 170/20 sway (169 src px of back-and-forth under the CTA) the least justified follow; this cuts
    # travel to 120 px and peak speed 87 -> 51 px/s, median off-centre 4.9 % (a fixed crop: 6.4 %, over the gate's 6 %): the hold gets its own landing.track run with those settings
    OVR = {int(k): tuple(float(v) for v in vs.split(",")) for k, vs in (x.split(":") for x in os.environ.get("HOLD_TRACK", "3:140,25,10;9:140,25,10;14:100,35,12").split(";") if x)}
    for i, sg in zip(idx, segs_l):
        if i in OVR:
            sl, tol, _ = OVR[i]
            n_all_i, x_all_i, _ = landing.track(_sn, _sx, [sg], slope_px_s=sl*CW[lvl]/608, k=3, fixed_under=tol*CW[lvl]/608, fps=FPSX, tolerance=tol*CW[lvl]/608)
        else:
            n_all_i, x_all_i = n_all, x_all
        _SIG_h = OVR[i][2] if i in OVR else _SIG
        m = (np.asarray(n_all_i) >= sg["n0"]) & (np.asarray(n_all_i) < sg["n1"]); fr_ = np.arange(sg["n0"], sg["n1"])
        n_ai, x_ai = np.asarray(n_all_i), np.asarray(x_all_i)
        cxf = np.interp(fr_, n_ai[m], x_ai[m]) if m.sum() > 1 else np.full(len(fr_), float(x_ai[m][0]) if m.any() else punch[i]["cx"])
        if _SIG_h > 0 and len(cxf) > 3:
            _k = np.arange(-3*int(_SIG_h), 3*int(_SIG_h)+1); _w = np.exp(-_k**2/(2*_SIG_h**2)); _w /= _w.sum()
            _c0 = cxf[0]; cxf = np.convolve(np.pad(cxf, (len(_k)//2, len(_k)//2), mode="edge"), _w, "valid")
            cxf = cxf - (cxf[0] - _c0)*np.exp(-np.arange(len(cxf))/_SIG_h)
        cxf = np.clip(cxf, CW[lvl]/2, 2160 - CW[lvl]/2)
        head = np.interp(fr_, _sn, _sx)
        p = punch[i]; assert len(cxf) == p["frames"] == items[f"dan{i:02d}"]["n"], (i, len(cxf), p["frames"])
        p["cx_fixed_r3"] = p["cx"]; p["track"] = [round(float(v), 2) for v in cxf]; p["cx"] = round(float(cxf[0]), 1)
        off = np.abs(head - cxf)/CW[lvl]*100; sp = np.abs(np.diff(cxf))*FPSX if len(cxf) > 1 else np.zeros(1)
        p.update(track_travel_px=round(float(np.abs(np.diff(cxf)).sum()), 1), landing_err_px=round(float(abs(head[0] - cxf[0])), 1),
                 off_centre_pct_med=round(float(np.median(off)), 2), off_centre_pct_max=round(float(off.max()), 2),
                 pan_p90_px_s=round(float(np.percentile(sp, 90)), 1), moving_frac=round(float((sp > 5*CW[lvl]/608).mean()), 3),
                 track_max_px_s=round(float(sp.max()), 1), track_settings=list(OVR.get(i, (_SL, _TOL, _SIG))))
        print(f"dan{i:02d} {lvl:4} n={len(cxf):3d} land_err {p['landing_err_px']:5.1f}  off med {p['off_centre_pct_med']:5.2f}% max {p['off_centre_pct_max']:5.2f}%"
              f"  travel {p['track_travel_px']:6.1f}  p90 {p['pan_p90_px_s']:6.1f} px/s  max {p['track_max_px_s']:6.1f}  moving {p['moving_frac']:.2f}"
              f"  (fixed r3 off max {np.abs(head - p['cx_fixed_r3']).max()/CW[lvl]*100:5.2f}%)")
# 16:9 (static, one centre): round 3 moved dan08 to cx16 1078 and dan09 followed it, 10 source px off every other hold (1088), a small
# sideways hop on the dan07 -> dan08 zoom cut. One centre for the whole film.
for i, p in enumerate(punch):
    if abs(p.get("cx16", 1088.0) - 1088.0) > 0.5: print(f"dan{i:02d} cx16 {p['cx16']} -> 1088.0"); p["cx16_r3"] = p["cx16"]; p["cx16"] = 1088.0
if not os.environ.get("DRY"): json.dump(B, open("beats.json", "w"), indent=2)
print("beats.json: track on", sum("track" in p for p in punch), "holds")
