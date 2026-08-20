#!/usr/bin/env python3
"""Generic longform EDL builder (longform-edit Step 3).
  in-point  = first word's start - 0.12 pad, clamped to previous word's end
  out-point = last word's end + 0.08, may snap FORWARD into silence (<=0.40s),
              never across the next word's onset
  Stretched first word (>0.8s) => onset refined to last silence_end inside it - 0.10
  Every edge asserted inside (or within 0.08s of) a measured silence; else FLAG.
usage: build_edl.py <slug> <SRC_BASENAME> <ranges.py>
"""
import json, sys, importlib.util
from pathlib import Path

slug, src, ranges_file = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = Path(f"/Volumes/Seagate 4TB/_edit_work/{slug}")
spec = importlib.util.spec_from_file_location("r", ranges_file)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
RANGES = mod.RANGES
GRADE = mod.GRADE
SRC_PATH = mod.SRC_PATH

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
for (a, b, beat) in RANGES:
    first = next((w for w in words if w["start"] >= a - 0.05), None)
    # A STRETCHED LAST WORD (>0.8s) has an unreliable 'end' -- Whisper folds the
    # following pause into it, so an end-based filter drops the word entirely and
    # the out-point lands on the word before, clipping real speech. Admit it on
    # its START instead; the out-point is then snapped to the first REAL silence.
    lasts = [w for w in words
             if w["end"] > a and (w["end"] <= b + 0.05
                                  or (w["end"] - w["start"] > 0.8 and w["start"] <= b + 0.05))]
    last = lasts[-1] if lasts else None
    if not first or not last: sys.exit(f"range {beat}: no words found")
    wdur = first["end"] - first["start"]
    in_t = first["start"] - 0.12
    if wdur > 0.8:
        se = silence_ends_within(first["start"], first["end"] - 0.1)
        if se:
            in_t = se[-1] - 0.10
            flags.append(f"{beat}: stretched first word {first['text']!r} ({wdur:.2f}s) -> onset {in_t:.2f}")
    # Clamp to the previous word's end so the pad never bites its tail -- but
    # SKIP a stretched previous word (>0.8s): Whisper folds the pause into it,
    # so its 'end' is the next word's onset and clamping there clips 10-20ms
    # off the head of this beat's first word.
    prevs = [w for w in words if w["end"] <= first["start"] + 0.01 and w["end"] > first["start"] - 5]
    if prevs and prevs[-1]["end"] > in_t and (prevs[-1]["end"] - prevs[-1]["start"]) <= 0.8:
        in_t = prevs[-1]["end"] + 0.01
    out_t = last["end"] + 0.08
    if last["end"] - last["start"] > 0.8:
        cands = [st for (st, e) in silences if st >= last["start"] + 0.15 and e - st >= 0.25]
        out_t = cands[0] + 0.05 if cands else last["start"] + 0.60
        flags.append(f"{beat}: stretched last word {last['text']!r} -> out snapped to {out_t:.2f}")
    snapped = False
    if not in_silence(out_t):
        cands = [s for (s, e) in silences if out_t - 0.05 <= s <= out_t + 0.40]
        if cands:
            out_t = cands[0] + 0.05
            snapped = True
    # Clamp so the out-point never crosses the next (cut) word's onset -- BUT a
    # measured silence outranks Whisper's claimed onset. Whisper routinely starts
    # the next word early (it has no silence model), and clamping to that claim
    # chops the tail off the last KEPT word. If we snapped into a real measured
    # silence, that silence is the ground truth and the clamp is skipped.
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
    print(f"{beat:24s} {in_t:8.2f}-{out_t:8.2f} ({out_t-in_t:6.2f}s) | {head} … {tail}")

# An adjacent pair with almost no source removed is not an edit, it is an
# artificial split -- render.py's 30ms fade-out then fade-in lands mid-speech and
# dips the audio. max-jump QC cannot see it (a dip is not a step), so assert here.
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
