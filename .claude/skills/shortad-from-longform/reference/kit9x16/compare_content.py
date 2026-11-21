#!/usr/bin/env python3
"""ANSWER-KEY TEST for auto_content.py: compare an auto-written content.json with a hand-written one.

  python3 compare_content.py --auto B/content.json --auto-assets B/assets.py --key KEY/content.json --key-assets KEY/assets.py
                             [--key-root KEY_BUILD_DIR] [--out report.json] [--tol 0.2]

Beats are paired by time overlap (IoU), lower thirds and CTAs likewise. Reported per pair: kind, t0/t1 error, text
(exact and case/punctuation-insensitive), media file, label_kind. A REAL vs AI label swap is a HARD FAILURE (exit 2).
The key's own hand choices that no measurement of the master can reproduce (a substituted stock clip, a Dan-directed
revision) show up as media/timing differences and are listed, never hidden.
Regression use: `python3 compare_content.py ... --baseline answer_keys/<ad>.json` fails (exit 1) if any score drops.
"""
import argparse
import difflib
import importlib.util
import json
import os
import re
import sys

KIND_EQ = {("stmt", "window"), ("window", "stmt"), ("winmedia", "card"), ("card", "winmedia"), ("bleed2", "bleed")}


def load_media(path, root):
    if not path or not os.path.exists(path):
        return {}
    spec = importlib.util.spec_from_file_location("m_" + str(abs(hash(path))), path)
    m = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    try:
        os.chdir(root or os.path.dirname(path))
        spec.loader.exec_module(m)
    finally:
        os.chdir(cwd)
    master = getattr(m, "MASTER", None)
    out = {}
    for k, v in m.MEDIA.items():
        p = v[1]
        lift = master is not None and os.path.abspath(p) == os.path.abspath(master)
        full = p if os.path.isabs(p) else os.path.join(root or os.path.dirname(path), p)
        # a clip cut from HIS master (auto_content's assets_auto/, AV-07's assets_ad10/ crops) counts as a lift of it
        derived = v[0] == "vid" and any(x in full for x in ("/assets_auto/", "/assets_ad10/"))
        out[k] = dict(typ=v[0], file=os.path.basename(p), path=full, lift=derived or lift or "muhammad" in os.path.basename(p).lower(),
                      t=v[2] if len(v) > 2 else 0)
    return out


def norm(s):
    s = (s or "").lower().replace("'", "").replace("’", "").replace("-", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", s)).strip()


_SAME = {}


def same_picture(pa, pb):
    """Two files that hold the same photograph (a library copy and a reference-ad copy, jpg vs png): ORB + RANSAC."""
    import cv2
    import numpy as np
    k = tuple(sorted((pa, pb)))
    if k in _SAME:
        return _SAME[k]
    def feat(p):
        if os.path.splitext(p)[1].lower() in (".mp4", ".mov"):
            cap = cv2.VideoCapture(p); ok, im = cap.read(); cap.release()
            im = im if ok else None
        else:
            im = cv2.imread(p)
        if im is None:
            return None, None
        s = min(1.0, 1000 / max(im.shape[:2]))
        g = cv2.cvtColor(cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        kp, d = cv2.ORB_create(1500).detectAndCompute(g, None)
        return np.float32([x.pt for x in kp]) if kp else None, d
    (qa, da), (qb, db) = feat(pa), feat(pb)
    ok = False
    if da is not None and db is not None:
        m = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2)
        good = [x for x, y in (t for t in m if len(t) == 2) if x.distance < 0.75 * y.distance]
        if len(good) >= 12:
            H, mask = cv2.findHomography(np.float32([qa[g.queryIdx] for g in good]), np.float32([qb[g.trainIdx] for g in good]), cv2.RANSAC, 6.0)
            ok = mask is not None and int(mask.sum()) >= 60
    _SAME[k] = ok
    return ok


def text_of(b):
    if b.get("bullets"):
        return " | ".join(b["bullets"]) + (" || " + b["header"] if b.get("header") else "")
    if b.get("headline"):
        return b["headline"] + " / " + (b.get("sub") or "")
    if b.get("parts"):
        return " ".join(p[0] for p in b["parts"])
    if b.get("lines"):
        return " / ".join(b["lines"])
    return None


def iou(a, b):
    i = max(0.0, min(a["t1"], b["t1"]) - max(a["t0"], b["t0"]))
    u = max(a["t1"], b["t1"]) - min(a["t0"], b["t0"])
    return i / u if u > 0 else 0.0


def pair(A, K):
    """Greedy by IoU, each side used once, IoU > 0.2."""
    cand = sorted(((iou(a, k), i, j) for i, a in enumerate(A) for j, k in enumerate(K)), reverse=True)
    ua, uk, pairs = set(), set(), []
    for s, i, j in cand:
        if s < 0.2 or i in ua or j in uk:
            continue
        ua.add(i); uk.add(j); pairs.append((i, j, s))
    return pairs, [i for i in range(len(A)) if i not in ua], [j for j in range(len(K)) if j not in uk]


def media_same(ma, mk):
    """True = the same file (or both lifted from his master); "same picture" = another file of the same photo."""
    if not ma or not mk:
        return None
    if ma["lift"] and mk["lift"]:
        return True
    if ma["file"] == mk["file"]:
        return True
    if os.path.exists(ma["path"]) and os.path.exists(mk["path"]) and same_picture(ma["path"], mk["path"]):
        return "same picture"
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", required=True)
    ap.add_argument("--auto-assets")
    ap.add_argument("--key", required=True)
    ap.add_argument("--key-assets")
    ap.add_argument("--key-root")
    ap.add_argument("--tol", type=float, default=0.2)
    ap.add_argument("--out")
    ap.add_argument("--baseline", help="a previous report: fail if any headline score is lower now")
    a = ap.parse_args()
    CA, CK = json.load(open(a.auto)), json.load(open(a.key))
    MA = load_media(a.auto_assets, os.path.dirname(os.path.abspath(a.auto)))
    MK = load_media(a.key_assets, a.key_root)
    rows, hard = [], []

    def section(name, A, K):
        pairs, ea, ek = pair(A, K)
        for i, j, s in pairs:
            x, k = A[i], K[j]
            kx, kk = x.get("kind", name), k.get("kind", name)
            r = dict(section=name, t=k["t0"], key_kind=kk, auto_kind=kx,
                     kind_ok=kx == kk or (kx, kk) in KIND_EQ,
                     dt0=round(x["t0"] - k["t0"], 3), dt1=round(x["t1"] - k["t1"], 3), iou=round(s, 3))
            tk, ta = text_of(k), text_of(x)
            if tk or ta:
                r.update(key_text=tk, auto_text=ta, text_exact=(tk == ta),
                         text_norm=(norm(tk) == norm(ta)), text_ratio=round(difflib.SequenceMatcher(None, norm(tk), norm(ta)).ratio(), 3))
            if k.get("media") or x.get("media"):
                ma, mk = MA.get(x.get("media")), MK.get(k.get("media"))
                r.update(key_media=mk and mk["file"], auto_media=ma and ma["file"],
                         key_lift=mk and mk["lift"], auto_lift=ma and ma["lift"], media_ok=media_same(ma, mk))
            lk, la = k.get("label_kind"), x.get("label_kind")
            if lk or la or k.get("media"):
                r.update(key_label=lk, auto_label=la, label_ok=(lk == la))
                if lk and la and lk != la:
                    if r.get("media_ok") in (True, "same picture"):
                        hard.append(dict(t=k["t0"], key=lk, auto=la))
                    else:
                        r["label_note"] = "different pictures: the key substituted another picture here, so the labels answer different pictures"
            rows.append(r)
        for i in ea:
            rows.append(dict(section=name, t=A[i]["t0"], auto_only=True, auto_kind=A[i].get("kind", name), auto_text=text_of(A[i]),
                             auto_t1=A[i]["t1"], auto_media=(MA.get(A[i].get("media")) or {}).get("file")))
        for j in ek:
            rows.append(dict(section=name, t=K[j]["t0"], key_only=True, key_kind=K[j].get("kind", name), key_text=text_of(K[j]),
                             key_t1=K[j]["t1"], key_media=(MK.get(K[j].get("media")) or {}).get("file")))
        return len(pairs), len(ea), len(ek)

    sb = section("beats", CA["beats"], CK["beats"])
    sl = section("lower_thirds", CA.get("lower_thirds", []), CK.get("lower_thirds", []))
    sc = section("ctas", CA.get("ctas", []), CK.get("ctas", []))
    P = [r for r in rows if "iou" in r]

    def rate(key, sub=None):
        v = [r[key] for r in (sub or P) if key in r and r[key] is not None]
        return (sum(1 for x in v if x), len(v))
    tol = a.tol
    both = lambda r: abs(r["dt0"]) <= tol and abs(r["dt1"]) <= tol
    S = dict(
        beats=dict(expected=len(CK["beats"]), found=len(CA["beats"]), paired=sb[0], auto_only=sb[1], missed=sb[2]),
        lower_thirds=dict(expected=len(CK.get("lower_thirds", [])), found=len(CA.get("lower_thirds", [])), paired=sl[0], auto_only=sl[1], missed=sl[2]),
        ctas=dict(expected=len(CK.get("ctas", [])), found=len(CA.get("ctas", [])), paired=sc[0], auto_only=sc[1], missed=sc[2]),
        kinds_correct=rate("kind_ok"),
        times_within_tol=(sum(1 for r in P if both(r)), len(P)),
        t0_within_tol=(sum(1 for r in P if abs(r["dt0"]) <= tol), len(P)),
        t1_within_tol=(sum(1 for r in P if abs(r["dt1"]) <= tol), len(P)),
        median_abs_dt=round(sorted(abs(r["dt0"]) for r in P)[len(P) // 2], 3) if P else None,
        text_exact=rate("text_exact"), text_norm=rate("text_norm"),
        media_same_file=(sum(1 for r in P if r.get("media_ok") is True), sum(1 for r in P if "media_ok" in r and r["media_ok"] is not None)),
        media_correct=(sum(1 for r in P if r.get("media_ok") in (True, "same picture")), sum(1 for r in P if "media_ok" in r and r["media_ok"] is not None)),
        label_correct=rate("label_ok"),
        label_hard_failures=hard,
    )
    out = dict(summary=S, tol_s=tol, rows=sorted(rows, key=lambda r: (r["section"], r["t"])))
    if a.out:
        json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(S, indent=1))
    rc = 2 if hard else 0
    if a.baseline and os.path.exists(a.baseline):
        base = json.load(open(a.baseline))["summary"]
        worse = []
        for k in ("kinds_correct", "times_within_tol", "text_norm", "media_correct", "label_correct"):
            if tuple(S[k])[0] < tuple(base[k])[0]:
                worse.append(f"{k}: {base[k]} -> {S[k]}")
        for k in ("beats", "lower_thirds", "ctas"):
            if S[k]["paired"] < base[k]["paired"]:
                worse.append(f"{k} paired: {base[k]['paired']} -> {S[k]['paired']}")
        if worse:
            print("REGRESSION vs baseline:\n  " + "\n  ".join(worse))
            rc = rc or 1
    if hard:
        print("HARD FAILURE: real/AI label swapped at", hard)
    return rc


if __name__ == "__main__":
    sys.exit(main())
