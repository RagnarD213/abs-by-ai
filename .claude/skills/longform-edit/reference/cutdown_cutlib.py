#!/usr/bin/env python3
"""Cut-down builder for the invest-health variants.

Derives a variant EDL from the FINAL v3 edl.json by SUBTRACTING resolved
deletion intervals, so every v3 decision (ranges, pause-capper, extra splits,
out-overrides, grade, fps) is inherited unchanged.

Cut placement follows /longform-edit Step 3 in full:
  out-edge (cut_a) = last KEPT word's end + 0.08, snapped forward into a measured
      silence (<=0.40s), never across the first DELETED word's onset unless the
      point is already inside a measured silence (trap 6).
  in-edge  (cut_b) = first KEPT word after the deletion, start - 0.12, refined
      when that word is STRETCHED (>0.8s -> Whisper folded a pause into it,
      trap 2), never biting the tail of the last deleted word (trap 3), and NOT
      clamped to a stretched preceding word (trap 4).
  A stretched LAST kept word is admitted on its START and the out-edge snapped
      to the first silence >=0.25s after it (trap 5); if that word ends in a
      fricative the -45 dB boundary is used instead (trap 7).
  Zero-length / degenerate word clusters are REFUSED, never cut through (trap 1).
Every edge that cannot be placed inside a measured silence is FLAGGED, and a
20 ms RMS envelope at -45 dB is profiled for it (trap 8) so the flag can be
judged instead of guessed.
"""
import json, math, struct, subprocess, sys, wave
from pathlib import Path

SRC_DIR = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/"
               "Media/longform-raw/absbyai-0803-shoot/invest-health")
FFMPEG = Path("/Volumes/Extreme/_edit_work/invest-health-cutdowns/bin/ffmpeg")
WAV = SRC_DIR / "C1511.wav"

WORDS = []
for _s in json.load(open(SRC_DIR / "C1511.whisper.json"))["segments"]:
    for _w in _s.get("words", []):
        _t = _w["word"].strip()
        if _t:
            WORDS.append({"t": _t, "s": _w["start"], "e": _w["end"]})
SIL32 = [tuple(x) for x in json.load(open(SRC_DIR / "silences.json"))]

# Only words that SURVIVE the v3 edit can sit either side of a new join — the
# rest are already on the cutting-room floor. Every prev/next lookup uses this
# list, so a deletion that swallows a whole v3 range resolves to the join Dan
# will actually hear.
_V3 = json.load(open(SRC_DIR / "edit" / "edl.json"))["ranges"]
def _kept(w):
    m = 0.5 * (w["s"] + w["e"])
    return any(r["start"] <= m <= r["end"] for r in _V3)
KEPT = [i for i, w in enumerate(WORDS) if _kept(w)]
KEPT_SET = set(KEPT)

# Whole-roll -45 dB silence map. Used ONLY to PLACE an edge (and to report the
# trough it landed in) when -32 dB shows no pause — never promoted to a pass
# criterion, per the skill's trailing-fricative note. Real validation is the
# re-transcription of every new joint from the finished render.
SIL45 = [tuple(x) for x in json.load(open(Path(__file__).resolve().parent / "silences45.json"))]

_sil45_cache = {}
def sil45(a, b):
    """measured -45 dB silences in [a,b] — sees unvoiced trailing fricatives that
    -32 dB cannot (trap 7)."""
    key = (round(a, 1), round(b, 1))
    if key in _sil45_cache:
        return _sil45_cache[key]
    p = subprocess.run([str(FFMPEG), "-v", "info", "-nostdin", "-ss", f"{a:.3f}",
                        "-t", f"{b-a:.3f}", "-i", str(WAV),
                        "-af", "silencedetect=noise=-45dB:d=0.06", "-f", "null", "-"],
                       capture_output=True, text=True)
    out, st = [], None
    import re
    for line in p.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m: st = float(m.group(1))
        m = re.search(r"silence_end:\s*(-?[\d.]+)", line)
        if m and st is not None:
            out.append((a + st, a + float(m.group(1)))); st = None
    if st is not None:
        out.append((a + st, b))
    _sil45_cache[key] = out
    return out

_pcm = None
def _load_pcm():
    global _pcm
    if _pcm is None:
        w = wave.open(str(WAV), "rb")
        assert w.getnchannels() == 1 or True
        n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
        raw = w.readframes(n); w.close()
        sm = struct.unpack(f"<{len(raw)//2}h", raw)
        if ch > 1:
            sm = sm[::ch]
        _pcm = (sm, sr)
    return _pcm

def rms_profile(a, b, step=0.020):
    """20 ms RMS envelope in dBFS across [a,b] (trap 8: find the real trough when
    Whisper reports no gap and silencedetect reports no silence)."""
    sm, sr = _load_pcm()
    i0, i1 = int(a * sr), int(b * sr)
    st = max(1, int(step * sr))
    out = []
    for i in range(i0, i1 - st, st):
        ch = sm[i:i + st]
        v = (sum(x * x for x in ch) / len(ch)) ** 0.5 / 32768 + 1e-9
        out.append((i / sr, 20 * math.log10(v)))
    return out

def in_silence(t, tol=0.08, sils=SIL32):
    return any(a - tol <= t <= b + tol for a, b in sils)

def gap45_between(lo, hi, minw=0.05):
    """widest -45 dB trough fully inside (lo, hi)"""
    c = [(e - s_, s_, e) for (s_, e) in SIL45 if s_ >= lo - 0.02 and e <= hi + 0.02 and e - s_ >= minw]
    return max(c) if c else None

def silence_ends_within(a, b):
    return [e for (s, e) in SIL32 if a <= e <= b]

FRICATIVE_END = ("s", "sh", "f", "th", "ch", "x", "z", "ce", "se")
def ends_fricative(word):
    w = word.lower().strip(".,!?\"'")
    return w.endswith(("s", "f", "z", "x", "sh", "th", "ch", "ce", "se"))

DEGEN = 0.012   # a word this short is a Whisper hallucination boundary

def resolve_cut(a, b, label="", snap=(8, 8)):
    """Delete every word whose MIDPOINT falls in [a,b]; return the cut interval.
    Returns (cut_a, cut_b, info)."""
    dels = [i for i in KEPT if a <= 0.5 * (WORDS[i]["s"] + WORDS[i]["e"]) <= b]
    if not dels:
        raise SystemExit(f"cut {label}: no KEPT words with midpoint in [{a},{b}]")
    k0, k1 = KEPT.index(dels[0]), KEPT.index(dels[-1])
    if k0 == 0 or k1 + 1 >= len(KEPT):
        raise SystemExit(f"cut {label}: deletion touches the ends of the cut")

    # ---- snap both edges to a MEASURED PAUSE, preferring a sentence boundary ----
    # Dan speaks continuously; a cut asked for mid-phrase has no pause to land in
    # and every downstream assertion fails. Shift the edge by up to SNAP kept
    # words to reach a pause, and report the shift so the text change is visible.
    SNAP_H, SNAP_T = snap
    def _sil_after(w):
        if in_silence(w["e"] + 0.06) or any(w["e"] - 0.05 <= st <= w["e"] + 0.45
                                            for st, _e in SIL32):
            return 2
        return 1 if any(w["e"] - 0.06 <= st <= w["e"] + 0.35 for st, _e in SIL45) else 0
    def _sil_before(w):
        if in_silence(w["s"] - 0.10) or any(w["s"] - 0.45 <= en <= w["s"] + 0.05
                                            for _s, en in SIL32):
            return 2
        return 1 if any(w["s"] - 0.35 <= en <= w["s"] + 0.06 for _s, en in SIL45) else 0
    def _sent(t):
        return t.rstrip().endswith((".", "?", "!"))
    best = None
    for c in range(max(1, k0 - SNAP_H), min(k1 + 1, k0 + SNAP_H + 1)):
        pw = WORDS[KEPT[c - 1]]
        # A cut that starts a new SENTENCE is what makes a cut-down read as
        # writing rather than as an edit — and Dan's only reliable pauses are at
        # sentence ends, so this also lands the edge in measured silence.
        sa = _sil_after(pw)
        score = (6 if _sent(pw["t"]) else 0) + sa
        cand = (score, -abs(c - k0), c)
        if best is None or cand > best:
            best = cand
    k0s = best[2]
    best = None
    for c in range(max(k0s, k1 - SNAP_T), min(len(KEPT) - 1, k1 + SNAP_T + 1)):
        nw = WORDS[KEPT[c + 1]]
        sb = _sil_before(nw)
        score = (6 if _sent(WORDS[KEPT[c]]["t"]) else 0) + sb
        cand = (score, -abs(c - k1), c)
        if best is None or cand > best:
            best = cand
    k1s = best[2]

    flags = []
    if k0s != k0 or k1s != k1:
        flags.append(f"snapped to pause: head {k0s-k0:+d} word(s), tail {k1s-k1:+d} word(s)")
    dels = KEPT[k0s:k1s + 1]
    i0, i1 = dels[0], dels[-1]
    prev, nxt = WORDS[KEPT[k0s - 1]], WORDS[KEPT[k1s + 1]]
    first_del, last_del = WORDS[i0], WORDS[i1]

    # trap 1 — degenerate cluster around either edge means the boundary is fiction
    for tag, idx in (("prev", i0 - 1), ("next", i1 + 1)):
        window = WORDS[max(0, idx - 2): idx + 3]
        if sum(1 for w in window if w["e"] - w["s"] <= DEGEN) >= 2:
            flags.append(f"DEGENERATE-CLUSTER at {tag} edge — do not cut here")

    # ---- out edge (after the last kept word before the deletion) ----
    pdur = prev["e"] - prev["s"]
    if pdur > 0.8:
        # trap 5 — a stretched last word's END is fake; admit it on its START and
        # snap to the first measured silence >= 0.25s after that start.
        sils = sil45(prev["s"], min(prev["s"] + 6.0, first_del["s"] + 2.0)) \
            if ends_fricative(prev["t"]) else SIL32
        cands = [s for (s, e) in sils if s >= prev["s"] + 0.25]
        cut_a = (cands[0] + 0.06) if cands else prev["s"] + 0.65
        flags.append(f"stretched last kept word {prev['t']!r} ({pdur:.2f}s)"
                     + (" +fricative -45dB" if ends_fricative(prev['t']) else "")
                     + f" -> out {cut_a:.2f}")
    else:
        cut_a = prev["e"] + 0.08
        if not in_silence(cut_a):
            cands = [s for (s, e) in SIL32 if cut_a - 0.05 <= s <= cut_a + 0.40]
            if cands:
                cut_a = cands[0] + 0.05
        # trap 6 — measured silence outranks Whisper's next-word onset claim
        if not in_silence(cut_a) and cut_a > first_del["s"]:
            cut_a = max(prev["e"], first_del["s"] - 0.01)
        # never clip a trailing fricative that -32dB cannot see (trap 7)
        if ends_fricative(prev["t"]) and cut_a < prev["e"] + 0.02:
            s45 = sil45(max(0, prev["e"] - 0.4), prev["e"] + 0.8)
            c = [s for (s, e) in s45 if s >= prev["e"] - 0.02]
            if c:
                cut_a = max(cut_a, min(c[0] + 0.05, first_del["s"] - 0.01))

    # ---- in edge (the first kept word after the deletion) ----
    ndur = nxt["e"] - nxt["s"]
    cut_b = nxt["s"] - 0.12
    if ndur > 0.8:
        # trap 2 — Whisper folded the pre-resume pause INTO this word
        se = silence_ends_within(nxt["s"], nxt["e"] - 0.1)
        if se:
            cut_b = se[-1] - 0.10
            flags.append(f"stretched first kept word {nxt['t']!r} ({ndur:.2f}s)"
                         f" -> in {cut_b:.2f}")
    # trap 3/4 — never bite the tail of the last DELETED word, but do not clamp
    # to it if it is itself stretched (its end is the next word's onset)
    if (last_del["e"] - last_del["s"]) <= 0.8 and last_del["e"] > cut_b:
        cut_b = last_del["e"] + 0.01

    # trap 8 — no -32 dB silence does not mean no pause. Profile the envelope and
    # place the edge inside the measured -45 dB trough instead of guessing.
    if not in_silence(cut_a):
        g = gap45_between(prev["e"] - 0.12, first_del["s"] + 0.12, minw=0.03)
        if g:
            cut_a = min(max(cut_a, g[1] + 0.02), g[2] - 0.02)
            flags.append(f"OUT edge on a -45dB trough {g[0]*1000:.0f} ms "
                         f"(after {prev['t']!r})")
        else:
            flags.append(f"OUT edge {cut_a:.2f} NO MEASURED PAUSE (after {prev['t']!r})")
    if not in_silence(cut_b):
        g = gap45_between(last_del["e"] - 0.12, nxt["s"] + 0.12, minw=0.03)
        if g:
            cut_b = min(max(cut_b, g[1] + 0.02), g[2] - 0.02)
            flags.append(f"IN edge on a -45dB trough {g[0]*1000:.0f} ms "
                         f"(before {nxt['t']!r})")
        else:
            flags.append(f"IN edge {cut_b:.2f} NO MEASURED PAUSE (before {nxt['t']!r})")
    if cut_b - cut_a < 0.30:
        flags.append(f"cut only {cut_b-cut_a:.2f}s wide")

    _b = " ".join(WORDS[i]["t"] for i in KEPT[max(0, k0s - 9):k0s])
    _a = " ".join(WORDS[i]["t"] for i in KEPT[k1s + 1:k1s + 10])
    info = {
        "label": label, "flags": flags, "join": f"{_b}  ]|[  {_a}",
        "prev": prev["t"], "next": nxt["t"],
        "text": " ".join(WORDS[i]["t"] for i in dels),
        "span": (a, b),
        "len": cut_b - cut_a,
    }
    return cut_a, cut_b, info


# ---------------- EDL subtraction ----------------

ZOOM_VF = "crop=1728:972:96:0,scale=1920:1080:flags=lanczos"
MIN_PIECE = 0.60      # a sliver shorter than this is dropped, not kept

def build_variant(cuts, out_edl, name, protect=(), chip_src=(), verbose=True):
    v3 = json.load(open(SRC_DIR / "edit" / "edl.json"))
    ranges = [dict(r) for r in v3["ranges"]]
    for r in ranges:
        r.pop("vf", None)

    resolved, infos = [], []
    for c in cuts:
        a, b, label = c[0], c[1], c[2]
        ca, cb, info = resolve_cut(a, b, label, snap=(c[3] if len(c) > 3 else (8, 8)))
        for (pa, pb, pname) in protect:
            if ca < pb and cb > pa:
                info["flags"].append(f"OVERLAPS PROTECTED SPAN {pname} ({pa}-{pb})")
        resolved.append((ca, cb, label))
        infos.append(info)

    # Deletions that RESOLVE into each other (typically because a v3 gap sits
    # between them) are merged and re-resolved so the reported join is the real
    # one. Merges are printed, never silent.
    merges = []
    while True:
        resolved.sort()
        for k in range(len(resolved) - 1):
            (a1, b1, l1), (a2, b2, l2) = resolved[k], resolved[k + 1]
            if a2 <= b1 + MIN_PIECE:
                lo = min(c[0] for c in cuts if c[2] in (l1.split("+")[0], l2.split("+")[0]))
                hi = max(c[1] for c in cuts if c[2] in (l1.split("+")[-1], l2.split("+")[-1]))
                lbl = l1 + "+" + l2
                ca, cb, info = resolve_cut(lo, hi, lbl)
                merges.append(f"merged {l1} + {l2} -> {ca:.2f}-{cb:.2f}")
                resolved[k:k + 2] = [(ca, cb, lbl)]
                infos = [i for i in infos if i["label"] not in (l1, l2)] + [info]
                break
        else:
            break
    order = resolved

    # subtract
    dropped = []
    pieces = []
    for r in ranges:
        segs = [(r["start"], r["end"])]
        for (ca, cb, _l) in order:
            new = []
            for (pa, pb) in segs:
                if cb <= pa or ca >= pb:
                    new.append((pa, pb)); continue
                if ca > pa:
                    new.append((pa, min(ca, pb)))
                if cb < pb:
                    new.append((max(cb, pa), pb))
            segs = new
        for k, (pa, pb) in enumerate(segs):
            if pb - pa < MIN_PIECE:
                dropped.append((r["beat"], pa, pb))
                continue
            beat = r["beat"] if len(segs) == 1 else f"{r['beat']}~{k}"
            pieces.append({"source": "C1511", "start": round(pa, 3),
                           "end": round(pb, 3), "beat": beat})

    # zoom parity across the NEW range list
    for i, p in enumerate(pieces):
        if i % 2 == 1:
            p["vf"] = ZOOM_VF

    lost_chips = [t for t in chip_src
                  if not any(r["start"] <= t <= r["end"] for r in pieces)]
    total = sum(p["end"] - p["start"] for p in pieces)
    edl = {"sources": v3["sources"], "grade": v3["grade"], "fps": v3["fps"],
           "ranges": pieces}
    out_edl = Path(out_edl)
    out_edl.parent.mkdir(parents=True, exist_ok=True)
    json.dump(edl, open(out_edl, "w"), indent=1)

    if verbose:
        nflag = 0
        print(f"=== {name}: {len(cuts)} deletions ===")
        infos.sort(key=lambda i: i["span"][0])
        by_label = {i["label"]: i for i in infos}
        for (ca, cb, _l) in order:
            info = by_label[_l]
            print(f"\n[{info['label']}] {ca:8.2f} -> {cb:8.2f}  (-{cb-ca:5.2f}s)")
            print(f"    JOIN: ...{info['join']}...")
            print(f"    del : {info['text'][:220]}")
            for f in info["flags"]:
                nflag += 1
                print(f"    FLAG: {f}")
        for m in merges:
            print("  NOTE:", m)
        print(f"\n{len(pieces)} ranges, {len(dropped)} slivers dropped, {nflag} flags")
        print("chip anchors lost:", lost_chips if lost_chips else "none")
        if dropped:
            for d in dropped:
                print("   sliver:", d)
        print(f"kept {total:.1f}s = {total/60:.2f} min "
              f"(v3 {sum(r['end']-r['start'] for r in v3['ranges']):.1f}s) -> {out_edl}")
    return total, infos
