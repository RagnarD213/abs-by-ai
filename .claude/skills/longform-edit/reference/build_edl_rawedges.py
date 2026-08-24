#!/usr/bin/env python3
"""Spray-tan REV1 EDL builder = build_edl_generic.py + per-range edge overrides.

Ranges may be (a, b, beat) or (a, b, beat, mode) with mode in
  "rawin"  -- use `a` literally as the in-point  (word snapping skipped)
  "rawout" -- use `b` literally as the out-point (word snapping skipped)
  "raw"    -- both
Needed by rev1 because both of Dan's cut fixes land at edges where Whisper's
word boundaries are unusable: a STRETCHED word ("you", 1.60s) at one, and a
next-word onset claimed 0.29s before the measured silence ends at the other.
Everything else is byte-identical to the generic builder.
usage: build_edl_rev1.py <slug> <SRC_BASENAME> <ranges.py>
"""
import json, sys, importlib.util
from pathlib import Path

slug, src, ranges_file = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
spec = importlib.util.spec_from_file_location("r", ranges_file)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
RANGES, GRADE, SRC_PATH = mod.RANGES, mod.GRADE, mod.SRC_PATH

words = []
for s in json.load(open(BASE / f"{src}.whisper.json"))["segments"]:
    for w in s.get("words", []):
        words.append({"start": w["start"], "end": w["end"], "text": w["word"].strip()})
silences = json.load(open(BASE / "silences.json"))

def in_silence(t, tol=0.08):
    return any(a - tol <= t <= b + tol for a, b in silences)
def silence_ends_within(a, b):
    return [e for (s, e) in silences if a <= e <= b]

out, flags, prev_out = [], [], -1.0
for row in RANGES:
    a, b, beat = row[0], row[1], row[2]
    mode = row[3] if len(row) > 3 else ""
    raw_in  = mode in ("rawin", "raw")
    raw_out = mode in ("rawout", "raw")
    first = next((w for w in words if w["start"] >= a - 0.05), None)
    lasts = [w for w in words
             if w["end"] > a and (w["end"] <= b + 0.05
                                  or (w["end"] - w["start"] > 0.8 and w["start"] <= b + 0.05))]
    last = lasts[-1] if lasts else None
    if not first or not last: sys.exit(f"range {beat}: no words found")

    if raw_in:
        in_t = a
    else:
        wdur = first["end"] - first["start"]
        in_t = first["start"] - 0.12
        if wdur > 0.8:
            se = silence_ends_within(first["start"], first["end"] - 0.1)
            if se:
                in_t = se[-1] - 0.10
                flags.append(f"{beat}: stretched first word {first['text']!r} ({wdur:.2f}s) -> onset {in_t:.2f}")
        prevs = [w for w in words if w["end"] <= first["start"] + 0.01 and w["end"] > first["start"] - 5]
        if prevs and prevs[-1]["end"] > in_t and (prevs[-1]["end"] - prevs[-1]["start"]) <= 0.8:
            in_t = prevs[-1]["end"] + 0.01

    snapped = False
    if raw_out:
        out_t = b
    else:
        out_t = last["end"] + 0.08
        if last["end"] - last["start"] > 0.8:
            cands = [st for (st, e) in silences if st >= last["start"] + 0.15 and e - st >= 0.25]
            out_t = cands[0] + 0.05 if cands else last["start"] + 0.60
            flags.append(f"{beat}: stretched last word {last['text']!r} -> out snapped to {out_t:.2f}")
        if not in_silence(out_t):
            cands = [s for (s, e) in silences if out_t - 0.05 <= s <= out_t + 0.40]
            if cands:
                out_t = cands[0] + 0.05
                snapped = True
        nxt = next((w for w in words if w["start"] >= last["end"] - 0.01), None)
        if nxt and out_t > nxt["start"] and not snapped and not in_silence(out_t):
            out_t = max(last["end"], nxt["start"] - 0.01)

    if not in_silence(in_t):  flags.append(f"{beat}: IN  {in_t:.2f} not in silence (word {first['text']!r})")
    if not in_silence(out_t): flags.append(f"{beat}: OUT {out_t:.2f} not in silence (word {last['text']!r})")
    if in_t <= prev_out:      flags.append(f"{beat}: OVERLAP ({in_t:.2f} <= {prev_out:.2f})")
    prev_out = out_t
    out.append({"source": src, "start": round(in_t, 3), "end": round(out_t, 3), "beat": beat})
    head = " ".join(w["text"] for w in words if in_t <= w["start"] < in_t + 3.2)[:64]
    tail = " ".join(w["text"] for w in words if out_t - 3.2 < w["end"] <= out_t)[-58:]
    tag = f" [{mode}]" if mode else ""
    print(f"{beat:24s} {in_t:8.2f}-{out_t:8.2f} ({out_t-in_t:6.2f}s){tag} | {head} … {tail}")

for x, y in zip(out, out[1:]):
    if y["start"] - x["end"] < 0.20:
        flags.append(f"ARTIFICIAL SPLIT: {x['beat']} -> {y['beat']} removes only "
                     f"{y['start']-x['end']:.3f}s -- merge these two ranges")

total = sum(r["end"] - r["start"] for r in out)
print(f"\n{len(out)} ranges  kept {total:.1f}s = {total/60:.1f} min")
print("FLAGS:" if flags else "FLAGS: none")
for f in flags: print("  -", f)
json.dump({"sources": {src: SRC_PATH}, "fps": "30000/1001", "grade": GRADE, "ranges": out},
          open(BASE / "edl.json", "w"), indent=1)
print(f"\nwrote {BASE/'edl.json'}")
