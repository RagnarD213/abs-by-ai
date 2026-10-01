#!/usr/bin/env python3
"""Two renders of the same vertical, beat by beat: how different are they, and where?

  python3 compare_renders.py --a NEW.mp4 --b OLD.mp4 --beats NEW_BUILD/beats.json [--beats-b OLD_BUILD/beats.json] --out report.json

Both files are decoded frame by frame at 108x192 grey (BT.709). Per frame: mean |a-b| in grey levels. Reported per beat
of A's beat sheet (and per beat of B's when given): median / max difference and the frames above 12 levels (a
different picture, not encoder noise: two encodes of one picture read ~1-2). Also the sheet of the 12 most different
frames side by side (A left, B right) for a person to look at.
"""
import argparse
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
W, H = 108, 192


def frames(p):
    raw = subprocess.run([FF, "-nostdin", "-v", "error", "-i", p, "-vf",
                          f"scale={W}:{H}:in_color_matrix=bt709:in_range=tv,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True); ap.add_argument("--b", required=True)
    ap.add_argument("--beats", required=True); ap.add_argument("--beats-b")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    A, B = frames(a.a), frames(a.b)
    n = min(len(A), len(B))
    d = np.abs(A[:n] - B[:n]).mean(axis=(1, 2))
    fps = 30000 / 1001

    def per_beat(path):
        bj = json.load(open(path))
        rows = []
        items = [dict(kind=b["kind"], t0=b["t0"], t1=b["t1"], media=b.get("media")) for b in bj["beats"]]
        items += [dict(kind="lt", t0=o["t0"], t1=o["t1"]) for o in bj.get("lower_thirds", [])]
        items += [dict(kind="cta", t0=o["t0"], t1=o["t1"]) for o in bj.get("ctas", [])]
        for it in sorted(items, key=lambda x: x["t0"]):
            f0, f1 = int(it["t0"] * fps), min(n, int(it["t1"] * fps))
            if f1 <= f0:
                continue
            seg = d[f0:f1]
            rows.append(dict(it, median=round(float(np.median(seg)), 2), max=round(float(seg.max()), 2),
                             frames_over_12=int((seg > 12).sum()), frames=int(f1 - f0)))
        return rows
    rep = dict(a=a.a, b=a.b, frames_a=len(A), frames_b=len(B), median_all=round(float(np.median(d)), 2),
               frames_over_12=int((d > 12).sum()), share_over_12=round(float((d > 12).mean()), 4),
               beats_a=per_beat(a.beats))
    if a.beats_b:
        rep["beats_b"] = per_beat(a.beats_b)
    # talk stretches (outside every beat of A) as one row
    bj = json.load(open(a.beats))
    mask = np.ones(n, bool)
    for b in bj["beats"] + bj.get("lower_thirds", []) + bj.get("ctas", []):
        mask[int(b["t0"] * fps):int(b["t1"] * fps)] = False
    rep["talk_only"] = dict(frames=int(mask.sum()), median=round(float(np.median(d[mask])), 2) if mask.any() else None,
                            frames_over_12=int((d[mask] > 12).sum()))
    worst = np.argsort(-d)[:12]
    from PIL import Image
    tiles = []
    for f in sorted(worst):
        im = np.concatenate([A[f], np.full((H, 4), 255, np.int16), B[f]], axis=1).clip(0, 255).astype(np.uint8)
        tiles.append(Image.fromarray(im))
    sheet = Image.new("L", (tiles[0].width * 6, tiles[0].height * 2), 255)
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 6) * t.width, (i // 6) * t.height))
    sp = os.path.splitext(a.out)[0] + "_worst.png"
    sheet.save(sp)
    rep["worst_frames"] = [dict(frame=int(f), t=round(f / fps, 3), diff=round(float(d[f]), 1)) for f in sorted(worst)]
    rep["worst_sheet"] = sp
    json.dump(rep, open(a.out, "w"), indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("beats_a", "beats_b")}, indent=1))


if __name__ == "__main__":
    main()
