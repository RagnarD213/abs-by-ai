#!/usr/bin/env python3
"""RECOVER HIS EDIT from the finished master and Dan's raw roll(s), with no editing session (skill Step 1 as one script).

  python3 kit_recover.py --build B --master his.mp4 [--raw ROLL ...] [--shoot SHOOT_DIR ...]

Stages (each cached in B; delete a file to redo its stage):
  words    B/m.whisper.json      his master transcribed (local Whisper small, word timestamps)
  rolls    B/rolls.json          which raw roll(s) he cut from: word alignment against each candidate roll's
                                 transcript (the footage index's <roll>.roll/words.json, else Whisper), >= 95 % of his
                                 words must land or the job escalates (wrong shoot)
  audio    B/his_mix16.wav, B/lav16_<roll>.wav   16 kHz mono; the lav by the roll index's pick_lav verdict
  profile  B/offset_profile.json  dense acoustic offset (0.1 s hops, 0.7 s windows, GCC-PHAT: his mix is EQ'd and
                                 compressed, plain correlation locks at ~0.6, PHAT at ~0.75+; skill A7)
  edl      B/edl_final.json      runs of constant offset -> segments; every boundary in a gap of HIS words
  grade    B/his.cube, B/grade.py  his look as a 33^3 LUT fitted from matched pixels (BT.709 decode both sides,
                                 centre of frame only), + SUBJECT_CX from his framing. The kit draws its own vignette.
Writes B/recover_report.json: coverage, profile lock, segment count, grade fit error. No model anywhere.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
SR = 16000
LOCK = 0.30          # plain correlation at the found lag that counts as a lock (his mix has a music bed under it)
PY = sys.executable


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def norm_w(w):
    return "".join(c for c in w.lower().replace("'", "").replace("’", "") if c.isalnum())


# ------------------------------------------------------------------------------------------------ words
def transcribe(src, out):
    if os.path.exists(out):
        return
    import whisper
    tmp = out + ".16k.wav"
    wav16(src, tmp)                                   # our own ffmpeg: whisper's loader wants one on PATH
    audio = rd(tmp).astype(np.float32)
    m = whisper.load_model("small")
    r = m.transcribe(audio, word_timestamps=True, language="en", fp16=False)
    os.remove(tmp)
    json.dump(r, open(out, "w"))


def words_of(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "segments" in d:
        W = [(w["word"].strip(), float(w["start"]), float(w["end"])) for s in d["segments"] for w in s.get("words", [])]
    elif isinstance(d, dict) and "words" in d:
        W = [(w["word"].strip(), float(w["start"]), float(w["end"])) for w in d["words"]]
    else:
        W = [((w.get("word") or w.get("w")).strip(), float(w.get("start", w.get("t"))), float(w.get("end", w.get("e")))) for w in d]
    return [(norm_w(w), a, b) for w, a, b in W if norm_w(w)]


def align(A, B):
    """Needleman-Wunsch, monotonic: gaps in the ROLL are cheap (it is full of unused takes), gaps in HIS cut are dear.
    -> list of (i_his, j_roll) matched pairs."""
    n, m = len(A), len(B)
    GA, GB, MATCH, MISS = -3.0, -0.05, 2.0, -2.0
    S = np.zeros((n + 1, m + 1), np.float32)
    P = np.zeros((n + 1, m + 1), np.int8)
    S[1:, 0] = GA * np.arange(1, n + 1)
    S[0, 1:] = GB * np.arange(1, m + 1)
    P[1:, 0] = 1; P[0, 1:] = 2
    bw = np.array([b for b in B])
    for i in range(1, n + 1):
        eq = np.where(bw == A[i - 1], MATCH, MISS).astype(np.float32)
        diag = S[i - 1, :-1] + eq
        up = S[i - 1, 1:] + GA
        best = np.maximum(diag, up)
        src = np.where(diag >= up, 0, 1).astype(np.int8)
        row = np.empty(m + 1, np.float32); row[0] = S[i, 0]
        # left moves (gaps in his cut side = skipping roll words) are sequential
        for j in range(1, m + 1):
            v = best[j - 1]; s = src[j - 1]
            l = row[j - 1] + GB
            if l > v:
                v, s = l, 2
            row[j] = v; P[i, j] = s
        S[i] = row
    i, j, out = n, m, []
    while i > 0 and j > 0:
        p = P[i, j]
        if p == 0:
            if A[i - 1] == B[j - 1]:
                out.append((i - 1, j - 1))
            i -= 1; j -= 1
        elif p == 1:
            i -= 1
        else:
            j -= 1
    return out[::-1]


# ------------------------------------------------------------------------------------------------ audio
def wav16(src, out, af=None, amap=None):
    if os.path.exists(out):
        return
    cmd = [FF, "-nostdin", "-v", "error", "-y", "-i", src]
    if amap:
        cmd += ["-map", amap]
    cmd += ["-vn"] + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", out]
    run(cmd)


def rd(p):
    w = wave.open(p)
    return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768


def bp(x, lo=250, hi=4000):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def profile(H, R, cands, hop=0.10, win=0.70, search=0.6):
    """Offset of every window of his mix against one roll's lav. The candidates are EVERY place in the roll where
    his words around that moment occur (word trigrams): Dan repeats lines across takes, so the single word-aligned
    guess lands on the wrong take (Ad 10 opened 47 s off). Each candidate is searched +-search with GCC-PHAT (his mix
    is EQ'd and compressed, skill A7) and scored by the plain correlation at the found lag; the best wins."""
    HB, RB = bp(H), bp(R)
    out = []
    dur = len(H) / SR
    for t in np.arange(0, dur - win, hop):
        a = int(t * SR); hb = HB[a:a + int(win * SR)]
        if np.sqrt((H[a:a + int(win * SR)] ** 2).mean()) < 0.003:
            out.append((round(float(t), 3), None, 0.0)); continue
        best = (None, 0.0)
        for g in cands(t):
            r0 = max(0, int((t + g - search) * SR)); r1 = min(len(RB), int((t + g + win + search) * SR))
            r = RB[r0:r1]
            if len(r) < len(hb) + 10:
                continue
            N = 1 << int(np.ceil(np.log2(len(r) + len(hb))))
            X = np.fft.rfft(r, N) * np.conj(np.fft.rfft(hb, N))
            cc = np.fft.irfft(X / (np.abs(X) + 1e-9), N)[:len(r) - len(hb) + 1]
            k = int(np.argmax(cc))
            seg = r[k:k + len(hb)]
            plain = float(np.dot(seg, hb) / (np.linalg.norm(seg) * np.linalg.norm(hb) + 1e-9))
            if plain > best[1]:
                best = ((r0 + k) / SR - t, plain)
        out.append((round(float(t), 3), None if best[0] is None else round(best[0], 4), round(max(0.0, best[1]), 3)))
    return out


def candidates(Wh, RW, pairs):
    """-> cands(t): offsets of every roll occurrence of his words near t (trigrams, then bigrams), plus the aligned
    guess, deduplicated to 0.25 s."""
    from collections import defaultdict
    tri = defaultdict(list)
    for j in range(len(RW) - 2):
        tri[(RW[j][0], RW[j + 1][0], RW[j + 2][0])].append(RW[j][1])
    bi = defaultdict(list)
    for j in range(len(RW) - 1):
        bi[(RW[j][0], RW[j + 1][0])].append(RW[j][1])
    per_word = []
    for i in range(len(Wh)):
        offs = []
        if i + 2 < len(Wh):
            offs += [rt - Wh[i][1] for rt in tri.get((Wh[i][0], Wh[i + 1][0], Wh[i + 2][0]), [])]
        if not offs and i + 1 < len(Wh):
            offs += [rt - Wh[i][1] for rt in bi.get((Wh[i][0], Wh[i + 1][0]), [])]
        per_word.append(offs)
    aligned = {i: RW[j][1] - Wh[i][1] for i, j in pairs}
    ht = np.array([w[1] for w in Wh])

    def cands(t):
        lo, hi = np.searchsorted(ht, t - 2.0), np.searchsorted(ht, t + 2.7)
        c = set()
        for i in range(lo, hi):
            for o in per_word[i]:
                c.add(round(o * 4) / 4)
            if i in aligned:
                c.add(round(aligned[i] * 4) / 4)
        return sorted(c)[:12] if len(c) <= 12 else sorted(c)
    return cands


# ------------------------------------------------------------------------------------------------ edl
def build_edl(prof_by_roll, Wh, dur):
    """Runs of constant offset -> segments; boundaries moved into a gap of his own words."""
    samples = []                                      # (t, off, score, roll) best roll per hop
    tt = sorted({p[0] for pr in prof_by_roll.values() for p in pr})
    by = {r: {p[0]: p for p in pr} for r, pr in prof_by_roll.items()}
    for t in tt:
        cand = [(by[r][t][2], by[r][t][1], r) for r in by if t in by[r] and by[r][t][1] is not None]
        if cand:
            sc, off, r = max(cand)
            if sc >= LOCK:
                samples.append((t + 0.35, off, sc, r))
    runs = []
    for t, o, sc, r in samples:
        if runs and runs[-1]["roll"] == r and abs(o - np.median(runs[-1]["o"][-6:])) < 0.025:
            runs[-1]["t"].append(t); runs[-1]["o"].append(o); runs[-1]["s"].append(sc)
        else:
            runs.append(dict(t=[t], o=[o], s=[sc], roll=r))
    runs = [r for r in runs if len(r["t"]) >= 3]
    # merge neighbours with the same offset (a pause or a graphic between them)
    m = []
    for r in runs:
        if m and m[-1]["roll"] == r["roll"] and abs(np.median(m[-1]["o"]) - np.median(r["o"])) < 0.025:
            for k in ("t", "o", "s"):
                m[-1][k] += r[k]
        else:
            m.append(r)
    runs = m
    gaps = [(Wh[i][2], Wh[i + 1][1]) for i in range(len(Wh) - 1) if Wh[i + 1][1] - Wh[i][2] > 0.02]
    segs = []
    for i, r in enumerate(runs):
        segs.append(dict(roll=r["roll"], off=float(np.median(r["o"])), score=round(float(np.median(r["s"])), 3),
                         first=min(r["t"]) - 0.35, last=max(r["t"]) + 0.35))
    bounds = [0.0]
    for a, b in zip(segs[:-1], segs[1:]):
        lo, hi = a["last"] - 0.35, b["first"] + 0.35
        cand = [(g1 - g0, (g0 + g1) / 2) for g0, g1 in gaps if lo - 0.3 <= (g0 + g1) / 2 <= hi + 0.3]
        if cand:
            cut = max(cand)[1]
        else:
            cut = (a["last"] + b["first"]) / 2
        bounds.append(max(bounds[-1] + 0.1, round(cut, 3)))
    bounds.append(round(dur, 6))
    E = []
    for i, s in enumerate(segs):
        c0, c1 = bounds[i], bounds[i + 1]
        E.append(dict(i=i, cut_in=round(c0, 4), cut_out=round(c1, 4), dur=round(c1 - c0, 4),
                      src_in=round(c0 + s["off"], 4), src_out=round(c1 + s["off"], 4), score=s["score"], roll=s["roll"]))
    return E


# ------------------------------------------------------------------------------------------------ grade
def fit_grade(B, master, E, rolls, fps):
    """His look as a 3D LUT from matched pixels: auto_measure (neutral grade) gives his framing and the raw frame
    under every talk frame; the centre of the frame (no vignette, no graphics) gives colour pairs."""
    import cv2
    sys.path.insert(0, HERE)
    import auto_measure as am
    A = os.path.join(B, "auto_grade")
    os.makedirs(A, exist_ok=True)
    neutral = os.path.join(A, "grade_neutral.py")
    open(neutral, "w").write('CURVES = "null"\nSUBJECT_CX = 960\n')
    cmd = [PY, os.path.join(HERE, "auto_measure.py"), "--build", A, "--master", master, "--edl", os.path.join(B, "edl_final.json"),
           "--grade", neutral]
    if len(rolls) == 1:
        cmd += ["--raw", list(rolls.values())[0]]
    else:
        json.dump(rolls, open(os.path.join(A, "rolls.json"), "w")); cmd += ["--rolls", os.path.join(A, "rolls.json")]
    if not os.path.exists(os.path.join(A, "auto", "frames.npz")):
        run(cmd)
    Aa = os.path.join(A, "auto")
    F = json.load(open(os.path.join(Aa, "framing.json")))
    M = am.mm(os.path.join(Aa, "m256.rgb"))
    raws = {os.path.splitext(os.path.basename(p))[0]: am.mm(os.path.join(Aa, f"r_{os.path.splitext(os.path.basename(p))[0]}.rgb"))
            for p in rolls.values()}
    starts = np.array([e["cut_in"] for e in E])
    X, Y, cxs = [], [], []
    yy, xx = np.mgrid[0:am.H, 0:am.W]
    rad = np.hypot((xx - am.W / 2) / (am.W / 2), (yy - am.H / 2) / (am.H / 2))
    for f in F:
        if f.get("frac", 0) < 0.92:
            continue
        n = f["n"]
        i = max(0, int(np.searchsorted(starts, n / fps + 1e-6)) - 1)
        roll = E[i].get("roll")
        rp = rolls.get(roll) or list(rolls.values())[0]
        R = raws[os.path.splitext(os.path.basename(rp))[0]]
        k = int(f["k"])
        if not 0 <= k < len(R):
            continue
        Mt = np.float32([[f["s"], 0, -f["dx"]], [0, f["s"], -f["dy"]]])
        w = cv2.warpAffine(np.ascontiguousarray(R[k]), Mt, (am.W, am.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        c = am.cell_scores(am.gray(M[n]), am.gray(w))
        ok = np.kron(c > 0.8, np.ones((16, 16), bool)) & (rad < 0.55)
        # a flat region only: edges carry misregistration, not colour
        g = cv2.GaussianBlur(am.gray(M[n]).astype(np.float32), (0, 0), 1.0)
        edge = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)) > 25
        ok &= ~edge
        X.append(w[ok].astype(np.float32) / 255); Y.append(M[n][ok].astype(np.float32) / 255)
        if f["box"] == "c":
            cxs.append(((am.BOXES["c"][0] + am.BOXES["c"][1]) / 2 + f["dx"]) / f["s"] * (1920 / am.W))
    X = np.concatenate(X); Y = np.concatenate(Y)
    if len(X) > 3_000_000:
        sel = np.random.default_rng(0).choice(len(X), 3_000_000, replace=False); X, Y = X[sel], Y[sel]
    # global model: 3x3 + offset on a cubic per-channel basis, then a smoothed residual on a 17^3 grid
    def basis(x):
        return np.concatenate([x, x ** 2, x ** 3, np.ones((len(x), 1), np.float32)], axis=1)
    Bm = basis(X)
    coef, *_ = np.linalg.lstsq(Bm, Y, rcond=None)
    pred = Bm @ coef
    G = 17
    idx = np.clip(np.round(X * (G - 1)).astype(int), 0, G - 1)
    flat = idx[:, 0] * G * G + idx[:, 1] * G + idx[:, 2]
    cnt = np.bincount(flat, minlength=G ** 3).astype(np.float64)
    res = np.stack([np.bincount(flat, weights=(Y - pred)[:, c], minlength=G ** 3) for c in range(3)], 1)
    from scipy.ndimage import gaussian_filter
    cnt3 = gaussian_filter(cnt.reshape(G, G, G), 1.0)
    res3 = np.stack([gaussian_filter(res[:, c].reshape(G, G, G), 1.0) for c in range(3)], -1)
    resid = res3 / np.maximum(cnt3, 1e-6)[..., None]
    conf = np.clip(cnt3 / 50.0, 0, 1)[..., None]
    resid *= conf                                           # no data -> the global model alone
    N3 = 33
    gr = np.linspace(0, 1, N3)
    bb, gg, rr = np.meshgrid(gr, gr, gr, indexing="ij")     # .cube order: r fastest
    pts = np.stack([rr.ravel(), gg.ravel(), bb.ravel()], 1).astype(np.float32)
    base = basis(pts) @ coef
    from scipy.ndimage import map_coordinates
    q = pts * (G - 1)
    add = np.stack([map_coordinates(resid[..., c], [q[:, 0], q[:, 1], q[:, 2]], order=1, mode="nearest") for c in range(3)], 1)
    lut = np.clip(base + add, 0, 1)
    with open(os.path.join(B, "his.cube"), "w") as f:
        f.write("TITLE \"his grade, fitted by kit_recover.py\"\nLUT_3D_SIZE 33\n")
        for v in lut:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    # fit error on the pairs, in 8-bit levels
    qx = X * (G - 1)
    fitted = basis(X) @ coef + np.stack([map_coordinates(resid[..., c], [qx[:, 0], qx[:, 1], qx[:, 2]], order=1, mode="nearest")
                                         for c in range(3)], 1)
    err = float(np.median(np.abs(fitted - Y)) * 255)
    base_err = float(np.median(np.abs(X - Y)) * 255)
    sx = int(round(float(np.median(cxs)))) if cxs else 960
    open(os.path.join(B, "grade.py"), "w").write(
        '"""His BT.709 grade, fitted by kit9x16/kit_recover.py from matched master/raw pixels (centre of frame,\n'
        f'flat regions, {len(X):,} pairs; median error {err:.2f} levels, ungraded {base_err:.2f})."""\n\nimport os\n\n'
        'LUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "his.cube")\n\n'
        'CURVES = (\n    "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,"\n'
        '    f"format=rgb48le,lut3d=file=\'{LUT}\':interp=tetrahedral,"\n'
        '    "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int"\n)\n\n'
        f"SUBJECT_CX = {sx}\n")
    return dict(pairs=int(len(X)), median_err_levels=round(err, 2), ungraded_err_levels=round(base_err, 2), subject_cx=sx)


# ------------------------------------------------------------------------------------------------ picture refinement
def refine_edl(B, E, rolls, fps, span=20, wide=45):
    """The audio lock places each segment on HIS MIX; his PICTURE is what the vertical reproduces, and where his
    graphics cover the voice-lock (music under a card) a segment can span two takes. So the picture decides, every
    3rd frame (zpic2's method): the raw offset dk (+-span frames, +-wide when poor) where Dan's head box agrees best
    with his master; runs of steady dk inside an audio segment become picture segments, split where dk steps.
    Writes nothing itself; returns the refined EDL + a log. The audio lock is kept in edl_audio.json."""
    sys.path.insert(0, HERE)
    import auto_measure as am
    Aa = os.path.join(B, "auto_grade", "auto")
    F = json.load(open(os.path.join(Aa, "framing.json")))
    M = am.mm(os.path.join(Aa, "m256.rgb"))
    raws = {n: am.mm(os.path.join(Aa, f"r_{os.path.splitext(os.path.basename(p))[0]}.rgb")) for n, p in rolls.items()}

    def best_dk(e, f):
        Rr = raws[e.get("roll") or list(rolls)[0]]
        n = f["n"]
        k0 = int(round((e["src_in"] + n / fps - e["cut_in"]) * fps))
        x0, x1, y0, y1 = am.BOXES[f["box"]]
        T = am.gray(M[n])[y0:y1, x0:x1]
        def sc(dk):
            k = k0 + dk
            if not 0 <= k < len(Rr):
                return -1.0
            return am.ncc(T, am.warp(am.gray(Rr[k]), f["s"], f["dx"], f["dy"])[y0:y1, x0:x1])
        s0 = {dk: sc(dk) for dk in range(-span, span + 1)}
        d = max(s0, key=s0.get)
        if s0[d] < 0.85:
            s1 = {dk: sc(dk) for dk in range(-wide, wide + 1, 2) if abs(dk) > span}
            if s1:
                d1 = max(s1, key=s1.get)
                if s1[d1] > s0[d] + 0.05:
                    d = d1; s0[d] = s1[d1]
        return d, s0[d], s0.get(0, -1)

    out, log = [], []
    for e in E:
        samp = [f for f in F if e["cut_in"] * fps <= f["n"] < e["cut_out"] * fps and f.get("frac", 0) >= 0.6]
        if len(samp) < 3:
            out.append(e); log.append(dict(i=e["i"], samples=len(samp), runs=[])); continue
        est = [(f["n"],) + best_dk(e, f) for f in samp]
        # a sample counts when the picture clearly prefers it (a still head agrees with everything)
        ds = np.array([x[1] if x[2] > x[3] + 0.005 else 0 for x in est], float)
        sm = np.array([np.median(ds[max(0, i - 2):i + 3]) for i in range(len(ds))])
        runs = [[0, 0, sm[0]]]
        for i in range(1, len(sm)):
            if abs(sm[i] - runs[-1][2]) > 2:
                runs.append([i, i, sm[i]])
            else:
                runs[-1][1] = i
        runs = [r for r in runs if r[1] - r[0] + 1 >= 4] or [[0, len(sm) - 1, float(np.median(sm))]]
        bounds = [e["cut_in"]]
        for r0, r1 in zip(runs[:-1], runs[1:]):
            bounds.append(round((est[r0[1]][0] + est[r1[0]][0]) / 2 / fps, 4))
        bounds.append(e["cut_out"])
        for q, r in enumerate(runs):
            dk = int(round(float(np.median(ds[r[0]:r[1] + 1]))))
            c0, c1 = bounds[q], bounds[q + 1]
            if c1 - c0 < 0.05:
                continue
            base = e["src_in"] + (c0 - e["cut_in"])
            out.append(dict(e, cut_in=round(c0, 4), cut_out=round(c1, 4), dur=round(c1 - c0, 4),
                            src_in=round(base + dk / fps, 4), src_out=round(base + (c1 - c0) + dk / fps, 4),
                            picture_shift_frames=dk))
        log.append(dict(i=e["i"], samples=len(samp), runs=[(round(bounds[q], 2), int(round(float(np.median(ds[r[0]:r[1] + 1])))))
                                                            for q, r in enumerate(runs)]))
    for i, e in enumerate(out):
        e["i"] = i
    return out, log


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--master", required=True)
    ap.add_argument("--raw", action="append", default=[], help="a raw roll (repeat for several)")
    ap.add_argument("--shoot", action="append", default=[], help="a shoot folder to search for his roll(s)")
    ap.add_argument("--min-coverage", type=float, default=0.95)
    a = ap.parse_args()
    B = os.path.abspath(a.build); os.makedirs(B, exist_ok=True)
    master = os.path.abspath(a.master)
    rep = dict(master=master)
    fps = 30000 / 1001
    # words
    mw = os.path.join(B, "m.whisper.json")
    transcribe(master, mw)
    Wh = words_of(mw)
    dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                master], capture_output=True, text=True).stdout.strip())
    # rolls
    rp = os.path.join(B, "rolls.json")
    cand = list(a.raw)
    for d in a.shoot:
        cand += sorted(glob.glob(os.path.join(d, "*.MP4")) + glob.glob(os.path.join(d, "*.mp4")))
    def roll_words(p):
        idx = os.path.splitext(p)[0] + ".roll/words.json"
        if os.path.exists(idx):
            return words_of(idx)
        cache = os.path.join(B, f"{os.path.splitext(os.path.basename(p))[0]}.whisper.json")
        transcribe(p, cache)
        return words_of(cache)
    if not os.path.exists(rp):
        his = [w for w, _, _ in Wh]
        scores = []
        for p in cand:
            RW = roll_words(p)
            rw = set(w for w, _, _ in RW)
            quick = sum(1 for w in his if w in rw) / max(1, len(his))
            if quick < 0.6:
                continue
            pairs = align(his, [w for w, _, _ in RW])
            scores.append((len(pairs) / len(his), p))
        scores.sort(reverse=True)
        rep["roll_scores"] = [(round(s, 3), os.path.basename(p)) for s, p in scores[:5]]
        if not scores:
            raise SystemExit("no raw roll carries his words -- wrong shoot folder (escalate)")
        chosen = [scores[0][1]]
        covered = scores[0][0]
        if covered < a.min_coverage:                   # a multi-roll cut: add rolls while they add coverage
            for s, p in scores[1:4]:
                if s > 0.15:
                    chosen.append(p)
        json.dump({os.path.splitext(os.path.basename(p))[0]: p for p in chosen}, open(rp, "w"), indent=1)
    rolls = json.load(open(rp))
    # audio
    his16 = os.path.join(B, "his_mix16.wav")
    wav16(master, his16)
    H = rd(his16)
    prof_by_roll, cover = {}, {}
    for name, path in rolls.items():
        lav = os.path.join(B, f"lav16_{name}.wav")
        idx = os.path.splitext(path)[0] + ".roll.json"
        af, amap = None, None
        if os.path.exists(idx):
            L = json.load(open(idx)).get("audio", {}).get("lav", {})
            af = L.get("filter"); amap = L.get("map")
        wav16(path, lav, af=af, amap=amap)
        R = rd(lav)
        RW = roll_words(path)
        pairs = align([w for w, _, _ in Wh], [w for w, _, _ in RW])
        cover[name] = round(len(pairs) / max(1, len(Wh)), 3)
        pf = os.path.join(B, f"offset_profile_{name}.json")
        if not os.path.exists(pf):
            json.dump(profile(H, R, candidates(Wh, RW, pairs)), open(pf, "w"))
        prof_by_roll[name] = json.load(open(pf))
    rep["word_coverage"] = cover
    total = max(cover.values()) if len(cover) == 1 else min(1.0, sum(cover.values()))
    if total < a.min_coverage and len(rolls) == 1:
        rep["escalation"] = f"only {total:.1%} of his words are on {list(rolls)[0]} (need {a.min_coverage:.0%})"
    # edl
    ep = os.path.join(B, "edl_final.json")
    if not os.path.exists(ep):
        E = build_edl(prof_by_roll, [(w, s, e) for w, s, e in Wh], dur)
        if len(rolls) == 1:
            for e in E:
                e["roll"] = None
        json.dump(E, open(ep, "w"), indent=1)
    E = json.load(open(ep))
    lock = [p[2] for pr in prof_by_roll.values() for p in pr if p[1] is not None]
    rep["profile_lock_median"] = round(float(np.median(lock)), 3) if lock else None
    rep["segments"] = len(E)
    # grade (its measurement also gives the framing the picture refinement needs)
    if not os.path.exists(os.path.join(B, "grade.py")):
        rep["grade"] = fit_grade(B, master, E, {k: v for k, v in rolls.items()}, fps)
    # picture refinement of the audio EDL
    if not os.path.exists(os.path.join(B, "edl_audio.json")):
        json.dump(E, open(os.path.join(B, "edl_audio.json"), "w"), indent=1)
    if not any("picture_shift_frames" in e for e in E):
        E, rlog = refine_edl(B, json.load(open(os.path.join(B, "edl_audio.json"))), rolls, fps)
        json.dump(E, open(ep, "w"), indent=1)
        rep["picture_refinement"] = dict(audio_segments=len(rlog), picture_segments=len(E), log=rlog)
    json.dump(rep, open(os.path.join(B, "recover_report.json"), "w"), indent=1)
    print(json.dumps(rep, indent=1))
    return 3 if rep.get("escalation") else 0


if __name__ == "__main__":
    sys.exit(main())
