#!/usr/bin/env python3
"""THE JUNK-FOOTAGE PASS. Six detectors that used to live in three skills' work/ folders, run as
ONE report, produced BEFORE the render, listing every candidate with its class, timecode,
measurement and suggested action. It turns "double-check everything" into a list.

  junk.py <delivered.mp4>                                   delivered mode: transcribes the file
  junk.py <source roll> --ranges ranges.py|--edl edl.json|--keeps tight_cuts.json
          [--words roll.words.json] [--tight tight.mov]     pre-render mode: the cut, before it exists
  common: [--out junk_report.json] [--model small] [--verify-model medium.en] [--no-verify]
          [--pieces segments.json]  (shorts: each piece gets its own HEAD / PAUSE / SPLICE rows)

WHY. Junk footage is 1 of the 11 rejections in `_shared/qc_corpus/`: the spray-tan longform, Dan --
"junk footage and repeated takes were kept in here. Eliminate this junk footage." The detectors
already existed and already worked; they had never been run as one pass. On a single shorts batch
junkscan.py "found all six of Dan's timecodes and nine more he had not reached yet".

THE SIX, and where each came from (2026-09-24, `handoff-20260911-junk-footage-pass.md`):

  PAUSE      shorts/…/work/junkscan.py     a measured gap ≥ 0.55 s inside a kept piece. ⚠ 0.55-0.65 s
                                           is breathing rhythm, not dead air (shorts/SKILL.md:445):
                                           reported, never stripped. ≥ 1.0 s is high confidence.
  HEAD       junkscan.py                   speech starts > 0.45 s after the piece's first frame
  SPLICE     junkscan.py                   a picture cut inherited from the source edit inside a
                                           piece -- "every splice inside a short is a NAKED JUMP CUT
                                           unless it is hidden"
  SWALLOWED  shorts/…/work/fixonsets.py    a gap ≥ 0.25 s wholly INSIDE a word. Dan's "junk footage
                                           in the beginning at 0:01" was a 0.95 s hesitation Whisper
                                           swallowed inside the word "you're".
  STRETCH    ad-edit/reference/repeat_scan "a stretched word is a hidden restart until proven
                                           otherwise" -- every word > 0.7 s, VERIFIED by
                                           re-transcribing the span in isolation
  REPEAT     repeat_scan.py                every repeated 4-gram within 25 s, classified RESTART
                                           (junk) or ANAPHORA (deliberate) by what followed each
                                           occurrence: his rhetorical repeats are deliberate,
                                           re-INTRODUCTIONS of the same item are junk
  ORPHAN     ad-edit/reference/orphan_scan speech-level energy no word covers -- the abandoned
                                           take Whisper silently dropped. ⚠ It PASSED Dan's 0:32
                                           repeat, which is why REPEAT runs beside it. Always both.
  HARD_SPLICE ad-edit/reference/hard_splices  pre-render: which joins on the tight cut are
                                           MEASURABLY discontinuous (frame difference over the
                                           file's own p99). On Ad 2: 135 splices, 76 hard, 37
                                           uncovered, only 22 both.
  PAUSEJUMP  shorts/…/work/pausejump.py    pre-render: how visible the join a pause REMOVAL would
                                           create is, against the file's adjacent-frame baseline.
                                           Measured 4.97-12.46 against a 1.30 baseline: every
                                           removal needs a picture cut or an insert over it.

VERIFICATION. STRETCH, RESTART and ORPHAN candidates are re-transcribed alone (a 4 s window,
medium.en, no prior context) before they count. `verified` is "confirmed", "not confirmed" or
None (--no-verify). The delivery gate's `junk:repeated_take` row fails a file on CONFIRMED
candidates only -- an unverified flag is a lead, not a finding.

⚠ Do not re-render any delivered master to run this; it reads files, it never writes media.
⚠ Media/ is gitignored. This module lives in the repo so it enforces something.
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from _shared.cut import speech as S                          # noqa: E402

REPORT_VERSION = "1.0.0"

# The detectors' PROVEN defaults, carried from the scripts they came from. These are detector
# settings, not delivery bounds: what makes a file FAIL lives in _shared/deliver/formats.py.
PAUSE_MIN = 0.55          # junkscan.py PAUSE_MIN
BREATH_MAX = 0.65         # shorts/SKILL.md:445 -- 0.55-0.65 s is breathing rhythm
PAUSE_HIGH = 1.00         # Dan flagged 1.21 s ("slight pause here, cut this"); the capper's 1.3 missed it
HEAD_MAX = 0.45           # junkscan.py "slow start"
SWALLOW_MIN = 0.25        # fixonsets.py rule 3
STRETCH_MIN = 0.70        # repeat_scan.py --stretch
REPEAT_N = 4              # repeat_scan.py --n
REPEAT_WINDOW = 25.0      # repeat_scan.py --window
ORPHAN_DB = -38.0         # orphan_scan.py THRESH (absolute floor of the relative rule below)
ORPHAN_REL_DB = 12.0      # speech-level = within 12 dB of the file's own speaking level
ORPHAN_MIN = 0.30         # orphan_scan.py MINLEN
ORPHAN_PAD = 0.12         # orphan_scan.py word cover pad
VERIFY_HALF = 2.0         # the 4 s isolated window
VERIFY_TAIL = 1.5         # extend PAST the span: truncating Whisper drops the last word
MAX_VERIFY = 60           # per class; the rest are reported unverified (low confidence)


# ---------------------------------------------------------------------------- timelines
def pieces_from_ranges(ranges):
    """[(a, b, name?, ...)] on the SOURCE -> pieces with output offsets and the output joins."""
    pieces, off = [], 0.0
    for r in ranges:
        a, b = float(r[0]), float(r[1])
        name = r[2] if len(r) > 2 and isinstance(r[2], str) else f"{a:.2f}-{b:.2f}"
        pieces.append(dict(a=a, b=b, off=round(off, 3), name=name))
        off += b - a
    joins = [round(p["off"], 3) for p in pieces[1:]]
    return pieces, joins


def load_ranges(path):
    """ranges.py (RANGES = [...]), edl.json ({"ranges": [{"start","end","beat"}]}) or
    tight_cuts.json ({"keeps": [[a, b], ...]})."""
    if path.endswith(".py"):
        ns = {}
        exec(open(path).read(), ns)                          # noqa: S102 -- our own recipe file
        return [tuple(r) for r in ns["RANGES"]]
    d = json.load(open(path))
    if "ranges" in d:
        return [(r["start"], r["end"], r.get("beat") or r.get("name") or "") for r in d["ranges"]]
    if "keeps" in d:
        return [(a, b) for a, b in d["keeps"]]
    raise SystemExit(f"{path}: expected RANGES, ranges or keeps")


def map_words_to_output(words, pieces):
    """Source-timeline words -> the cut's timeline. A word straddling a cut edge is clipped to it;
    a word wholly outside every piece is dropped (it was cut)."""
    out = []
    for p in pieces:
        for w in words:
            if w["e"] <= p["a"] or w["t"] >= p["b"]:
                continue
            t, e = max(w["t"], p["a"]), min(w["e"], p["b"])
            if e - t <= 0.01:
                continue
            out.append(dict(w=w["w"], t=round(p["off"] + t - p["a"], 3),
                            e=round(p["off"] + e - p["a"], 3), p=w.get("p"),
                            src=round(t, 3), piece=p["name"]))
    out.sort(key=lambda w: w["t"])
    return out


def concat_audio(media, pieces, out_wav, amap=None, af=None):
    """The cut's AUDIO, before any render exists: the pieces concatenated at 16 kHz mono."""
    parts = []
    with tempfile.TemporaryDirectory(prefix="cut-concat-") as tmp:
        for i, p in enumerate(pieces):
            f = os.path.join(tmp, f"{i:04d}.wav")
            S.wav16k(media, f, amap, af, ss=p["a"], dur=p["b"] - p["a"])
            parts.append(f)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as fh:
            for f in parts:
                fh.write(f"file '{f}'\n")
        subprocess.run([S.FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                        lst, "-c", "copy", out_wav], check=True)
    return out_wav


def to_source(t, pieces):
    """Output time -> (source time, piece name), or (None, None)."""
    for p in pieces or []:
        if p["off"] <= t <= p["off"] + (p["b"] - p["a"]) + 1e-6:
            return round(p["a"] + t - p["off"], 3), p["name"]
    return None, None


# ---------------------------------------------------------------------------- the detectors
def _cand(cls, t, end=None, measure=None, action="", confidence="medium", note=""):
    return dict(cls=cls, t=round(float(t), 3), end=None if end is None else round(float(end), 3),
                measure=measure or {}, action=action, confidence=confidence, note=note,
                verified=None, resolution=None)


def detect_pauses(gaps, pieces=None, dur=None, edge=0.05):
    """PAUSE: a measured gap ≥ PAUSE_MIN inside a piece (never touching its edges)."""
    out = []
    spans = ([(p["off"], p["off"] + p["b"] - p["a"]) for p in pieces] if pieces
             else [(0.0, dur if dur else 1e9)])
    for g0, g1 in gaps:
        L = g1 - g0
        if L < PAUSE_MIN:
            continue
        for a, b in spans:
            if g0 >= a + edge and g1 <= b - edge:
                if L < BREATH_MAX:
                    out.append(_cand("PAUSE", g0, g1, dict(seconds=round(L, 2)),
                                     "keep -- breathing rhythm, not dead air", "low"))
                else:
                    out.append(_cand("PAUSE", g0, g1, dict(seconds=round(L, 2)),
                                     "tighten to ~0.5 s (0.30 tail + 0.20 lead) and cover the join "
                                     "with a picture cut or an insert",
                                     "high" if L >= PAUSE_HIGH else "medium"))
                break
    return out


def detect_head(words, pieces=None):
    """HEAD: how long after a piece's first frame speech starts."""
    out = []
    starts = [(p["off"], p["name"]) for p in pieces] if pieces else [(0.0, "file")]
    for a, name in starts:
        first = next((w["t"] for w in words if w["t"] >= a - 0.01), None)
        if first is None:
            continue
        d = first - a
        if d > HEAD_MAX:
            out.append(_cand("HEAD", a, first, dict(seconds=round(d, 2), piece=name),
                             "trim the head: start the piece ~0.20 s before the first word",
                             "high" if d > 1.0 else "medium"))
    return out


def detect_splices(joins, pieces=None, margin=0.25):
    """SPLICE: an inherited picture cut inside a piece (shorts cut from a spliced long-form)."""
    out = []
    if not pieces:
        return out
    for p in pieces:
        a, b = p["off"], p["off"] + p["b"] - p["a"]
        for c in joins:
            if a + margin < c < b - margin:
                out.append(_cand("SPLICE", c, None, dict(piece=p["name"]),
                                 "a naked jump cut unless hidden: punch ≥ 10 % or insert over it",
                                 "medium"))
    return out


def detect_swallowed(words, gaps):
    """SWALLOWED: a gap ≥ SWALLOW_MIN wholly inside a word. Also returns Whisper's boundaries
    corrected against the measured silence (fixonsets rules 1-3), bounded so no word inverts."""
    out, fixed = [], []
    for w in words:
        t, e = w["t"], w["e"]
        nw = dict(w)
        if e - t > 1e-4:
            g = S.gap_at(gaps, t)
            if g and g[1] < e:
                nw["t"] = round(g[1], 3)                                   # rule 1
            else:
                for g0, g1 in gaps:
                    if g0 > e:
                        break
                    if g0 > t + 0.02 and g1 < e - 0.02 and g1 - g0 >= SWALLOW_MIN:   # rule 3
                        L = g1 - g0
                        out.append(_cand("SWALLOWED", g0, g1,
                                         dict(seconds=round(L, 2), word=w["w"].strip(),
                                              word_span=[t, e]),
                                         ("re-time the word to the gap's end (a timing correction, "
                                          "not junk)" if L < 0.45 else
                                          "the word's real onset is the gap's end; the gap is dead "
                                          "air Whisper hid -- treat as PAUSE and cover the join"),
                                         "high" if L >= 0.9 else ("medium" if L >= 0.45 else "low")))
                        nw["t"] = round(g1, 3)
                        break
            g = S.gap_at(gaps, nw["e"])
            if g and g[0] > nw["t"]:
                nw["e"] = round(g[0], 3)                                   # rule 2
            if nw["e"] <= nw["t"]:
                nw = dict(w)
        fixed.append(nw)
    return out, fixed


def detect_stretched(words):
    """STRETCH: every word longer than STRETCH_MIN. A hidden restart until verified otherwise."""
    return [_cand("STRETCH", w["t"], w["e"],
                  dict(seconds=round(w["e"] - w["t"], 2), word=w["w"].strip()),
                  "re-transcribe the span alone; if it hides a restart, cut the WHOLE restated "
                  "sentence, not the flub inside it", "medium")
            for w in words if w["e"] - w["t"] > STRETCH_MIN]


def _sim(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0


def detect_repeats(words, gaps=(), n=REPEAT_N, window=REPEAT_WINDOW):
    """REPEAT: a repeated n-gram within `window` seconds, classified by HOW it was delivered.

    Three kinds, measured on the rev-0 spray-tan reconstruction (2026-09-24), where Dan's 4:00
    junk take and eleven of his deliberate repeats sat side by side:

    RESTART (junk, the re-take): a measured HESITATION -- a gap past breathing rhythm (> 0.65 s)
      or a word stretched past 0.7 s -- within 1.5 s before the second copy or inside it, AND the
      second copy re-says what the first said (whole ≥ 0.6 or continuation ≥ 0.4). A weaker re-say
      (the first attempt abandoned within 8 words, but little text in common) needs a STRONG
      hesitation, ≥ 1.0 s. "then this if[0.7s] you[1.6s] have someone who can help you" is this.
      "If you are super pale. now,[0.7s] if you are super pale" is this.
    REINTRO (listen): no hesitation, but the SAME PHRASE said again after ≥ 8 words of other
      content -- the next four words after each copy agree (≥ 0.6) and so does the continuation
      (≥ 0.5). The doubled Oura-ring introduction is this; so is "We have an AI personal trainer,
      which takes your before picture and your goal… We have an AI nutritionist, which takes your
      before picture and your goal…" -- a deliberate parallel list. Measured on C1512 take 60
      (2026-09-24): no detector separates those two, so REINTRO is LOW confidence, goes to the
      report for a listen, and never fails the gate on its own.
    ANAPHORA (deliberate): everything else. "He's trying to avoid cancer. He's trying to avoid
      skin damage." "The lighting was a little bit better. The camera was a little bit better."
      "We have an AI personal trainer, which… We have an AI nutritionist, which…" -- a fluent
      parallel structure whose items differ. His rhetorical repeats are deliberate; only
      re-INTRODUCTIONS of the same item are junk (longform-edit junk rule 3).
    """
    toks = [(w["t"], w["e"], S.norm(w["w"]), w["w"]) for w in words if S.norm(w["w"])]
    stretched = [(w["t"], w["e"]) for w in words if w["e"] - w["t"] > STRETCH_MIN]
    # a hesitation is a gap PAST breathing rhythm (> 0.65 s: the edit's own 0.50 s natural beat and
    # a 0.54 s sentence pause are not one) or a stretched word; a STRONG one is ≥ 1.0 s either way
    breaks = [(g0, g1) for g0, g1 in gaps if g1 - g0 > BREATH_MAX] + stretched
    strong = [(g0, g1) for g0, g1 in gaps if g1 - g0 >= PAUSE_HIGH] + \
             [(t, e) for t, e in stretched if e - t >= 1.0]

    def hesitation(t_lo, t_hi, which=None):
        return any(b1 > t_lo and b0 < t_hi for b0, b1 in (which if which is not None else breaks))

    out, seen = [], {}
    for i in range(len(toks) - n + 1):
        g = " ".join(x[2] for x in toks[i:i + n])
        t = toks[i][0]
        if g in seen and t - toks[seen[g]][0] <= window:
            j = seen[g]
            cont_a = [x[2] for x in toks[j + n:i]]
            cont_b = [x[2] for x in toks[i + n:i + n + max(len(cont_a), 1) + 2]]
            sim = _sim(cont_a, cont_b)
            whole = _sim([x[2] for x in toks[j:i]], [x[2] for x in toks[i:i + (i - j)]])
            head = _sim([x[2] for x in toks[j + n:j + n + 4]], [x[2] for x in toks[i + n:i + n + 4]])
            second_end = toks[min(i + n - 1, len(toks) - 1)][1]
            first_end = toks[min(j + n - 1, len(toks) - 1)][1]
            # the hesitation must come AFTER the first copy's own words: two copies 1.3 s apart
            # ("you look and[0.8 s] you don't want to get cancer and you don't want to get
            # prematurely aged") otherwise count the first copy's stretched word as the break
            lo = max(t - 1.5, first_end)
            brk = hesitation(lo, second_end)
            brk_strong = hesitation(lo, second_end, strong)
            resaid_strong = whole >= 0.6 or sim >= 0.4
            resaid_weak = len(cont_a) <= 8
            # measured on rev 2 (2026-09-24): "the photographer was a little bit better And[0.86 s]
            # I was a little bit leaner" is a list with a breath, not a restart -- a WEAK re-say
            # needs a STRONG hesitation (Dan's 4:00 take: 1.6 s + 1.46 s) before it counts
            if (brk and resaid_strong) or (brk_strong and resaid_weak):
                kind = "RESTART"
                conf = "high" if resaid_strong else "medium"
                action = ("junk: cut the whole restated sentence back to the first copy's start "
                          "(cutting only the flub leaves the repeat)")
            elif not brk and head >= 0.6 and sim >= 0.5 and len(cont_a) >= 8:
                kind, conf = "REINTRO", "low"
                action = ("listen: the same phrase said twice, fluently -- a re-introduction of the same item "
                          "is junk (keep one copy, cut the other sentence whole); a parallel list "
                          "('an AI trainer, which takes… an AI nutritionist, which takes…') is deliberate. "
                          "No detector can tell these apart; a person can in two seconds")
            else:
                kind, conf = "ANAPHORA", "low"
                action = "keep -- a deliberate rhetorical repeat (fluent, different item)"
            out.append(_cand("REPEAT", toks[j][0], toks[i + n - 1][1],
                             dict(gram=g, first=round(toks[j][0], 2), second=round(t, 2),
                                  gap_s=round(t - toks[j][0], 2), kind=kind, hesitation=brk,
                                  continuation_similarity=round(sim, 2), whole_similarity=round(whole, 2),
                                  item_similarity=round(head, 2), words_between=len(cont_a)),
                             action, conf))
        seen[g] = i
    # one row per (first, second) pair: the same restart repeats for every n-gram inside it
    merged = []
    for c in out:
        if merged and abs(c["measure"]["first"] - merged[-1]["measure"]["first"]) < 1.0 and \
                abs(c["measure"]["second"] - merged[-1]["measure"]["second"]) < 1.0:
            m = merged[-1]
            if not m["measure"]["gram"].endswith("…"):
                m["measure"]["gram"] += " …"
            m["end"] = max(m["end"], c["end"])
            rank = {"ANAPHORA": 0, "REINTRO": 1, "RESTART": 2}
            if rank[c["measure"]["kind"]] > rank[m["measure"]["kind"]]:
                m["measure"]["kind"], m["confidence"], m["action"] = c["measure"]["kind"], c["confidence"], c["action"]
            elif c["measure"]["kind"] == m["measure"]["kind"] and c["confidence"] == "high":
                m["confidence"] = "high"
            continue
        merged.append(c)
    return merged


def detect_orphans(db, words, thr=None):
    """ORPHAN: speech-level energy no word covers, ≥ ORPHAN_MIN long."""
    if thr is None:
        thr = max(ORPHAN_DB, S.speech_level(db) - ORPHAN_REL_DB)
    n = len(db)
    cov = np.zeros(n, bool)
    for w in words:
        i0 = max(0, int((w["t"] - ORPHAN_PAD) / S.HOP_S))
        i1 = min(n, int((w["e"] + ORPHAN_PAD) / S.HOP_S) + 1)
        cov[i0:i1] = True
    hot = (db > thr) & ~cov
    out, i = [], 0
    while i < n:
        if hot[i]:
            j = i
            while j < n and hot[j]:
                j += 1
            L = (j - i) * S.HOP_S
            if L >= ORPHAN_MIN:
                out.append(_cand("ORPHAN", i * S.HOP_S, j * S.HOP_S,
                                 dict(seconds=round(L, 2), peak_db=round(float(db[i:j].max()), 1),
                                      threshold_db=round(thr, 1)),
                                 "re-transcribe alone: if it is speech, an abandoned take shipped",
                                 "high" if L >= 0.8 else "medium"))
            i = j
        else:
            i += 1
    return out


def detect_hard_splices(tight_video, joins):
    """HARD_SPLICE (pre-render): joins whose frame difference exceeds the tight cut's own p99."""
    out = []
    if not joins:
        return out
    with tempfile.TemporaryDirectory(prefix="cut-hs-") as tmp:
        meta = os.path.join(tmp, "diff.txt")
        subprocess.run([S.FF, "-nostdin", "-v", "error", "-i", tight_video, "-vf",
                        "scale=320:180,tblend=all_mode=difference,signalstats,"
                        f"metadata=print:key=lavfi.signalstats.YAVG:file={meta}",
                        "-an", "-f", "null", "-"], check=True)
        vals = []
        for blk in open(meta).read().split("frame:")[1:]:
            t = re.search(r"pts_time:([\d.]+)", blk)
            v = re.search(r"YAVG=([\d.]+)", blk)
            if t and v:
                vals.append((float(t.group(1)), float(v.group(1))))
    if not vals:
        return out
    ys = sorted(v for _, v in vals)
    p99 = ys[int(len(ys) * 0.99)]
    ts = np.array([t for t, _ in vals])
    vs = np.array([v for _, v in vals])
    for j in joins:
        near = vs[np.abs(ts - j) < 0.05]
        d = float(near.max()) if len(near) else 0.0
        if d > p99:
            out.append(_cand("HARD_SPLICE", j, None,
                             dict(frame_diff=round(d, 2), p99=round(p99, 2), ratio=round(d / max(p99, 1e-6), 2)),
                             "force a punch boundary or cover this join; it reads as a jump",
                             "high" if d > 2 * p99 else "medium"))
    return out


def _frame_gray(video, t, w=320, h=180):
    p = subprocess.run([S.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                        "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8)
    return a[:w * h].reshape(h, w).astype(np.float32) if len(a) >= w * h else None


def detect_pausejump(source_video, pauses, pieces, fps=29.97, reference_joins=None):
    """PAUSEJUMP (pre-render): how visible the join a PAUSE removal creates, on the SOURCE picture,
    against the source's adjacent-frame baseline. ≥ 3x the baseline is a real jump (measured
    4.97-12.46 against 1.30 on the supplements roll)."""
    out = []
    if not pauses:
        return out
    dur = S.media_duration(source_video) or 0
    probes = [dur * f for f in (0.2, 0.4, 0.6, 0.8)] if dur > 10 else [1.0]
    base_vals = []
    for t in probes:
        a, b = _frame_gray(source_video, t), _frame_gray(source_video, t + 1.0 / fps)
        if a is not None and b is not None:
            base_vals.append(float(np.abs(a - b).mean()))
    base = float(np.median(base_vals)) if base_vals else 1.0
    ref = None
    if reference_joins:
        rv = []
        for a_src, b_src in reference_joins[:6]:
            fa, fb = _frame_gray(source_video, a_src - 0.08), _frame_gray(source_video, b_src + 0.08)
            if fa is not None and fb is not None:
                rv.append(float(np.abs(fa - fb).mean()))
        ref = float(np.median(rv)) if rv else None
    for c in pauses:
        if c["confidence"] == "low":
            continue
        s0, _ = to_source(c["t"], pieces)
        s1, _ = to_source(c["end"], pieces)
        if s0 is None or s1 is None:
            continue
        fa, fb = _frame_gray(source_video, s0 - 0.05), _frame_gray(source_video, s1 + 0.05)
        if fa is None or fb is None:
            continue
        j = float(np.abs(fa - fb).mean())
        r = j / max(base, 1e-6)
        verdict = "invisible" if r < 1.5 else ("mild -- punch it" if r < 3.0 else "real jump -- punch or insert")
        out.append(_cand("PAUSEJUMP", c["t"], c["end"],
                         dict(jump=round(j, 2), baseline=round(base, 2), x_baseline=round(r, 2),
                              x_splice=None if not ref else round(j / max(ref, 1e-6), 2),
                              source=[s0, s1]),
                         f"{verdict}: a pause removal is as visible as the fault it fixes",
                         "high" if r >= 3.0 else ("medium" if r >= 1.5 else "low")))
    return out


# ---------------------------------------------------------------------------- verification
_CONTRACTIONS = {"gonna": "going to", "wanna": "want to", "gotta": "got to", "kinda": "kind of",
                 "alright": "all right", "yall": "you all", "y'all": "you all", "cause": "because",
                 "til": "until", "lemme": "let me", "dunno": "do not know", "outta": "out of"}


def _canon(raw_words):
    """Tokens two Whisper models will agree on: lower, no punctuation, contractions expanded."""
    out = []
    for w in raw_words:
        n = S.norm(w)
        if not n:
            continue
        n = _CONTRACTIONS.get(n, n)
        n = re.sub(r"'", "", n)
        out.extend(n.split())
    return out


def verify(cands, wav, words, model="medium.en", quiet=False):
    """Re-transcribe each STRETCH / RESTART / ORPHAN span alone and mark it confirmed or not."""
    todo = [c for c in cands if c["cls"] in ("STRETCH", "ORPHAN") or
            (c["cls"] == "REPEAT" and c["measure"].get("kind") in ("RESTART", "REINTRO"))]
    per = {}
    for c in todo:
        per.setdefault(c["cls"], []).append(c)
    for cls, lst in per.items():
        lst.sort(key=lambda c: -(c["measure"].get("seconds") or c["measure"].get("gap_s") or 0))
        for c in lst[MAX_VERIFY:]:
            c["verified"] = None
            c["note"] = (c["note"] + " " if c["note"] else "") + f"unverified: over the {MAX_VERIFY}-per-class cap"
            c["confidence"] = "low"
        lst[:] = lst[:MAX_VERIFY]
    n = sum(len(v) for v in per.values())
    if n and not quiet:
        print(f"  verifying {n} candidate(s) by isolated re-transcription ({model})", flush=True)
    for c in per.get("STRETCH", []):
        t0, t1 = c["t"] - VERIFY_HALF, c["end"] + VERIFY_TAIL
        iso = S.retranscribe_span(wav, t0, t1, model)
        # the words whose MIDPOINT falls inside the stretched token's own span: the full pass says
        # there is one word here. Three or more, or a repeated bigram nearby, is a hidden restart.
        # ⚠ Not "extra words in a padded window": timing slop and spelling ("Alright" vs "All
        # right") confirmed two clean words on the rev-2 spray-tan master that way (2026-09-24).
        # medium.en's word timings do not line up with the full pass's, so nothing here counts
        # words by position. The restart SIGNATURE is textual: the isolated pass hears a repeated
        # bigram in this window that the full pass does not ("out of shape, I've been out of
        # shape" stitched to one copy), or three or more words more than the full pass heard.
        # Anaphora repeats in BOTH passes and so never confirms; a spelling split ("All right")
        # adds one token, not three.
        # ⚠ both passes are canonicalised the same way first: medium.en writes "going to" where
        # small wrote "gonna", which manufactured a repeated bigram on the rev-2 master. And no
        # token COUNT: the two passes disagree by two or three words at the window's edges.
        # ⚠ and the repeat has to sit AT the stretched word, not in the clip's last second: whisper
        # hallucinates a repeated tail on a truncated clip ("...their own face on their own face",
        # Muhammad Ad 1 at 0:56, 2026-09-24), which is a fact about the clip edge, not the speech.
        iso_in = [w for w in iso if w["e"] > t0 and w["t"] < t1]
        near = _canon([w["w"] for w in iso_in])
        times = [w["t"] for w in iso_in for _ in _canon([w["w"]])]
        main = _canon([w["w"] for w in S.words_in(words, t0, t1)])
        rep_main = {b for b in zip(main, main[1:]) if list(zip(main, main[1:])).count(b) > 1}
        new_repeat = set()
        pairs = list(zip(near, near[1:]))
        for k, b in enumerate(pairs):
            if b in rep_main or pairs.count(b) < 2:
                continue
            at = [times[i] for i, bb in enumerate(pairs) if bb == b]
            if max(at) > t1 - 1.0:                          # a copy in the clip's last second: tail echo
                continue
            if any(c["t"] - 1.5 <= x <= c["end"] + 0.5 for x in at):
                new_repeat.add(b)
        c["measure"]["isolated"] = " ".join(w["w"].strip() for w in iso
                                            if w["e"] > c["t"] - 0.5 and w["t"] < c["end"] + 0.5)
        if new_repeat:
            c["verified"] = "confirmed"
            c["confidence"] = "high"
            c["note"] = "hidden restart: the isolated pass hears words the full pass folded into one token"
        else:
            c["verified"] = "not confirmed"
            c["confidence"] = "low"
            c["note"] = "a long word or a folded pause (see SWALLOWED / PAUSE), not a restart"
    for c in per.get("REPEAT", []):
        t0, t1 = c["measure"]["first"] - 1.0, c["end"] + VERIFY_TAIL
        iso = S.retranscribe_span(wav, t0, t1, model)
        main_n = len(S.words_in(words, t0, t1))
        if main_n and len(iso) < 0.4 * main_n:               # the isolated pass gave up mid-clip
            iso = S.retranscribe_span(wav, t0 - 1.0, t1 + 1.0, model)
        if main_n and len(iso) < 0.4 * main_n:
            c["verified"] = None
            c["note"] = (f"inconclusive: the isolated pass heard {len(iso)} of ~{main_n} words twice "
                         f"running; listen to it")
            continue
        text = S.text_of(iso)
        gram = c["measure"]["gram"].replace(" …", "")
        cnt = text.count(gram)
        c["measure"]["isolated"] = " ".join(w["w"].strip() for w in iso)
        if cnt >= 2:
            c["verified"] = "confirmed"
        else:
            # the isolated pass may phrase it differently; fall back to a fuzzy twice-check
            toks = text.split()
            n = len(gram.split())
            hits = sum(1 for i in range(max(0, len(toks) - n + 1))
                       if _sim(toks[i:i + n], gram.split()) >= 0.75)
            c["verified"] = "confirmed" if hits >= 2 else "not confirmed"
            if c["verified"] == "not confirmed":
                c["confidence"] = "low"
                c["note"] = "the isolated pass does not hear the phrase twice (a transcript seam, not speech)"
    for c in per.get("ORPHAN", []):
        t0, t1 = c["t"] - VERIFY_TAIL, c["end"] + VERIFY_TAIL
        iso = S.retranscribe_span(wav, t0, t1, model)
        inside = [w for w in iso if w["e"] > c["t"] - 0.1 and w["t"] < c["end"] + 0.1]
        real = [w for w in inside if (w.get("p") or 0) >= 0.4]
        c["measure"]["isolated"] = " ".join(w["w"].strip() for w in inside)
        if len(real) >= 2:
            c["verified"] = "confirmed"
            c["confidence"] = "high"
            c["note"] = "speech the full pass dropped -- an abandoned take"
        else:
            c["verified"] = "not confirmed"
            c["confidence"] = "low"
            c["note"] = "energy without words (breath, movement, music, a laugh)"
    return cands


# ---------------------------------------------------------------------------- the report
def build_report(media, mode, words, words_source, db, gaps, joins=(), pieces=None,
                 wav=None, tight=None, source_video=None, verify_model="medium.en",
                 do_verify=True, quiet=False):
    dur = len(db) * S.HOP_S
    sw, fixed = detect_swallowed(words, gaps)
    cands = []
    cands += detect_pauses(gaps, pieces, dur)
    cands += detect_head(fixed, pieces)
    cands += detect_splices(list(joins), pieces)
    cands += sw
    cands += detect_stretched(words)
    cands += detect_repeats(fixed, gaps)
    cands += detect_orphans(db, fixed)
    if tight and joins:
        cands += detect_hard_splices(tight, list(joins))
    if source_video and pieces:
        ref = [(pieces[i]["b"], pieces[i + 1]["a"]) for i in range(len(pieces) - 1)]
        cands += detect_pausejump(source_video, [c for c in cands if c["cls"] == "PAUSE"], pieces,
                                  reference_joins=ref)
    if do_verify and wav:
        verify(cands, wav, fixed, verify_model, quiet)
    pauses = [c for c in cands if c["cls"] == "PAUSE"]
    for c in [c for c in cands if c["cls"] == "SWALLOWED"]:
        twin = next((p for p in pauses if abs(p["t"] - c["t"]) < 0.03 and abs(p["end"] - c["end"]) < 0.03), None)
        if twin:
            twin["note"] = f"inside the word {c['measure']['word']!r}: Whisper swallowed it (fixonsets rule 3)"
            twin["measure"]["word"] = c["measure"]["word"]
            cands.remove(c)
    for c in cands:
        if pieces:
            s, name = to_source(c["t"], pieces)
            c["src"] = s
            c["piece"] = name
    cands.sort(key=lambda c: (c["t"], c["cls"]))
    by = {}
    for c in cands:
        by[c["cls"]] = by.get(c["cls"], 0) + 1
    confirmed = [c for c in cands if c["verified"] == "confirmed"]
    high = [c for c in cands if c["confidence"] == "high" and c["verified"] in ("confirmed", None)
            and c["cls"] not in ("STRETCH", "ORPHAN", "REPEAT")] + confirmed
    return dict(
        junk_report_version=REPORT_VERSION, when=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        mode=mode, media=os.path.abspath(media), sha256=S.sha256(media),
        duration=round(dur, 2), words=len(words), words_source=words_source,
        gaps=dict(threshold_db=round(S.gap_threshold(db), 1), count=len(gaps)),
        speech_level_db=round(S.speech_level(db), 1),
        joins=[round(j, 3) for j in joins], pieces=pieces or [],
        verified=bool(do_verify and wav), verify_model=verify_model if do_verify else None,
        summary=dict(candidates=len(cands), by_class=by, confirmed=len(confirmed),
                     high_unresolved=len([c for c in high if not c.get("resolution")])),
        candidates=cands,
    )


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def print_report(r, limit=None):
    print(f"\nJUNK REPORT {r['junk_report_version']}  {os.path.basename(r['media'])}  [{r['mode']}]")
    print(f"  {r['duration']:.1f} s, {r['words']} words ({r['words_source']}), {r['gaps']['count']} gaps "
          f"below {r['gaps']['threshold_db']} dB, speech level {r['speech_level_db']} dB, "
          f"{len(r['joins'])} joins; verified: {r['verified']}")
    s = r["summary"]
    print(f"  {s['candidates']} candidates {s['by_class']}; {s['confirmed']} confirmed; "
          f"{s['high_unresolved']} high-confidence unresolved\n")
    for c in r["candidates"][:limit]:
        v = {"confirmed": "✔", "not confirmed": "✘", None: " "}[c["verified"]]
        m = {k: v_ for k, v_ in c["measure"].items() if k not in ("isolated",)}
        src = f"  src {mmss(c['src'])}" if c.get("src") is not None else ""
        print(f"  {v} {c['confidence'][:4]:4s} {c['cls']:11s} {mmss(c['t']):>8s}"
              f"{('-' + mmss(c['end'])) if c['end'] else '':>9s}{src}  {m}")
        print(f"                 -> {c['action']}{('  [' + c['note'] + ']') if c['note'] else ''}")


# ---------------------------------------------------------------------------- entry points
def run_delivered(media, words=None, words_path=None, model="small", verify_model="medium.en",
                  do_verify=True, joins=(), pieces=None, quiet=False, amap=None, af=None):
    """Delivered mode: the file's own audio is the timeline."""
    with tempfile.TemporaryDirectory(prefix="cut-junk-") as tmp:
        wav = S.wav16k(media, os.path.join(tmp, "a.wav"), amap, af)
        a = S.pcm(wav)
        db = S.envelope(a)
        gaps = S.gaps_from_envelope(db)
        if words is None:
            if words_path:
                words, src = S.load_words(words_path), f"file:{words_path}"
            else:
                words, src = S.transcribe(media, model, amap, af, quiet=quiet)
        else:
            src = "given"
        return build_report(media, "delivered", words, src, db, gaps, joins, pieces, wav,
                            verify_model=verify_model, do_verify=do_verify, quiet=quiet)


def run_prerender(source, ranges, words_path=None, model="small", verify_model="medium.en",
                  do_verify=True, tight=None, pieces_path=None, quiet=False, amap=None, af=None):
    """Pre-render mode: the cut as its EDL describes it, measured on the source before any render."""
    pieces, joins = pieces_from_ranges(ranges)
    if words_path:
        src_words, src = S.load_words(words_path), f"file:{words_path}"
    else:
        # the roll sidecar's transcript beside the source, if the rolls tool has built one
        side = os.path.join(os.path.splitext(source)[0] + ".roll", "words.json")
        if os.path.exists(side):
            src_words, src = S.load_words(side), f"sidecar:{side}"
        else:
            src_words, src = S.transcribe(source, model, amap, af, quiet=quiet)
    words = map_words_to_output(src_words, pieces)
    with tempfile.TemporaryDirectory(prefix="cut-junk-") as tmp:
        wav = concat_audio(source, pieces, os.path.join(tmp, "cut.wav"), amap, af)
        a = S.pcm(wav)
        db = S.envelope(a)
        gaps = S.gaps_from_envelope(db)
        sub = None
        if pieces_path:                                       # shorts: pieces on the OUTPUT timeline
            d = json.load(open(pieces_path))
            sub, off = [], 0.0
            for s in d if isinstance(d, list) else d.get("pieces", d.get("segments", [])):
                a_, b_ = float(s.get("start", s.get("a"))), float(s.get("end", s.get("b")))
                sub.append(dict(a=a_, b=b_, off=round(off, 3), name=s.get("id", s.get("name", f"{a_:.2f}"))))
                off += b_ - a_
        return build_report(source, "pre-render", words, src, db, gaps, joins, sub or pieces, wav,
                            tight=tight, source_video=source, verify_model=verify_model,
                            do_verify=do_verify, quiet=quiet)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", help="the delivered file, or the source roll in pre-render mode")
    ap.add_argument("--ranges", help="ranges.py / edl.json / tight_cuts.json -> pre-render mode")
    ap.add_argument("--edl", help="alias of --ranges")
    ap.add_argument("--keeps", help="alias of --ranges")
    ap.add_argument("--words", help="a word file for the media (any of the four formats)")
    ap.add_argument("--tight", help="pre-render: the tight cut's picture, for HARD_SPLICE")
    ap.add_argument("--pieces", help="shorts: pieces on the output timeline (segments json)")
    ap.add_argument("--joins", help="delivered mode: json list of join times, or a plan.json")
    ap.add_argument("--model", default="small")
    ap.add_argument("--verify-model", default="medium.en")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--map", help="audio stream map for a multi-mic roll, e.g. 0:a:0")
    ap.add_argument("--af", help="audio filter for a two-mic roll, e.g. pan=mono|c0=c1")
    ap.add_argument("--out", help="junk_report.json path (default beside the media)")
    ap.add_argument("--quiet", action="store_true")
    A = ap.parse_args()
    if not os.path.exists(A.media):
        raise SystemExit(f"not on disk: {A.media}")
    rp = A.ranges or A.edl or A.keeps
    if rp:
        r = run_prerender(A.media, load_ranges(rp), A.words, A.model, A.verify_model,
                          not A.no_verify, A.tight, A.pieces, A.quiet, A.map, A.af)
    else:
        joins = ()
        if A.joins:
            d = json.load(open(A.joins))
            joins = d.get("joins", []) if isinstance(d, dict) else d
        r = run_delivered(A.media, None, A.words, A.model, A.verify_model, not A.no_verify,
                          joins, None, A.quiet, A.map, A.af)
    out = A.out or (os.path.splitext(A.media)[0] + ".junk_report.json")
    json.dump(r, open(out, "w"), indent=1)
    print_report(r)
    print(f"\n  -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
