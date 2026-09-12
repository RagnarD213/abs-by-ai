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


def _ncc_max(F, T):
    """Peak normalised cross-correlation of template T anywhere in frame F.

    Full NCC, not a fixed-crop correlation: the app screen appears as a full frame in a vertical
    ad, as a phone PiP beside Dan in a longform, and at whatever size an editor chose in between.
    A gate pinned to one crop only sees the layout it was written for.
    """
    th, tw = T.shape
    if th > F.shape[0] or tw > F.shape[1]:
        return -1.0, None
    n = th * tw
    P = np.pad(np.cumsum(np.cumsum(F, 0), 1), ((1, 0), (1, 0)))
    P2 = np.pad(np.cumsum(np.cumsum(F * F, 0), 1), ((1, 0), (1, 0)))
    box = lambda I: I[th:, tw:] - I[:-th, tw:] - I[th:, :-tw] + I[:-th, :-tw]   # noqa: E731
    mu = box(P) / n
    sd = np.sqrt(np.maximum(box(P2) / n - mu * mu, 0.0))
    fh = 1 << int(np.ceil(np.log2(F.shape[0] + th - 1)))
    fw = 1 << int(np.ceil(np.log2(F.shape[1] + tw - 1)))
    c = np.fft.irfft2(np.fft.rfft2(F, (fh, fw)) * np.conj(np.fft.rfft2(T, (fh, fw))), (fh, fw))
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

    Calibrated 2026-09-11 on the corpus:
        FINAL_spraytan_PRE_REBUILD  REJECTED   the app "Meet the new you" BEFORE/AFTER screen is on
                                               screen as a phone PiP from ~18:04 (measured below)
        website rev 4               approved   best NCC 0.484 over 6,900 frames, 0 frames over 0.72
    """
    src = plan.get("banned_source")
    times = plan.get("banned_times")
    if not src or not os.path.exists(src):
        return unmeasured(key, f"`banned_source` not readable ({src!r}) -- is the asset library "
                               f"mounted? Without the screen itself nothing can scan for it")
    if not times:
        return unmeasured(key, "the plan gives no `banned_times` into the banned source")
    W, H = pr["width"], pr["height"]
    gw = cfg.get("grid_w", 192)
    gh = max(2, int(round(gw * H / W / 2)) * 2)
    scales = cfg.get("scales", (1.00, 0.92, 0.80, 0.65, 0.50))
    tpl = []
    for t in times:
        for frac in scales:
            th = int(round(gh * frac))
            tw = max(2, int(round(th * cfg.get("source_aspect", 1080 / 1920))))
            raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", src,
                                  "-frames:v", "1", "-vf", f"scale={tw}:{th},format=gray",
                                  "-f", "rawvideo", "-"], capture_output=True).stdout
            if len(raw) < tw * th:
                continue
            tpl.append((t, frac, _norm(np.frombuffer(raw[:tw * th], np.uint8).reshape(th, tw))))
    if not tpl:
        return unmeasured(key, "no template frame could be read out of the banned source")

    thr = cfg["max_ncc"]
    p = subprocess.Popen([C.FF, "-v", "error", "-i", video, "-vf", f"scale={gw}:{gh},format=gray",
                          "-an", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    best, hits, n = (-1.0, None, None), [], 0
    while True:
        raw = p.stdout.read(gw * gh)
        if len(raw) < gw * gh:
            break
        F = np.frombuffer(raw, np.uint8).reshape(gh, gw).astype(np.float32)
        n += 1
        for t, frac, T in tpl:
            v, _pos = _ncc_max(F, T)
            if v > best[0]:
                best = (v, round(n / pr["fps"], 2), (t, frac))
            if v > thr:
                hits.append((round(n / pr["fps"], 2), round(v, 3)))
                break
    p.stdout.close()
    p.wait()
    return Row(key, not hits,
               f"{n} frames scanned against {len(tpl)} templates; best {best[0]:.3f} at "
               f"{best[1]}s (source {best[2]}); {len(hits)} frame(s) over {thr}: {hits[:6]}",
               dict(frames=n, best=round(best[0], 3), best_at=best[1], hits=hits[:60], max_ncc=thr))


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

    def reads(kind, t):
        ref = refs[kind]
        h, w = ref.shape
        x, y = pos.get(kind, (40, 40))
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
                c = reads(kind, t)
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
