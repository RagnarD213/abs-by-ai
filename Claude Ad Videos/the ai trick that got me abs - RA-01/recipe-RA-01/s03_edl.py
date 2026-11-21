#!/usr/bin/env python3
"""RA-01 EDL: take spans by PHRASE, edges validated against the envelope, then airtight pause
removal measured on the real 5 ms RMS envelope (ad-edit lesson 20 -- Whisper only names the words).

  DROP=R3B python3 s03_edl.py     drops line L11 for length (plan section 3, first cut listed)

Writes cut.json: the source spans that survive, the tight word list, the seams, the duration.
"""
import json, os, re
FD = 1001/30000
SIL_DB, MINSIL = -40.0, 0.26
# ⚠ MIN_REMOVE IS A JUMP-CUT RULE, NOT A TIDINESS RULE. Removing 67-100 ms of pause buys almost
# nothing and costs a splice, and three of them landed in one tired passage (33.70 / 34.27 / 35.34)
# where the watch-pass judge measured the subject jumping while the framing held. A pause cut that
# saves less than an eighth of a second is not worth a join: the whole class goes away for 0.40 s
# of runtime.
KEEP_TAIL, KEEP_HEAD, MIN_REMOVE = 0.080, 0.130, 0.125
HOOK_SAFE = 2.00
EDGE_SEARCH = 0.45

DROP = set(x for x in os.environ.get("DROP", "").split(",") if x)
wh = json.load(open("tx/c1663.whisper.json"))
WS = [w for s in wh["segments"] for w in s.get("words", [])]
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
SEQ = [norm(w["word"]) for w in WS]
env = json.load(open("env.json")); HOP, DB = env["hop"], env["db"]
dbat = lambda t: DB[int(t/HOP)] if 0 <= int(t/HOP) < len(DB) else -99.0

def find(phrase, after=0.0):
    toks = norm(phrase).split()
    start = next((i for i, w in enumerate(WS) if w["start"] >= after), 0)
    for i in range(start, len(SEQ)-len(toks)+1):
        if SEQ[i:i+len(toks)] == toks:
            return i
    raise KeyError(f"phrase not found after {after}s: {phrase!r}")

def snap_quiet(t, direction):
    """Move the edge to the quietest instant within EDGE_SEARCH -- a range edge must not land on a
    word (website-video lesson 81: every edge validated against a -40 dB envelope)."""
    lo, hi = (t-EDGE_SEARCH, t+0.05) if direction < 0 else (t-0.05, t+EDGE_SEARCH)
    n = int((hi-lo)/HOP)
    best, bv = t, 1e9
    for i in range(max(n, 1)):
        x = lo + i*HOP
        v = dbat(x)
        if v < bv - 0.001:
            bv, best = v, x
    return round(best, 3), round(bv, 1)

SPEC = json.load(open("edl_spec.json"))
raw = []
for r in SPEC["ranges"]:
    if r["name"] in DROP:
        print(f'  {r["name"]:>4}  DROPPED ({r["lines"]})'); continue
    i = find(r["from"], after=r["after"])
    j = find(r["to"], after=WS[i]["start"]) + len(norm(r["to"]).split()) - 1
    raw.append({"name": r["name"], "lines": r["lines"], "a0": WS[i]["start"], "b0": WS[j]["end"],
                "first_word": WS[i]["word"].strip(), "last_word": WS[j]["word"].strip()})
# One shared edge between ranges that are CONTIGUOUS in the source, so a forward snap on one and a
# backward snap on the next can never cross and duplicate audio (they crossed by 0.465 s on the
# first run: R3B's "hit my goal" and R3C's "and you can change").
edges = []
for k, r in enumerate(raw):
    lo = snap_quiet(r["a0"] - 0.12, -1)
    hi = snap_quiet(r["b0"] + 0.12, +1)
    edges.append([lo, hi])
for k in range(len(raw)-1):
    gap = raw[k+1]["a0"] - raw[k]["b0"]
    if gap < 1.20:                      # consecutive in the take: one boundary, in the gap
        a, b = raw[k]["b0"] + 0.02, raw[k+1]["a0"] - 0.02
        n = max(int((b-a)/HOP), 1)
        best, bv = (a+b)/2, 1e9
        for i in range(n):
            x = a + i*HOP
            if dbat(x) < bv: bv, best = dbat(x), x
        edges[k][1] = (round(best, 3), round(bv, 1))
        edges[k+1][0] = (round(best, 3), round(bv, 1))
# ⚠ ROUND 2, R1: THE FILE OPENS ON THE FIRST WORD. Round 1 began with 0.84 s of near-silence
# (-55 to -60 dBFS) over a still card, against an approved reference that speaks from 0.0 s -- the
# hook did not land. The head edge is therefore pulled up to LEAD seconds before the first word,
# whatever the quiet-snap found. The snap still protects every OTHER edge.
# Whisper's word start is not the sound: it put "This" at 26.92 where the envelope does not move
# until 27.185 and the CTC alignment on the finished mix reads 27.30. The head edge is therefore
# set from the ENVELOPE ONSET -- the first sample 15 dB over the local floor, held for 15 ms -- and
# HEAD_SRC lets the one-step CTC correction below pin it exactly.
LEAD = 0.12
_first = raw[0]["a0"]
if os.environ.get("HEAD_SRC"):
    _head = float(os.environ["HEAD_SRC"])
    print(f"  head edge pinned by HEAD_SRC -> {_head:.3f}s")
else:
    _lo = max(0.0, _first - 0.80)
    _floor = sorted(dbat(_lo + i*HOP) for i in range(int(0.50/HOP)))[int(0.25/HOP)]
    _thr = _floor + 15.0
    _onset = None
    for i in range(int((_first - 0.80)/HOP), int((_first + 0.80)/HOP)):
        if all(dbat((i+k)*HOP) > _thr for k in range(3)):
            _onset = i*HOP; break
    if _onset is None:
        _onset = _first
        print("  WARNING: no envelope onset found near the first word; falling back to Whisper's time")
    _head = round(_onset - LEAD, 3)
    print(f"  envelope onset {_onset:.3f}s (floor {_floor:.1f} dB, threshold {_thr:.1f}) "
          f"-> head edge {_head:.3f}s")
if _head > edges[0][0][0]:
    edges[0][0] = (_head, edges[0][0][1])

ranges = []
for k, r in enumerate(raw):
    a, adb = edges[k][0]; b, bdb = edges[k][1]
    assert b > a, (r, a, b)
    ranges.append({"name": r["name"], "lines": r["lines"], "start": round(a, 3), "end": round(b, 3),
                   "first_word": r["first_word"], "last_word": r["last_word"],
                   "edge_db": [adb, bdb]})
for k in range(len(ranges)-1):
    assert ranges[k+1]["start"] >= ranges[k]["end"] - 1e-6, (ranges[k], ranges[k+1])
rw, off = [], 0.0
for ri, rg in enumerate(ranges):
    for w in WS:
        # a word belongs to this range only if MOST of it is inside: Whisper timed the discarded
        # take-1 "It" at 40.90 against a range edge of 40.91, and a 10 ms sliver put a word in the
        # cut that the audio does not contain ("It it inspired me...").
        ov = min(w["end"], rg["end"]) - max(w["start"], rg["start"])
        keep = ov >= 0.6*max(w["end"]-w["start"], 1e-6) and ov > 0.02
        # ⚠ EXCEPT THE WORD THE HEAD EDGE IS CUT INTO. R1's head trim lands inside Whisper's span
        # for "This" -- Whisper starts it at 26.92 where the envelope does not move until 27.185
        # and the CTC alignment reads 27.30 -- so the 60 % test threw the first word of the ad out
        # of the word list while the audio still said it. The first range's opening word is kept
        # whenever any of it survives; its time is clamped to the edge and the CTC pass re-times it.
        if ri == 0 and not keep and ov > 0.0 and w["start"] < rg["start"] < w["end"]:
            keep = True
            print(f"  head-edge word kept: {w['word'].strip()!r} "
                  f"({w['start']:.3f}-{w['end']:.3f} vs edge {rg['start']:.3f})")
        if keep:
            rw.append({"t": round(off + max(w["start"], rg["start"]) - rg["start"], 3),
                       "e": round(off + min(w["end"], rg["end"]) - rg["start"], 3), "w": w["word"]})
    off += rg["end"] - rg["start"]
SPAN_END = round(off, 3)

DBC = []
for rg in ranges:
    DBC.extend(DB[int(rg["start"]/HOP):int(rg["end"]/HOP)])
runs, cur = [], None
for i in range(min(int(SPAN_END/HOP), len(DBC))):
    if DBC[i] < SIL_DB: cur = (cur[0], i) if cur else (i, i)
    else:
        if cur: runs.append(cur); cur = None
if cur: runs.append(cur)
sil = [(a*HOP, (b+1)*HOP) for a, b in runs if (b-a+1)*HOP >= MINSIL]

frames = lambda t: round(t/FD)
snapf = lambda t: round(frames(t)*FD, 6)

# real seams: only where consecutive kept ranges are NOT contiguous in the source
seams_cat, off = [], 0.0
for k, rg in enumerate(ranges[:-1]):
    off += rg["end"] - rg["start"]
    if abs(ranges[k+1]["start"] - rg["end"]) > 0.05:
        seams_cat.append((round(off, 3), rg["name"] + "|" + ranges[k+1]["name"]))

# Pause cuts we refuse to make. The 'pounds' -> 'this' cut lands inside the 0.43 s of Dan that
# separates the BEFORE picture from the AFTER pictures -- too short to carry a level change, so the
# splice reads as a naked jump (the watch-pass judge called it the worst in the file). Keeping the
# pause is the fix: it costs 0.20 s of runtime and makes that beat one continuous shot.
PROTECT = [("pounds", "this")]
# ⚠ ROUND 2, R7: NO PAUSE CUT AFTER THE LAST WORD. Round 1's last splice sat at 56.056 s, 0.21 s
# after "below.", inside the tail the end hold replaces anyway. It bought 0.133 s and cost the one
# join in the file that measured as a discontinuity: the bed was still releasing from the ducker
# (-57 dBFS) when the splice brought in a louder stretch of room tone, so the level stepped to
# -38.6 dBFS in 40 ms (the reviewer's D10). Removing the cut removes the step; the ducker's own
# 420 ms release is then the only thing happening there.
LAST_WORD_E = max(w["e"] for w in rw)
cuts = []
for s0, s1 in sil:
    if s0 >= LAST_WORD_E - 0.02:
        print(f"  tail protected: no pause cut after the last word ({s0:.3f}s)")
        continue
    prev_w = max((w for w in rw if w["e"] <= s0+0.12), key=lambda w: w["e"], default=None)
    next_w = min((w for w in rw if w["t"] >= s1-0.02), key=lambda w: w["t"], default=None)
    ci, co = snapf(s0+KEEP_TAIL), snapf(s1-KEEP_HEAD)
    if co - ci < MIN_REMOVE or ci <= HOOK_SAFE:
        continue
    aw = prev_w["w"].strip().strip(".,!?") if prev_w else "?"
    bw = next_w["w"].strip().strip(".,!?") if next_w else "?"
    if (aw, bw) in PROTECT:
        print(f"  protected: the pause between {aw!r} and {bw!r} is kept ({co-ci:.3f}s)")
        continue
    cuts.append({"in": ci, "out": co, "rm": round(co-ci, 3),
                 "a": prev_w["w"].strip() if prev_w else "?",
                 "b": next_w["w"].strip() if next_w else "?"})
keeps, prev = [], 0.0
for c in cuts:
    keeps.append([round(prev, 6), c["in"]]); prev = c["out"]
keeps.append([round(prev, 6), snapf(SPAN_END)])
keeps = [k for k in keeps if k[1]-k[0] > 0.05]
dur = sum(b-a for a, b in keeps)

def to_tight(t):
    acc = 0.0
    for a, b in keeps:
        if t < a: return round(acc, 3)
        if t <= b: return round(acc + t - a, 3)
        acc += b - a
    return round(acc, 3)

bounds, off = [], 0.0
for rg in ranges:
    bounds.append((off, off + rg["end"]-rg["start"], rg["start"], rg["name"]))
    off += rg["end"] - rg["start"]
pieces = []
for a, b in keeps:
    x = a
    while x < b - 1e-6:
        for c0, c1, s0, nm in bounds:
            if c0 - 1e-6 <= x < c1 - 1e-6:
                y = min(b, c1)
                pieces.append({"src_in": round(s0 + (x-c0), 6), "src_out": round(s0 + (y-c0), 6),
                               "t_in": to_tight(x), "t_out": round(to_tight(x) + (y-x), 6),
                               "range": nm})
                x = y; break
        else:
            x = b
words_tight = [{"t": to_tight(w["t"]), "e": to_tight(w["e"]), "w": w["w"]} for w in rw]
out = {"ranges": ranges, "dropped": sorted(DROP), "keeps": keeps, "pieces": pieces, "cuts": cuts,
       "seams": [{"t": to_tight(t), "what": w} for t, w in seams_cat],
       "dur": round(dur, 3), "span_end": SPAN_END, "words": words_tight}
json.dump(out, open("cut.json", "w"), indent=1)
print(f"\nspan {SPAN_END:.2f}s -> tight {dur:.2f}s   {len(cuts)} pause cuts, "
      f"{sum(c['rm'] for c in cuts):.2f}s removed")
print(f"{len(rw)} words, {len(rw)/dur*60:.0f} wpm, {len(pieces)} source pieces, "
      f"seams {[s['t'] for s in out['seams']]}")
print(f"HEADROOM to the 59.00 s ceiling before the end hold: {59.00-dur:.2f}s")
