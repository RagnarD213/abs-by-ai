#!/usr/bin/env python3
"""content.json FROM AN APPROVED BEAT SHEET -- the content decisions (which insert / plate / lower third /
CTA goes with which words) lifted out of a hand-written beats.py, with PHRASE ANCHORS so the same
content can be laid onto a different cut of the same script (the from-raw build).

  python3 content_from_beats.py --beats /Volumes/Extreme/_edit_work/ad1-sq/beats.py --cwd /Volumes/Extreme/_edit_work/ad1-sq
                                --words m.whisper.json --out content.json

Every base beat keeps its timecodes (t0/t1, valid on THIS cut) AND gains `at`/`until`: the first and last
words spoken inside the beat on the cut it was read from. Lower thirds and CTAs the same. The kit's
design devices (pushes, flashes, picture cuts, caption suppression) are NOT copied -- the kit generates
those; only what his cut SHOWS is content.
"""
import argparse
import importlib.util
import json
import os
import re

_n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def load_beats(path, cwd):
    here = os.getcwd()
    os.chdir(cwd)
    try:
        spec = importlib.util.spec_from_file_location("beats_src", path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    finally:
        os.chdir(here)
    return m


def load_words(path):
    d = json.load(open(path))
    out = []
    if isinstance(d, dict) and "segments" in d:
        for s in d["segments"]:
            for w in s.get("words", []):
                if w["word"].strip():
                    out.append((w["word"].strip(), float(w["start"]), float(w["end"])))
    else:
        for w in d:
            out.append((w.get("w") or w["word"].strip(), float(w.get("t", w.get("start"))), float(w.get("e", w.get("end")))))
    return out


def phrase_in(words, t0, t1, n=3):
    """The first n words that START inside [t0, t1] and the last n that END inside it."""
    inside = [w for w in words if t0 - 0.05 <= w[1] and w[2] <= t1 + 0.05]
    if not inside:
        near = min(words, key=lambda w: abs(w[1] - t0))
        inside = [near]
    first = " ".join(w[0] for w in inside[:n])
    last = " ".join(w[0] for w in inside[-n:])
    return first, last, inside[0][1], inside[-1][2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beats", required=True)
    ap.add_argument("--cwd", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--treat", help="a sqassets.py whose SQ table names each media's label kind (real | ai | None)")
    a = ap.parse_args()
    m = load_beats(a.beats, a.cwd)
    labels = {}
    if a.treat:
        tm = load_beats(a.treat, a.cwd)
        labels = {k: v.get("label") for k, v in tm.SQ.items()}
    words = load_words(a.words)
    tl, ov = m.timeline()
    beats = []
    for b in tl:
        if b["kind"] == "talk":
            continue
        first, last, wt0, wt1 = phrase_in(words, b["t0"], b["t1"])
        item = {k: v for k, v in b.items() if k not in ("t0", "t1")}
        if b.get("media") in labels and labels[b["media"]]:
            item["label_kind"] = labels[b["media"]]          # real | ai -- the kit places the chip by measurement
        item.update(t0=b["t0"], t1=b["t1"], at=first, until=last,
                    pad_pre=round(max(0.0, wt0 - b["t0"]), 3), pad_post=round(max(0.0, b["t1"] - wt1), 3))
        beats.append(item)
    lts, ctas = [], []
    for o in ov:
        first, last, wt0, wt1 = phrase_in(words, o["t0"], o["t1"])
        if o["kind"] == "lt":
            lts.append(dict(lines=o["lines"], t0=o["t0"], t1=o["t1"], at=first, until=last,
                            **({"y_bottom": o["y_bottom"]} if "y_bottom" in o else {})))
        elif o["kind"] == "cta":
            ctas.append(dict(t0=o["t0"], t1=o["t1"], at=first, top=o.get("top"), big=o.get("big"),
                             **({"big_size": o["big_size"]} if "big_size" in o else {})))
    out = dict(source=os.path.abspath(a.beats), words=os.path.abspath(a.words), dur=float(getattr(m, "DUR", tl[-1]["t1"])),
               cta_top=getattr(m, "CTA_TOP", None), cta_big=getattr(m, "CTA_BIG", None),
               no_caps_kinds=sorted(getattr(m, "NO_CAPS_KINDS", ["window", "title", "stmt", "cta"])),
               deviations=getattr(m, "DEVIATIONS", []), beats=beats, lower_thirds=lts, ctas=ctas)
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"{len(beats)} content beats, {len(lts)} lower thirds, {len(ctas)} CTAs -> {a.out}")


if __name__ == "__main__":
    main()
