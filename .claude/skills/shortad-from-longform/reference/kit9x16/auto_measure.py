#!/usr/bin/env python3
"""MEASUREMENT for auto_content.py: where did the editor put something over Dan's graded raw picture?

For every frame of his master (decoded BT.709) this renders the matching raw frame through the recovered audio EDL
and grade.py, fits his framing (scale + offset: his punch-ins and his window crops) and scores how well the two
pictures agree -- over a head/torso box and cell by cell. Where the master stops agreeing with Dan's graded raw
picture, the editor added something (a graphic, a photo, b-roll, a lower third, a CTA pill).

  python3 auto_measure.py --build B --master his.mp4 --edl edl_final.json --raw ROLL [--rolls rolls.json] --grade grade.py

Writes (all under B/auto/):
  m256.rgb, r_<roll>.rgb      256x144 rgb24 caches (master; each raw roll graded)
  framing.json                the framing fit samples: n, r, s, dx, dy, box
  frames.npz                  per master frame: r_box (NCC over the fitted box), k (raw frame), cells (9x16 match
                              scores), luma, cut (scene-change score), box id
No model anywhere. Numbers are calibrated on Ad 10 and Ad 1 (auto_content README section)."""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")
W, H = 256, 144
FPS = 30000 / 1001
BOXES = {"c": (64, 166, 8, 112), "r": (150, 252, 8, 112), "l": (4, 106, 8, 112)}   # x0, x1, y0, y1 at 256x144
SCALES = np.round(np.arange(1.00, 1.84, 0.04), 3)


def probe(path):
    o = subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate,nb_frames,duration",
                        "-of", "json", path], capture_output=True, text=True).stdout
    s = json.loads(o)["streams"][0]
    a, b = s["r_frame_rate"].split("/")
    return float(a) / float(b), int(s.get("nb_frames") or 0), float(s.get("duration") or 0)


def load_grade(path):
    spec = importlib.util.spec_from_file_location("grade_mod", path)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


def decode(src, out, vf_pre="", graded_chain=None):
    """src -> WxH rgb24 raw frames. Master: BT.709 in. Raw: scaled first, then HIS grade chain, then BT.709 -> rgb."""
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return
    if graded_chain:
        vf = f"scale={W}:{H}:flags=area:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,{graded_chain}," \
             f"scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
    else:
        vf = f"scale={W}:{H}:flags=area:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24"
    tmp = out + ".part"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", src, "-an", "-vf", vf, "-f", "rawvideo", tmp], check=True)
    os.replace(tmp, out)


def mm(path):
    n = os.path.getsize(path) // (W * H * 3)
    return np.memmap(path, np.uint8, "r").reshape(n, H, W, 3)


def load_edl(path):
    E = json.load(open(path))
    out = []
    for s in E:
        out.append(dict(cut_in=float(s["cut_in"]), cut_out=float(s["cut_out"]), src_in=float(s["src_in"]), roll=s.get("roll")))
    return out


def gray(a):
    return cv2.cvtColor(np.ascontiguousarray(a), cv2.COLOR_RGB2GRAY)


def ncc(a, b):
    a = a.astype(np.float32).ravel(); b = b.astype(np.float32).ravel()
    a -= a.mean(); b -= b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 1e-3 else 0.0


def fit_one(Mg, Rg, boxes=("c", "r", "l"), scales=SCALES):
    """Best (r, s, dx, dy, box) placing a master box inside the scaled raw frame. master(x,y) = s*raw(x',y') - (dx,dy)."""
    best = (-1.0, 1.0, 0.0, 0.0, "c")
    for bk in boxes:
        x0, x1, y0, y1 = BOXES[bk]
        T = Mg[y0:y1, x0:x1]
        if T.std() < 4:
            continue
        for s in scales:
            Rs = cv2.resize(Rg, (int(round(W * s)), int(round(H * s))), interpolation=cv2.INTER_LINEAR)
            if Rs.shape[0] < T.shape[0] or Rs.shape[1] < T.shape[1]:
                continue
            res = cv2.matchTemplate(Rs, T, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(res)
            if mx > best[0]:
                best = (float(mx), float(s), float(loc[0] - x0), float(loc[1] - y0), bk)
    return best


def warp(R, s, dx, dy):
    M = np.float32([[s, 0, -dx], [0, s, -dy]])
    return cv2.warpAffine(np.ascontiguousarray(R), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def cell_scores(Mg, Wg):
    """9x16 grid of 16x16 cells: NCC where textured, 1 - |mean diff|/40 where both are flat (vectorised)."""
    a = Mg.astype(np.float32).reshape(9, 16, 16, 16).transpose(0, 2, 1, 3).reshape(9, 16, 256)
    b = Wg.astype(np.float32).reshape(9, 16, 16, 16).transpose(0, 2, 1, 3).reshape(9, 16, 256)
    am_, bm_ = a.mean(-1, keepdims=True), b.mean(-1, keepdims=True)
    ac, bc = a - am_, b - bm_
    sa, sb = np.sqrt((ac * ac).mean(-1)), np.sqrt((bc * bc).mean(-1))
    n = (ac * bc).mean(-1) / np.maximum(sa * sb, 1e-6)
    flat = (sa < 3) & (sb < 3)
    return np.where(flat, np.maximum(0.0, 1 - np.abs(am_[..., 0] - bm_[..., 0]) / 40), n).astype(np.float32)


def frac_at(Mg, arr, k, f, span=3):
    """Best whole-frame cell-match fraction over raw frames k-span..k+span at framing f -> (frac, kk, cells)."""
    best = (-1.0, k, None)
    for kk in range(k - span, k + span + 1):
        if 0 <= kk < len(arr):
            c = cell_scores(Mg, warp(gray(arr[kk]), f[1], f[2], f[3]))
            fr = float((c > 0.5).mean())
            if fr > best[0]:
                best = (fr, kk, c)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--master", required=True)
    ap.add_argument("--edl", required=True)
    ap.add_argument("--raw", help="the single raw roll (or give --rolls)")
    ap.add_argument("--rolls", help="json {roll_name: path} for a multi-roll EDL")
    ap.add_argument("--grade", required=True)
    ap.add_argument("--step", type=int, default=3, help="framing-fit sample spacing in frames")
    a = ap.parse_args()
    A = os.path.join(a.build, "auto")
    os.makedirs(A, exist_ok=True)
    g = load_grade(a.grade)
    chain = g.CURVES
    mfps, mn, mdur = probe(a.master)
    decode(a.master, os.path.join(A, "m256.rgb"))
    rolls = json.load(open(a.rolls)) if a.rolls else {None: a.raw}
    R = {}
    for name, path in rolls.items():
        tag = os.path.splitext(os.path.basename(path))[0]
        rp = os.path.join(A, f"r_{tag}.rgb")
        decode(path, rp, graded_chain=chain)
        R[name] = (mm(rp), probe(path)[0])
    M = mm(os.path.join(A, "m256.rgb"))
    N = len(M)
    E = load_edl(a.edl)
    starts = np.array([e["cut_in"] for e in E])

    def raw_of(n):
        t = n / mfps
        i = max(0, int(np.searchsorted(starts, t + 1e-6)) - 1)
        e = E[i]
        roll = e["roll"] if e["roll"] in R else next(iter(R))
        arr, rf = R[roll]
        k = int(round((e["src_in"] + t - e["cut_in"]) * rf))
        return roll, min(max(k, 0), len(arr) - 1), i

    # ---- scene-change score on the master (cuts between his shots and inside insert montages)
    small = np.stack([cv2.resize(gray(M[n]), (64, 36), interpolation=cv2.INTER_AREA) for n in range(N)]).astype(np.float32)
    cut = np.zeros(N, np.float32)
    cut[1:] = np.abs(small[1:] - small[:-1]).mean(axis=(1, 2))
    luma = small.mean(axis=(1, 2))

    # ---- framing fit, sampled. A candidate framing is judged by the WHOLE-FRAME cell agreement it produces
    #      (a box NCC alone passes a wrong framing on a plain background: 0.82 on the fridge, Ad 10 4.5 s).
    fits = []
    prev = None
    prev_fr = 0.0
    koff = 0                 # his picture's offset from the audio EDL: he HOLDS a take across an audio splice (A12.2)
    for n in range(0, N, a.step):
        roll, k0, _ = raw_of(n)
        arr = R[roll][0]
        k = min(max(k0 + koff, 0), len(arr) - 1)
        Mg = gray(M[n])
        same_shot = prev is not None and cut[max(1, n - a.step + 1):n + 1].max() < 6.0
        if prev is not None:
            fr, kk, _ = frac_at(Mg, arr, k, prev, span=2)
            if fr >= 0.75 or (same_shot and prev_fr < 0.35 and fr < 0.35):
                fits.append(dict(n=n, frac=round(fr, 3), s=prev[1], dx=prev[2], dy=prev[3], box=prev[4], k=kk,
                                 koff=kk - k0, reuse=True))
                prev_fr = fr
                continue
        Mh = cv2.resize(Mg, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
        Rh = cv2.resize(gray(arr[k]), (W // 2, H // 2), interpolation=cv2.INTER_AREA)
        cands = []
        for bk in ("c", "r", "l"):
            x0, x1, y0, y1 = (v // 2 for v in BOXES[bk])
            T = Mh[y0:y1, x0:x1]
            if T.std() < 4:
                continue
            bb = (-1.0,)
            for s_ in SCALES:
                Rs = cv2.resize(Rh, (int(round(W // 2 * s_)), int(round(H // 2 * s_))), interpolation=cv2.INTER_LINEAR)
                res = cv2.matchTemplate(Rs, T, cv2.TM_CCOEFF_NORMED)
                _, mx, _, loc = cv2.minMaxLoc(res)
                if mx > bb[0]:
                    bb = (float(mx), float(s_), float(2 * (loc[0] - x0)), float(2 * (loc[1] - y0)), bk)
            if bb[0] >= 0.45:
                fine = np.round(np.arange(bb[1] - 0.04, bb[1] + 0.041, 0.01), 3)
                cands.append(fit_one(Mg, gray(arr[k]), boxes=(bk,), scales=fine))
        if prev is not None:
            cands.append(prev)
        best, best_fr, best_k = (0.0, 1.0, 0.0, 0.0, "c"), -1.0, k
        for c_ in cands:
            for kc in {k, k0}:
                fr, kk, _ = frac_at(Mg, arr, kc, c_, span=3)
                if fr > best_fr:
                    best, best_fr, best_k = c_, fr, kk
        # still poor: is it a held take? search ~2 s of raw either side with the candidate framings
        if best_fr < 0.5 and cands and not (same_shot and prev_fr < 0.35):
            for c_ in cands:
                for dk in range(-60, 61, 3):
                    kc = k0 + dk
                    if 0 <= kc < len(arr):
                        fr, kk, _ = frac_at(Mg, arr, kc, c_, span=1)
                        if fr > best_fr + 0.12 and fr >= 0.45:
                            best, best_fr, best_k = c_, fr, kk
        koff = best_k - k0 if best_fr >= 0.45 else koff
        fits.append(dict(n=n, frac=round(best_fr, 3), s=best[1], dx=best[2], dy=best[3], box=best[4], k=best_k,
                         koff=best_k - k0, reuse=False))
        prev, prev_fr = best, best_fr
    json.dump(fits, open(os.path.join(A, "framing.json"), "w"))

    # ---- per frame: the nearest sample's framing (or the next one's, whichever agrees better), best raw frame +-3
    fs = {f["n"]: f for f in fits}
    frac = np.zeros(N, np.float32); ks = np.zeros(N, np.int32); cells = np.zeros((N, 9, 16), np.float32)
    boxid = np.zeros(N, np.int8); scl = np.zeros(N, np.float32); r_box = np.zeros(N, np.float32)
    bmap = {"c": 0, "r": 1, "l": 2}
    for n in range(N):
        roll, k, _ = raw_of(n)
        arr = R[roll][0]
        Mg = gray(M[n])
        base = n - n % a.step
        opts = [fs[x] for x in (base, base + a.step) if x in fs]
        # his pushes are RAMPS (Ad 1 opens on a 1.09 -> 1.26 zoom; windows push slowly): between two samples the
        # framing is interpolated, never held
        if len(opts) == 2 and n != base and opts[0]["box"] == opts[1]["box"]:
            w_ = (n - base) / a.step
            opts.append(dict(box=opts[0]["box"], **{q: (1 - w_) * opts[0][q] + w_ * opts[1][q] for q in ("s", "dx", "dy")}))
        best = (-1.0, k, None, opts[0])
        offs = {0} | {int(f_.get("koff", 0)) for f_ in (fs.get(base), fs.get(base + a.step)) if f_}
        for f in opts:
            for o_ in offs:
                kc = min(max(k + o_, 0), len(arr) - 1)
                fr, kk, c = frac_at(Mg, arr, kc, (0, f["s"], f["dx"], f["dy"], f["box"]), span=3)
                if fr > best[0]:
                    best = (fr, kk, c, f)
        frac[n], ks[n], cells[n] = best[0], best[1], best[2]
        f = best[3]
        boxid[n] = bmap[f["box"]]; scl[n] = f["s"]
        x0, x1, y0, y1 = BOXES[f["box"]]
        r_box[n] = ncc(Mg[y0:y1, x0:x1], warp(gray(arr[best[1]]), f["s"], f["dx"], f["dy"])[y0:y1, x0:x1])
    np.savez_compressed(os.path.join(A, "frames.npz"), frac=frac, r_box=r_box, k=ks, cells=cells, luma=luma, cut=cut, box=boxid,
                        scale=scl, fps=mfps)
    vis = (frac >= 0.5).mean()
    print(f"auto_measure: {N} frames, {len(fits)} framing samples ({sum(1 for f in fits if f['reuse'] is False)} full searches); "
          f"Dan's graded raw picture visible on {100 * vis:.1f}% of frames -> {A}/frames.npz")


if __name__ == "__main__":
    main()
