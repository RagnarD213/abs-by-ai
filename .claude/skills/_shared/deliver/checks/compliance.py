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
import subprocess

import numpy as np

from .. import common as C
from ..common import Row, unmeasured


# ---------------------------------------------------------------------------- banned screens
def _norm(a):
    a = a.astype(np.float32)
    a -= a.mean()
    return a / max(float(a.std()), 1e-6)


def _fft_shape(fh_in, th):
    return 1 << int(np.ceil(np.log2(fh_in + th - 1)))


def _ncc_peak(FT, F, T, th, tw, fh, fw):
    """Peak normalised cross-correlation of template T anywhere in frame F.

    Full NCC, not a fixed-crop correlation: the app screen appears as a full frame in a vertical
    ad, as a phone PiP beside Dan in a longform, and at whatever size an editor chose in between.
    A gate pinned to one crop only sees the layout it was written for.

    FT is the frame's rfft2 at this (fh, fw), passed in so it is computed ONCE per scale rather
    than once per template -- four templates share each scale, so hoisting it cuts the scan by ~4x.
    """
    if th > F.shape[0] or tw > F.shape[1]:
        return -1.0, None
    n = th * tw
    P = np.pad(np.cumsum(np.cumsum(F, 0), 1), ((1, 0), (1, 0)))
    P2 = np.pad(np.cumsum(np.cumsum(F * F, 0), 1), ((1, 0), (1, 0)))
    box = lambda I: I[th:, tw:] - I[:-th, tw:] - I[th:, :-tw] + I[:-th, :-tw]   # noqa: E731
    mu = box(P) / n
    sd = np.sqrt(np.maximum(box(P2) / n - mu * mu, 0.0))
    c = np.fft.irfft2(FT * np.conj(np.fft.rfft2(T, (fh, fw))), (fh, fw))
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

    specs = []                      # (t, scale, phone_h, TOP, BOTTOM, expected dy)
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
            T = S[int(ph * top0):int(ph * top1)]
            B = S[int(ph * bot0):int(ph * bot1)]
            if T.shape[0] < 8 or B.shape[0] < 8 or T.shape[1] > gw or B.shape[0] > gh:
                continue
            specs.append((t, frac, ph, _norm(T), _norm(B), int(ph * (bot0 - top0))))
    if not specs:
        return unmeasured(key, "no template strip could be read out of the banned source")

    pre = cfg["prescreen_ncc"]
    both = cfg["min_strip_ncc"]
    slop = cfg["position_slop_px"]
    p = subprocess.Popen([C.FF, "-v", "error", "-i", video, "-vf", f"scale={gw}:{gh},format=gray",
                          "-an", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    best, hits, n = (-1.0, None, None), [], 0
    ffts = {}
    while True:
        raw = p.stdout.read(gw * gh)
        if len(raw) < gw * gh:
            break
        F = np.frombuffer(raw, np.uint8).reshape(gh, gw).astype(np.float32)
        n += 1
        ffts.clear()
        hit = False
        for t, frac, ph, T, B, dy in specs:
            # STAGE 1: the cheap top strip. Most frames die here.
            th, tw = T.shape
            shp = (_fft_shape(gh, th), _fft_shape(gw, tw))
            if shp not in ffts:
                ffts[shp] = np.fft.rfft2(F, shp)
            vt, pt = _ncc_peak(ffts[shp], F, T, th, tw, *shp)
            if vt < pre:
                continue
            # STAGE 2: the bottom strip must agree, and agree about WHERE.
            bh, bw = B.shape
            shp2 = (_fft_shape(gh, bh), _fft_shape(gw, bw))
            if shp2 not in ffts:
                ffts[shp2] = np.fft.rfft2(F, shp2)
            vb, pb = _ncc_peak(ffts[shp2], F, B, bh, bw, *shp2)
            score = min(vt, vb)
            if score > best[0]:
                best = (score, round(n / pr["fps"], 2), (t, frac, round(vt, 3), round(vb, 3)))
            if vt >= both and vb >= both and pt and pb \
                    and abs(pb[1] - pt[1]) <= slop and abs((pb[0] - pt[0]) - dy) <= slop:
                hits.append((round(n / pr["fps"], 2), round(vt, 3), round(vb, 3), frac))
                hit = True
                break
        if hit:
            continue
    p.stdout.close()
    p.wait()
    return Row(key, not hits,
               f"{n} frames x {len(specs)} layout templates; best paired score {best[0]:.3f} at "
               f"{best[1]}s {best[2]}; {len(hits)} frame(s) with BOTH chrome strips over {both} at "
               f"consistent positions: {hits[:6]}",
               dict(frames=n, best=round(best[0], 3), best_at=best[1], hits=hits[:60],
                    min_strip_ncc=both, prescreen=pre))


# ---------------------------------------------------------------------------- labels
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
    return Row(key, not findings,
               f"scanned {n} frames on {rec.get('when')}; {len(findings)} finding(s): {findings[:4]}",
               dict(frames=n, findings=findings[:20]))


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
