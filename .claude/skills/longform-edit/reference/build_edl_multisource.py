#!/usr/bin/env python3
"""Multi-source longform EDL builder (longform-edit Step 3), for a video cut from
several rolls. Same six cut-placement rules as build_edl_generic.py; words and
silences are loaded PER SOURCE and every rule is applied inside that source.
usage: build_edl.py <slug> <ranges.py>
ranges.py must define RANGES = [(source, start, end, beat), ...], SOURCES = {name: path},
GRADES = {name: filter}
"""
import json, sys, importlib.util
from pathlib import Path

slug, ranges_file = sys.argv[1], sys.argv[2]
BASE = Path(f"/Volumes/Seagate 4TB/_edit_work/{slug}")
spec = importlib.util.spec_from_file_location("r", ranges_file)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
RANGES, SOURCES, GRADES = mod.RANGES, mod.SOURCES, mod.GRADES

WORDS, SIL = {}, {}
for s in SOURCES:
    ws = []
    for seg in json.load(open(BASE / f"{s}.whisper.json"))["segments"]:
        for w in seg.get("words", []):
            ws.append({"start": w["start"], "end": w["end"], "text": w["word"].strip()})
    WORDS[s] = ws
    SIL[s] = json.load(open(BASE / f"sil_{s}.json"))

def in_silence(s, t, tol=0.08):
    return any(a - tol <= t <= b + tol for a, b in SIL[s])
def silence_ends_within(s, a, b):
    return [e for (st, e) in SIL[s] if a <= e <= b]

out, flags = [], []
prev_out = {}
for R in RANGES:
    s, a, b, beat = R[0], R[1], R[2], R[3]
    mode = R[4] if len(R) > 4 else ""
    words, sils = WORDS[s], SIL[s]
    # "rawin"/"rawout"/"raw": use the literal timecode instead of word-snapping.
    # Required for a SILENT range (a live workout set) -- there are no words to
    # snap to, so the resolver would reach forward to the next spoken word and
    # delete the whole set.
    if mode == "raw":
        out.append({"source": s, "start": round(a,3), "end": round(b,3),
                    "beat": beat, "grade": GRADES[s]})
        if not in_silence(s, a): flags.append(f"{beat}: RAW IN {a:.2f} not in silence")
        if not in_silence(s, b): flags.append(f"{beat}: RAW OUT {b:.2f} not in silence")
        prev_out[s] = b
        print(f"{s} {beat:26s} {a:8.2f}-{b:8.2f} ({b-a:6.2f}s) | [raw]")
        continue
    first = next((w for w in words if w["start"] >= a - 0.05), None)
    lasts = [w for w in words
             if w["end"] > a and (w["end"] <= b + 0.05
                                  or (w["end"] - w["start"] > 0.8 and w["start"] <= b + 0.05))]
    last = lasts[-1] if lasts else None
    if not first or not last: sys.exit(f"range {beat}: no words found in {s}")
    if mode == "rawin":
        in_t = a
        if not in_silence(s, in_t):
            flags.append(f"{beat}: RAW IN {in_t:.2f} not in silence")
    else:
        wdur = first["end"] - first["start"]
        in_t = first["start"] - 0.12
        if wdur > 0.8:
            se = silence_ends_within(s, first["start"], first["end"] - 0.1)
            if se:
                in_t = se[-1] - 0.10
                flags.append(f"{beat}: stretched first word {first['text']!r} ({wdur:.2f}s) -> onset {in_t:.2f}")
        prevs = [w for w in words if w["end"] <= first["start"] + 0.01 and w["end"] > first["start"] - 5]
        if prevs and prevs[-1]["end"] > in_t and (prevs[-1]["end"] - prevs[-1]["start"]) <= 0.8:
            in_t = prevs[-1]["end"] + 0.01
    if mode == "rawout":
        out_t = b
        if not in_silence(s, out_t):
            flags.append(f"{beat}: RAW OUT {out_t:.2f} not in silence")
        out.append({"source": s, "start": round(in_t,3), "end": round(out_t,3),
                    "beat": beat, "grade": GRADES[s]})
        prev_out[s] = out_t
        head = " ".join(w["text"] for w in words if in_t <= w["start"] < in_t + 3.2)[:60]
        print(f"{s} {beat:26s} {in_t:8.2f}-{out_t:8.2f} ({out_t-in_t:6.2f}s) | {head} … [rawout]")
        continue
    out_t = last["end"] + 0.08
    if last["end"] - last["start"] > 0.8:
        cands = [st for (st, e) in sils if st >= last["start"] + 0.15 and e - st >= 0.25]
        out_t = cands[0] + 0.05 if cands else last["start"] + 0.60
        flags.append(f"{beat}: stretched last word {last['text']!r} -> out snapped to {out_t:.2f}")
    snapped = False
    if not in_silence(s, out_t):
        cands = [st for (st, e) in sils if out_t - 0.05 <= st <= out_t + 0.40]
        if cands:
            out_t = cands[0] + 0.05; snapped = True
    nxt = next((w for w in words if w["start"] >= last["end"] - 0.01), None)
    if nxt and out_t > nxt["start"] and not snapped and not in_silence(s, out_t):
        out_t = max(last["end"], nxt["start"] - 0.01)
    if not in_silence(s, in_t):  flags.append(f"{beat}: IN  {in_t:.2f} not in silence (word {first['text']!r})")
    if not in_silence(s, out_t): flags.append(f"{beat}: OUT {out_t:.2f} not in silence (word {last['text']!r})")
    if s in prev_out and in_t <= prev_out[s]:
        flags.append(f"{beat}: OVERLAP in {s} ({in_t:.2f} <= {prev_out[s]:.2f})")
    prev_out[s] = out_t
    out.append({"source": s, "start": round(in_t, 3), "end": round(out_t, 3),
                "beat": beat, "grade": GRADES[s]})
    head = " ".join(w["text"] for w in words if in_t <= w["start"] < in_t + 3.2)[:60]
    tail = " ".join(w["text"] for w in words if out_t - 3.2 < w["end"] <= out_t)[-52:]
    print(f"{s} {beat:26s} {in_t:8.2f}-{out_t:8.2f} ({out_t-in_t:6.2f}s) | {head} … {tail}")

for x, y in zip(out, out[1:]):
    if x["source"] == y["source"] and y["start"] - x["end"] < 0.20:
        flags.append(f"ARTIFICIAL SPLIT: {x['beat']} -> {y['beat']} removes only "
                     f"{y['start']-x['end']:.3f}s -- merge these two ranges")

total = sum(r["end"] - r["start"] for r in out)
print(f"\n{len(out)} ranges  kept {total:.1f}s = {total/60:.1f} min")
print("FLAGS:" if flags else "FLAGS: none")
for f in flags: print("  -", f)
json.dump({"sources": SOURCES, "fps": "30000/1001", "ranges": out},
          open(BASE / "edl.json", "w"), indent=1)
print(f"\nwrote {BASE/'edl.json'}")
