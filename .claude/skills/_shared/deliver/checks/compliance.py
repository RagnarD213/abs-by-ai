#!/usr/bin/env python3
"""Compliance rows -- the ones that are a Google Ads strike, an app-store rejection or a broken
promise to a viewer rather than a quality miss.

Three of the four were prose in a SKILL.md until 2026-09-11: the Negative Events scan is manual in
every skill, the banned-screen scan was template-driven in `/ad-edit` only (which is how a
side-by-side before/after reached the delivered spray-tan longform for 5.6 s at 18:04), and the
AI-GENERATED label check existed in `qc_frame.py` for `/ad-edit` only while `/make-ad` states the
same requirement with no check behind it.
"""
import os
import re
import shutil
import subprocess
import tempfile

import numpy as np

from .. import common as C
from .. import contract as CONTRACT
from ..common import Row, unmeasured


# ---------------------------------------------------------------------------- banned screens
def _norm(a):
    a = a.astype(np.float32)
    a -= a.mean()
    return a / max(float(a.std()), 1e-6)


def _fft_shape(fh_in, th):
    return 1 << int(np.ceil(np.log2(fh_in + th - 1)))


class _Frame:
    """One grid frame with its integral images and its FFTs, computed once and shared by every
    template strip that is matched against it (2026-09-12: the box sums and the frame FFT were
    being recomputed per template, 56 times per frame)."""

    __slots__ = ("F", "P", "P2", "ffts")

    def __init__(self, F):
        self.F = F
        self.P = np.pad(np.cumsum(np.cumsum(F, 0), 1), ((1, 0), (1, 0)))
        self.P2 = np.pad(np.cumsum(np.cumsum(F * F, 0), 1), ((1, 0), (1, 0)))
        self.ffts = {}

    def fft(self, shp):
        if shp not in self.ffts:
            self.ffts[shp] = np.fft.rfft2(self.F, shp)
        return self.ffts[shp]


class _Tmpl:
    """A normalised template strip with its conjugate FFT at the frame's padded shape, computed once."""

    __slots__ = ("T", "th", "tw", "shp", "TF")

    def __init__(self, T, gh, gw):
        self.T = T
        self.th, self.tw = T.shape
        self.shp = (_fft_shape(gh, self.th), _fft_shape(gw, self.tw))
        self.TF = np.conj(np.fft.rfft2(T, self.shp))


def _ncc_peak(fr, tm):
    """Peak normalised cross-correlation of template strip `tm` anywhere in frame `fr`.

    Full NCC, not a fixed-crop correlation: the app screen appears as a full frame in a vertical
    ad, as a phone PiP beside Dan in a longform, and at whatever size an editor chose in between.
    A gate pinned to one crop only sees the layout it was written for.
    """
    F, th, tw = fr.F, tm.th, tm.tw
    if th > F.shape[0] or tw > F.shape[1]:
        return -1.0, None
    n = th * tw
    box = lambda I: I[th:, tw:] - I[:-th, tw:] - I[th:, :-tw] + I[:-th, :-tw]   # noqa: E731
    mu = box(fr.P) / n
    sd = np.sqrt(np.maximum(box(fr.P2) / n - mu * mu, 0.0))
    fh, fw = tm.shp
    c = np.fft.irfft2(fr.fft(tm.shp) * tm.TF, (fh, fw))
    c = c[:F.shape[0] - th + 1, :F.shape[1] - tw + 1]
    # ⚠ A FLAT PATCH HAS NO CORRELATION, IT HAS A DIVISION BY ZERO. Measured 2026-09-11: flooring
    # the VARIANCE at 1e-6 (sd 1e-3 on a 0-255 scale) made the letterboxed black bars either side of
    # a card in the spray-tan longform score 24.604 -- twenty-four times the maximum a normalised
    # correlation can reach -- and 299 frames "matched" a screen that is not in them. A patch with
    # less than one grey level of structure cannot match a detailed template; it scores 0.
    flat = sd < 1.0
    r = np.zeros_like(c)
    np.divide(c, n * sd, out=r, where=~flat)
    peak = float(r.max()) if r.size else -1.0
    # and the invariant itself, asserted, so a normalisation bug can never again look like a hit
    if peak > 1.001:
        raise AssertionError(f"normalised cross-correlation returned {peak:.3f}; it cannot exceed "
                             f"1.0 -- the normalisation is wrong, not the picture")
    i = int(np.argmax(r))
    return peak, divmod(i, r.shape[1])


def banned_screen(key, pr, cfg, plan, video, work):
    """compliance:banned_screen -- the app's side-by-side before/after and email-capture screens.

    ⚠ EVERY FRAME, NOT A SAMPLE. The email-capture form was once exposed for exactly ONE frame at
    179.41 s and a 2 fps scan stepped straight over it; on Ad 3 a 2 fps scan reported a clean 0.647
    where the full-rate scan reported 1.000 and failed the build. A compliance gate that samples
    cannot see a single-frame violation, so this one decodes the whole picture.

    ⚠ AND IT MATCHES THE LAYOUT, NOT THE RECORDING. This is the finding that rebuilt the row on
    2026-09-11. Whole-screen template matching -- the method in BOTH gates this was ported from --
    matches an INSTANCE: the banned source is one person's generation, so roughly 30% of that screen
    is photographs that differ in every other generation of it. Measured on the file the row exists
    for, the spray-tan longform, which shows the screen as a phone PiP at ~18:04:

        whole screen, best scale        0.581      <- under any usable bound
        the two photos only             0.491      <- correctly low: different photos
        chrome TOP    (nav + "Meet the new you" + BEFORE/AFTER labels)     0.657 .. 0.683
        chrome BOTTOM (body-fat row + "Lock in this goal" + Safari bar)    0.617 .. 0.623

    So neither strip clears a single-correlation bound on its own either. What is decisive is that
    they agree about WHERE: at the true scale the top strip peaked at (14, 42) and the bottom at
    (112, 43) -- the same column, and 98 px apart against the 101 px the layout predicts. Two
    independent chrome strips at the geometrically correct offset is evidence a chance correlation
    cannot manufacture. That pairing is what this row tests.
    """
    src = plan.get("banned_source")
    times = plan.get("banned_times")
    if not src or not os.path.exists(src):
        return unmeasured(key, f"`banned_source` not readable ({src!r}) -- is the asset library "
                               f"mounted? Without the screen itself nothing can scan for it")
    if not times:
        return unmeasured(key, "the plan gives no `banned_times` into the banned source")
    W, H = pr["width"], pr["height"]
    gw = cfg.get("grid_w", 384)
    gh = max(2, int(round(gw * H / W / 2)) * 2)
    scales = cfg["scales"]
    # ⚠ THE SOURCE'S OWN ASPECT, PROBED -- never a constant. The default was 1080/1920 = 0.5625 and
    # the actual recording is 1320x2868 = 0.4603, so every template was stretched 22% wider than the
    # screen it was looking for. Measured 2026-09-11: that alone loses the match.
    sp = C.probe(src)
    aspect = sp["width"] / sp["height"]
    top0, top1 = cfg["chrome_top"]
    bot0, bot1 = cfg["chrome_bottom"]

    photo0, photo1 = cfg["photo_band"]
    lcol, rcol = cfg["photo_cols"]
    slop = cfg["position_slop_px"]

    def lr_corr(F, y0, x0, ph, pw):
        """Left/right correlation of the photo band of a phone box at (y0, x0) of size (ph, pw)."""
        r0, r1 = y0 + int(ph * photo0), y0 + int(ph * photo1)
        L = F[r0:r1, x0 + int(pw * lcol[0]):x0 + int(pw * lcol[1])]
        R = F[r0:r1, x0 + int(pw * rcol[0]):x0 + int(pw * rcol[1])]
        w = min(L.shape[1], R.shape[1])
        L, R = L[:, :w], R[:, :w]
        if L.size < 16 or L.std() < 1.0 or R.std() < 1.0:
            return 0.0
        return float(np.corrcoef(L.ravel(), R.ravel())[0, 1])

    def photo_band(F, y0, x0, ph, pw):
        """Is the band between the chrome strips a PHOTOGRAPH? (white fraction, luma sd)"""
        r0, r1 = y0 + int(ph * photo0), y0 + int(ph * photo1)
        band = F[r0:r1, x0 + int(pw * lcol[0]):x0 + int(pw * rcol[1])]
        if band.size < 16:
            return 1.0, 0.0
        return float((band > 215).mean()), float(band.std())

    specs = []                      # (t, kind, scale, phone_h, phone_w, TOP, BOTTOM, expected dy)
    kinds = {}
    for t in times:
        for frac in scales:
            ph = int(round(gh * frac))
            pw = max(2, int(round(ph * aspect)))
            raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", src,
                                  "-frames:v", "1", "-vf", f"scale={pw}:{ph},format=gray",
                                  "-f", "rawvideo", "-"], capture_output=True).stdout
            if len(raw) < pw * ph:
                continue
            S = np.frombuffer(raw[:pw * ph], np.uint8).reshape(ph, pw).astype(np.float32)
            if t not in kinds:
                # THE SCREEN'S OWN KIND, READ OFF THE SOURCE: a before/after screen's photo band
                # correlates left with right (the same person in the same pose twice); a single-
                # photo screen does not. Measured 2026-09-12 on the recording: "Meet the new you"
                # +0.81, the email-capture "Download Your Future Self" -0.26.
                kinds[t] = "paired" if lr_corr(S, 0, 0, ph, pw) >= cfg["pair_self_min"] else "single"
            T = S[int(ph * top0):int(ph * top1)]
            B = S[int(ph * bot0):int(ph * bot1)]
            if T.shape[0] < 8 or B.shape[0] < 8 or T.shape[1] > gw or B.shape[0] > gh:
                continue
            specs.append((t, kinds[t], frac, ph, pw, _Tmpl(_norm(T), gh, gw), _Tmpl(_norm(B), gh, gw),
                          int(ph * (bot0 - top0))))
    if not specs:
        return unmeasured(key, "no template strip could be read out of the banned source")

    pre = cfg["prescreen_ncc"]
    both = {"paired": cfg["min_strip_ncc_paired"], "single": cfg["min_strip_ncc_single"]}
    white_max, sd_min = cfg["photo_white_max"], cfg["photo_sd_min"]
    p = subprocess.Popen([C.FF, "-v", "error", "-i", video, "-vf", f"scale={gw}:{gh},format=gray",
                          "-an", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    best = {"paired": (-1.0, None, None), "single": (-1.0, None, None)}
    hits, n = [], 0
    while True:
        raw = p.stdout.read(gw * gh)
        if len(raw) < gw * gh:
            break
        fr = _Frame(np.frombuffer(raw, np.uint8).reshape(gh, gw).astype(np.float32))
        n += 1
        for t, kind, frac, ph, pw, T, B, dy in specs:
            # STAGE 1: the cheap top strip. Most frames die here.
            vt, pt = _ncc_peak(fr, T)
            if vt < pre:
                continue
            # STAGE 2: the bottom strip must agree, and agree about WHERE.
            vb, pb = _ncc_peak(fr, B)
            if not (pt and pb and abs(pb[1] - pt[1]) <= slop and abs((pb[0] - pt[0]) - dy) <= slop):
                continue
            score = min(vt, vb)
            # STAGE 3: the layout's own signature inside the phone box the chrome located -- the
            # band between the strips is a PHOTOGRAPH on every banned screen and a white panel on
            # every look-alike. (L/R pairing is recorded for the reader; it is not the test -- a
            # white table reads L/R 0.59 at the coarse grid, a real before/after 0.37-0.60.)
            white, sd = photo_band(fr.F, pt[0], pt[1], ph, pw)
            lr = lr_corr(fr.F, pt[0], pt[1], ph, pw) if kind == "paired" else None
            photo = white <= white_max and sd >= sd_min
            if score > best[kind][0]:
                best[kind] = (score, round(n / pr["fps"], 2),
                              dict(t=t, scale=frac, top=round(vt, 3), bottom=round(vb, 3),
                                   white=round(white, 2), sd=round(sd, 1),
                                   lr=None if lr is None else round(lr, 3), photo=photo))
            if score >= both[kind] and photo:
                hits.append((round(n / pr["fps"], 2), kind, round(vt, 3), round(vb, 3),
                             round(white, 2), round(sd, 1), frac))
                break
    p.stdout.close()
    p.wait()
    bp, bs = best["paired"], best["single"]
    return Row(key, not hits,
               f"{n} frames x {len(specs)} layout templates ({sum(1 for k in kinds.values() if k == 'paired')} "
               f"paired + {sum(1 for k in kinds.values() if k == 'single')} single screens); best consistent "
               f"paired-screen match {bp[0]:.3f} at {bp[1]}s {bp[2]} (needs both strips >= {both['paired']}); "
               f"best consistent single-screen match {bs[0]:.3f} at {bs[1]}s {bs[2]} (needs both >= "
               f"{both['single']}); and the band between the strips must be a photograph (white "
               f"<= {white_max}, sd >= {sd_min}); {len(hits)} frame(s) hit (t, kind, top, bottom, white, "
               f"sd, scale): {hits[:6]}",
               dict(frames=n, best_paired=bp, best_single=bs, hits=hits[:60],
                    min_strip_ncc=both, photo_white_max=white_max, photo_sd_min=sd_min, prescreen=pre))


# ---------------------------------------------------------------------------- labels
def _measure_label_clearance(video, tracks, clearance_px):
    """Check each full label rectangle against an independent delivered-frame person mask."""
    from PIL import Image
    from scipy.ndimage import binary_dilation
    from .framing import PERSONMASK
    if not os.path.exists(PERSONMASK):
        return None, 0, f"Apple Vision person segmenter is not built: {PERSONMASK}"
    import cv2
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        return None, 0, f"cannot decode delivered file for label clearance: {video}"
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    jobs = []
    for state in tracks:
        if state.get("visibility", "full") != "full":
            continue
        path = state.get("image")
        if not path or not os.path.exists(path):
            continue
        with Image.open(path) as im:
            rect = CONTRACT.transform_rect(state, im.size)
        if rect is None:
            continue
        a, b = (float(x) for x in state["beat"])
        times = state.get("sample_times") or [a + (b - a) * f for f in (0.2, 0.5, 0.8)]
        for t in times:
            jobs.append((max(0, int(round(t * fps))), state.get("name", "?"), float(t), rect))
    if not jobs:
        cap.release()
        return None, 0, "no full label state has a readable image, transform and sample time"
    tmp = tempfile.mkdtemp(prefix="label_clearance_")
    inputs, meta = [], {}
    try:
        by_frame = {}
        for job in jobs:
            by_frame.setdefault(job[0], []).append(job)
        wanted, n = set(by_frame), 0
        while wanted:
            ok, frame = cap.read()
            if not ok:
                break
            if n in wanted:
                path = os.path.join(tmp, f"{n:08d}.png")
                Image.fromarray(frame[..., ::-1]).save(path, compress_level=1)
                inputs.append(path)
                meta[path] = by_frame[n]
                wanted.remove(n)
            n += 1
        cap.release()
        if wanted:
            return None, len(inputs), f"could not decode {len(wanted)} declared label frame(s)"
        masks = os.path.join(tmp, "m")
        for i in range(0, len(inputs), 200):
            r = subprocess.run([PERSONMASK, masks] + inputs[i:i + 200],
                               capture_output=True, text=True)
            if r.returncode:
                return None, i, f"person segmenter failed: {(r.stderr or r.stdout)[-300:]}"
        obstruct, checked = [], 0
        for path in inputs:
            mp = os.path.join(masks, os.path.basename(path).replace(".png", ".mask.png"))
            if not os.path.exists(mp):
                return None, checked, f"person segmenter returned no mask for {os.path.basename(path)}"
            mask = np.asarray(Image.open(mp).convert("L").resize((W, H))) > 127
            mask = binary_dilation(mask, iterations=clearance_px)
            for _frame, name, t, (x, y, w, h) in meta[path]:
                checked += 1
                if x < 0 or y < 0 or x + w > W or y + h > H:
                    obstruct.append((name, round(t, 3), "label rectangle outside delivered frame"))
                    continue
                contact = int(mask[y:y + h, x:x + w].sum())
                if contact:
                    obstruct.append((name, round(t, 3), contact))
        return obstruct, checked, None
    finally:
        cap.release()
        shutil.rmtree(tmp, ignore_errors=True)


def _tracked_labels(key, cfg, plan, video):
    err = CONTRACT.contract_error(plan, key)
    if err:
        return unmeasured(key, err)
    tracks = plan.get("label_tracks") or []
    if not tracks:
        return Row.na(key, "this cut declares no label tracks")
    threshold = cfg["min_track_corr"]
    missing, wrong, partial, scores = [], [], [], []
    cache = plan.setdefault("_pixel_corr_cache", {})
    jobs = []
    for i, state in enumerate(tracks):
        if state.get("visibility", "full") == "partial":
            continue
        if int(state.get("search_px", 0)) > cfg["max_search_px"]:
            continue
        a, b = (float(x) for x in state["beat"])
        times = state.get("sample_times") or [a + (b - a) * f for f in (0.2, 0.5, 0.8)]
        for j, t in enumerate(times):
            jobs.append((f"{i}-{j}-expected", state, t, "image"))
            if state.get("wrong_image"):
                jobs.append((f"{i}-{j}-wrong", state, t, "wrong_image"))
    CONTRACT.pixel_correlations(video, jobs, cache)
    for state in tracks:
        from PIL import Image
        path = state.get("image")
        if int(state.get("search_px", 0)) > cfg["max_search_px"]:
            missing.append((state.get("name", "?"), "search_px exceeds format maximum"))
            continue
        if not path or not os.path.exists(path):
            missing.append((state.get("name", "?"), "reference missing"))
            continue
        with Image.open(path) as im:
            source_size = im.size
        rect = CONTRACT.transform_rect(state, source_size)
        if rect is None:
            missing.append((state.get("name", "?"), "invalid transform"))
            continue
        a, b = (float(x) for x in state["beat"])
        visibility = state.get("visibility", "full")
        if visibility == "partial":
            partial.append((state.get("name", "?"), [a, b]))
            continue
        times = state.get("sample_times") or [a + (b - a) * f for f in (0.2, 0.5, 0.8)]
        for t in times:
            c = cache.get(CONTRACT.correlation_key(state, t, "image"))
            o = cache.get(CONTRACT.correlation_key(state, t, "wrong_image")) if state.get("wrong_image") else None
            scores.append(c)
            if c is None or c < threshold:
                missing.append((state.get("name", "?"), round(t, 3),
                                None if c is None else round(c, 3)))
            if o is not None and o >= threshold and (c is None or o >= c - cfg["wrong_margin"]):
                wrong.append((state.get("name", "?"), round(t, 3), round(o, 3),
                              None if c is None else round(c, 3)))
    clearance = plan.get("label_clearance")
    obstruct = []
    clearance_checked = 0
    if clearance:
        if clearance.get("sha256") != plan.get("_sha256"):
            return unmeasured(key, "label_clearance evidence is stale (video sha256 differs)")
        report = clearance.get("clearance_report")
        report_sha = clearance.get("clearance_report_sha256")
        if report and (not os.path.exists(report) or
                       (report_sha and CONTRACT.file_sha256(report) != report_sha)):
            return unmeasured(key, "label_clearance report is missing or its sha256 changed")
        obstruct = clearance.get("obstructions") or []
        clearance_checked = int(clearance.get("checked") or
                                sum(x.get("visibility", "full") == "full" for x in tracks))
    else:
        obstruct, clearance_checked, clearance_error = _measure_label_clearance(
            video, tracks, cfg["clearance_px"])
        if clearance_error:
            return unmeasured(key, f"label face/abs clearance was not measured: {clearance_error}")
    ok = not missing and not wrong and not obstruct
    measured = [x for x in scores if x is not None]
    return Row(key, ok,
               f"{len(tracks)} renderer label state(s); min delivered-pixel correlation "
               f"{min(measured) if measured else 'n/a'} (min {threshold}); {len(missing)} missing, "
               f"{len(wrong)} wrong-label, {len(obstruct)} face/abs obstruction(s); "
               f"clearance checked on {clearance_checked} state sample(s); {len(partial)} declared "
               f"transition state(s) reported but not treated as missing",
               dict(missing=missing[:30], wrong=wrong[:30], obstructions=obstruct[:30],
                    partial=partial[:30], min_corr=min(measured) if measured else None))


def labels(key, pr, cfg, plan, video, work):
    """compliance:labels -- every picture of Dan's physique carries EXACTLY ONE label.

    ⚠ DAN'S RULE, 2026-09-11, now standing in AGENTS.md: his REAL photographs carry
    "Real picture of me -- not AI-generated"; AI images of him carry "AI-GENERATED". The two are
    mutually exclusive and every picture of his physique carries exactly one of them. Viewers were
    taking his real photos for AI, which is the reason the first label exists at all.

    So this row does not check presence. It checks the PAIRING: the AI chip reads on every declared
    AI insert and on no declared real photo, and the real-picture chip reads on every declared real
    photo and on no declared AI insert.
    """
    if "label_tracks" in plan:
        return _tracked_labels(key, cfg, plan, video)
    ai = plan.get("ai_inserts")
    real = plan.get("real_photos")
    chips = plan.get("label_chips") or {}
    if ai is None or real is None:
        return unmeasured(key, "the plan must declare BOTH `ai_inserts` and `real_photos` (an "
                               "empty list is a legal answer). Without both, a mutually exclusive "
                               "pair of labels cannot be checked -- only presence can, and presence "
                               "is what let a real photo of Dan read as AI")
    if not ai and not real:
        return Row.na(key, "this cut carries no picture of Dan's physique: "
                           "`ai_inserts` and `real_photos` are both empty")
    for want in ("ai", "real"):
        if want not in chips or not os.path.exists(chips.get(want, "")):
            return unmeasured(key, f"`label_chips.{want}` is not on disk ({chips.get(want)!r}); "
                                   f"the gate needs the chip image to look for it")
    from PIL import Image

    def chip_ref(path):
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        w -= w % 2
        h -= h % 2                                   # ffmpeg crops to even sizes
        flat = Image.alpha_composite(Image.new("RGBA", im.size, (80, 80, 80, 255)), im)
        return np.asarray(flat.convert("L"), dtype=np.float32)[:h, :w]

    refs = {k: chip_ref(v) for k, v in chips.items() if k in ("ai", "real")}
    pos = plan.get("label_pos") or {}
    thr = cfg["min_corr"]
    # ⚠ AN INSERT MAY CARRY ITS LABEL SOMEWHERE ELSE, AND AT ANOTHER SIZE. One chip image and one
    # position per KIND assumes every chip of that kind is drawn identically -- true of a build whose
    # labels all sit on a full-bleed frame, false of an editor's card language, where the chip hangs
    # off the card's own animated media hole and its font shrinks to the card's width. Measured on Ad 5
    # (a goal-image card 10 px off read 0.23) and again on the Ad 1 square (a card chip read -0.03
    # against a full-frame reference) -- in BOTH cases every label was present and correct, and the row
    # was reporting the instrument, not the build. So an insert may declare its OWN `chip` and `pos`;
    # absent those it falls back to the per-kind pair exactly as before. This cannot make a wrong label
    # pass: each chip still has to correlate >= min_corr with its own reference at its own position,
    # and the cross-label test is unchanged.
    extra = {}

    def _ref_for(kind, b):
        c = (b or {}).get("chip")
        if not c:
            return refs[kind]
        if c not in extra:
            extra[c] = chip_ref(c)
        return extra[c]

    def reads(kind, t, b=None):
        ref = _ref_for(kind, b)
        h, w = ref.shape
        x, y = ((b or {}).get("pos") or pos.get(kind, (40, 40)))
        raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                              "-vf", f"crop={w}:{h}:{x}:{y},format=gray", "-f", "rawvideo", "-"],
                             capture_output=True).stdout
        if len(raw) < w * h:
            return None
        got = np.frombuffer(raw[:w * h], np.uint8).reshape(h, w).astype(np.float32)
        if got.std() < 1e-6 or ref.std() < 1e-6:
            return 0.0
        return float(np.corrcoef(ref.ravel(), got.ravel())[0, 1])

    missing, crossed, scores = [], [], []
    for kind, beats in (("ai", ai), ("real", real)):
        other = "real" if kind == "ai" else "ai"
        for b in beats:
            a, z = b["beat"]
            for t in (a + 0.9, (a + z) / 2, max(a + 0.9, z - 0.9)):
                if t >= z:
                    continue
                c = reads(kind, t, b)
                o = reads(other, t)
                if c is None:
                    missing.append((b.get("name", "?"), round(t, 2), "no frame"))
                    continue
                scores.append(round(c, 3))
                if c < thr:
                    missing.append((b.get("name", "?"), round(t, 2), round(c, 3)))
                if o is not None and o >= thr:
                    crossed.append((b.get("name", "?"), round(t, 2), f"{other} label present"))
    ok = not missing and not crossed
    return Row(key, ok,
               f"{len(ai)} AI insert(s) + {len(real)} real photo(s); label correlation min "
               f"{min(scores) if scores else 'n/a'} (min {thr}); {len(missing)} missing "
               f"{missing[:4]}; {len(crossed)} carrying the WRONG label {crossed[:4]}",
               dict(missing=missing[:20], crossed=crossed[:20], min_corr=thr,
                    scores_min=min(scores) if scores else None))


# ---------------------------------------------------------------------------- spoken content
def drug_names(key, pr, cfg, plan, video, work):
    """compliance:drug_names -- the brand names are never spoken. "weight loss medication" only."""
    words = plan.get("transcript_words") or plan.get("words")
    if not words:
        return unmeasured(key, "the plan gives no `transcript_words` -- transcribe the FINISHED "
                               "render (not the script: the script is what we meant to say)")
    text = " ".join(w["w"] if isinstance(w, dict) else str(w) for w in words)
    pat = re.compile(cfg["pattern"], re.I)
    hits = sorted(set(m.group(0).lower() for m in pat.finditer(text)))
    return Row(key, not hits, f"{len(hits)} banned name(s) spoken: {hits}", dict(hits=hits))


def negative_events(key, pr, cfg, plan, video, work):
    """compliance:negative_events -- Google's "Negative Events and Imagery", scanned by a person.

    ⚠ THIS ROW DOES NOT PRETEND TO AUTOMATE A JUDGMENT CALL. The trigger is a zoomed-in close-up of
    an overweight body part framed with disgust or shame (the fat-belly close-up plus a disapproving
    reaction is the classic strike, and it already limited one of our Demand Gen creatives).
    Close-ups of fit bodies are fine. No template separates those. What the row DOES enforce is that
    the scan happened on THIS file and its result was written down -- the same shape as the watch
    pass, which is the only reason a "watch the video" rule has ever survived a build running late.

    The plan records:  "negative_events_scan": {"sha256": "<this file>", "when": "...",
                                                "frames_checked": N, "findings": [...]}
    """
    rec = plan.get("negative_events_scan")
    if not rec:
        return unmeasured(key, "no `negative_events_scan` in the plan. Sample frames across the "
                               "finished cut, look for close-ups of out-of-shape body parts framed "
                               "with shame, and record {sha256, when, frames_checked, findings}. "
                               "A certain violation you replace yourself; an unsure one you leave "
                               "in and flag for Dan")
    have = plan.get("_sha256")
    if rec.get("sha256") != have:
        return Row(key, False, f"the scan on record is for {str(rec.get('sha256'))[:12]}, "
                               f"this file is {str(have)[:12]} -- rescan the delivered render")
    n = int(rec.get("frames_checked") or 0)
    if n < cfg["min_frames"]:
        return Row(key, False, f"only {n} frames checked (min {cfg['min_frames']})")
    findings = rec.get("findings") or []
    confirmed, review, cleared, malformed = [], [], [], []
    for f in findings:
        if not isinstance(f, dict):
            malformed.append(f)
            continue
        disposition = f.get("disposition")
        # Backward compatibility is intentionally conservative. Older scans wrote `severity:
        # uncertain`; those are review candidates, not proven violations and certainly not passes.
        if not disposition and "uncertain" in str(f.get("severity", "")).lower():
            disposition = "needs_review"
        if disposition == "confirmed_violation":
            confirmed.append(f)
        elif disposition == "needs_review":
            review.append(f)
        elif disposition == "cleared":
            cleared.append(f)
        else:
            malformed.append(f)
    val = dict(frames=n, confirmed=confirmed[:20], review=review[:20], cleared=cleared[:20],
               malformed=malformed[:20])
    if confirmed:
        return Row(key, False,
                   f"scanned {n} frames on {rec.get('when')}; {len(confirmed)} confirmed "
                   f"violation(s), {len(review)} review candidate(s): {confirmed[:4]}", val)
    if malformed:
        return unmeasured(key, f"{len(malformed)} finding(s) have no auditable disposition; use "
                               "confirmed_violation, needs_review, or cleared: "
                               f"{malformed[:3]}")
    if review:
        return Row.review(key,
                          f"scanned {n} frames on {rec.get('when')}; {len(review)} unresolved "
                          f"candidate(s): {review[:4]}", val)
    return Row(key, True,
               f"scanned {n} frames on {rec.get('when')}; no confirmed or unresolved negative-"
               f"events finding ({len(cleared)} reviewer-cleared)", val)


def script_fidelity(key, pr, cfg, plan, video, work):
    """compliance:script_fidelity -- the finished render says what the cut says it says.

    Transcribed FROM THE FINISHED RENDER. A plan can claim any words; only the file proves them, and
    a dropped half-sentence at a join is invisible to every other row here.
    """
    said = plan.get("transcript_words")
    want = plan.get("words")
    if not said or not want:
        return unmeasured(key, "needs both `transcript_words` (the FINISHED render, transcribed) "
                               "and `words` (what the cut intended)")
    import difflib
    norm = lambda ws: re.sub(r"[^a-z0-9 ]", " ", " ".join(   # noqa: E731
        (w["w"] if isinstance(w, dict) else str(w)) for w in ws).lower()).split()
    a, b = norm(want), norm(said)
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    lo = cfg["min_ratio"]
    return Row(key, ratio >= lo,
               f"{ratio*100:.1f}% of the intended words are in the render "
               f"({len(a)} expected, {len(b)} heard; min {lo*100:.0f}%)",
               dict(ratio=round(ratio, 4), expected=len(a), heard=len(b), min=lo))
