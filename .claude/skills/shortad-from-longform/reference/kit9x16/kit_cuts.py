#!/usr/bin/env python3
"""THE POSE-MATCHED CUT (cut_rules.md), as code. Decides, for every audio splice inside a talk beat,
the frame the PICTURE cuts on: his frame (from a master) or the pose-matched frame (from raw), and
whether the cut has to be covered.

  python3 kit_cuts.py decide  --build DIR --mode master|raw [--reference his.mp4] --raw ROLL --grade grade.py
                              --edl edl_final.json --talk talk_spans.json [--search 15] [--cover-below X]
  python3 kit_cuts.py calibrate                       -> piccuts_calibration.json (his trusted cuts vs attempt 1's)

Writes <build>/piccuts.json:  [{i, cut, n0, k, pic_frame, conf, method, sim_at_k, sim_at_0, clamped, cover}]
and <build>/edl_picture.json: the audio EDL with every talk splice moved by k frames on the PICTURE side
only (cut_in / src_in of the incoming segment and cut_out / src_out of the outgoing one), with n0/n1 frame
indices, audio_cut_in and rel, in the shape build_base_pic.py / kit_base.py consume.

The instruments are `a2/piccuts.py`'s, verbatim: 480x270 gray frames at the grade, a Gaussian(1.2)
high-pass, NCC over the head-and-torso box, a scale/fy fit against HIS framing when a reference exists.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FPS = 30000 / 1001
H, Wd = 270, 480
BOX = (slice(30, 200), slice(120, 360))            # piccuts.py: the head-and-torso box of a centred talking head
SC = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]        # his framing search (scale)
FY = [0.30, 0.42, 0.50]                             # ...and the vertical anchor


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


def frames_from(src, t0, n, vf):
    """n gray frames from src starting at t0 (seek snapped to the frame grid), through vf."""
    t0 = max(0.0, round(t0 * FPS) / FPS - 0.0002)
    cmd = [FF, "-nostdin", "-v", "error", "-ss", f"{t0:.5f}", "-i", src, "-frames:v", str(n),
           "-vf", f"{vf + ',' if vf else ''}scale={Wd}:{H},setpts=N/({FPS:.6f})/TB", "-r", f"{FPS:.6f}",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    a = np.frombuffer(b[:n * H * Wd], np.uint8).reshape(-1, H, Wd).astype(np.float32)
    return a


def hp(a):
    return a - np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32)


def ncc(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / max(np.sqrt((a * a).sum() * (b * b).sum()), 1e-6))


def best_match(his_hp, our):
    """piccuts.py: fit OUR frame to HIS framing (scale / fy) and return the best hp-NCC in the box."""
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
    """From raw: how alike two of OUR frames are in the head-and-torso box (no reference to fit to)."""
    return ncc(hp(a)[BOX], hp(b)[BOX])


def load_edl(path):
    E = json.load(open(path))
    out = []
    for i, s in enumerate(E):
        if "cut_in" in s:
            out.append(dict(i=i, cut_in=float(s["cut_in"]), cut_out=float(s["cut_out"]), src_in=float(s["src_in"]),
                            src_out=float(s.get("src_out", s["src_in"] + s["cut_out"] - s["cut_in"])), roll=s.get("roll")))
        else:                                                    # the Codex trial's edit.json shape
            a, b = s["out_seconds"]
            out.append(dict(i=i, cut_in=float(a), cut_out=float(b), src_in=float(s["src_in"]), src_out=float(s["src_out"]), roll=s.get("roll")))
    return out


def talk_at(spans, t):
    return any(a <= t < b for a, b in spans)


def decide(args):
    E = load_edl(args.edl)
    spans = [tuple(x) for x in json.load(open(args.talk))]
    grade = grade_filter(args.grade)
    W = args.search
    N = 2 * W + 1
    rolls = json.load(open(args.rolls)) if args.rolls else {}
    def roll_of(seg):
        r = seg.get("roll")
        return rolls.get(r, args.raw) if r else args.raw
    out = []
    for i in range(1, len(E)):
        cur, prev = E[i], E[i - 1]
        t = cur["cut_in"]
        if not (talk_at(spans, t) and talk_at(spans, t - 0.05) and talk_at(spans, t + 0.05)):
            continue                                              # a splice under an insert, a plate or at a beat edge is not a picture cut
        n0 = round(t * FPS)
        pn0 = round(prev["cut_in"] * FPS)
        # the outgoing take over the window: frames n0-W .. n0+W come from prev's source, continuing past its out
        a_src = prev["src_in"] + (n0 - W - pn0) / FPS
        b_src = cur["src_in"] - W / FPS
        # clamp to what the raw holds (a take at the start of a roll, or a negative seek)
        clamped = False
        if b_src < 0:
            clamped = True
        A = frames_from(roll_of(prev), a_src, N, grade)
        B = frames_from(roll_of(cur), max(0.0, b_src), N, grade)
        if len(A) < N or len(B) < N:
            out.append(dict(i=i, cut=round(t, 3), n0=n0, k=0, pic_frame=n0, conf=0.0, method="short-extraction",
                            clamped=True, cover="push", note=f"his {N} A {len(A)} B {len(B)}"))
            print(f"splice {t:8.3f}: short extraction A {len(A)} B {len(B)} -> k=0, covered", flush=True)
            continue
        rec = dict(i=i, cut=round(t, 3), n0=n0, clamped=clamped)
        # self-similarity at every k: the last outgoing frame (A[W+k-1]) against the first incoming (B[W+k])
        sims = {}
        for k in range(-W, W + 1):
            ia, ib = W + k - 1, W + k
            if 0 <= ia < N and 0 <= ib < N:
                sims[k] = self_sim(A[ia], B[ib])
        rec["sim_at_0"] = round(sims.get(0, 0.0), 3)
        if args.mode == "master":
            his = frames_from(args.reference, (n0 - W) / FPS, N, None)
            if len(his) < N:
                rec.update(k=0, pic_frame=n0, conf=0.0, method="reference-short", cover="push")
                out.append(rec)
                continue
            ra, rb = [], []
            for k in range(N):
                h = hp(his[k])
                ra.append(best_match(h, A[k]))
                rb.append(best_match(h, B[k]))
            ra, rb = np.array(ra), np.array(rb)
            d = rb - ra
            cross = None
            for k in range(N - 2):
                if d[k] > 0 and d[k + 1] > 0 and d[k + 2] > 0 and (k == 0 or d[k - 1] <= 0):
                    cross = k
                    break
            if cross is not None:
                rel = cross - W
                conf = float(min(ra[:max(1, cross - 1)].mean() if cross > 1 else ra[0], rb[cross:cross + 5].mean()))
            else:
                rel, conf = 0, 0.0
            rec.update(ra=[round(float(v), 3) for v in ra], rb=[round(float(v), 3) for v in rb])
            if cross is not None and conf >= args.trusted:
                rec.update(k=rel, conf=round(conf, 3), method="his-frame")
            else:
                # not trusted: fall through to the pose match, and say so
                kbest = max(sims, key=lambda k: (round(sims[k], 2), -abs(k)))
                rec.update(k=kbest, conf=round(conf, 3), method="pose-match (his frame untrusted)")
        else:
            kbest = max(sims, key=lambda k: (round(sims[k], 2), -abs(k)))
            rec.update(k=kbest, conf=round(sims[kbest], 3), method="pose-match")
        k = rec["k"]
        rec["sim_at_k"] = round(sims.get(k, 0.0), 3)
        rec["pic_frame"] = n0 + k
        rec["cover"] = "push" if rec["sim_at_k"] < args.cover_below else None
        rec["sims"] = {str(kk): round(v, 3) for kk, v in sims.items()}
        out.append(rec)
        print(f"splice {t:8.3f} (f{n0})  k {k:+d}  sim@k {rec['sim_at_k']:.2f}  sim@0 {rec['sim_at_0']:.2f}  "
              f"{rec['method']}  conf {rec['conf']:.2f}{'  COVER' if rec['cover'] else ''}", flush=True)
    os.makedirs(args.build, exist_ok=True)
    json.dump(out, open(os.path.join(args.build, "piccuts.json"), "w"), indent=1)
    # ---- the picture EDL: move each talk splice by k on the picture side only
    P = [dict(s) for s in E]
    byi = {r["i"]: r for r in out}
    for i in range(1, len(P)):
        r = byi.get(i)
        k = r["k"] if r else 0
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
    json.dump(P, open(os.path.join(args.build, "edl_picture.json"), "w"), indent=1)
    moved = sum(1 for r in out if r["k"])
    cov = sum(1 for r in out if r.get("cover"))
    print(f"{len(out)} talk splices: {moved} moved off the audio, {cov} to cover; "
          f"-> {args.build}/piccuts.json, edl_picture.json ({P[-1]['n1']} frames)")


def calibrate(args):
    """The cover threshold, measured: self-similarity at HIS k on Muhammad's trusted Ad 2 cuts vs at k=0 on
    attempt 1's splices (the 23-of-72 naked cut Dan rejected). Writes piccuts_calibration.json."""
    SSD = "/Volumes/Extreme/_edit_work"
    RAW2 = ("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content"
            " | jeff chagrin | dan rose/C1592.MP4")
    RAW1 = RAW2.replace("C1592", "C1591")
    W = args.search
    N = 2 * W + 1
    res = dict(search=W, sets={})
    # --- his: ad2-vert-v2 piccuts.json (pic_rel, confidence) + edl_final.json + grade.txt
    d2 = os.path.join(SSD, "ad2-vert-v2")
    E = load_edl(os.path.join(d2, "edl_final.json"))
    g2 = grade_filter(os.path.join(d2, "grade.txt"))
    his = []
    for r in json.load(open(os.path.join(d2, "piccuts.json"))):
        if r.get("pic_rel") is None or r.get("confidence", 0) < args.trusted:
            continue
        i = r["i"]
        cur, prev = E[i], E[i - 1]
        n0 = round(cur["cut_in"] * FPS)
        pn0 = round(prev["cut_in"] * FPS)
        A = frames_from(RAW2, prev["src_in"] + (n0 - W - pn0) / FPS, N, g2)
        B = frames_from(RAW2, cur["src_in"] - W / FPS, N, g2)
        if len(A) < N or len(B) < N:
            continue
        k = int(r["pic_rel"])
        ia, ib = W + k - 1, W + k
        s_k = self_sim(A[ia], B[ib]) if 0 <= ia < N and 0 <= ib < N else None
        s_0 = self_sim(A[W - 1], B[W])
        best = max(self_sim(A[W + q - 1], B[W + q]) for q in range(-W + 1, W))
        his.append(dict(i=i, cut=cur["cut_in"], k=k, conf=r["confidence"], sim_at_his_k=round(s_k, 3) if s_k is not None else None,
                        sim_at_0=round(s_0, 3), best_sim=round(best, 3)))
        print(f"his  splice {cur['cut_in']:8.3f} k {k:+d} conf {r['confidence']:.2f}  sim@k {s_k:.2f}  sim@0 {s_0:.2f}  best {best:.2f}", flush=True)
    res["sets"]["muhammad-ad2-trusted"] = his
    # --- attempt 1: the EDL it shipped with (vert9x16/edl_final_a1.json.bak), cut ON the audio splice
    d1 = os.path.join(SSD, "ad1-8-14/vert9x16")
    E1 = load_edl(os.path.join(d1, "edl_final_a1.json.bak"))
    g1 = grade_filter(os.path.join(d1, "grade.py"))
    a1 = []
    for i in range(1, len(E1)):
        cur, prev = E1[i], E1[i - 1]
        n0 = round(cur["cut_in"] * FPS)
        pn0 = round(prev["cut_in"] * FPS)
        A = frames_from(RAW1, prev["src_in"] + (n0 - W - pn0) / FPS, N, g1)
        B = frames_from(RAW1, cur["src_in"] - W / FPS, N, g1)
        if len(A) < N or len(B) < N:
            continue
        s_0 = self_sim(A[W - 1], B[W])
        best = max(self_sim(A[W + q - 1], B[W + q]) for q in range(-W + 1, W))
        a1.append(dict(i=i, cut=cur["cut_in"], sim_at_0=round(s_0, 3), best_sim=round(best, 3)))
        print(f"a1   splice {cur['cut_in']:8.3f}  sim@0 {s_0:.2f}  best {best:.2f}", flush=True)
    res["sets"]["ad1-vertical-attempt1"] = a1
    hk = [x["sim_at_his_k"] for x in his if x["sim_at_his_k"] is not None]
    a0 = [x["sim_at_0"] for x in a1]
    res["summary"] = dict(his_at_k=dict(n=len(hk), median=round(float(np.median(hk)), 3) if hk else None,
                                        p10=round(float(np.percentile(hk, 10)), 3) if hk else None),
                          attempt1_at_0=dict(n=len(a0), median=round(float(np.median(a0)), 3) if a0 else None,
                                             p90=round(float(np.percentile(a0, 90)), 3) if a0 else None),
                          note="cover_below = the midpoint of the two medians IF they separate; if they do not, the "
                               "self-similarity is not the discriminator and the rule falls back to covering every "
                               "splice his method does not trust -- say so in template.json")
    if hk and a0:
        res["summary"]["midpoint"] = round((float(np.median(hk)) + float(np.median(a0))) / 2, 3)
        res["summary"]["separates"] = bool(np.percentile(hk, 10) > np.percentile(a0, 90))
    json.dump(res, open(os.path.join(HERE, "piccuts_calibration.json"), "w"), indent=1)
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
    d.add_argument("--talk", required=True, help="json [[t0, t1], ...] of the TALK beats")
    d.add_argument("--search", type=int, default=15)
    d.add_argument("--trusted", type=float, default=0.60)
    d.add_argument("--cover-below", type=float, required=True)
    c = sub.add_parser("calibrate")
    c.add_argument("--search", type=int, default=15)
    c.add_argument("--trusted", type=float, default=0.60)
    a = ap.parse_args()
    return dict(decide=decide, calibrate=calibrate)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
