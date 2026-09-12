#!/usr/bin/env python3
"""Caption rows.

⚠ TWO FORMATS HAVE OPPOSITE CAPTION RULES AND THAT IS NOT A BUG TO NORMALISE AWAY. Organic
longforms carry NO burned captions -- the .srt sidecar is the deliverable (Dan, 2026-08-27). Ads and
Shorts carry them. So `captions:burned` is a per-format config value with two legal settings, and a
format must state which it is; it may not stay silent.
"""
import os
import re
import subprocess

import numpy as np

from .. import common as C
from ..common import Row, unmeasured


# ---------------------------------------------------------------------------- caption files
def _secs(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def read_cues(path):
    """[(start, end, text)] from an .ass or .srt file."""
    if not path or not os.path.exists(path):
        return None
    txt = open(path, errors="replace").read()
    if path.lower().endswith(".ass"):
        out = []
        for line in txt.splitlines():
            if line.startswith("Dialogue:"):
                f = line.split(",", 9)
                out.append((_secs(f[1]), _secs(f[2]), f[9]))
        return out
    out = []
    for blk in re.split(r"\n\s*\n", txt.strip()):
        m = re.search(r"(\d\d:\d\d:\d\d[,.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d+)", blk)
        if not m:
            continue
        a, b = (x.replace(",", ".") for x in m.groups())
        body = blk[m.end():].strip()
        out.append((_secs(a), _secs(b), body))
    return out


def _ass_ink_bbox(ass_path, cue_line, w, h, out_dir):
    """Render ONE cue over pure green and take the bbox of everything that is not green.

    This is the only honest way to know where a caption actually inks: fill, outline and shadow all
    move the bottom edge, and `MarginV` is none of them. (website-video rev 2 shipped MarginV 300
    inking at y 727-806 over lower thirds at y 757-905 -- 49 px of overlap on every lower-third
    beat, while QC compared captions only against full-screen cards.)
    """
    head = []
    for line in open(ass_path, errors="replace"):
        if line.startswith("Dialogue:"):
            break
        head.append(line.rstrip("\n"))
    f = cue_line.split(",", 9)
    f[1], f[2] = "0:00:00.00", "0:00:02.00"
    tmp = os.path.join(out_dir, "_cue.ass")
    open(tmp, "w").write("\n".join(head) + "\n" + ",".join(f) + "\n")
    raw = subprocess.run([C.FF, "-v", "error", "-f", "lavfi",
                          "-i", f"color=c=0x00FF00:s={w}x{h}:r=30:d=2",
                          "-vf", f"ass={tmp}", "-ss", "1", "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    if len(raw) < w * h * 3:
        return None
    a = np.frombuffer(raw[:w * h * 3], np.uint8).reshape(h, w, 3).astype(int)
    ink = ~((a[..., 0] < 60) & (a[..., 1] > 190) & (a[..., 2] < 60))
    ys, xs = np.where(ink)
    return None if len(ys) == 0 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def _alpha_bbox(mov, dt, w, h):
    raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{max(0.0, dt):.3f}", "-i", mov,
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True).stdout
    if len(raw) < w * h * 4:
        return None
    al = np.frombuffer(raw[:w * h * 4], np.uint8).reshape(h, w, 4)[..., 3]
    ys, xs = np.where(al > 8)
    return None if len(ys) == 0 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def _vgap(c, g):
    """Vertical clearance between two bboxes; None = they do not overlap horizontally;
    negative = they overlap."""
    if c[2] < g[0] or c[0] > g[2]:
        return None
    if c[3] < g[1]:
        return g[1] - c[3]
    if c[1] > g[3]:
        return c[1] - g[3]
    return -(min(c[3], g[3]) - max(c[1], g[1]))


# ---------------------------------------------------------------------------- rows
def graphic_clearance(key, pr, cfg, plan, video, work):
    """captions:graphic_clearance -- every caption clears every graphic it shares a frame with.

    ⚠ THIS ROW NEEDS THE BUILD'S CAPTION FILE AND ITS GRAPHIC MOVs, and that is deliberate. A
    delivered-pixel version was attempted and abandoned on 2026-09-11 after four detectors: over the
    whole of website rev 2 (rejected) and rev 4 (approved), bright-outlined-static-shaped text
    clustering could not separate a caption from a phone screen recording's on-screen keyboard, from
    B-roll texture behind a locked-off camera, or from the two halves of one caption line split at a
    word space. Measured: at a 40 px column gap, "goal physique." alone read as two blocks 44 px
    apart. Rev 2 and rev 4 were indistinguishable on every statistic tried. The exact measurement --
    the cue's own rendered ink against the graphic's own alpha -- has no such ambiguity, and both
    inputs exist at delivery time because the build makes them.

    ⚠ CONSEQUENCE, recorded honestly: this row therefore CANNOT be proven against corpus entry
    `website-rev2`, whose build plan (tight_cuts.json, cap.ass, gfx/*.mov) is not on disk -- it
    lived in Media/, which is gitignored. The corpus keeps `captions:graphic_clearance` PENDING for
    that reason rather than letting the row go green on a NOT MEASURED. It clears the first time a
    delivery carries both the defect and its plan.
    """
    ass = plan.get("captions_ass")
    gfx = plan.get("graphics")
    if not ass or not os.path.exists(ass):
        return unmeasured(key, "the plan gives no readable `captions_ass`; the cue's own rendered "
                               "ink is the only honest measure of where a caption reaches")
    if not gfx:
        return unmeasured(key, "the plan declares no `graphics` (name, beat, mov) to clear")
    w, h = pr["width"], pr["height"]
    cues = [l.rstrip("\n") for l in open(ass, errors="replace") if l.startswith("Dialogue:")]
    gap_min = cfg["min_px"]
    pairs, bad = [], []
    for line in cues:
        f = line.split(",", 9)
        ca, cb, txt = _secs(f[1]), _secs(f[2]), f[9]
        hits = [g for g in gfx if not (cb <= g["beat"][0] + 0.02 or ca >= g["beat"][1] - 0.02)]
        if not hits:
            continue
        ink = _ass_ink_bbox(ass, line, w, h, work)
        if ink is None:
            continue
        for g in hits:
            mov = g.get("mov")
            if not mov or not os.path.exists(mov):
                bad.append((round(ca, 2), g["name"], "graphic MOV not on disk", txt[:40]))
                continue
            a, b = g["beat"]
            lo, hi = max(ca, a), min(cb, b)
            ts = [lo + 0.03, (lo + hi) / 2, hi - 0.03] if hi - lo > 0.1 else [(lo + hi) / 2]
            boxes = [_alpha_bbox(mov, min(t - a, (b - a) - 0.04), w, h) for t in ts]
            boxes = [x for x in boxes if x]
            if not boxes:
                continue
            gb = (min(x[0] for x in boxes), min(x[1] for x in boxes),
                  max(x[2] for x in boxes), max(x[3] for x in boxes))
            gp = _vgap(ink, gb)
            if gp is None:
                continue
            pairs.append(gp)
            if gp < gap_min:
                bad.append((round(ca, 2), g["name"], gp, txt[:40]))
    if not pairs and not bad:
        return unmeasured(key, "no caption cue overlaps any declared graphic beat -- either the "
                               "beats or the cue times are wrong, because a video with both should "
                               "have some")
    return Row(key, not bad,
               f"{len(pairs)} cue/graphic pairs; tightest {min(pairs) if pairs else 'n/a'} px "
               f"(min {gap_min} px); {len(bad)} collision(s): {bad[:5]}",
               dict(pairs=len(pairs), tightest=min(pairs) if pairs else None,
                    min_px=gap_min, bad=bad[:20]))


def card_collision(key, pr, cfg, plan, video, work):
    """captions:card_collision -- no caption sits on a full-screen card."""
    cues = read_cues(plan.get("captions_ass") or plan.get("srt"))
    cards = plan.get("cards")
    if cues is None:
        return unmeasured(key, "the plan gives no readable `captions_ass` or `srt`")
    if cards is None:
        return unmeasured(key, "the plan declares no `cards` (the full-screen beats). An empty "
                               "list is a legal answer and says there are none")
    # 0.02 s slack: ASS timestamps are centisecond-quantised (ad-edit lesson 66)
    bad = [(round(a, 2), t[:40]) for a, b, t in cues
           if any(not (b <= s + 0.02 or a >= e - 0.02) for s, e in cards)]
    return Row(key, not bad, f"{len(cues)} cues, {len(cards)} cards, {len(bad)} on a card: {bad[:6]}",
               dict(cues=len(cues), cards=len(cards), bad=bad[:20]))


def burned(key, pr, cfg, plan, video, work):
    """captions:burned -- burned captions are present, or absent, as this format requires.

    Burned captions leave a signature: near-white pixels with a dark outline in a band across the
    lower third, on most frames of a talking-head video.
    """
    want = cfg["present"]
    band = cfg["band"]                                    # (x, y, w, h) as a fraction of the frame
    W, H = pr["width"], pr["height"]
    cw, cy = int(W * band[2]), int(H * band[1])
    cx, ch = int(W * band[0]), int(H * band[3])
    dur = pr["vdur"]
    hits = n = 0
    for t in np.linspace(dur * 0.05, dur * 0.95, cfg.get("samples", 36)):
        raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                              "-vf", f"crop={cw}:{ch}:{cx}:{cy},format=gray",
                              "-f", "rawvideo", "-"], capture_output=True).stdout
        if not raw:
            continue
        b = np.frombuffer(raw, dtype=np.uint8)
        n += 1
        if 0.004 < (b > 225).mean() < 0.20 and (b < 40).mean() > 0.01:
            hits += 1
    frac = hits / max(n, 1)
    if want:
        lo = cfg["min_frac"]
        return Row(key, frac >= lo,
                   f"burned captions on {frac*100:.0f}% of {n} sampled frames (min {lo*100:.0f}%)",
                   dict(frac=round(frac, 3), min=lo, samples=n))
    hi = cfg["max_frac"]
    return Row(key, frac <= hi,
               f"no burned captions required; detected on {frac*100:.0f}% of {n} sampled frames "
               f"(max {hi*100:.0f}%)",
               dict(frac=round(frac, 3), max=hi, samples=n))


def within_runtime(key, pr, cfg, plan, video, work):
    """captions:within_runtime -- no cue starts or ends past the end of the picture."""
    cues = read_cues(plan.get("captions_ass") or plan.get("srt"))
    if cues is None:
        return unmeasured(key, "the plan gives no readable `captions_ass` or `srt`")
    dur = pr["vdur"]
    tol = cfg.get("tolerance_s", 0.10)
    over = [(round(a, 2), round(b, 2)) for a, b, _ in cues if b > dur + tol]
    return Row(key, not over, f"{len(cues)} cues, last ends {max(b for _, b, _ in cues):.2f}s "
                              f"against a {dur:.2f}s picture; {len(over)} past the end: {over[:5]}",
               dict(cues=len(cues), over=over[:20]))


def sync(key, pr, cfg, plan, video, work):
    """captions:sync -- a cue starts when the speech in it starts.

    Dan, 2026-09-08: the highlighted word must be the word being said. Measured off the DELIVERED
    audio: for every cue that follows at least `gap` of silence, the speech onset after the cue's
    start must land inside the tolerance. A caption that runs early reads as a different sentence.
    """
    cues = read_cues(plan.get("captions_ass") or plan.get("srt"))
    if cues is None:
        return unmeasured(key, "the plan gives no readable `captions_ass` or `srt`")
    sr = 16000
    a = C.pcm(video, ac=1, sr=sr)
    hop = int(sr * 0.005)
    fr = a[:len(a) // hop * hop].reshape(-1, hop)
    env = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    thr = float(np.percentile(env, 50)) - 12
    speech = env > thr
    gap = cfg.get("silence_before_s", 0.30)
    tol = cfg["tolerance_ms"] / 1000.0
    # ⚠ SEARCH BACKWARDS AS WELL AS FORWARDS. Searching only forward from the cue can produce a
    # negative offset for nothing, so a caption that arrives LATE -- the speech already running when
    # the cue appears -- would read as perfectly synced. Both directions, or the row is one-sided.
    back = cfg.get("search_back_s", 0.60)
    fwd = cfg.get("search_fwd_s", 1.50)
    offs = []
    for st, _en, _t in cues:
        i = int(st / 0.005)
        g = int(gap / 0.005)
        b = int(back / 0.005)
        if i - g - b < 0 or i + int(fwd / 0.005) >= len(speech):
            continue
        if speech[max(0, i - g - b):i - b].mean() > 0.15:
            continue                                        # not preceded by silence: skip
        w = speech[i - b:i + int(fwd / 0.005)]
        nxt = np.where(w)[0]
        if not len(nxt):
            continue
        offs.append(round(float(nxt[0] * 0.005 - back), 3))
    if len(offs) < cfg.get("min_samples", 5):
        return unmeasured(key, f"only {len(offs)} cue(s) start after {gap}s of silence -- not "
                               f"enough to measure caption sync on this cut")
    med = float(np.median(offs))
    worst = max(offs, key=abs)
    return Row(key, abs(med) <= tol and abs(worst) <= tol * 3,
               f"{len(offs)} cues measured: speech starts a median {med*1000:+.0f} ms after the cue "
               f"(worst {worst*1000:+.0f} ms, max {tol*1000:.0f} ms)",
               dict(n=len(offs), median_ms=round(med * 1000, 1), worst_ms=round(worst * 1000, 1),
                    tol_ms=cfg["tolerance_ms"]))
