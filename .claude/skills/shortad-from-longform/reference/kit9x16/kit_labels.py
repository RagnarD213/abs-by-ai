#!/usr/bin/env python3
"""LABEL CHIPS PLACED BY MEASURING HIM -- the approved square's method (a11_sq_ad1/sqlabelplace.py,
Dan 2026-09-13: "put that above my head or somewhere it doesn't block my face or abs") ported to the
9:16 full-bleed beats. For every bleed beat whose content carries `label_kind` (real | ai): render the
beat WITHOUT a chip, person-mask every 3rd frame + the last (stills push, so frame 0 is not enough),
take the union, dilate it CLEAR px, and search chip placements in preference order:
   A  one line, fully ABOVE his head          (Dan's first choice)
   B  beside his head, one to three lines, high in the frame
   C  anywhere else clear of him, above the caption band
Bigger type beats fewer lines. Writes the chip layer PNG per beat, `chip_png` + `chip_box` into
beats.json, label_place.json and a proof tile per beat; `--verify <delivered>` re-masks the delivered
file and fails if any chip box comes within VERIFY_PX of him.

  python3 kit_labels.py --build DIR            # place (renders the labelled bleed beats chip-less first)
  python3 kit_labels.py --build DIR --verify master.mp4
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
PERSONMASK = os.path.join(REPO, ".claude/skills/shorts/reference/recentre/personmask")
sys.path.insert(0, os.path.join(REPO, ".claude/skills/_shared"))
from motionlib import font, text_size  # noqa: E402

FPS = 30000 / 1001
VW, VH = 1080, 1920
REAL_LABEL = "Real picture of me — not AI-generated"
AI_LABEL = "AI-GENERATED"
CLEAR = 16                    # px of clearance between the chip and any pixel of him (sqlabelplace)
VERIFY_PX = 8                 # the delivered-file bound (sqlabelplace --verify)
TOP_SAFE = 150                # nothing readable above this (vlib TOP_SAFE)
CHIP_BOTTOM_MAX = 1340        # above the caption band (CAP_Y 1400 minus the shadow)
INK = (255, 255, 255, 255)


def chip_parts(label, lines):
    if lines == 1 or label != REAL_LABEL:
        return [label]
    if lines == 2:
        return ["Real picture of me", "— not AI-generated"]
    return ["Real picture", "of me — not", "AI-generated"]


def chip_dims(label, lines, size):
    f = font(size, "SemiBold")
    parts = chip_parts(label, lines)
    w = max(text_size(p, f)[0] for p in parts) + 34
    h = (int(size * 1.18) * len(parts) + 22) if lines > 1 else text_size(parts[0], f)[1] + 22
    return int(w), int(h)


def chip_at(label, x, y, lines=1, size=34):
    f = font(size, "SemiBold")
    parts = chip_parts(label, lines)
    w, h = chip_dims(label, lines, size)
    lay = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x, y, x + w, y + h], radius=9, fill=(0, 0, 0, 215))
    if len(parts) == 1:
        d.text((x + 17, y + 11), parts[0], font=f, fill=INK, anchor="lt")
    else:
        lh = int(size * 1.18)
        asc = f.getmetrics()[0]
        for i, p_ in enumerate(parts):
            d.text((x + (w - text_size(p_, f)[0]) // 2, y + 11 + i * lh + asc), p_, font=f, fill=INK, anchor="ls")
    return lay


def masks_for(video, idxs, d):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + "/m")
    sel = "+".join(f"eq(n,{i})" for i in idxs)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", video, "-vf", f"select='{sel}'", "-fps_mode", "passthrough",
                    f"{d}/%04d.png"], check=True)
    fs = sorted(glob.glob(f"{d}/*.png"))
    if not fs:
        raise SystemExit(f"no frames extracted from {video} at {idxs[:4]}")
    subprocess.run([PERSONMASK, f"{d}/m"] + fs, check=True, capture_output=True)
    ms = []
    for f in fs:
        mf = f"{d}/m/" + os.path.basename(f).replace(".png", ".mask.png")
        ms.append(np.array(Image.open(mf).convert("L").resize((VW, VH))) > 127)
    return fs, ms


def dilate(m, r):
    from scipy.ndimage import binary_dilation
    return binary_dilation(m, iterations=r)


def head_box(m):
    ys, xs = np.nonzero(m)
    y0 = ys.min()
    hs = xs[ys <= y0 + 0.12 * VH]
    return int(hs.min()), int(y0), int(hs.max()), int(y0 + 0.12 * VH)


def candidates(label, union, hbox):
    """Every clear placement worth trying, in preference order: class A (above the head) before B (beside
    it) before C (anywhere clear), bigger type before fewer lines; per (class, size, lines) the best
    position plus mirrored / lower alternates, because the VALIDATION below can refuse the first."""
    hx0, hy0, hx1, hy1 = hbox
    hcx = (hx0 + hx1) / 2
    dil = dilate(union, CLEAR)
    ii = np.pad(dil.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))

    def clear(x, y, w, h):
        return ii[y + h, x + w] - ii[y, x + w] - ii[y + h, x] + ii[y, x] == 0
    lines_opts = (1, 2, 3) if label == REAL_LABEL else (1,)
    out = []
    for cls in ("A", "B", "C"):
        for size in (44, 40, 36, 34, 32, 30, 28):
            for lines in lines_opts:
                w, h = chip_dims(label, lines, size)
                found = []
                for y in range(TOP_SAFE, CHIP_BOTTOM_MAX - h + 1, 6):
                    for x in range(40, VW - 40 - w + 1, 6):
                        if not clear(x, y, w, h):
                            continue
                        above = y + h <= hy0
                        beside = (not above) and y < hy1
                        if cls == "A" and not above:
                            continue
                        if cls == "B" and not beside:
                            continue
                        cost = abs(x + w / 2 - hcx) + (0 if cls == "A" else 0.5 * y)
                        found.append((cost, x, y))
                found.sort()
                picked = []
                for cost, x, y in found:                      # the best, then alternates at least 150 px away
                    if all(abs(x - px) + abs(y - py) >= 150 for _, px, py in picked):
                        picked.append((cost, x, y))
                    if len(picked) >= 3:
                        break
                for cost, x, y in picked:
                    out.append(dict(cls=cls, lines=lines, size=size, x=x, y=y, w=w, h=h))
    return out


def validate(label, c, frames, tag):
    """⚠ VALIDATE WITH THE CHIP IN THE FRAME. The gate's compliance:labels row person-masks the DELIVERED
    frame, chip and all, and Apple Vision absorbs a dark chip into the person on some pictures (the kit's
    first Ad 1 render: `today_towel` read 33,275 px of contact = the whole chip box, at a placement that
    is 16 px clear of him on the chip-less frame). A placement only counts if the segmenter still reads
    the chip box as clear WITH the chip drawn, on the first, middle and last frames of the beat."""
    d = f"labels/_val_{tag}"
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d + "/m")
    lay = chip_at(label, c["x"], c["y"], c["lines"], c["size"])
    ps = []
    for i, f in enumerate(frames):
        im = Image.open(f).convert("RGBA")
        im.alpha_composite(lay)
        q = f"{d}/{i:02d}.png"
        im.convert("RGB").save(q)
        ps.append(q)
    subprocess.run([PERSONMASK, f"{d}/m"] + ps, check=True, capture_output=True)
    worst = 0
    for q in ps:
        m = np.array(Image.open(f"{d}/m/" + os.path.basename(q).replace(".png", ".mask.png")).convert("L").resize((VW, VH))) > 127
        worst = max(worst, int(dilate(m, VERIFY_PX)[c["y"]:c["y"] + c["h"], c["x"]:c["x"] + c["w"]].sum()))
    shutil.rmtree(d, ignore_errors=True)
    return worst


def render_beats(build, idxs):
    """render.py --only i,j renders those segments into out/s{i}.mp4 (chip-less when chip_png is absent)."""
    subprocess.run([sys.executable, "render.py", "--only", ",".join(str(i) for i in idxs)], cwd=build, check=True)


def place(build):
    os.chdir(build)
    sys.path.insert(0, os.getcwd())
    J = json.load(open("beats.json"))
    import beats as B
    tl, _ = B.timeline()
    todo = [(i, b) for i, b in enumerate(tl) if b["kind"] == "bleed" and b.get("label_kind") in ("real", "ai")]
    if not todo:
        print("no labelled full-bleed beats")
        return
    # 1. render them WITHOUT a chip
    for i, b in todo:
        b.pop("chip_png", None)
    for jb in J["beats"]:
        jb.pop("chip_png", None); jb.pop("chip_box", None)
    json.dump(J, open("beats.json", "w"), indent=1)
    render_beats(build, [i for i, _ in todo])
    os.makedirs("labels", exist_ok=True)
    res = {}
    prev = 0
    starts = {}
    for i, b in enumerate(tl):
        cum = round(b["t1"] * FPS)
        starts[i] = (prev, cum - prev)
        prev = cum
    for i, b in todo:
        n0, nfr = starts[i]
        key = b.get("media") or f"beat{i}"
        label = REAL_LABEL if b["label_kind"] == "real" else AI_LABEL
        vid = f"out/s{i:03d}.mp4"
        idxs = sorted(set(list(range(0, nfr, 3)) + [nfr - 1]))
        fs, ms = masks_for(vid, idxs, f"labels/{key}")
        union = np.any(ms, axis=0)
        if union.sum() < 2000:
            raise SystemExit(f"{key}: the person mask found nobody in the beat -- is this a picture of Dan?")
        hb = head_box(union)
        c, tried = None, []
        probe = [fs[0], fs[len(fs) // 2], fs[-1]]
        for cand in candidates(label, union, hb)[:24]:
            contact = validate(label, cand, probe, key)
            tried.append((cand["cls"], cand["lines"], cand["size"], cand["x"], cand["y"], contact))
            if contact == 0:
                c = cand
                break
        if not c:
            raise SystemExit(f"{key}: no placement the segmenter reads as clear with the chip drawn (tried {tried[:8]}...) -- "
                             "pick a different picture (Dan prefers a correct different picture over a cropped right one)")
        lay = chip_at(label, c["x"], c["y"], c["lines"], c["size"])
        png = os.path.abspath(f"labels/chip_{key}.png")
        lay.save(png)
        res[key] = dict(c, beat=[b["t0"], b["t1"]], head=hb, label=label, png=png, tried=tried,
                        body=[int(v) for v in (np.nonzero(union)[1].min(), np.nonzero(union)[0].min(),
                                               np.nonzero(union)[1].max(), np.nonzero(union)[0].max())])
        for jb in J["beats"]:
            if jb.get("media") == b.get("media") and abs(jb["t0"] - b["t0"]) < 0.01:
                jb["chip_png"] = png
                jb["chip_box"] = [c["x"], c["y"], c["w"], c["h"]]
                jb["label"] = label
        tiles = []
        for f in (fs[0], fs[-1]):
            im = Image.open(f).convert("RGBA")
            im.alpha_composite(lay)
            arr = np.array(im)
            edge = dilate(union, 2) & ~union
            arr[edge] = [255, 0, 0, 255]
            tiles.append(Image.fromarray(arr).convert("RGB").resize((540, 960)))
        sheet = Image.new("RGB", (1080, 960))
        sheet.paste(tiles[0], (0, 0))
        sheet.paste(tiles[1], (540, 0))
        sheet.save(f"labels/{key}_proof.jpg")
        print(f"{key:16s} {label[:12]:12s} class {c['cls']} {c['lines']}L@{c['size']} at {c['x']},{c['y']} {c['w']}x{c['h']}  head {hb}", flush=True)
    json.dump(J, open("beats.json", "w"), indent=1)
    json.dump(res, open("label_place.json", "w"), indent=1)
    print(f"{len(res)} chips placed -> label_place.json, labels/*_proof.jpg; beats.json updated (re-render those beats)")


def verify(build, video):
    os.chdir(build)
    sys.path.insert(0, os.getcwd())
    import beats as B
    tl, _ = B.timeline()
    prev, bad, out = 0, 0, {}
    for i, b in enumerate(tl):
        cum = round(b["t1"] * FPS)
        n0, nfr = prev, cum - prev
        prev = cum
        if b["kind"] != "bleed" or not b.get("chip_box"):
            continue
        x, y, w, h = b["chip_box"]
        key = b.get("media") or f"beat{i}"
        idxs = sorted(set([n0 + k for k in range(0, nfr, 3)] + [n0 + nfr - 1]))
        fs, ms = masks_for(video, idxs, f"labels/verify_{key}")
        worst = max(int(dilate(m, VERIFY_PX)[y:y + h, x:x + w].sum()) for m in ms)
        ok = worst == 0
        bad += not ok
        out[key] = dict(box=[x, y, w, h], frames=len(ms), contact_px=worst, ok=ok)
        print(f"{'PASS' if ok else 'FAIL'}  {key:16s} box {x},{y} {w}x{h}  {len(ms)} frames  contact {worst} px")
    json.dump(out, open(video + ".labelcheck.json", "w"), indent=1)
    print("LABELS OFF HIS BODY", "PASS" if not bad else f"FAIL ({bad})")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--verify")
    a = ap.parse_args()
    if a.verify:
        return 1 if verify(a.build, a.verify) else 0
    place(a.build)
    return 0


if __name__ == "__main__":
    sys.exit(main())
