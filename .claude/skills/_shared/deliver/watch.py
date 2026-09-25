#!/usr/bin/env python3
"""THE WATCH PASS -- the one shared module that looks at the MOVING PICTURE of a delivered file.

  watch.py <delivered file> --plan plan.json [--out DIR] [--log logs/watch_pass.json] [--clips]
  watch.py --judge logs/watch_pass.json --findings findings.json --by "<who judged>"
  watch.py --checklist

WHY THIS FILE EXISTS. Ad 1 attempt 1 passed 11/11 on a metric gate and Dan rejected it ("truly
awful... definitely won't work"): every check measured format, none ever looked at the moving
picture. Longform attempt 2 passed 15/15 and Dan found 13 problems, eight of which a human sees in
one viewing. A build once shipped all 7 lower thirds, all 3 CTA pills and all 11 flashes INVISIBLE
with every metric green. Three per-skill watch scripts grew out of those rejections, each welded to
its own build's beat sheet (`import beats`), its own ffmpeg path, and a directory of 6,000 PNGs.
None could run on a file from another skill. This is the union of the three, plan-driven and
streamed, and `_shared/deliver/gate.py`'s `watch:pass` row refuses a file whose log it did not
write for that file's sha256.

WHAT IT DOES, on the EXACT delivered file:

  1 SCAN -- every frame, streamed at native rate to a 160x90 grid (never a PNG per frame, never a
    sampled rate: the email-capture screen was once exposed for exactly one frame and a 2 fps scan
    stepped over it). Frozen runs, black frames, and hard discontinuities that are NOT at a
    boundary the plan declares. Consecutive over-threshold frames are ONE event (a dissolve, a
    wiping graphic and a fast passage each trip every frame they last; eighty "jumps" that are one
    0.4 s animation is noise). The threshold is the file's own noise, not a constant.
  2 NAKED SPLICES -- the instrument `cut:naked_splices` is built on. A jump cut is a same-scene,
    same-framing, single-frame discontinuity where the subject moves and the background does not.
    Two frame-difference detectors failed in a row on a real one (a whole-frame gray diff scored it
    at 2.0x its local median; `cut:uncovered_joins` reads the rejected Ad 1 vertical at 0.0/min),
    because a subject jump is LOCAL and a whole-frame mean dilutes it. So: a sharp single-frame
    spike in the PEAK BLOCK of a 16x9 grid, the same palette both sides, most blocks still -- then
    the pair of frames is grabbed at exact `-ss` and tested against a global scale/shift alignment.
    A deliberate push or pan aligns; a jump cut does not.
  3 GRAPHIC PRESENCE -- for every declared graphic with a MOV (or a `source_picture`), is the
    graphic actually IN the delivered pixels at that time? The only check that sees an overlay that
    rendered to an .mov and never composited.
  4 BOUNDARY STRIPS -- at every boundary, the five CONSECUTIVE frames at -2/-1/0/+1/+2 as one
    image, plus the -1|0 pair at half resolution. This is the instrument a person (or the audit
    subagent) judges a cut with: a 1 s contact sheet cannot see a jump cut, and `fps=1/N` sheets
    lag content by ~N/2 s (ad-edit lesson 94: three false alarms in one review).
  5 CONTACT SHEETS -- ~25 exact-index frames per image over the whole runtime, for the checklist
    items a strip cannot show (hair at the edge, a junk card, a label over his face, a wide level).
  6 THE LOG -- logs/watch_pass.json naming this file's sha256, every sheet and strip by name, the
    scan findings, and `judged` (empty until the judge writes it back with --judge). The gate's
    `watch:pass` row passes only when `inspected` is true, every image has a verdict, and no defect
    is left open.

WHO JUDGES. A fresh subagent in the session reads every sheet and strip against CHECKLIST (below,
also written to the out dir as CHECKLIST.md) and writes findings.json; `--judge` folds them in.
$0. It doubles as the independent audit every skill's Step 7b requires. A model-API route was
considered and not built: the local Anthropic key is recorded invalid (memory
`load-time-optimizations`) and a flag that does not run is worse than no flag.

⚠ There is no --skip and no --no-watch. The row's three states are pass / fail / NOT MEASURED.
⚠ Frames are never written one per PNG and never sampled. Sheets are exact frame indices.
⚠ Nothing here is a bound. `cut:naked_splices`'s per-minute limit lives in formats.py.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from _shared.deliver import common as C                      # noqa: E402

WATCH_VERSION = "1.2.0"   # 2026-09-23: exact-frame grabs decode two seconds of lead-in

# ---------------------------------------------------------------------------- the scan settings
# ⚠ These are part of the naked-splice calibration in formats.py. Change one and re-measure.
SCAN_LONG, SCAN_SHORT = 160, 90     # the scan grid, oriented like the file (never squashed)
BLOCKS_LONG, BLOCKS_SHORT = 16, 9   # block grid over the scan frame (10x10 px blocks)
ALIGN_LONG, ALIGN_SHORT = 320, 180  # the alignment test's frame, grabbed for candidates only
FROZEN_D = 0.05             # mean abs gray diff below which two frames are the same frame
FROZEN_MIN_FRAMES = 8       # a2/watch.py and recipe/watch.py: >= 8 frames = a frozen run
BLACK_LUM = 3.0             # reported by the scan; cut:black_frames applies formats.py's bound
MERGE_S = 0.40              # consecutive over-threshold frames within this are one event
BOUNDARY_TOL_S = 0.25       # an event this close to a declared boundary is explained by it
NAKED_PEAK = 20.0           # the peak block of a subject jump (0-255 mean abs diff)
NAKED_SHARP = 2.0           # ...and at least this many times its neighbours' peak (a spike)
NAKED_STILL = 0.25          # ...with at least this fraction of blocks still (same framing)
STILL_BLOCK = 3.0           # a block under this mean abs diff did not move
TEX_MIN = 6.0               # a block whose spatial std is under this is FLAT (sky, wall, a card panel) and
                            # says nothing about motion: it reads "still" under a zoom too. Stillness is
                            # counted over textured blocks only (Muhammad's 16:9 pushes read 58-85 % "still"
                            # on the flat patio wall before this, 2026-09-16).
HOT_BLOCK = 8.0             # a block over this moved
NAKED_HOT_MIN = 8           # ...and at least this many blocks moved: a subject is many blocks, a
                            # caption word lighting up is one or two (approved verticals read 20-27
                            # peak / 0.9 still on every karaoke word flip, 2026-09-16)
PALETTE_SAME = 0.10         # L1/2 histogram distance under which the scene is the same
SUBJECT_ROWS = 0.70         # the naked-splice statistics are taken over the TOP 70 % of the frame.
                            # Captions and lower thirds live below it in every format (formats.py:
                            # the 16:9 band starts at 0.861 of the height, 9:16 at 0.70, 1:1 at
                            # 0.72) and a karaoke caption LINE swap reads exactly like a subject
                            # jump otherwise -- sharp, same palette, background still, 8-24 blocks
                            # hot (website rev 4, 2026-09-16). A head and shoulders never sit
                            # there, so a subject jump loses nothing.
ALIGN_SCALES = tuple(round(0.80 + 0.03 * i, 2) for i in range(16))     # 0.80 .. 1.25
ALIGN_EXPLAINS = 0.40       # best aligned residual / unaligned residual: below this it is a push/pan
ALIGN_MARGIN_BLOCKS = 1     # the alignment region is the changed blocks' bbox plus this margin, so the
                            # background beside a jumped subject is inside it and a translation that
                            # lands the subject misaligns the background. A push scales the whole
                            # region about its own centre and aligns -- also inside a vertical
                            # layout's window, where a global scale of the frame never did.
SHEET_TILES = 25            # frames per contact sheet (5x5)
SHEET_MAX_FRAMES = 300      # 1 fps up to 5 minutes, then the interval grows

# ---------------------------------------------------------------------------- the checklist
# Each item cites the rejection or lesson it comes from. A judge scores EVERY sheet and strip
# against this list and names the item when it finds one.
CHECKLIST = [
    ("hair_top", "hair at or over the top edge of the frame",
     "website-rev3 (Dan: 'basically not usable'); framing:hair_top fails it, the judge confirms by eye"),
    ("out_of_frame", "head or an arm out of frame with space on the other side",
     "v2-short3-offcentre ('one of my arms is cut off and there's space on the other side')"),
    ("junk_card", "a junk or placeholder card; text running off-screen; garbled type",
     "ad-edit / longform lessons; the rev-0 spray-tan junk; shortad [A2] trap 5 (garbled lowercase)"),
    ("naked_splice", "a naked splice: same scene both sides, the subject jumps",
     "ad1-vertical-attempt1 (23 of 72 splices); read the -1|0 pair, not the sheet"),
    ("label_over_face", "a graphic or label chip over his face or over his abs; a caption on a card or the CTA pill",
     "website rev 2; Ad 1/2 square audit; AGENTS.md label placement rule"),
    ("black_or_frozen", "a black frame; a frozen segment; the same shot twice in a row",
     "shortad [R1]: six one-frame blacks, twelve frozen card beats"),
    ("wide_level", "a wide level where none should exist (head under ~27 % of the frame height)",
     "website-rev1 ('don't ever use this super wide crop')"),
    ("visual_junk", "visual junk with no audio signature: a look-away, adjusting glasses, drinking, "
                    "recomposing while already talking, a repeated take",
     "longform-edit SKILL.md junk passes 1-5 and 7: 'the 14:30 junk had NO audio signature'"),
    ("graphic_missing", "a declared lower third, card, flash or CTA that never appears",
     "the build that shipped 7 lower thirds, 3 CTA pills and 11 flashes invisible"),
    ("ai_giveaway", "an AI clip giveaway: breath smoke, a fogging mirror, melting hands, drifting objects",
     "memory ai-clip-artifact-giveaways; website-video rev 4/5"),
    ("placeholder", "any visible PLACEHOLDER — <id> chip or other temporary approval slate",
     "edit-queue Phase 2: a draft may never become a delivery"),
]
VERDICTS = ("clean", "defect", "expected")
# expected = the strip shows a change the plan declares (a dissolve into an insert, a card popping
# on, a declared push). It is not a defect and it is not "clean" -- the judge saw it and explains it.


def judge_prompt(video, out, log, n_sheets, n_strips):
    """The brief an executor hands a FRESH subagent. Every image gets a verdict; no sampling."""
    out = os.path.abspath(out)
    return f"""# Judge this watch pass (paste to a fresh subagent)

You are the independent judge of the watch pass on `{os.path.abspath(video)}`. Nothing about this file has
been looked at by a person yet; you are that person. Be skeptical: the session that built it believes it is fine.

1. Read `{out}/CHECKLIST.md` -- all {len(CHECKLIST)} items, each with the rejection it comes from.
2. Look at EVERY image, one at a time, and give EVERY image a verdict. There are {n_sheets} contact sheets in
   `{out}/sheets/` and {n_strips} boundary strips in `{out}/strips/` (each strip has a `pair_*` image beside it:
   the -1|0 frames at half resolution -- read the pair whenever a strip suggests a cut). Do not sample. Do not
   stop early. An image you did not open cannot be `clean`.
3. A strip is five CONSECUTIVE frames at -2/-1/0/+1/+2 around a boundary. A jump cut is visible ONLY here: same
   scene both sides, the subject moves. Sheets are for framing, cards, labels and junk; a sheet cannot show a cut.
4. When something looks wrong on a sheet, grab the exact frames before you call it a defect. Decode at least
   two seconds before the target or put `-ss` after `-i`; a short input seek can expose undecoded H.264 delta
   blocks that are not in sequential playback. Never judge a defect from a downscaled tile. `personmask`
   (shorts/reference/recentre/personmask) gives a person mask if you need to measure where he sits.
5. Write `{os.path.dirname(os.path.abspath(log))}/findings.json`:
   {{"entries": [{{"image": "<file name>", "verdict": "clean"|"defect"|"expected", "item": "<checklist key, for a
   defect>", "t": <seconds>, "note": "<what you saw; for expected, what the plan declares there>"}}, ...]}}
   One entry per image at least; several for an image with several findings.
6. Report back: the count of clean / expected / defect, every defect with its time and item, and your explicit
   opinion of any trade-off the build made (a tracking crop that swaps a centering fault for a visible pan, a
   cut moved to hide a jump, a label moved off the abs onto something else).

Then the session runs: `python3 .claude/skills/_shared/deliver/watch.py --judge {os.path.abspath(log)} --findings
<findings.json> --by "<you>"` and re-runs the delivery gate. A defect you record blocks delivery until the file is
re-rendered (or Dan accepts it in his own words). That is the point.
"""


def checklist_md():
    out = ["# The watch-pass checklist", "",
           "Score EVERY sheet and EVERY strip against these. Name the item key when you find one.",
           "Verdicts: `clean`, `defect`, or `expected` (a change the plan declares -- say which).", ""]
    for k, what, src in CHECKLIST:
        out.append(f"- **`{k}`** -- {what}.  _({src})_")
    out += ["", "A strip is five CONSECUTIVE frames at -2/-1/0/+1/+2 around a boundary; the `pair_*` image",
            "beside it is the -1|0 pair at half resolution. A jump cut is visible ONLY there: same scene both",
            "sides and the subject moves. Grab suspect frames with exact `-ss` before calling anything a",
            "defect from a sheet -- sheets are for framing, cards, labels and junk, not for cuts.", ""]
    return "\n".join(out)


def geometry(w, h):
    """(scan w, scan h, blocks x, blocks y, align w, align h) oriented like the file."""
    if w >= h:
        return SCAN_LONG, SCAN_SHORT, BLOCKS_LONG, BLOCKS_SHORT, ALIGN_LONG, ALIGN_SHORT
    return SCAN_SHORT, SCAN_LONG, BLOCKS_SHORT, BLOCKS_LONG, ALIGN_SHORT, ALIGN_LONG


# ---------------------------------------------------------------------------- decoding
def stream_frames(video, w, h, pix="rgb24"):
    """Yield (index, frame ndarray) at the file's NATIVE frame rate, streamed. Never a PNG."""
    ch = 3 if pix == "rgb24" else 1
    n = w * h * ch
    p = subprocess.Popen([C.FF, "-v", "error", "-nostdin", "-i", video, "-vf", f"scale={w}:{h}",
                          "-an", "-f", "rawvideo", "-pix_fmt", pix, "-"],
                         stdout=subprocess.PIPE, bufsize=n * 32)
    k = 0
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) < n:
                break
            f = np.frombuffer(buf, dtype=np.uint8)
            yield k, (f.reshape(h, w, ch) if ch == 3 else f.reshape(h, w))
            k += 1
    finally:
        p.stdout.close()
        p.wait()


def grab(video, k, n, fps, w, h, pix="gray"):
    """n consecutive frames starting at frame index k, EXACT (never a sampled sheet).

    `-ss` lands within a frame of where it is asked to (measured 2026-09-16: one frame early on
    some indices, exact on others), so every output frame's pts is read back from `showinfo` and
    the run is sliced to the indices actually wanted. The decoder gets two seconds of lead-in.
    Three frames was not enough for H.264 delta reconstruction after an input seek: isolated
    labels and card regions appeared sliced even though sequential playback was clean (AV-07).
    """
    ch = 3 if pix == "rgb24" else 1
    lead = max(3, int(round(fps * 2.0)))
    t = max(0.0, (k - lead - 0.5) / fps)
    r = subprocess.run([C.FF, "-v", "info", "-nostdin", "-ss", f"{t:.5f}", "-copyts", "-i", video,
                        "-frames:v", str(n + 2 * lead), "-vf", f"scale={w}:{h},showinfo", "-an",
                        "-f", "rawvideo", "-pix_fmt", pix, "-"], capture_output=True)
    sz = w * h * ch
    got = len(r.stdout) // sz
    a = np.frombuffer(r.stdout[:got * sz], dtype=np.uint8)
    a = a.reshape(got, h, w, ch) if ch == 3 else a.reshape(got, h, w)
    # -copyts keeps the ORIGINAL timestamps, so showinfo's pts_time names the frame outright.
    # Without it the first output pts is re-based to a constant half-frame offset whichever frame
    # the seek actually kept, and the index was one off on some boundaries (measured 2026-09-16).
    pts = [float(x) for x in re.findall(r"pts_time:\s*([0-9.]+)", r.stderr.decode(errors="replace"))]
    if not pts or got == 0:
        return a[:0]
    first = int(round(pts[0] * fps))
    lo, hi = k - first, k - first + n
    if lo < 0:
        return a[:0]
    return a[lo:hi]


# ---------------------------------------------------------------------------- 1. the scan
def scan(video, fps, w=None, h=None):
    """One streamed pass. Returns per-frame arrays; keeps NO frames.

    d[i]    mean abs gray diff between frame i and i+1          (n-1)
    lum[i]  mean gray of frame i                                (n)
    blk[i]  16x9 (or 9x16) block mean abs diffs, i -> i+1       (n-1, 144)
    tex[i]  16x9 block spatial std of frame i (its texture)     (n, 144)
    hist[i] 64-bin coarse RGB histogram of frame i, normalised  (n, 64)
    """
    if w is None or h is None:
        pr = C.probe(video)
        w, h = pr["width"], pr["height"]
    SW, SH, GX, GY, _, _ = geometry(w, h)
    d, lum, blk, hist, tex = [], [], [], [], []
    prev = None
    bh, bw = SH // GY, SW // GX
    for k, f in stream_frames(video, SW, SH, "rgb24"):
        g = (0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]).astype(np.float32)
        lum.append(float(g.mean()))
        q = (f >> 6).astype(np.int32)
        idx = (q[:, :, 0] * 16 + q[:, :, 1] * 4 + q[:, :, 2]).ravel()
        hh = np.bincount(idx, minlength=64).astype(np.float32)
        hist.append(hh / max(hh.sum(), 1.0))
        tex.append(g.reshape(GY, bh, GX, bw).std(axis=(1, 3)).ravel())
        if prev is not None:
            ad = np.abs(g - prev)
            d.append(float(ad.mean()))
            blk.append(ad.reshape(GY, bh, GX, bw).mean(axis=(1, 3)).ravel())
        prev = g
    return dict(n=len(lum), fps=fps, w=w, h=h, grid=(SW, SH, GX, GY),
                d=np.array(d, np.float32), lum=np.array(lum, np.float32),
                blk=np.array(blk, np.float32).reshape(-1, GX * GY) if blk else np.zeros((0, GX * GY), np.float32),
                tex=np.array(tex, np.float32).reshape(-1, GX * GY) if tex else np.zeros((0, GX * GY), np.float32),
                hist=np.array(hist, np.float32))


def _runs_below(d, thr, min_len):
    out, i = [], 0
    while i < len(d):
        if d[i] < thr:
            j = i
            while j < len(d) and d[j] < thr:
                j += 1
            if j - i >= min_len:
                out.append((i, j - i))
            i = j
        else:
            i += 1
    return out


def _merge(hits, fps, gap_s=MERGE_S):
    """Consecutive over-threshold frames -> one event [first index, last index]."""
    events, run = [], []
    gap = max(2, int(gap_s * fps))
    for k in hits:
        if run and k - run[-1] <= gap:
            run.append(k)
        else:
            if run:
                events.append((run[0], run[-1]))
            run = [k]
    if run:
        events.append((run[0], run[-1]))
    return events


def _in_spans(t, spans, tol=BOUNDARY_TOL_S):
    return any(a - tol <= t <= b + tol for a, b in spans)


def analyse(sc, boundaries, declared):
    """Frozen runs, black frames and UNEXPLAINED jump events, off the scan arrays."""
    d, lum, fps = sc["d"], sc["lum"], sc["fps"]
    bts = [t for t, _ in boundaries]
    frozen = []
    for i, ln in _runs_below(d, FROZEN_D, FROZEN_MIN_FRAMES):
        t0 = (i + 1) / fps
        frozen.append(dict(t=round(t0, 2), seconds=round(ln / fps, 2),
                           inside_declared=_in_spans(t0, declared, 0.0)))
    black = [round(i / fps, 3) for i, v in enumerate(lum) if v < BLACK_LUM]
    if len(d):
        med = float(np.median(d))
        mad = float(np.median(np.abs(d - med))) or 0.05
        p99 = float(np.percentile(d, 99))
        thr = max(p99, med + 6.0 * mad, 2.0)
    else:
        med = mad = p99 = thr = 0.0
    hits = [int(k) for k in np.where(d > thr)[0]]
    events = []
    for a, b in _merge(hits, fps):
        t0, t1 = (a + 1) / fps, (b + 1) / fps
        peak = float(d[a:b + 1].max())
        explained = any(t0 - BOUNDARY_TOL_S <= bt <= t1 + 0.10 for bt in bts) or \
            _in_spans(t0, declared)
        events.append(dict(t=round(t0, 2), peak=round(peak, 2), seconds=round(t1 - t0 + 1 / fps, 2),
                           explained=explained))
    return dict(frames=sc["n"], fps=round(fps, 3), median_diff=round(med, 3), mad=round(mad, 3),
                p99=round(p99, 3), threshold=round(thr, 3),
                frozen=frozen, black=black,
                jumps=[e for e in events if not e["explained"]],
                explained_jumps=len([e for e in events if e["explained"]]))


# ---------------------------------------------------------------------------- 2. naked splices
def align_residual(a, b, bbox_px):
    """(unaligned residual, best aligned residual, (s, dx, dy)) over bbox_px = (x0, y0, x1, y1).

    Frame `a` is scaled about the region's own centre and shifted, and compared with `b` inside
    the region. A push or a pan moves EVERY textured pixel of the shot consistently and some
    (s, dx, dy) brings `a` onto `b`. A jump cut moves the subject against a background that did
    not move, and no transform explains both. The region is the changed blocks' bbox plus a
    margin, so that background is inside it.
    """
    import cv2
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    h, w = a.shape
    x0, y0, x1, y1 = bbox_px
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return 0.0, 0.0, (1.0, 0, 0)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    roi = (slice(y0, y1), slice(x0, x1))
    base = float(np.abs(a - b)[roi].mean())
    best, arg = base, (1.0, 0, 0)
    bb = b[roi]
    win = cv2.createHanningWindow((x1 - x0, y1 - y0), cv2.CV_32F)

    def residual(s, dx, dy):
        M = np.array([[s, 0.0, cx - s * cx + dx], [0.0, s, cy - s * cy + dy]], np.float32)
        wa = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=-1.0)[roi]
        m = wa >= 0
        if m.mean() < 0.7:
            return None
        return float(np.abs(wa[m] - bb[m]).mean())

    # per scale: the exact translation by phase correlation (the dominant shift of the region --
    # for a push at the right scale it is ~0, for a pan it is the pan; for a jump cut the still
    # background dominates and the shift is ~0, so nothing improves), then the residual.
    rmax = max(4.0, 0.15 * max(x1 - x0, y1 - y0))
    for s in ALIGN_SCALES:
        M = np.array([[s, 0.0, cx - s * cx], [0.0, s, cy - s * cy]], np.float32)
        wa = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)[roi]
        try:
            (dx, dy), _ = cv2.phaseCorrelate(np.ascontiguousarray(wa, np.float32),
                                             np.ascontiguousarray(bb, np.float32), win)
        except cv2.error:
            dx = dy = 0.0
        tries = [(0.0, 0.0)]
        if abs(dx) <= rmax and abs(dy) <= rmax:
            tries.append((float(dx), float(dy)))
        for tdx, tdy in tries:
            if s == 1.0 and tdx == 0.0 and tdy == 0.0:
                continue
            rr = residual(s, tdx, tdy)
            if rr is not None and rr < best:
                best, arg = rr, (s, round(tdx, 1), round(tdy, 1))
    return base, best, arg


def _subject_blocks(sc):
    """The block indices of the scan grid that lie in the top SUBJECT_ROWS of the frame."""
    _, _, gx, gy = sc["grid"]
    rows = max(1, int(round(gy * SUBJECT_ROWS)))
    return np.arange(gx * gy).reshape(gy, gx)[:rows].ravel()


def naked_candidates(sc):
    """Sharp single-frame spikes in the peak block, same palette both sides, most blocks still.

    All three block statistics are taken over the top SUBJECT_ROWS of the frame (see the note at
    that constant); the palette is the whole frame's.
    """
    d, hist, fps = sc["d"], sc["hist"], sc["fps"]
    n = len(d)
    if n < 3:
        return []
    sub = _subject_blocks(sc)
    blk = sc["blk"][:, sub]
    tex = sc["tex"][:-1, sub]                       # texture of the frame BEFORE each transition
    peak = blk.max(axis=1)
    textured = tex >= TEX_MIN
    still_n = ((blk < STILL_BLOCK) & textured).sum(axis=1)
    tex_n = textured.sum(axis=1)
    still = np.where(tex_n >= 6, still_n / np.maximum(tex_n, 1), 0.0)
    hot = (blk >= HOT_BLOCK).sum(axis=1)
    _, _, gx, gy = sc["grid"]
    out = []
    for i in range(1, n - 1):
        if peak[i] < NAKED_PEAK:
            continue
        if peak[i] < NAKED_SHARP * max(peak[i - 1], peak[i + 1], 1e-3):
            continue
        if still[i] < NAKED_STILL or hot[i] < NAKED_HOT_MIN:
            continue
        hb = sub[np.where(blk[i] >= HOT_BLOCK)[0]]
        bx, by = hb % gx, hb // gx
        bbox = (int(bx.min()), int(by.min()), int(bx.max()) + 1, int(by.max()) + 1)   # in blocks
        a0, a1 = max(0, i - 3), i + 1            # frames i-3..i  (before the cut)
        b0, b1 = i + 1, min(len(hist), i + 5)    # frames i+1..i+4 (after)
        pal = float(np.abs(hist[a0:a1].mean(0) - hist[b0:b1].mean(0)).sum() / 2.0)
        if pal >= PALETTE_SAME:
            continue
        out.append(dict(i=i, k=i + 1, t=round((i + 1) / fps, 3), peak=round(float(peak[i]), 1),
                        still=round(float(still[i]), 2), textured=int(tex_n[i]), hot=int(hot[i]),
                        bbox=bbox, pal=round(pal, 3), d=round(float(d[i]), 2)))
    return out


def naked_splices(video, sc, declared, fps):
    """The measurement behind cut:naked_splices: candidates confirmed by the alignment test.

    Returns (naked list, candidates list). A candidate inside a declared beat (a punch, a graphic,
    an insert, a covered span, a card) is subtracted: the plan says that change is deliberate.
    """
    cands = naked_candidates(sc)
    SW, SH, GX, GY, AW, AH = geometry(sc["w"], sc["h"])
    px, py = AW / GX, AH / GY                       # one scan block, in alignment pixels
    naked = []
    for c in cands:
        fr = grab(video, c["k"] - 1, 2, fps, AW, AH, "gray")
        if len(fr) < 2:
            c.update(verdict="not_grabbed")
            continue
        bx0, by0, bx1, by1 = c["bbox"]
        m = ALIGN_MARGIN_BLOCKS
        bbox_px = (int((bx0 - m) * px), int((by0 - m) * py), int((bx1 + m) * px), int((by1 + m) * py))
        base, best, (s, dx, dy) = align_residual(fr[0], fr[1], bbox_px)
        c.update(base=round(base, 2), best=round(best, 2), s=s, dx=dx, dy=dy,
                 ratio=round(best / max(base, 1e-6), 3))
        if c["ratio"] <= ALIGN_EXPLAINS:
            c["verdict"] = "aligned (a push or pan)"
            continue
        if _in_spans(c["t"], declared):
            c["verdict"] = "declared beat"
            continue
        c["verdict"] = "NAKED"
        naked.append(c)
    return naked, cands


# ---------------------------------------------------------------------------- 3. graphic presence
def graphic_presence(video, plan, fps, w, h):
    """Is each declared graphic actually in the delivered pixels at 62 % of its beat?"""
    out = []
    src = plan.get("source_picture")
    for g in (plan.get("graphics") or []):
        a, b = float(g["beat"][0]), float(g["beat"][1])
        t = a + (b - a) * 0.62
        k = int(round(t * fps))
        name = g.get("name") or os.path.basename(g.get("mov") or "?")
        dl = grab(video, k, 1, fps, w, h, "gray")
        if not len(dl):
            out.append(dict(name=name, t=round(t, 2), present=None, why="delivered frame not decodable"))
            continue
        dl = dl[0].astype(np.float32)
        mov = g.get("mov")
        if mov and os.path.exists(mov):
            raw = subprocess.run([C.FF, "-v", "error", "-nostdin", "-ss", f"{max(0.0, t - a):.3f}",
                                  "-i", mov, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f",
                                  "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
            if len(raw) < w * h * 4:
                out.append(dict(name=name, t=round(t, 2), present=None,
                                why=f"the MOV has no frame at +{t - a:.2f}s"))
                continue
            m = np.frombuffer(raw[:w * h * 4], dtype=np.uint8).reshape(h, w, 4)
            mask = m[:, :, 3] > 128
            if mask.sum() < 200:
                out.append(dict(name=name, t=round(t, 2), present=None,
                                why="the MOV is transparent at that instant (sample fell in its animation?)"))
                continue
            mg = (0.299 * m[:, :, 0] + 0.587 * m[:, :, 1] + 0.114 * m[:, :, 2]).astype(np.float32)
            x, y = mg[mask], dl[mask]
            corr = float(np.corrcoef(x, y)[0, 1]) if x.std() > 1 and y.std() > 1 else 0.0
            out.append(dict(name=name, t=round(t, 2), method="mov_alpha_corr", corr=round(corr, 3),
                            opaque_px=int(mask.sum()), present=bool(corr >= 0.5)))
        elif src and os.path.exists(src):
            sg = grab(src, k, 1, fps, w, h, "gray")
            if not len(sg):
                out.append(dict(name=name, t=round(t, 2), present=None, why="source_picture frame not decodable"))
                continue
            delta = float(np.abs(dl - sg[0].astype(np.float32)).mean())
            out.append(dict(name=name, t=round(t, 2), method="source_delta", delta=round(delta, 3),
                            present=bool(delta > 0.5)))
        else:
            out.append(dict(name=name, t=round(t, 2), present=None,
                            why="no `mov` on disk and no `source_picture` in the plan -- NOT MEASURED"))
    return out


# ---------------------------------------------------------------------------- boundaries
def boundaries_from_plan(plan, dur):
    """Every instant the plan says the picture changes state. (t, label), deduped, in range."""
    b = []

    def add(t, label):
        try:
            t = float(t)
        except (TypeError, ValueError):
            return
        if 0.1 < t < dur - 0.1:
            b.append((round(t, 2), label))

    for t in (plan.get("joins") or []):
        add(t, "join")
    for seg in (plan.get("punch") or []):
        if len(seg) >= 2:
            add(seg[0], f"punch:{seg[2] if len(seg) > 2 else ''}".rstrip(":"))
    for key in ("graphics", "ai_inserts", "real_photos", "graphic_regions", "talking_head_windows"):
        for g in (plan.get(key) or []):
            bt = g.get("beat")
            if bt and len(bt) >= 2:
                nm = g.get("name") or key
                add(bt[0], f"{nm} in")
                add(bt[1], f"{nm} out")
    for key in ("covered", "cards"):
        for ab in (plan.get(key) or []):
            if len(ab) >= 2:
                add(ab[0], f"{key} in")
                add(ab[1], f"{key} out")
    b.sort()
    out = []
    for t, label in b:
        if out and abs(t - out[-1][0]) < 0.03:
            if label not in out[-1][1]:
                out[-1] = (out[-1][0], out[-1][1] + " / " + label)
        else:
            out.append((t, label))
    return out


def declared_spans(plan):
    spans = []
    for seg in (plan.get("punch") or []):
        if len(seg) >= 2:
            spans.append((float(seg[0]), float(seg[1])))
    for key in ("graphics", "ai_inserts", "real_photos", "graphic_regions"):
        for g in (plan.get(key) or []):
            bt = g.get("beat")
            if bt and len(bt) >= 2:
                spans.append((float(bt[0]), float(bt[1])))
    for key in ("covered", "cards"):
        for ab in (plan.get(key) or []):
            if len(ab) >= 2:
                spans.append((float(ab[0]), float(ab[1])))
    return spans


# ---------------------------------------------------------------------------- 4/5. the images
def _font(size=16):
    from PIL import ImageFont
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:                                    # noqa: BLE001
            continue
    return ImageFont.load_default()


def _tile_size(w, h, long_side):
    if w >= h:
        return long_side, max(2, int(round(long_side * h / w)))
    return max(2, int(round(long_side * w / h))), long_side


def _mmss(t):
    return f"{int(t // 60):02d}-{t % 60:05.2f}"


def strips(video, boundaries, out, fps, w, h):
    """Per boundary: -2/-1/0/+1/+2 consecutive frames as one strip, and the -1|0 pair at half size."""
    from PIL import Image, ImageDraw
    os.makedirs(out, exist_ok=True)
    fnt = _font(15)
    tw, th = _tile_size(w, h, 480 if w >= h else 640)
    if w < h:
        tw, th = 360, 640
    pw, ph = w // 2, h // 2
    made, pairs = [], []
    for n, (t, label) in enumerate(boundaries):
        k0 = int(round(t * fps))
        fr = grab(video, max(0, k0 - 2), 5, fps, tw, th, "rgb24")
        if len(fr) < 3:
            continue
        first = max(0, k0 - 2)
        im = Image.new("RGB", (tw * len(fr), th + 22), (18, 18, 18))
        dr = ImageDraw.Draw(im)
        for i in range(len(fr)):
            k = first + i
            dr.rectangle([i * tw, 0, (i + 1) * tw, 22], fill=(200, 30, 30) if k < k0 else (30, 120, 200))
            dr.text((i * tw + 4, 3), f"{k - k0:+d}f  {k / fps:.3f}s", font=fnt, fill=(255, 255, 255))
            im.paste(Image.fromarray(fr[i]), (i * tw, 22))
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label)[:40]
        name = f"strip_{n:03d}_{_mmss(t)}_{safe}.jpg"
        im.save(os.path.join(out, name), quality=88)
        made.append(name)
        pr = grab(video, max(0, k0 - 1), 2, fps, pw, ph, "rgb24")
        if len(pr) == 2:
            pim = Image.new("RGB", (pw * 2 + 6, ph + 22), (18, 18, 18))
            pd = ImageDraw.Draw(pim)
            pd.rectangle([0, 0, pw, 22], fill=(200, 30, 30))
            pd.rectangle([pw + 6, 0, 2 * pw + 6, 22], fill=(30, 120, 200))
            pd.text((4, 3), f"-1f  {(k0 - 1) / fps:.3f}s", font=fnt, fill=(255, 255, 255))
            pd.text((pw + 10, 3), f"0  {k0 / fps:.3f}s   {label}", font=fnt, fill=(255, 255, 255))
            pim.paste(Image.fromarray(pr[0]), (0, 22))
            pim.paste(Image.fromarray(pr[1]), (pw + 6, 22))
            pname = f"pair_{n:03d}_{_mmss(t)}.jpg"
            pim.save(os.path.join(out, pname), quality=88)
            pairs.append(pname)
    return made, pairs


def clips(video, boundaries, out, w, h):
    os.makedirs(out, exist_ok=True)
    made = []
    for n, (t, _) in enumerate(boundaries):
        c = os.path.join(out, f"clip_{n:03d}_{_mmss(t)}.mp4")
        subprocess.run([C.FF, "-v", "error", "-nostdin", "-y", "-ss", f"{max(0, t - 1.0):.3f}", "-t", "2.0",
                        "-i", video, "-vf", f"scale={w // 2}:{h // 2}", "-an", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", c], check=False)
        if os.path.exists(c):
            made.append(os.path.basename(c))
    return made


def sheets(video, n_frames, fps, out, w, h):
    """Contact sheets of EXACT frame indices: 1 fps up to SHEET_MAX_FRAMES, then a wider stride.

    One streamed decode at tile size; the wanted indices are picked as they pass. No `fps=1/N`
    filter: it lags content by ~N/2 s and every timestamp on the sheet would be wrong.
    """
    from PIL import Image, ImageDraw
    os.makedirs(out, exist_ok=True)
    fnt = _font(14)
    dur = n_frames / fps
    interval = 1.0 if dur <= SHEET_MAX_FRAMES else dur / SHEET_MAX_FRAMES
    wanted = [int(round(t * fps)) for t in np.arange(0.0, dur, interval)]
    wanted = sorted(set(k for k in wanted if k < n_frames))
    want_set, tiles = set(wanted), {}
    tw, th = _tile_size(w, h, 384)
    for k, f in stream_frames(video, tw, th, "rgb24"):
        if k in want_set:
            tiles[k] = f.copy()
    made = []
    cols = 5
    for s in range(0, len(wanted), SHEET_TILES):
        ks = wanted[s:s + SHEET_TILES]
        rows = (len(ks) + cols - 1) // cols
        im = Image.new("RGB", (cols * tw, rows * (th + 18)), (18, 18, 18))
        dr = ImageDraw.Draw(im)
        for i, k in enumerate(ks):
            x, y = (i % cols) * tw, (i // cols) * (th + 18)
            dr.text((x + 4, y + 2), f"{C.mmss(k / fps)}  f{k}", font=fnt, fill=(255, 255, 255))
            if k in tiles:
                im.paste(Image.fromarray(tiles[k]), (x, y + 18))
        name = f"sheet_{s // SHEET_TILES:02d}_{_mmss(ks[0] / fps)}_to_{_mmss(ks[-1] / fps)}.jpg"
        im.save(os.path.join(out, name), quality=85)
        made.append(name)
    return made, round(interval, 3)


# ---------------------------------------------------------------------------- 6. the log + judge
def run(video, plan_path=None, out=None, log=None, want_clips=False, quiet=False):
    t0 = time.time()
    if not os.path.exists(video):
        raise SystemExit(f"not on disk: {video}")
    plan = {}
    if plan_path:
        if not os.path.exists(plan_path):
            raise SystemExit(f"--plan {plan_path} is not on disk")
        plan = json.load(open(plan_path))
        base = os.path.dirname(os.path.abspath(plan_path))
        for g in (plan.get("graphics") or []):
            if g.get("mov") and not os.path.isabs(g["mov"]):
                g["mov"] = os.path.normpath(os.path.join(base, g["mov"]))
        if plan.get("source_picture") and not os.path.isabs(plan["source_picture"]):
            plan["source_picture"] = os.path.normpath(os.path.join(base, plan["source_picture"]))
    vdir = os.path.dirname(os.path.abspath(video))
    out = out or os.path.join(vdir, "watch")
    log = log or os.path.join(vdir, "logs", "watch_pass.json")
    os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(log)), exist_ok=True)

    pr = C.probe(video)
    fps, w, h = pr["fps"], pr["width"], pr["height"]
    sha = C.sha256(video)
    say = (lambda *a: None) if quiet else print
    say(f"watch pass {WATCH_VERSION}   {os.path.basename(video)}   {w}x{h} @ {fps:.3f}   sha {sha[:12]}")

    sc = scan(video, fps, w, h)
    dur = sc["n"] / fps
    declared = declared_spans(plan)
    bnd = boundaries_from_plan(plan, dur)
    rep = analyse(sc, bnd, declared)
    say(f"  scan: {rep['frames']} frames  median diff {rep['median_diff']}  threshold {rep['threshold']}")
    say(f"  frozen runs >= {FROZEN_MIN_FRAMES} frames: {len(rep['frozen'])}   black frames: {len(rep['black'])}"
        f"   unexplained jumps: {len(rep['jumps'])}  (explained by the plan: {rep['explained_jumps']})")

    naked, cands = naked_splices(video, sc, declared, fps)
    rate = len(naked) / max(dur / 60.0, 1e-6)
    say(f"  naked splices: {len(naked)} of {len(cands)} candidates = {rate:.2f}/min"
        f"   first {[c['t'] for c in naked[:8]]}")

    gp = graphic_presence(video, plan, fps, w, h) if plan.get("graphics") else []
    if gp:
        miss = [g for g in gp if g.get("present") is False]
        unm = [g for g in gp if g.get("present") is None]
        say(f"  graphics present {len(gp) - len(miss) - len(unm)}/{len(gp)}"
            f"{'  MISSING ' + str([m['name'] for m in miss]) if miss else ''}"
            f"{'  NOT MEASURED ' + str([m['name'] for m in unm]) if unm else ''}")

    # every boundary gets a strip: the plan's, plus everything the scan found on its own
    detected = [(e["t"], "detected jump") for e in rep["jumps"]] + \
               [(c["t"], "NAKED splice") for c in naked]
    allb = sorted(set(bnd + detected))
    st, pairs = strips(video, allb, os.path.join(out, "strips"), fps, w, h)
    sh, interval = sheets(video, sc["n"], fps, os.path.join(out, "sheets"), w, h)
    cl = clips(video, allb, os.path.join(out, "clips"), w, h) if want_clips else []
    open(os.path.join(out, "CHECKLIST.md"), "w").write(checklist_md())
    open(os.path.join(out, "JUDGE_PROMPT.md"), "w").write(judge_prompt(video, out, log, len(sh), len(st)))
    say(f"  {len(allb)} boundaries ({len(bnd)} declared, {len(detected)} detected) -> {len(st)} strips, "
        f"{len(pairs)} pairs, {len(sh)} sheets @ {interval}s{', ' + str(len(cl)) + ' clips' if cl else ''}")

    d = dict(
        watch_version=WATCH_VERSION, tool="_shared/deliver/watch.py",
        video=os.path.basename(video), path=os.path.abspath(video), sha256=sha,
        bytes=os.path.getsize(video), size=f"{w}x{h}", fps=round(fps, 3), duration=round(dur, 3),
        when=time.strftime("%Y-%m-%dT%H:%M:%S%z"), plan=os.path.abspath(plan_path) if plan_path else None,
        out=os.path.abspath(out),
        boundaries=len(allb),
        boundary_list=[dict(t=t, label=lb, strip=st[i] if i < len(st) else None) for i, (t, lb) in enumerate(allb)],
        reviewed=0, inspected=False, judged=[], judged_by=None, open_defects=None,
        scan=rep,
        naked_splices=dict(count=len(naked), per_min=round(rate, 3), candidates=len(cands),
                           naked=[{k: v for k, v in c.items() if k != "i"} for c in naked],
                           settings=dict(grid="x".join(map(str, sc["grid"][:2])),
                                         blocks="x".join(map(str, sc["grid"][2:])), peak=NAKED_PEAK,
                                         sharp=NAKED_SHARP, still=NAKED_STILL, hot_min=NAKED_HOT_MIN,
                                         subject_rows=SUBJECT_ROWS, tex_min=TEX_MIN,
                                         palette=PALETTE_SAME, align_explains=ALIGN_EXPLAINS,
                                         align_margin_blocks=ALIGN_MARGIN_BLOCKS)),
        graphic_presence=gp,
        sheets=sh, sheet_interval_s=interval, strips=st, pairs=pairs, clips=cl,
        checklist=[k for k, _, _ in CHECKLIST], seconds=round(time.time() - t0, 1),
    )
    json.dump(d, open(log, "w"), indent=1)
    say(f"  -> {log}   ({d['seconds']}s)\n"
        f"  next: a fresh subagent judges every image in {out}/sheets and {out}/strips against "
        f"{out}/CHECKLIST.md (brief: {out}/JUDGE_PROMPT.md), writes findings.json, then:\n"
        f"    python3 {os.path.abspath(__file__)} --judge {os.path.abspath(log)} --findings <findings.json> --by \"<who>\"")
    return d, log


def judge(log_path, findings_path, by):
    """Fold a judge's findings into the log. Every sheet, strip and pair needs a verdict."""
    d = json.load(open(log_path))
    f = json.load(open(findings_path))
    entries = f.get("entries") if isinstance(f, dict) else f
    if not isinstance(entries, list):
        raise SystemExit("findings.json must be {\"entries\": [{image, verdict, item?, note?, t?, disposition?}]}")
    names = set(d.get("sheets", [])) | set(d.get("strips", [])) | set(d.get("pairs", []))
    seen, bad = {}, []
    for e in entries:
        img = os.path.basename(str(e.get("image", "")))
        v = e.get("verdict")
        if img not in names:
            bad.append(f"{img}: not an image this pass wrote")
            continue
        if v not in VERDICTS:
            bad.append(f"{img}: verdict {v!r} is not one of {VERDICTS}")
            continue
        if v == "defect" and not e.get("item"):
            bad.append(f"{img}: a defect must name a checklist item")
            continue
        if v == "expected" and not e.get("note"):
            bad.append(f"{img}: 'expected' must say what the plan declares there")
            continue
        seen.setdefault(img, []).append(e)
    missing = sorted(names - set(seen))
    strips_done = [s for s in d.get("strips", []) if s in seen]
    open_defects = [e for es in seen.values() for e in es
                    if e.get("verdict") == "defect" and e.get("disposition") != "accepted_by_dan"]
    d["judged"] = [e for es in seen.values() for e in es]
    d["judged_by"] = by
    d["judged_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    d["reviewed"] = len(strips_done)
    d["inspected"] = not missing and not bad
    d["open_defects"] = len(open_defects)
    d["judge_problems"] = bad + [f"{m}: no verdict" for m in missing]
    json.dump(d, open(log_path, "w"), indent=1)
    print(f"judged by {by}: {len(d['judged'])} verdicts over {len(seen)}/{len(names)} images; "
          f"{d['reviewed']}/{d['boundaries']} boundaries reviewed; {len(open_defects)} open defect(s)")
    for b in bad:
        print("  ✗", b)
    if missing:
        print(f"  ✗ {len(missing)} image(s) without a verdict -- inspected stays false: {missing[:6]}")
    return 0 if d["inspected"] and not open_defects else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("--plan")
    ap.add_argument("--out", help="artifact dir (default <video dir>/watch)")
    ap.add_argument("--log", help="the log (default <video dir>/logs/watch_pass.json)")
    ap.add_argument("--clips", action="store_true", help="also a 2 s clip per boundary")
    ap.add_argument("--judge", metavar="LOG", help="fold findings into this log")
    ap.add_argument("--findings")
    ap.add_argument("--by")
    ap.add_argument("--checklist", action="store_true")
    A = ap.parse_args()
    if A.checklist:
        print(checklist_md())
        return 0
    if A.judge:
        if not A.findings or not A.by:
            ap.error("--judge needs --findings and --by")
        return judge(A.judge, A.findings, A.by)
    if not A.video:
        ap.error("a video is required")
    run(A.video, A.plan, A.out, A.log, A.clips)
    return 0


if __name__ == "__main__":
    sys.exit(main())
