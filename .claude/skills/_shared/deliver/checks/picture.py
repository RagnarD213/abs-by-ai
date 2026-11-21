#!/usr/bin/env python3
"""Picture rows: how much of the runtime is not the one camera shot, how long it sits still, and
how many joins the edit left bare.

Every row here is measured off the DELIVERED PICTURE. A plan can claim thirty cutaways; only the
file proves it. Where a plan IS supplied the rows use it to get sharper (declared punches stop
counting as jump cuts), but none of them needs it to run.

⚠ THE DECODE SETTINGS ARE PART OF THE CALIBRATION. Every bound in formats.py was measured with the
exact fps/scale below. Change `fps=6, 64x36` or `fps=2, 48x27` and every number in formats.py is
measuring something else. If you must change them, re-measure the whole corpus and say so.
"""
import numpy as np

from .. import common as C
from .. import watch as W
from ..common import Row, unmeasured


class Picture:
    """Lazy, once-per-run decodes of the delivered file. Three representations, no more."""

    def __init__(self, video, dur, fps=None, width=None, height=None):
        self.v, self.dur = video, dur
        self.fps, self.w, self.h = fps, width, height
        self._g6 = self._rgb2 = self._rgb12 = self._stream = None

    def stream(self):
        """The watch pass's NATIVE-RATE scan (watch.scan): every frame, 160x90 oriented like the
        file. The fourth representation, and the only one that is not sampled -- a one-frame black
        or a one-frame jump is invisible at 6 fps (the email-capture screen was once exposed for
        exactly one frame and a 2 fps scan stepped over it)."""
        if self._stream is None:
            if self.fps is None or self.w is None or self.h is None:
                pr = C.probe(self.v)
                self.fps, self.w, self.h = pr["fps"], pr["width"], pr["height"]
            self._stream = W.scan(self.v, self.fps, self.w, self.h)
        return self._stream

    @property
    def g6(self):
        """6 fps, 64x36 gray -- the change-event representation (qc_style.scene_times)."""
        if self._g6 is None:
            self._g6 = C.gray(self.v, 6, 64, 36).astype(np.float32)
        return self._g6

    @property
    def rgb2(self):
        """2 fps, 48x27 rgb -- the palette representation (qc_style.coverage_of)."""
        if self._rgb2 is None:
            self._rgb2 = C.rgb(self.v, 2, 48, 27)
        return self._rgb2

    @property
    def rgb12(self):
        """12 fps, 48x27 rgb -- fine enough to land a join inside one event."""
        if self._rgb12 is None:
            self._rgb12 = C.rgb(self.v, 12, 48, 27)
        return self._rgb12

    # ------------------------------------------------------------------ derived, cached
    _events = None

    def change_events(self):
        """Visual-change times, measured directly rather than with ffmpeg's `scene` filter.

        `select='gt(scene,0.25)'` only sees HARD cuts. It scored one rebuild at 44 changes and
        reported a 44.9 s static stretch through a passage carrying seven full-frame cutaways --
        because each dissolved over 0.14 s and a dissolve spreads the change across four frames,
        none of which trips the threshold. A gate that a cut satisfies but a dissolve does not is
        measuring the encoder, not the edit. (longform-edit/reference/qc_style.py, 2026-08)
        """
        if self._events is not None:
            return self._events
        d = np.abs(np.diff(self.g6, axis=0)).mean(1)
        med = float(np.median(d))
        mad = float(np.median(np.abs(d - med))) or 0.5
        thr = max(med + 6.0 * mad, 3.0)
        ts, last = [], -9.0
        for i in np.where(d > thr)[0]:
            t = (i + 1) / 6.0
            if t - last >= 0.4:
                ts.append(round(t, 2))
            last = t
        self._events = ts
        return ts

    _hist = None

    def palette(self):
        """Coarse RGB histogram per 2 fps frame, and its distance from the programme median.

        The first attempt compared each frame to the per-pixel MEDIAN frame and called anything far
        from it "covered". That scored a rebuild at 100%, which is nonsense: once every shot is a
        punch-in, no frame matches the plate and the metric stops measuring cutaways and starts
        measuring reframes. A punch-in keeps the SCENE -- same sky, same pool, same patio -- so what
        separates a cutaway from a reframe is the PALETTE. (qc_style.coverage_of, 2026-08)
        """
        if self._hist is not None:
            return self._hist
        F = self.rgb2
        q = (F >> 6).astype(np.int32)
        idx = q[:, :, 0] * 16 + q[:, :, 1] * 4 + q[:, :, 2]
        H = np.stack([np.bincount(idx[i], minlength=64) for i in range(len(F))]).astype(np.float32)
        H /= np.maximum(H.sum(1, keepdims=True), 1e-9)
        self._hist = (H, np.abs(H - np.median(H, axis=0)).sum(1) / 2.0)
        return self._hist


# ---------------------------------------------------------------------------- rows
def coverage(key, pic, cfg, plan):
    """style:coverage -- the fraction of runtime that is NOT the main talking-head scene."""
    _, d = pic.palette()
    cov = float((d > 0.12).mean())          # 0.12: see formats.py COVERAGE_THRESHOLD note
    lo = cfg["min"]
    return Row(key, cov >= lo,
               f"{cov*100:.0f}% of runtime is off the main scene (min {lo*100:.0f}%)",
               dict(coverage=round(cov, 4), min=lo))


def static_run(key, pic, cfg, plan):
    """style:static_run -- the longest stretch with no visual change at all."""
    ts = pic.change_events()
    edges = [0.0] + ts + [pic.dur]
    runs = [(edges[i], edges[i + 1] - edges[i]) for i in range(len(edges) - 1)]
    at, worst = max(runs, key=lambda r: r[1])
    lo = cfg["max"]
    return Row(key, worst <= lo,
               f"longest stretch with no visual change {worst:.1f}s at {C.mmss(at)} (max {lo}s)",
               dict(worst=round(worst, 2), at=round(at, 2), max=lo))


def change_rate(key, pic, cfg, plan):
    """style:change_rate -- picture changes per minute."""
    ts = pic.change_events()
    rate = len(ts) / max(pic.dur / 60, 1e-6)
    lo = cfg["min_per_min"]
    return Row(key, rate >= lo,
               f"{len(ts)} picture changes = {rate:.1f}/min (min {lo}/min)",
               dict(changes=len(ts), per_min=round(rate, 2), min=lo))


def uncovered_joins(key, pic, cfg, plan):
    """cut:uncovered_joins -- picture discontinuities the edit did not cover with a change of scene.

    WHAT IT MEASURES, precisely, because the name is broader than the measurement. A cutaway changes
    the palette. A jump cut does not: the scene stays, the subject moves. So every frame-to-frame
    spike whose colour histogram is essentially the same on both sides is a join the edit left in
    the open. A deliberate punch reframe reads the same way -- same scene, big pixel jump -- which
    is why the default bound is a RATE calibrated against cuts Dan APPROVED (which are full of
    punches), and why a plan that declares its punch and graphic beats gets the sharper measurement:
    declared beats are subtracted before the rate is taken.

    Measured 2026-09-11, all at fps=12 / 48x27, events merged inside 0.4 s:
        FINAL_spraytan_PRE_REBUILD  REJECTED ("41 uncovered joins")     3.2/min   (60 events)
        FINAL_abwheel  (8/20)       REJECTED                           2.2/min   (20)
        website rev 6               approved                           1.8/min   (7)
        zeeshan ad 1 16x9           approved                           1.7/min   (7)
        muhammad ad 2 16x9          reference                          1.3/min   (6)
        website rev 4               approved                           1.0/min   (4)
        website rev 5               approved                           0.8/min   (3)
        muhammad ad 1 16x9          reference                          0.8/min   (3)
    """
    G = pic.rgb12.astype(np.float32)
    g = G.mean(2)
    dd = np.abs(np.diff(g, axis=0)).mean(1)
    med = float(np.median(dd))
    mad = float(np.median(np.abs(dd - med))) or 0.5
    spikes = list(np.where(dd > max(med + 8 * mad, 2.5))[0])
    q = (G.astype(np.int32) >> 6)
    idx = q[:, :, 0] * 16 + q[:, :, 1] * 4 + q[:, :, 2]
    H = np.stack([np.bincount(idx[i], minlength=64) for i in range(len(G))]).astype(np.float32)
    H /= np.maximum(H.sum(1, keepdims=True), 1e-9)

    events, cur = [], []
    for i in spikes:                                    # merge inside 0.4 s = 5 frames at 12 fps
        if cur and i - cur[-1] <= 5:
            cur.append(i)
        else:
            if cur:
                events.append(cur)
            cur = [i]
    if cur:
        events.append(cur)

    declared = []
    for a, b, *_ in (plan.get("punch") or []):
        declared.append((a, b))
    for gx in (plan.get("graphics") or []) + (plan.get("ai_inserts") or []):
        declared.append(tuple(gx["beat"]))
    for ab in (plan.get("covered") or []):
        declared.append(tuple(ab))

    bare = []
    for grp in events:
        i = max(grp, key=lambda k: dd[k])
        t = i / 12.0
        a, b = max(0, grp[0] - 4), min(len(H) - 1, grp[-1] + 5)
        if grp[-1] + 1 > b:
            continue
        pal = float(np.abs(H[a:grp[0] + 1].mean(0) - H[grp[-1] + 1:b + 1].mean(0)).sum() / 2.0)
        if pal >= 0.10:                                  # the scene changed: this join is covered
            continue
        if any(x - 0.25 <= t <= y + 0.25 for x, y in declared):
            continue                                     # a declared punch or graphic beat
        bare.append((round(float(t), 2), round(float(pal), 3)))

    rate = len(bare) / max(pic.dur / 60, 1e-6)
    lo = cfg["max_per_min"]
    how = "declared beats subtracted" if declared else "no plan: deliberate punches count too"
    return Row(key, rate <= lo,
               f"{len(bare)} same-scene picture jumps = {rate:.1f}/min (max {lo}/min, {how}); "
               f"first {[t for t, _ in bare[:6]]}",
               dict(bare=len(bare), per_min=round(rate, 2), max=lo,
                    times=[t for t, _ in bare[:40]], declared_beats=len(declared)))


def black_frames(key, pic, cfg, plan):
    """cut:black_frames -- a black frame in the body of a cut is a hole, never a design choice.

    Measured on EVERY frame (the watch scan), not the 6 fps representation: shortad's watch pass
    found six ONE-FRAME blacks that a sampled scan sees one time in five. Changed 2026-09-16 (gate
    2.1.0); the bound is unchanged.
    """
    sc = pic.stream()
    fps, lum = sc["fps"], sc["lum"]
    lead = cfg.get("allow_lead_s", 0.0)
    tail = cfg.get("allow_tail_s", 0.0)
    bad = [round(i / fps, 3) for i, v in enumerate(lum)
           if v < cfg["max_luma"] and lead <= i / fps <= pic.dur - tail]
    return Row(key, not bad,
               f"{len(bad)} frame(s) under luma {cfg['max_luma']} in the body (every frame scanned): {bad[:8]}",
               dict(black=bad[:40], max_luma=cfg["max_luma"], frames=int(sc["n"])))


def naked_splices(key, pic, cfg, plan):
    """cut:naked_splices -- same-scene, same-framing single-frame jumps where the subject moves.

    ⚠ NOT the same instrument as cut:uncovered_joins. That row reads the rejected Ad 1 vertical
    (corpus `ad1-vertical-attempt1`, 23 of 72 splices naked) at 0.0/min, because a subject jump is
    LOCAL and a whole-frame mean at 48x27 dilutes it to nothing. This one reads the peak BLOCK of
    a 16x9 grid at native rate, requires a sharp single-frame spike with the same palette both
    sides, most blocks still and enough blocks moved to be a person (not a caption word), then
    grabs the two frames at exact `-ss` and tests them against a global scale/shift alignment.
    A push or a pan aligns; a jump cut does not. The measurement and its settings live in
    _shared/deliver/watch.py; the per-minute bound lives in formats.py beside the files it was
    measured on. Declared beats (punch, graphics, inserts, covered, cards) are subtracted.
    """
    sc = pic.stream()
    declared = W.declared_spans(plan)
    naked, cands = W.naked_splices(pic.v, sc, declared, sc["fps"])
    dur = sc["n"] / sc["fps"]
    rate = len(naked) / max(dur / 60.0, 1e-6)
    lo = cfg["max_per_min"]
    how = "declared beats subtracted" if declared else "no plan: every deliberate same-frame change counts too"
    return Row(key, rate <= lo,
               f"{len(naked)} naked splice(s) of {len(cands)} candidates = {rate:.2f}/min "
               f"(max {lo}/min, {how}); first {[c['t'] for c in naked[:6]]}",
               dict(naked=len(naked), per_min=round(rate, 3), max=lo, candidates=len(cands),
                    times=[c["t"] for c in naked[:40]], declared_beats=len(declared),
                    settings=dict(peak=W.NAKED_PEAK, sharp=W.NAKED_SHARP, still=W.NAKED_STILL,
                                  hot_min=W.NAKED_HOT_MIN, subject_rows=W.SUBJECT_ROWS,
                                  palette=W.PALETTE_SAME, align_explains=W.ALIGN_EXPLAINS)))


def min_segment(key, pic, cfg, plan):
    """cut:min_segment -- no framing segment shorter than the eye can read."""
    punch = plan.get("punch")
    if not punch:
        return unmeasured(key, "the plan declares no `punch` segments; "
                               "declare them, or declare this row not applicable with a reason")
    lo = cfg["min_seconds"]
    short = [(a, b, l) for a, b, *rest in punch for l in [rest[0] if rest else "?"] if b - a < lo]
    return Row(key, not short, f"{len(short)} segment(s) under {lo}s: {short[:6]}",
               dict(short=short[:20], min_seconds=lo))


def jump_cut(key, pic, cfg, plan):
    """cut:jump_cut -- two adjacent VISIBLE segments at the same framing.

    A join is a jump cut only when both sides are visible. A segment hidden under a full-frame
    insert or card carries the previous level on purpose; the framing changes across the insert
    instead. (website-video rev 4, 2026-09-08)
    """
    punch = plan.get("punch")
    if not punch:
        return unmeasured(key, "the plan declares no `punch` segments")
    covered = plan.get("punch_covered") or [False] * len(punch)
    same = []
    for i in range(len(punch) - 1):
        li = punch[i][2] if len(punch[i]) > 2 else None
        lj = punch[i + 1][2] if len(punch[i + 1]) > 2 else None
        if li is not None and li == lj and not (covered[i] or covered[i + 1]):
            same.append((round(punch[i][0], 2), round(punch[i + 1][0], 2), li))
    return Row(key, not same, f"{len(same)} adjacent visible segment pair(s) at one framing: {same[:5]}",
               dict(same=same[:20]))


def splice_visibility(key, pic, cfg, plan):
    """cut:splice_visibility -- a bare join above the file's OWN natural frame-diff ceiling.

    The ceiling is the file's own p99, not a constant: a busy cut and a locked-off talking head have
    different natural frame-to-frame movement, and a fixed threshold grades one of them wrongly.
    """
    joins = plan.get("joins")
    if not joins:
        return unmeasured(key, "the plan declares no `joins`; declare them, or declare this row "
                               "not applicable (a single continuous take has none)")
    g = pic.rgb12.astype(np.float32).mean(2)
    dd = np.abs(np.diff(g, axis=0)).mean(1)
    p99 = float(np.percentile(dd, 99))
    covered = [tuple(x) for x in (plan.get("covered") or [])]
    covered += [tuple(gx["beat"]) for gx in (plan.get("graphics") or []) + (plan.get("ai_inserts") or [])]
    bare = []
    for t in joins:
        if any(a - 0.05 <= t <= b + 0.05 for a, b in covered):
            continue
        i = int(round(t * 12))
        w = dd[max(0, i - 1):min(len(dd), i + 2)]
        if len(w) and float(w.max()) > p99 * cfg.get("ceiling_mult", 1.0):
            bare.append((round(t, 2), round(float(w.max()), 2)))
    return Row(key, not bare,
               f"{len(bare)}/{len(joins)} joins above the file's own p99 ceiling ({p99:.2f}): {bare[:6]}",
               dict(bare=bare[:30], p99=round(p99, 3), joins=len(joins)))
