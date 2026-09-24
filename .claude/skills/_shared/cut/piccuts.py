#!/usr/bin/env python3
"""THE POSE-MATCHED PICTURE CUT, shared by every video skill. The ONLY copy of this code.

Our cuts read as jump cuts because we cut the picture ON the audio splice. Muhammad cuts it 1-15 frames
away, on a frame where the outgoing and incoming takes are in the same pose (a J- or L-cut). On his Ad 2,
22 of 33 picture cuts sit off the audio splice by -15..+10 frames (confidence >= 0.6). The audio never
moves; only the picture cut does, and the length of the programme is unchanged.

Two modes:
  * master  -- an editor's finished render exists: recover HIS picture cut (render both takes from the raw
               at the grade, fit each to his framing, high-passed NCC against his frame; the crossover is
               his cut). Below --trusted confidence it falls through to the pose match.
  * raw     -- cutting from scratch: search +-W frames around the splice for the k where Dan's HEAD is in
               the same place and size on the last outgoing and the first incoming frame (mediapipe face box,
               centre shift + height change, in 1920-wide source px). Among k within HEAD_TIE px of the best,
               the highest high-passed NCC over the head-and-torso box wins (hands, shoulders), then the
               smaller |k|. No face on either frame: the NCC alone decides (the 2026-09-16 kit rule).

   Why head, not NCC (measured 2026-09-24 on Ad 1 attempt 1, 72 splices, strips in the VQC-C notes):
   the NCC choice left a median head jump of 33 px against 39 px ON the audio splice, and on 2.78 s and
   11.50 s it picked a frame WORSE than the audio cut (96 vs 47 px, 42 vs 15 px), because NCC rewards
   matching hands and background texture, not where the head is. The eye reads the head. Head choice:
   median 13 px, 4 of 72 over 40 px (NCC: 27); over the 28.5 px cover bound 10 (audio cut 50, NCC 39).

⚠ DAN'S VERDICT 2026-09-24 (the A/B this handoff asked for, one Ad 1 join at 1:09, head jump 48 px on the audio cut vs 6 px on the matched frame): "They both look bad. I wouldn't use either of these cuts. They both look like jump cuts." A matched frame alone does NOT hide a same-framing cut. The fix that passed his eye is the kit's: a framing STEP (instant punch-in or pull-out) on every bare talk cut, or an insert over it (blind tie with Muhammad, 2026-09-18). This tool only picks the least-bad frame for that stepped cut.

Every cut reports its head jump and similarity; a head jump above --cover-above-px (or, with no face, a
similarity below --cover-below) is flagged `cover: "push"` and `watch: true`, so the render covers it and
the watch pass looks at it, instead of guessing.

  python3 piccuts.py decide --build DIR --mode raw|master [--reference his.mp4] --raw ROLL [--rolls rolls.json]
                            [--grade grade.py|grade.txt|filter] --edl edl.json [--talk talk_spans.json]
                            [--search 15] [--trusted 0.60] --cover-below 0.44 [--min-take-frames 8]
  python3 piccuts.py strips --build DIR --raw ROLL [--rolls ..] [--grade ..] --edl edl.json [--piccuts P]
                            -> DIR/strips/*.jpg, frames -2/-1/0/+1/+2 around every picture cut, audio-cut
                               row (k=0) above the chosen row, for eyes (never a frame-difference score)
  python3 piccuts.py calibrate [--out piccuts_calibration.json]

Library use (from any skill):
  sys.path.insert(0, "<skills>/_shared/cut"); import piccuts
  out = piccuts.decide(E, spans, raw=..., grade=..., mode="raw", cover_below=0.44)
  P = piccuts.picture_edl(E, out)            # the picture EDL; the audio EDL is untouched

EDL shapes accepted (load_edl): {cut_in, cut_out, src_in[, src_out, roll]} (the ad pipelines),
{out_seconds: [a, b], src_in, src_out[, roll]} (edit.json), {roll, start, end} ranges (website/longform
source-range lists; the programme timeline is their running sum).

Writes <build>/piccuts.json: [{i, cut, n0, k, pic_frame, conf, method, sim_at_k, sim_at_0, clamped,
cover, watch, sims}] and <build>/edl_picture.json: the audio EDL with every decided splice moved by k frames
on the PICTURE side only, with n0/n1 frame indices, audio_cut_in and rel.

History: a2/piccuts.py (Ad 2 recovery, 2026-09-03) -> kit9x16/kit_cuts.py (the kit, 2026-09-16, from-raw
mode) -> here (2026-09-24, VQC-C). Numbers: kit9x16/cut_rules.md; calibration: piccuts_calibration.json.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FPS = 30000 / 1001
H, Wd = 270, 480
BOX = (slice(30, 200), slice(120, 360))            # the head-and-torso box of a centred talking head (480x270)
SC = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]        # his framing search (scale)
FY = [0.30, 0.42, 0.50]                             # ...and the vertical anchor
CALIBRATION = os.path.join(HERE, "piccuts_calibration.json")
TIE = 0.02                                          # similarity ties go to the smaller |k|
HEAD_TIE = 4.0                                      # head jumps within 4 source px of the best are a tie
_DET = None


def heads(frames):
    """(x, y, h) of the face box per RGB frame, in 1920x1080 source px; NaN where no face is found."""
    global _DET
    if _DET is None:
        import mediapipe as mp
        _DET = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4)
    out = []
    for f in frames:
        r = _DET.process(np.ascontiguousarray(f))
        if not r.detections:
            out.append((np.nan, np.nan, np.nan))
            continue
        b = max(r.detections, key=lambda d: d.score[0]).location_data.relative_bounding_box
        out.append(((b.xmin + b.width / 2) * 1920, (b.ymin + b.height / 2) * 1080, b.height * 1080))
    return np.array(out, float).reshape(-1, 3)


def head_jump(a, b):
    """Centre shift + height change between two face boxes, source px. NaN if either has no face."""
    return float(np.hypot(a[0] - b[0], a[1] - b[1]) + abs(a[2] - b[2]))


def gray(rgb):
    return (rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114).astype(np.float32)


# ---------------------------------------------------------------------------- instruments
def grade_filter(path):
    """`CURVES` from a grade.py, or the first line of a grade.txt, or the string itself."""
    if path is None:
        return None
    if os.path.exists(path) and path.endswith(".py"):
        spec = importlib.util.spec_from_file_location("grade_mod", path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.CURVES
    if os.path.exists(path):
        return open(path).read().strip()
    return path


def frames_from(src, t0, n, vf, pix="gray"):
    """n frames from src starting at t0 (seek snapped to the frame grid: an unsnapped seek duplicates the
    first frame), through vf, at 480x270. gray -> float32 (n,H,W); rgb24 -> uint8 (n,H,W,3)."""
    t0 = max(0.0, round(t0 * FPS) / FPS - 0.0002)
    ch = 3 if pix == "rgb24" else 1
    cmd = [FF, "-nostdin", "-v", "error", "-ss", f"{t0:.5f}", "-i", src, "-frames:v", str(n),
           "-vf", f"{vf + ',' if vf else ''}scale={Wd}:{H},setpts=N/({FPS:.6f})/TB", "-r", f"{FPS:.6f}",
           "-f", "rawvideo", "-pix_fmt", pix, "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    per = H * Wd * ch
    m = len(b) // per
    a = np.frombuffer(b[:m * per], np.uint8)
    if pix == "rgb24":
        return a.reshape(-1, H, Wd, 3)
    return a.reshape(-1, H, Wd).astype(np.float32)


def hp(a):
    return a - np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32)


def ncc(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / max(np.sqrt((a * a).sum() * (b * b).sum()), 1e-6))


def best_match(his_hp, our):
    """Fit OUR frame to HIS framing (scale / fy) and return the best hp-NCC in the box."""
    best = -9
    for s in SC:
        nh, nw = int(H / s), int(Wd / s)
        for fy in FY:
            y0 = int((H - nh) * fy)
            x0 = (Wd - nw) // 2
            r = np.asarray(Image.fromarray(our[y0:y0 + nh, x0:x0 + nw].astype(np.uint8)).resize((Wd, H)), dtype=np.float32)
            v = ncc(his_hp[BOX], hp(r)[BOX])
            if v > best:
                best = v
    return best


def self_sim(a, b):
    """How alike two of OUR frames are in the head-and-torso box: high-passed NCC (no reference to fit to)."""
    return ncc(hp(a)[BOX], hp(b)[BOX])


def pick_k(sims, jumps=None):
    """The k to cut the picture on. With head jumps: the smallest jump (ties within HEAD_TIE px), then the
    highest similarity, then the smaller |k|. Without (no face): the most alike k, ties within TIE to the
    smaller |k| -- the picture stays as near the audio as the pose allows."""
    if jumps:
        ok = {k: v for k, v in jumps.items() if k in sims and not np.isnan(v)}
        if ok:
            lo = min(ok.values())
            cand = [k for k, v in ok.items() if v <= lo + HEAD_TIE]
            top = max(sims[k] for k in cand)
            return min((k for k in cand if sims[k] >= top - TIE), key=lambda k: (abs(k), -sims[k]))
    top = max(sims.values())
    return min((k for k, v in sims.items() if v >= top - TIE), key=lambda k: (abs(k), -sims[k]))


# ---------------------------------------------------------------------------- EDLs
def load_edl(path_or_list):
    """Any of the three EDL shapes -> [{i, cut_in, cut_out, src_in, src_out, roll}] on one programme timeline."""
    E = json.load(open(path_or_list)) if isinstance(path_or_list, str) else path_or_list
    if isinstance(E, dict):
        E = E.get("ranges") or E.get("segments") or E.get("edl")
    out, t = [], 0.0
    for i, s in enumerate(E):
        if "cut_in" in s:
            out.append(dict(i=i, cut_in=float(s["cut_in"]), cut_out=float(s["cut_out"]), src_in=float(s["src_in"]),
                            src_out=float(s.get("src_out", s["src_in"] + s["cut_out"] - s["cut_in"])), roll=s.get("roll")))
        elif "out_seconds" in s:
            a, b = s["out_seconds"]
            out.append(dict(i=i, cut_in=float(a), cut_out=float(b), src_in=float(s["src_in"]), src_out=float(s["src_out"]),
                            roll=s.get("roll")))
        else:                                                   # a source-range list: {roll, start, end}
            d = float(s["end"]) - float(s["start"])
            out.append(dict(i=i, cut_in=t, cut_out=t + d, src_in=float(s["start"]), src_out=float(s["end"]), roll=s.get("roll")))
            t += d
    return out


def talk_at(spans, t):
    return spans is None or any(a <= t < b for a, b in spans)


# ---------------------------------------------------------------------------- the decision
def decide(E, spans=None, *, raw, rolls=None, grade=None, mode="raw", reference=None, search=15, trusted=0.60,
           cover_below=0.44, cover_above_px=None, min_take_frames=8, use_heads=True, only=None, log=print):
    """Decide k for every splice both sides of which are talk (spans None = every splice; `only` = a set of
    segment indices i to decide, e.g. just the joins a pause removal made). Returns the records."""
    E = load_edl(E) if not (E and "src_out" in E[0] and "i" in E[0]) else E
    rolls = rolls or {}
    if cover_above_px is None:
        cover_above_px = json.load(open(CALIBRATION))["summary"]["head"]["cover_above_px"]
    W = search
    N = 2 * W + 1

    def roll_of(seg):
        r = seg.get("roll")
        return rolls.get(r, raw) if r else raw

    out = []
    prev_pic = 0                                               # the previous picture cut, for min_take_frames
    for i in range(1, len(E)):
        cur, prev = E[i], E[i - 1]
        t = cur["cut_in"]
        n0 = round(t * FPS)
        if only is not None and i not in only:
            continue
        if not (talk_at(spans, t) and talk_at(spans, t - 0.05) and talk_at(spans, t + 0.05)):
            continue                                           # under an insert, a plate, or at a beat edge: not a picture cut
        pn0 = round(prev["cut_in"] * FPS)
        nn0 = round(E[i + 1]["cut_in"] * FPS) if i + 1 < len(E) else round(E[-1]["cut_out"] * FPS)
        # the outgoing take over the window continues past its out-point; the incoming starts before its in-point
        a_src = prev["src_in"] + (n0 - W - pn0) / FPS
        b_src = cur["src_in"] - W / FPS
        # a take at the head of its roll: B is missing its first `lead` frames -> those k are not available
        lead = max(0, int(np.ceil(-b_src * FPS - 1e-6))) if b_src < 0 else 0
        Ac = frames_from(roll_of(prev), a_src, N, grade, "rgb24")
        Bc = frames_from(roll_of(cur), b_src + lead / FPS, N - lead, grade, "rgb24")
        A, B = gray(Ac), gray(Bc)
        hA = heads(Ac) if use_heads else np.full((len(Ac), 3), np.nan)
        hB = heads(Bc) if use_heads else np.full((len(Bc), 3), np.nan)
        if lead:
            B = np.concatenate([np.full((lead, H, Wd), np.nan, np.float32), B]) if len(B) else B
            hB = np.concatenate([np.full((lead, 3), np.nan), hB])
        # the room a take has on screen: never shorter than min_take_frames on either side of the cut
        lo_k = max(-W, prev_pic + min_take_frames - n0)
        hi_k = min(W, nn0 - min_take_frames - n0)
        rec = dict(i=i, cut=round(t, 3), n0=n0, clamped=bool(lead) or lo_k > -W or hi_k < W)
        sims, jumps = {}, {}
        for k in range(-W, W + 1):
            ia, ib = W + k - 1, W + k
            if lo_k <= k <= hi_k and 0 <= ia < len(A) and 0 <= ib < len(B) and not np.isnan(B[ib]).any():
                sims[k] = self_sim(A[ia], B[ib])
                jumps[k] = head_jump(hA[ia], hB[ib])
        if not sims:
            rec.update(k=0, pic_frame=n0, conf=0.0, method="short-extraction", sim_at_k=None, sim_at_0=None, head_at_k=None,
                       cover="push", watch=True, note=f"A {len(A)} B {len(B)} room {lo_k}..{hi_k}")
            out.append(rec)
            prev_pic = n0
            log(f"splice {t:8.3f}: no usable frames (A {len(A)} B {len(B)}) -> k=0, covered, watch")
            continue
        rec["sim_at_0"] = round(sims[0], 3) if 0 in sims else None
        rec["head_at_0"] = round(jumps[0], 1) if 0 in jumps and not np.isnan(jumps[0]) else None
        if mode == "master":
            his = frames_from(reference, (n0 - W) / FPS, N, None)
            if len(his) < N or len(A) < N or len(B) < N:
                kb = pick_k(sims, jumps)
                rec.update(k=kb, conf=0.0, method="pose-match (reference short)")
            else:
                ra = np.array([best_match(hp(his[k]), A[k]) for k in range(N)])
                rb = np.array([best_match(hp(his[k]), B[k]) for k in range(N)])
                d = rb - ra
                cross = next((k for k in range(N - 2) if d[k] > 0 and d[k + 1] > 0 and d[k + 2] > 0
                              and (k == 0 or d[k - 1] <= 0)), None)
                if cross is not None:
                    rel = cross - W
                    conf = float(min(ra[:max(1, cross - 1)].mean() if cross > 1 else ra[0], rb[cross:cross + 5].mean()))
                else:
                    rel, conf = 0, 0.0
                rec.update(ra=[round(float(v), 3) for v in ra], rb=[round(float(v), 3) for v in rb])
                if cross is not None and conf >= trusted and rel in sims:
                    rec.update(k=rel, conf=round(conf, 3), method="his-frame")
                    # A trusted crossover can still choose a severe pose jump. Ad 10's 68.7 s cut measured 0.40
                    # self-similarity at Muhammad's frame versus 0.59 within the same search; the push did not
                    # hide it in the watch pass (AV-07, 2026-09-23). Prefer the materially cleaner pose when his
                    # choice falls below the cover threshold. Picture only; the audio splice is untouched.
                    # The same test on the head: his frame is kept unless it leaves a head jump over the cover
                    # bound AND the head match is at least 12 px cleaner (the size of a visible step).
                    kn = pick_k(sims)
                    kh = pick_k(sims, jumps)
                    jr, jh = jumps.get(rel, np.nan), jumps.get(kh, np.nan)
                    if sims[rel] < cover_below and sims[kn] >= sims[rel] + 0.12:
                        rec.update(k=kn, method="pose-match (his frame jumped)")
                    elif not np.isnan(jr) and not np.isnan(jh) and jr > cover_above_px and jh <= jr - 12:
                        rec.update(k=kh, method="head-match (his frame jumped)")
                else:
                    rec.update(k=pick_k(sims, jumps), conf=round(conf, 3), method="pose-match (his frame untrusted)")
        else:
            kb = pick_k(sims, jumps)
            has = not np.isnan(jumps.get(kb, np.nan))
            rec.update(k=kb, conf=round(sims[kb], 3), method="head-match" if has else "pose-match (no face)")
        k = rec["k"]
        rec["sim_at_k"] = round(sims[k], 3)
        jk = jumps.get(k, np.nan)
        rec["head_at_k"] = None if np.isnan(jk) else round(jk, 1)
        rec["pic_frame"] = n0 + k
        exposed = (jk > cover_above_px) if not np.isnan(jk) else (rec["sim_at_k"] < cover_below)
        rec["cover"] = "push" if exposed else None
        rec["watch"] = rec["cover"] is not None
        rec["sims"] = {str(kk): round(v, 3) for kk, v in sims.items()}
        rec["heads"] = {str(kk): (None if np.isnan(v) else round(v, 1)) for kk, v in jumps.items()}
        out.append(rec)
        prev_pic = n0 + k
        s0 = f"{rec['sim_at_0']:.2f}" if rec["sim_at_0"] is not None else " -- "
        f = lambda v: f"{v:5.1f}" if v is not None else "  -- "
        log(f"splice {t:8.3f} (f{n0})  k {k:+3d}  head@k {f(rec['head_at_k'])}px  head@0 {f(rec['head_at_0'])}px  "
            f"sim@k {rec['sim_at_k']:.2f}  sim@0 {s0}  {rec['method']}"
            f"{'  COVER+WATCH' if rec['cover'] else ''}")
    return out


def picture_edl(E, out):
    """The audio EDL with each decided splice moved by k on the PICTURE side only. Length is preserved: the
    outgoing segment gains exactly the frames the incoming one loses."""
    E = load_edl(E) if not (E and "src_out" in E[0] and "i" in E[0]) else E
    P = [dict(s) for s in E]
    byi = {r["i"]: r for r in out}
    for i in range(1, len(P)):
        k = byi[i]["k"] if i in byi else 0
        if k:
            dt = k / FPS
            P[i]["cut_in"] += dt
            P[i]["src_in"] += dt
            P[i - 1]["cut_out"] += dt
            P[i - 1]["src_out"] += dt
    prev = 0
    for i, s in enumerate(P):
        cum = round(s["cut_out"] * FPS)
        s["n0"], s["n1"] = prev, cum
        s["audio_cut_in"] = E[i]["cut_in"]
        s["rel"] = int(byi[i]["k"]) if i in byi else 0
        prev = cum
    assert P[-1]["n1"] == round(E[-1]["cut_out"] * FPS), "picture EDL changed the programme length"
    return P


def cmd_decide(a):
    if a.mode == "master" and not a.reference:
        raise SystemExit("--mode master needs --reference (his render)")
    E = load_edl(a.edl)
    spans = [tuple(x) for x in json.load(open(a.talk))] if a.talk else None
    rolls = json.load(open(a.rolls)) if a.rolls else {}
    out = decide(E, spans, raw=a.raw, rolls=rolls, grade=grade_filter(a.grade), mode=a.mode, reference=a.reference,
                 search=a.search, trusted=a.trusted, cover_below=a.cover_below, cover_above_px=a.cover_above_px,
                 min_take_frames=a.min_take_frames, use_heads=not a.no_heads,
                 log=lambda s: print(s, flush=True))
    os.makedirs(a.build, exist_ok=True)
    json.dump(out, open(os.path.join(a.build, "piccuts.json"), "w"), indent=1)
    P = picture_edl(E, out)
    json.dump(P, open(os.path.join(a.build, "edl_picture.json"), "w"), indent=1)
    moved = sum(1 for r in out if r["k"])
    cov = sum(1 for r in out if r.get("cover"))
    print(f"{len(out)} splices decided: {moved} moved off the audio, {cov} to cover + watch; "
          f"-> {a.build}/piccuts.json, edl_picture.json ({P[-1]['n1']} frames, length unchanged)")


# ---------------------------------------------------------------------------- strips, for eyes
def strip_rows(E, r, raw, rolls, grade, crop=None):
    """Two rows of five colour frames at -2,-1 | 0,+1,+2 around the picture cut: ON the audio splice (k=0),
    then at the decided k. crop = (x0, x1) fraction of the width to show (a 9:16 window on 16:9 raw)."""
    i, n0 = r["i"], r["n0"]
    cur, prev = E[i], E[i - 1]
    pn0 = round(prev["cut_in"] * FPS)
    rows = []
    for k in (0, r["k"]):
        a_src = prev["src_in"] + (n0 + k - 2 - pn0) / FPS
        b_src = cur["src_in"] + k / FPS
        A = frames_from(rolls.get(prev.get("roll"), raw) if prev.get("roll") else raw, a_src, 2, grade, "rgb24")
        B = frames_from(rolls.get(cur.get("roll"), raw) if cur.get("roll") else raw, max(0.0, b_src), 3, grade, "rgb24")
        fr = list(A) + list(B)
        if crop:
            x0, x1 = int(crop[0] * Wd), int(crop[1] * Wd)
            fr = [f[:, x0:x1] for f in fr]
        rows.append((k, fr))
    return rows


def cmd_strips(a):
    E = load_edl(a.edl)
    rolls = json.load(open(a.rolls)) if a.rolls else {}
    grade = grade_filter(a.grade)
    R = json.load(open(a.piccuts or os.path.join(a.build, "piccuts.json")))
    R = [r for r in R if a.all or r.get("k")]
    d = os.path.join(a.build, "strips")
    os.makedirs(d, exist_ok=True)
    crop = tuple(float(x) for x in a.crop.split(",")) if a.crop else None
    per = a.per_sheet
    for s in range(0, len(R), per):
        blocks = []
        for r in R[s:s + per]:
            rows = strip_rows(E, r, a.raw, rolls, grade, crop)
            fw, fh = rows[0][1][0].shape[1], rows[0][1][0].shape[0]
            im = Image.new("RGB", (5 * fw + 4 * 3 + 150, 2 * fh + 3), (20, 20, 20))
            dr = ImageDraw.Draw(im)
            for y, (k, fr) in enumerate(rows):
                for x, f in enumerate(fr[:5]):
                    im.paste(Image.fromarray(np.ascontiguousarray(f)), (150 + x * (fw + 3), y * (fh + 3)))
                lab = f"{r['cut']:.2f}s\nk {k:+d}\n" + ("AUDIO CUT" if k == 0 else "CHOSEN")
                sim = r.get("sims", {}).get(str(k))
                if sim is not None:
                    lab += f"\nsim {sim:.2f}"
                dr.text((6, y * (fh + 3) + 8), lab, fill=(255, 255, 0) if k else (200, 200, 200))
            # the cut sits between column 2 and column 3
            xcut = 150 + 2 * (fw + 3) - 2
            dr.line([(xcut, 0), (xcut, im.height)], fill=(255, 40, 40), width=2)
            blocks.append(im)
        sheet = Image.new("RGB", (blocks[0].width, sum(b.height + 8 for b in blocks)), (0, 0, 0))
        y = 0
        for b in blocks:
            sheet.paste(b, (0, y))
            y += b.height + 8
        p = os.path.join(d, f"strips_{s // per:02d}.jpg")
        sheet.save(p, quality=88)
        print(p, flush=True)


# ---------------------------------------------------------------------------- calibration
def cmd_calibrate(a):
    """The cover threshold, measured: self-similarity at HIS k on Muhammad's trusted Ad 2 cuts vs at k=0 on
    attempt 1's splices (the 23-of-72 naked cut Dan rejected). Writes piccuts_calibration.json."""
    SSD = "/Volumes/Extreme/_edit_work"
    RAW2 = ("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content"
            " | jeff chagrin | dan rose/C1592.MP4")
    RAW1 = RAW2.replace("C1592", "C1591")
    W = a.search
    N = 2 * W + 1
    res = dict(search=W, sets={})
    d2 = os.path.join(SSD, "ad2-vert-v2")
    E = load_edl(os.path.join(d2, "edl_final.json"))
    g2 = grade_filter(os.path.join(d2, "grade.txt"))
    his = []
    for r in json.load(open(os.path.join(d2, "piccuts.json"))):
        k = r.get("pic_rel", r.get("k"))
        conf = r.get("confidence", r.get("conf", 0))
        if k is None or conf < a.trusted:
            continue
        i = r["i"]
        cur, prev = E[i], E[i - 1]
        n0 = round(cur["cut_in"] * FPS)
        pn0 = round(prev["cut_in"] * FPS)
        Ac = frames_from(RAW2, prev["src_in"] + (n0 - W - pn0) / FPS, N, g2, "rgb24")
        Bc = frames_from(RAW2, cur["src_in"] - W / FPS, N, g2, "rgb24")
        if len(Ac) < N or len(Bc) < N:
            continue
        A, B, hA, hB = gray(Ac), gray(Bc), heads(Ac), heads(Bc)
        k = int(k)
        ia, ib = W + k - 1, W + k
        s_k = self_sim(A[ia], B[ib]) if 0 <= ia < N and 0 <= ib < N else None
        s_0 = self_sim(A[W - 1], B[W])
        best = max(self_sim(A[W + q - 1], B[W + q]) for q in range(-W + 1, W))
        hk_ = head_jump(hA[ia], hB[ib]) if 0 <= ia < N and 0 <= ib < N else np.nan
        his.append(dict(i=i, cut=cur["cut_in"], k=k, conf=conf, sim_at_his_k=round(s_k, 3) if s_k is not None else None,
                        sim_at_0=round(s_0, 3), best_sim=round(best, 3),
                        head_at_his_k=None if np.isnan(hk_) else round(hk_, 1),
                        head_at_0=None if np.isnan(head_jump(hA[W - 1], hB[W])) else round(head_jump(hA[W - 1], hB[W]), 1)))
    res["sets"]["muhammad-ad2-trusted"] = his
    d1 = os.path.join(SSD, "ad1-8-14/vert9x16")
    E1 = load_edl(os.path.join(d1, "edl_final_a1.json.bak"))
    g1 = grade_filter(os.path.join(d1, "grade.py"))
    a1 = []
    for i in range(1, len(E1)):
        cur, prev = E1[i], E1[i - 1]
        n0 = round(cur["cut_in"] * FPS)
        pn0 = round(prev["cut_in"] * FPS)
        Ac = frames_from(RAW1, prev["src_in"] + (n0 - W - pn0) / FPS, N, g1, "rgb24")
        Bc = frames_from(RAW1, cur["src_in"] - W / FPS, N, g1, "rgb24")
        if len(Ac) < N or len(Bc) < N:
            continue
        A, B, hA, hB = gray(Ac), gray(Bc), heads(Ac), heads(Bc)
        s_0 = self_sim(A[W - 1], B[W])
        best = max(self_sim(A[W + q - 1], B[W + q]) for q in range(-W + 1, W))
        h0 = head_jump(hA[W - 1], hB[W])
        a1.append(dict(i=i, cut=cur["cut_in"], sim_at_0=round(s_0, 3), best_sim=round(best, 3),
                       head_at_0=None if np.isnan(h0) else round(h0, 1)))
    res["sets"]["ad1-vertical-attempt1"] = a1
    hk = [x["sim_at_his_k"] for x in his if x["sim_at_his_k"] is not None]
    a0 = [x["sim_at_0"] for x in a1]
    res["summary"] = dict(his_at_k=dict(n=len(hk), median=round(float(np.median(hk)), 3) if hk else None,
                                        p10=round(float(np.percentile(hk, 10)), 3) if hk else None),
                          attempt1_at_0=dict(n=len(a0), median=round(float(np.median(a0)), 3) if a0 else None,
                                             p90=round(float(np.percentile(a0, 90)), 3) if a0 else None),
                          note="cover_below = the midpoint of the two medians. They OVERLAP: similarity is the cover "
                               "trigger, not the discriminator; the render's framing step covers every bare cut")
    hh = [x["head_at_his_k"] for x in his if x["head_at_his_k"] is not None]
    h0 = [x["head_at_0"] for x in a1 if x["head_at_0"] is not None]
    if hh and h0:
        res["summary"]["head"] = dict(
            his_at_k=dict(n=len(hh), median=round(float(np.median(hh)), 1), p90=round(float(np.percentile(hh, 90)), 1),
                          max=round(float(max(hh)), 1)),
            attempt1_at_0=dict(n=len(h0), median=round(float(np.median(h0)), 1), p10=round(float(np.percentile(h0, 10)), 1)),
            cover_above_px=round((float(np.median(hh)) + float(np.median(h0))) / 2, 1),
            separates=bool(np.median(hh) < np.percentile(h0, 25)),
            note="head jump = face-box centre shift + height change, 1920-wide source px, last outgoing vs first "
                 "incoming frame. cover_above_px = the midpoint of the two medians (the similarity row's rule). "
                 "Not his p90: his are 16:9 cuts, and a vertical magnifies the same jump 1.78x.")
    if hk and a0:
        res["summary"]["midpoint"] = round((float(np.median(hk)) + float(np.median(a0))) / 2, 3)
        res["summary"]["separates"] = bool(np.percentile(hk, 10) > np.percentile(a0, 90))
    res["measured"] = "2026-09-24 (head rows added, VQC-C); similarity rows first measured 2026-09-16"
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps(res["summary"], indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decide")
    d.add_argument("--build", required=True)
    d.add_argument("--mode", choices=["master", "raw"], required=True)
    d.add_argument("--reference")
    d.add_argument("--raw", required=True, help="the roll every segment reads from unless --rolls maps its `roll`")
    d.add_argument("--rolls", help="json {roll name: path}")
    d.add_argument("--grade", help="grade.py (CURVES) or grade.txt or a filter string")
    d.add_argument("--edl", required=True)
    d.add_argument("--talk", help="json [[t0, t1], ...] of the TALK beats; omitted = every splice is a talk splice")
    d.add_argument("--search", type=int, default=15)
    d.add_argument("--trusted", type=float, default=0.60)
    d.add_argument("--cover-below", type=float, default=0.44, help="calibrated 2026-09-16 (piccuts_calibration.json)")
    d.add_argument("--cover-above-px", type=float, help="head jump that still shows; default = the calibration's")
    d.add_argument("--no-heads", action="store_true", help="the 2026-09-16 NCC-only rule (for comparisons)")
    d.add_argument("--min-take-frames", type=int, default=8)
    s = sub.add_parser("strips")
    s.add_argument("--build", required=True)
    s.add_argument("--raw", required=True)
    s.add_argument("--rolls")
    s.add_argument("--grade")
    s.add_argument("--edl", required=True)
    s.add_argument("--piccuts")
    s.add_argument("--crop", help="x0,x1 fraction of the width, e.g. 0.34,0.66 for the 9:16 window")
    s.add_argument("--per-sheet", type=int, default=6)
    s.add_argument("--all", action="store_true", help="include cuts that stayed on the audio splice")
    c = sub.add_parser("calibrate")
    c.add_argument("--search", type=int, default=15)
    c.add_argument("--trusted", type=float, default=0.60)
    c.add_argument("--out", default=CALIBRATION)
    a = ap.parse_args()
    return dict(decide=cmd_decide, strips=cmd_strips, calibrate=cmd_calibrate)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
