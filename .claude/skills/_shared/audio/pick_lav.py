#!/usr/bin/env python3
"""WHICH TRACK IS THE LAV? Measured per file, never assumed.

  python3 pick_lav.py <roll or master> [--ss S] [--t D] [--out audio_source.json] [--analyse]

Every Jeff roll carries two DIFFERENT microphones: the 8/3 and 8/14 rolls as a hard-panned
2-channel stream (lav right, far mic left, 7.4-7.9 ms late, polarity inverted on 8/14), the
8/28 rolls as FOUR mono streams (lav a:1, far mic a:0, a:2/a:3 silent). "Right channel" was
written into four SKILL.md files and was still bypassed by code, and on the 8/28 rolls
`pan=mono|c0=c1` takes the FAR mic or renders silence. So this script probes every stream and
every channel, cross-correlates all live candidates within +/-20 ms, scores arrival time,
post-word decay, floor and clipping, and writes `<file>.audio_source.json`:

  { "map": "0:a:1", "filter": "pan=mono|c0=c0", "fc_label": "[0:a:1]", "lav": {...}, "far": {...},
    "delay_ms": 7.2, "polarity": "inverted", "verdict": "two-mics" }

Every build script reads that JSON; NO script hardcodes `c0=c1` again.
Exit 0 = decided. Exit 2 = AMBIGUOUS or nothing live: refuse, do not guess.

Verdicts: two-mics (one earlier/cleaner/drier candidate), single-live (only one channel has
signal -- the ab-wheel 8/14 rolls, dead left input), dual-mono (channels near-identical at
lag 0: a true mono/stereo master -> take the mid), ambiguous.
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

SILENT_DB = -60.0        # a candidate below this rms is a dead input
DUAL_MONO_CORR = 0.98    # at lag 0 -> same signal, not two mics


def candidates(path, ss, dur):
    out = []
    for s in C.probe_audio(path):
        for ch in range(s["channels"]):
            x = C.pcm(path, af=f"pan=mono|c0=c{ch}", ss=ss, dur=dur, amap=f"0:a:{s['a']}")
            if len(x) < C.SR * 2: continue
            rms = float(10 * np.log10((x ** 2).mean() + 1e-15))
            bands, floor, dry, _ = C.analyse(x) if rms > SILENT_DB else (None, None, float("nan"), None)
            out.append(dict(stream=s["a"], channel=ch, nch=s["channels"], rms_db=round(rms, 1),
                            live=rms > SILENT_DB,
                            snr_db=round(C.snr(x), 1) if rms > SILENT_DB else None,
                            dryness_db=round(dry, 2) if rms > SILENT_DB else None,
                            edt_ms=round(C.edt(x), 1) if rms > SILENT_DB else None,
                            clipped=int((np.abs(x) >= 0.999).sum()), _x=x))
    return out


def decide(cands):
    live = [c for c in cands if c["live"]]
    if not live: return None, None, dict(verdict="no-signal", why="every channel is below -60 dBFS")
    if len(live) == 1:
        return live[0], None, dict(verdict="single-live", why="only one channel carries signal")
    # pairwise lag search among the live candidates
    pairs = []
    for i in range(len(live)):
        for j in range(i + 1, len(live)):
            peak, lag, zero = C.xcorr(live[i]["_x"], live[j]["_x"])
            pairs.append(dict(a=i, b=j, peak=round(peak, 3), lag=lag, lag_ms=round(lag / C.SR * 1000, 2),
                              zero_lag=round(zero, 3)))
    # dual-mono: the two loudest are the same signal at lag 0
    loud = sorted(range(len(live)), key=lambda k: -live[k]["rms_db"])[:2]
    pr = next(p for p in pairs if {p["a"], p["b"]} == set(loud))
    if pr["lag"] == 0 and pr["zero_lag"] >= DUAL_MONO_CORR and live[loud[0]]["stream"] == live[loud[1]]["stream"]:
        return live[loud[0]], live[loud[1]], dict(verdict="dual-mono", pairs=pairs,
                                                   why=f"channels correlate {pr['zero_lag']:+.3f} at lag 0 -- one signal")
    # score: arrival (earliest by lag against every other live candidate), SNR, dryness
    pts = {k: 0 for k in range(len(live))}
    for p in pairs:
        # lag > 0 means a LAGS b (a arrives later)
        if abs(p["lag"]) >= 24:                     # 0.5 ms: a real path difference
            earlier = p["b"] if p["lag"] > 0 else p["a"]; pts[earlier] += 1
    snr_best = max(range(len(live)), key=lambda k: live[k]["snr_db"]); pts[snr_best] += 1
    dry_best = max(range(len(live)), key=lambda k: live[k]["dryness_db"]); pts[dry_best] += 1
    ranked = sorted(pts, key=lambda k: -pts[k])
    win, second = ranked[0], ranked[1]
    if pts[win] == pts[second]:
        return None, None, dict(verdict="ambiguous", pairs=pairs, points={str(k): v for k, v in pts.items()},
                                why="no candidate wins on arrival + floor + decay -- measure by hand")
    far = second
    pr = next(p for p in pairs if {p["a"], p["b"]} == {win, far})
    lag_win_vs_far = pr["lag"] if pr["a"] == win else -pr["lag"]     # >0 = lav lags far (should be <0)
    return live[win], live[far], dict(verdict="two-mics", pairs=pairs, points={str(k): v for k, v in pts.items()},
                                      delay_ms=round(-lag_win_vs_far / C.SR * 1000, 2),
                                      polarity="inverted" if pr["peak"] < 0 else "normal",
                                      pair_corr=pr["peak"],
                                      why=f"earlier by {abs(lag_win_vs_far)/C.SR*1000:.2f} ms, "
                                          f"SNR {live[win]['snr_db']} vs {live[far]['snr_db']} dB, "
                                          f"decay {live[win]['dryness_db']} vs {live[far]['dryness_db']} dB")


def strip(c):
    return {k: v for k, v in c.items() if k != "_x"} if c else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--ss", type=float); ap.add_argument("--t", type=float)
    ap.add_argument("--out"); ap.add_argument("--analyse", action="store_true", help="print only, write nothing")
    A = ap.parse_args()
    d = C.duration(A.file)
    ss = A.ss if A.ss is not None else max(2.0, min(d * 0.25, 120.0))
    dur = A.t if A.t is not None else max(5.0, min(45.0, d - ss - 1.0))
    cands = candidates(A.file, ss, dur)
    print(f"pick_lav  {os.path.basename(A.file)}  {d:.1f} s  window {ss:.0f}s +{dur:.0f}s  "
          f"{len(C.probe_audio(A.file))} audio stream(s)")
    print(f"  {'stream':6s} {'ch':>2s} {'rms dBFS':>9s} {'SNR':>6s} {'decay':>6s} {'EDT':>6s} {'clip':>6s}")
    for c in cands:
        print(f"  a:{c['stream']:<4d} {c['channel']:>2d} {c['rms_db']:>9.1f} "
              f"{(str(c['snr_db']) if c['live'] else '-'):>6s} {(str(c['dryness_db']) if c['live'] else '-'):>6s} "
              f"{(str(c['edt_ms']) if c['live'] else '-'):>6s} {c['clipped']:>6d}{'' if c['live'] else '   (silent)'}")
    lav, far, info = decide(cands)
    for p in info.get("pairs", []):
        a, b = [c for c in cands if c["live"]][p["a"]], [c for c in cands if c["live"]][p["b"]]
        print(f"  a:{a['stream']}c{a['channel']} vs a:{b['stream']}c{b['channel']}: peak {p['peak']:+.3f} at "
              f"{p['lag_ms']:+.2f} ms (zero-lag {p['zero_lag']:+.3f})")
    res = dict(file=os.path.abspath(A.file), duration=round(d, 3), window=[ss, dur],
               candidates=[strip(c) for c in cands], verdict=info["verdict"], why=info["why"],
               lav=strip(lav), far=strip(far), delay_ms=info.get("delay_ms"), polarity=info.get("polarity"),
               pair_corr=info.get("pair_corr"), version=C.STAMP_VERSION)
    if lav is None:
        print(f"\n  REFUSED: {info['verdict']} -- {info['why']}")
        sys.exit(2)
    if info["verdict"] == "dual-mono":
        res["map"] = f"0:a:{lav['stream']}"; res["filter"] = "pan=mono|c0=0.5*c0+0.5*c1"
    else:
        res["map"] = f"0:a:{lav['stream']}"; res["filter"] = f"pan=mono|c0=c{lav['channel']}"
    res["fc_label"] = f"[{res['map']}]"
    print(f"\n  {info['verdict'].upper()}: {info['why']}")
    print(f"  LAV = stream a:{lav['stream']} channel {lav['channel']}   ->   -map {res['map']} -af \"{res['filter']}\"")
    if far: print(f"  far = a:{far['stream']} c{far['channel']}  delay {res['delay_ms']} ms  polarity {res['polarity']}")
    if not A.analyse:
        out = A.out or C.source_json_path(A.file)
        json.dump(res, open(out, "w"), indent=1); print(f"  wrote {out}")


if __name__ == "__main__": main()
