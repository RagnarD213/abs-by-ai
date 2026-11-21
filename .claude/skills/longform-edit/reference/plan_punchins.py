#!/usr/bin/env python3
"""THE CUT PLAN: what to keep, and how each kept piece is framed.

Two separate problems, and the measurement below is what separates them.

  * The TALKING is not slow. Measured per beat, Dan reads at 194-239 wpm; the whole
    programme only averages 151 wpm because the three live sets drag it down. The
    reference cut runs 189 wpm. So general pause-removal is worth ~20 s here, not the
    ~95 s a whole-runtime wpm figure implies -- chasing that number by cutting the
    talking further would make him sound breathless and would not be an improvement.
  * The THREE LIVE SETS are 178 s of near-silent rollouts and hold 158 s of this
    video's 205 s of dead air. Shortening them is the entire runtime story. Each set
    is cut to three chunks: open wide on real reps, cut to a punch-in for the middle,
    cut back for the finish -- so the shortening reads as coverage rather than as a
    trim. Every set join lands on a FRAMING CHANGE for that reason.

Framing: the whole nine minutes is one locked wide shot in which Dan is 18-56% of the
frame width, which is why the delivered cut scene-detects as ONE cut. Every kept piece
gets a crop level (1.00 / 0.86 / 0.74 of frame width) centred on the tracked subject,
and the level changes at scheduled intervals and at every join big enough to see.
0.74 is the floor: measured on a torso crop, sharpness falls 124 -> 34 going from
1.00 to 0.74 and to 21 at 0.62, and 0.62 also cuts his feet off during rollouts.
"""
import json
import numpy as np

FD        = 1001 / 30000
TOTAL     = 538.271
SIL_DB    = -40.0        # our voice floor is p10 -49 dB, speech p50 -29 dB
MINSIL    = 0.24
KEEP_TAIL = 0.060        # breath left after the last word of a phrase
KEEP_HEAD = 0.090        # run-up before the next word
MIN_REMOVE= 0.060
HOOK_SAFE = 2.00

# The three live sets, cut to three chunks each. Boundaries sit in silence between
# reps; each one becomes a framing change so the body being in a different position
# across the join reads as a second camera, not as a splice.
SET_CHUNKS = {
 "set-1": [(305.805, 320.60), (338.00, 346.00), (362.50, 374.541)],
 "set-2": [(374.541, 384.80), (400.00, 407.00), (419.50, 427.193)],
 "set-3": [(443.143, 453.60), (468.00, 475.00), (489.50, 500.333)],
}
SET_SPANS = [(305.805, 374.541), (374.541, 427.193), (443.143, 500.333)]

# Deliberate silences that are CONTENT, not dead air. ranges.py keeps the 6.2 s
# silent demo on purpose -- Dan is showing the correct slow pace with no commentary.
# Trimmed, not removed.
PROTECT = [(196.27, 202.45, 3.5)]     # (a, b, keep_seconds)

CROPS = [1.00, 0.86, 0.74]

def frames(t): return round(t / FD)
def snapf(t):  return round(frames(t) * FD, 6)

def silences(db, hop):
    runs, cur = [], None
    for i, v in enumerate(db):
        if v < SIL_DB: cur = (cur[0], i) if cur else (i, i)
        else:
            if cur: runs.append(cur); cur = None
    if cur: runs.append(cur)
    return [(a*hop, (b+1)*hop) for a, b in runs if (b-a+1)*hop >= MINSIL]

def in_span(t, spans): return any(a <= t < b for a, b in spans)


def word_guard(cuts, words, pre=0.055, post=0.075):
    """Pull every cut inside the gap BETWEEN two spoken words.

    A -40 dB envelope cannot see a quietly-spoken function word. Left unguarded this
    plan removed 20 real words -- "But", "So,", "Second", "Remember," -- and clipped 3
    more, because an unstressed monosyllable at the head of a sentence sits under the
    same threshold as room tone. The envelope decides WHERE a pause is; the word
    timings decide how far into it a cut may reach.
    """
    ends   = sorted(w["e"] for w in words)
    starts = sorted(w["t"] for w in words)
    import bisect
    out = []
    for ci, co in cuts:
        i = bisect.bisect_right(ends, co)              # last word ending before the cut out
        prev_end = ends[i-1] if i else 0.0
        j = bisect.bisect_left(starts, ci)             # first word starting after the cut in
        next_start = starts[j] if j < len(starts) else 1e9
        a = max(ci, prev_end + pre)
        b = min(co, next_start - post)
        if b - a >= MIN_REMOVE: out.append((snapf(a), snapf(b)))
    return out

def build():
    env = json.load(open("audio/env.json"))
    db, hop = np.array(env["db"]), env["hop"]
    sil = silences(db, hop)

    cuts = []
    for s0, s1 in sil:
        if in_span(s0, SET_SPANS) or in_span(s1, SET_SPANS): continue
        ci, co = s0 + KEEP_TAIL, s1 - KEEP_HEAD
        for pa, pb, keep in PROTECT:                 # trim, never remove
            if pa - 0.6 <= s0 <= pb:
                co = min(co, ci + keep)
        if co - ci < MIN_REMOVE: continue
        if ci <= HOOK_SAFE: continue
        cuts.append((snapf(ci), snapf(co)))
    import timeline as T
    cuts = word_guard(cuts, T.WORDS)
    # the set trims are placed in measured silence between reps and must not be
    # word-guarded away -- there are no words there to protect
    for name, chunks in SET_CHUNKS.items():
        for (_, b), (c, _) in zip(chunks, chunks[1:]):
            cuts.append((snapf(b), snapf(c)))
    cuts.sort()

    keeps, prev = [], 0.0
    for ci, co in cuts:
        if ci > prev: keeps.append([round(prev, 6), ci])
        prev = max(prev, co)
    keeps.append([round(prev, 6), snapf(TOTAL)])
    keeps = [k for k in keeps if k[1] - k[0] > 0.05]
    removed = TOTAL - sum(b - a for a, b in keeps)
    return keeps, cuts, removed

def split_long(keeps, db, hop, target=7.0):
    """Split kept pieces longer than ~8 s so the framing can change mid-sentence.

    Nothing is removed at these splits -- the audio runs straight through -- so they are
    pure punch-in cuts, which is how the reference edit gets a cut every 7.7 s out of a
    single locked camera. Each split is nudged to the quietest 40 ms inside a +/-0.9 s
    window so it lands between words rather than through one.
    """
    out = []
    for a, b in keeps:
        d = b - a
        if d <= target * 1.25:
            out.append([a, b]); continue
        n = max(2, int(round(d / target)))
        prev = a
        for i in range(1, n):
            t = a + d * i / n
            lo, hi = int((t - 0.9)/hop), int((t + 0.9)/hop)
            lo, hi = max(0, lo), min(len(db)-1, hi)
            if hi > lo:
                w = 8                                   # 40 ms window
                q = [(db[j:j+w].mean(), j) for j in range(lo, hi-w)]
                t = (min(q)[1] + w/2) * hop
            t = snapf(t)
            if t - prev > 1.2 and b - t > 1.2:
                out.append([prev, t]); prev = t
        out.append([prev, b])
    return out


def frame_keeps(keeps):
    """Assign a crop level to every kept piece.

    A pause removal under 0.5 s barely moves the body on a locked shot and needs no
    coverage; anything bigger, and every set join, changes framing. On top of that a
    change is forced every ~7 s so the shot is never static for long -- that cadence is
    the reference cut's (54 cuts in 418 s = one every 7.7 s).
    """
    S = np.load("subject.npy")
    out, level, since, i, cur = [], 0, 0.0, 0, None
    for k, (a, b) in enumerate(keeps):
        gap = a - keeps[k-1][1] if k else 0.0
        change = k > 0 and (gap >= 0.5 or gap <= 0.001 or since >= 7.0)
        if change:
            level = (level + 1) % 3 if (i % 3) else (level + 2) % 3   # never repeat
            i += 1; since = 0.0
        since += b - a
        # subject box over this piece: use the widest it gets, so a rollout that
        # extends across the frame is never cropped through
        lo, hi = int(a*2), max(int(a*2)+1, int(b*2))
        box = S[lo:hi] if hi <= len(S) else S[lo:]
        if not len(box): box = S[min(lo, len(S)-1):min(lo, len(S)-1)+1]
        x0, y0, x1, y1 = box[:,0].min(), box[:,1].min(), box[:,2].max(), box[:,3].max()
        cx, cy = (x0+x1)/2, (y0+y1)/2
        need = (x1 - x0) + 0.10
        cw = CROPS[level]
        while cw < need and cw < 1.0:                  # never crop through him
            cw = CROPS[max(0, CROPS.index(cw) - 1)]
            if cw == 1.00: break
        if change or cur is None:
            cur = {"crop": round(cw, 3), "cx": round(float(cx), 4), "cy": round(float(cy), 4)}
        elif cw > cur["crop"]:
            cur = {**cur, "crop": round(cw, 3)}    # only ever widen mid-shot, never jump tighter
        out.append({"a": a, "b": b, **cur, "gap": round(gap, 3), "new_shot": bool(change or k == 0)})
    return out

if __name__ == "__main__":
    keeps, cuts, removed = build()
    env = json.load(open("audio/env.json"))
    keeps = split_long(keeps, np.array(env["db"]), env["hop"])
    fk = frame_keeps(keeps)
    dur = sum(b - a for a, b in keeps)
    W = json.load(open("words.json")) if False else None
    import timeline as T
    words = [w for w in T.WORDS]
    # how many words survive
    def kept(t):
        for a, b in keeps:
            if a <= t < b: return True
        return False
    nw = sum(1 for w in words if kept(w["t"]))
    print(f"{len(cuts)} cuts remove {removed:.1f}s -> {dur:.2f}s ({int(dur//60)}:{dur%60:05.2f})")
    print(f"{nw} of {len(words)} words survive   {nw/dur*60:.0f} wpm   "
          f"(reference cut 189 wpm, 418.1 s)")
    lv = {}
    for f in fk: lv[f["crop"]] = lv.get(f["crop"], 0) + f["b"] - f["a"]
    changes = sum(1 for a, b in zip(fk, fk[1:]) if a["crop"] != b["crop"])
    print(f"{len(fk)} kept pieces, {changes} framing changes "
          f"({changes/(dur/60):.1f}/min; reference cut 7.7/min)")
    print("  time per crop level: " + "  ".join(f"{k:.2f}={v:.0f}s" for k, v in sorted(lv.items())))
    json.dump({"keeps": keeps, "framed": fk, "dur": round(dur, 3)},
              open("plan.json", "w"), indent=1)
    print("plan.json written")
