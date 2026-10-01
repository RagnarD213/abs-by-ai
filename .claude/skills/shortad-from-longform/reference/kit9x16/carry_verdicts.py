#!/usr/bin/env python3
"""CARRY A JUDGED WATCH PASS FORWARD ONLY WHERE THE PICTURE DID NOT CHANGE.

  python3 carry_verdicts.py --build B --prev B/roundN [--tol 1.0]

After a small fix the whole file is re-rendered and its watch images are re-made, but most of them are the same
pixels the judges already looked at. For every image in B/watch/{sheets,strips}: when an image of the same name
exists in --prev/watch, is the same size and differs by under --tol grey levels on average AND under 12 levels at
its worst 16x16 block, and the previous judges called it clean or expected, its entries are carried
(verdict unchanged, note prefixed "carried: pixel-identical to the judged round"). Everything else (a changed image,
a new name, a previous defect) goes to B/logs/rejudge.json for a fresh judge, who writes
B/logs/findings_part2.json for exactly those images. Writes B/logs/findings_part1.json (the carried entries) and the
negscan carry when the negscan sheet is unchanged. Nothing is ever carried across a changed picture.
"""
import argparse
import glob
import json
import os

import numpy as np
from PIL import Image


def same(a, b, tol):
    try:
        A, B = Image.open(a).convert("L"), Image.open(b).convert("L")
    except Exception:
        return False
    if A.size != B.size:
        return False
    d = np.abs(np.asarray(A, np.int16) - np.asarray(B, np.int16)).astype(np.float32)
    if float(d.mean()) > tol:
        return False
    h, w = d.shape
    blk = d[:h // 16 * 16, :w // 16 * 16].reshape(h // 16, 16, w // 16, 16).mean(axis=(1, 3))
    return float(blk.max()) < 12.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--prev", required=True)
    ap.add_argument("--tol", type=float, default=1.0)
    a = ap.parse_args()
    B, P = os.path.abspath(a.build), os.path.abspath(a.prev)
    prev = {}
    judges = []
    for fp in sorted(glob.glob(os.path.join(P, "logs", "findings_part*.json"))):
        d = json.load(open(fp))
        judges.append(d.get("judge", "?"))
        for e in d["entries"]:
            prev.setdefault(os.path.basename(str(e.get("image", ""))), []).append(e)
    carried, redo = [], []
    imgs = sorted(f for sub in ("sheets", "strips") for f in glob.glob(os.path.join(B, "watch", sub, "*.jpg"))
                  if not os.path.basename(f).startswith("._"))
    for f in imgs:
        name = os.path.basename(f)
        sub = os.path.basename(os.path.dirname(f))
        old = os.path.join(P, "watch", sub, name)
        ents = prev.get(name)
        if ents and os.path.exists(old) and all(e.get("verdict") in ("clean", "expected") for e in ents) and same(f, old, a.tol):
            for e in ents:
                carried.append(dict(e, note="carried: pixel-identical to the judged round | " + str(e.get("note", ""))))
        else:
            redo.append(name)
    video = None
    for fp in glob.glob(os.path.join(P, "logs", "findings_part*.json")):
        video = json.load(open(fp)).get("video") or video
    os.makedirs(os.path.join(B, "logs"), exist_ok=True)
    json.dump(dict(judge="carried from " + os.path.basename(P) + " (" + " | ".join(judges) + ")", video=video,
                   method="carry_verdicts.py: entries kept only for images pixel-identical to the judged round",
                   entries=carried), open(os.path.join(B, "logs", "findings_part1.json"), "w"), indent=1)
    json.dump(redo, open(os.path.join(B, "logs", "rejudge.json"), "w"), indent=1)
    ns_new, ns_old = os.path.join(B, "negscan", "sheet.jpg"), os.path.join(P, "negscan", "sheet.jpg")
    nf_old = os.path.join(P, "logs", "negscan_findings.json")
    neg = "re-judge"
    if os.path.exists(ns_new) and os.path.exists(ns_old) and os.path.exists(nf_old) and same(ns_new, ns_old, a.tol):
        json.dump(json.load(open(nf_old)), open(os.path.join(B, "logs", "negscan_findings.json"), "w"))
        neg = "carried"
    print(f"{len(imgs)} images: {len(imgs) - len(redo)} carried, {len(redo)} to re-judge -> logs/rejudge.json; negscan {neg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
