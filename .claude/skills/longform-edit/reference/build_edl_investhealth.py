#!/usr/bin/env python3
"""Build the EDL for the 'Why You Should Invest More In Your Health' cut (C1511).

Rules (longform-edit skill, Step 3):
  in-point  = first word's start - 0.12s pad
  out-point = last word's end + 0.08s
  Each edge is then ASSERTED to sit inside (or within 0.08s of) a measured
  silence. If not, the word boundary stands and the join is FLAGGED.
  Stretched first words (>0.8s — Whisper folds a pause into the retake's first
  word) get their in-point refined to the last silence_end inside the word - 0.10.
"""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
words = []
for s in json.load(open(BASE / "C1511.whisper.json"))["segments"]:
    for w in s.get("words", []):
        words.append({"start": w["start"], "end": w["end"], "text": w["word"].strip()})
silences = json.load(open(BASE / "silences.json"))

# (start_approx, end_approx, beat)
RANGES = [
    (2.80, 33.78, "intro-halo"),
    (73.28, 82.70, "halo-take3"),
    (88.26, 103.88, "halo-science"),
    (111.16, 156.44, "job-partnership"),
    (178.00, 268.02, "relationship"),
    (274.20, 291.68, "single-dating"),
    (294.18, 363.80, "online-dating"),
    (364.24, 366.90, "top10-a"),
    (372.60, 377.68, "top10-b"),
    (387.72, 420.90, "productivity-intro"),
    (425.92, 433.70, "grind-retake"),
    (441.36, 457.92, "meal-service"),
    (469.22, 495.16, "productivity-retake"),
    (500.08, 549.14, "doctor-time"),
    (555.60, 601.80, "longterm-a"),
    (606.82, 614.58, "longterm-b"),
    (623.92, 656.52, "mental-health"),
    (666.40, 693.56, "therapy-costs"),
    (699.54, 709.82, "spiral"),
    (716.10, 730.20, "priority-retake"),
    (737.82, 763.60, "expensive"),
    (767.36, 805.36, "lawyers"),
    (810.78, 915.92, "diabetes-story"),
    (920.74, 935.86, "money-dead"),
    (944.32, 972.26, "heirs"),
    (986.14, 1002.00, "family-suing"),
    (1006.66, 1082.66, "young-activities"),
    (1088.44, 1109.28, "kids"),
    (1111.72, 1125.26, "wife"),
    (1127.78, 1148.82, "stress-point"),
    (1173.66, 1201.38, "brokie-transition"),
    (1206.98, 1247.36, "dont-cut-food"),
    # merged: Whisper's degenerate zero-length words around "Just electricity"
    # made the internal cut untrustworthy — the rendered joint clipped to
    # "utility, tricity". Keep the tiny spoken self-correction instead.
    (1254.96, 1293.26, "mattress-rent"),
    (1305.94, 1322.02, "what-to-sacrifice"),
    (1325.28, 1360.20, "bars-clubs"),
    (1360.58, 1365.96, "entertainment"),
    (1370.50, 1398.16, "not-forever"),
    (1411.74, 1419.02, "bars-why"),
    (1426.30, 1458.28, "overpriced"),
    (1464.48, 1517.66, "restaurants"),
    (1521.96, 1565.12, "absbyai-track"),
    (1570.32, 1606.16, "junk-food"),
    (1611.98, 1628.22, "vacation-a"),
    (1631.32, 1672.52, "vacation-b"),
    (1676.64, 1689.82, "vacation-money"),
    (1694.14, 1738.54, "therapy-cut"),
    (1740.76, 1753.74, "therapy-temp"),
    (1766.62, 1806.00, "recap-sacrifice"),
    (1810.54, 1817.06, "temporary-retake"),
    (1843.70, 1862.42, "brokie-setup"),
    (1884.90, 1911.58, "equipment-list"),
    (1939.10, 1965.56, "steal-disclaimer"),
    (1978.54, 1999.70, "brokie-food"),
    (2012.34, 2049.34, "costco"),
    (2056.58, 2076.50, "no-excuse"),
    (2089.28, 2109.80, "middle-intro"),
    (2113.00, 2164.56, "premium-protein"),
    (2170.38, 2256.90, "protein-401k"),
    (2269.40, 2345.18, "mattress"),
    (2348.86, 2404.31, "purple"),
    (2416.57, 2477.29, "fluids"),
    (2480.37, 2489.93, "hygiene"),
    (2498.33, 2524.23, "gym-intro"),
    (2529.67, 2628.71, "gym-reasons"),
    (2664.01, 2686.49, "sleep-tracker"),
    (2708.23, 2764.55, "tracker-options"),
    (2767.01, 2778.43, "whoop"),
    (2784.27, 2853.73, "glp1"),
    (2856.35, 2889.41, "food-noise"),
    (2894.45, 2939.21, "glp1-savings"),
    (2944.07, 2962.23, "cash-out"),
    (2966.81, 2980.65, "trt-intro"),
    (2984.57, 3010.73, "trt-benefits"),
    (3014.11, 3028.97, "trt-longterm"),
    (3033.23, 3046.57, "trt-40s"),
    (3056.11, 3075.39, "supp-intro"),
    (3077.47, 3166.41, "fishoil-vitd"),
    (3181.75, 3219.21, "magnesium"),
    (3233.91, 3246.89, "ballers-intro"),
    (3251.39, 3313.05, "home-gym"),
    (3316.07, 3358.11, "baller-benefits"),
    (3360.21, 3404.75, "both-worlds"),
    (3415.31, 3440.79, "mealprep-intro"),
    (3450.65, 3456.77, "clean-eats"),
    (3465.29, 3502.79, "120-week"),
    (3506.57, 3537.43, "personal-chef"),
    (3546.97, 3555.59, "outsource"),
    (3555.93, 3586.99, "maid-laundry"),
    (3595.35, 3681.93, "trainer-nutri"),
    (3695.43, 3738.19, "mega-ballers"),
    (3742.43, 3765.41, "peptides"),
    (3768.73, 3772.99, "beyond-scope"),
    (3779.19, 3787.19, "brian-johnson"),
    (3798.55, 3834.27, "bj-detail"),
    (3839.43, 3889.41, "summary-a"),
    (3896.83, 3920.39, "summary-b"),
    (3927.90, 3962.59, "summary-c"),
    (4062.33, 4126.51, "outro"),
]

def in_silence(t, tol=0.08):
    for a, b in silences:
        if a - tol <= t <= b + tol:
            return True
    return False

def silence_ends_within(a, b):
    return [e for (s, e) in silences if a <= e <= b]

ranges_out = []
flags = []
prev_out = -1.0
for (a, b, beat) in RANGES:
    first = next((w for w in words if w["start"] >= a - 0.05), None)
    lasts = [w for w in words if w["end"] <= b + 0.05 and w["end"] > a]
    last = lasts[-1] if lasts else None
    if not first or not last:
        sys.exit(f"range {beat}: no words found")
    # stretched first word: pause folded into the word — refine onset via silence
    wdur = first["end"] - first["start"]
    in_t = first["start"] - 0.12
    if wdur > 0.8:
        se = silence_ends_within(first["start"], first["end"] - 0.1)
        if se:
            in_t = se[-1] - 0.10
            flags.append(f"{beat}: stretched first word {first['text']!r} ({wdur:.2f}s) -> onset refined to {in_t:.2f}")
    # never bite the tail of the preceding (cut) word — a partial word at the
    # head of a segment is an audible fragment
    prevs = [w for w in words if w["end"] <= first["start"] + 0.01 and w["end"] > first["start"] - 5]
    if prevs and prevs[-1]["end"] > in_t:
        in_t = prevs[-1]["end"] + 0.01
    out_t = last["end"] + 0.08
    # out-point may snap FORWARD into silence (safe direction), never >0.4s
    if not in_silence(out_t):
        cands = [s for (s, e) in silences if out_t - 0.05 <= s <= out_t + 0.40]
        if cands:
            out_t = cands[0] + 0.05
    # and never into the next (cut) word's onset
    nxt = next((w for w in words if w["start"] >= last["end"] - 0.01), None)
    if nxt and out_t > nxt["start"]:
        out_t = max(last["end"], nxt["start"] - 0.01)
    ok_in = in_silence(in_t)
    ok_out = in_silence(out_t)
    if not ok_in:
        flags.append(f"{beat}: IN edge {in_t:.2f} not in silence (word {first['text']!r})")
    if not ok_out:
        flags.append(f"{beat}: OUT edge {out_t:.2f} not in silence (word {last['text']!r})")
    if in_t <= prev_out:
        flags.append(f"{beat}: OVERLAP with previous range ({in_t:.2f} <= {prev_out:.2f})")
    prev_out = out_t
    ranges_out.append({"source": "C1511", "start": round(in_t, 3), "end": round(out_t, 3), "beat": beat})
    head = " ".join(w["text"] for w in words if in_t <= w["start"] < in_t + 3)[:70]
    tail = " ".join(w["text"] for w in words if out_t - 3 < w["end"] <= out_t)[-70:]
    print(f"{beat:22s} {in_t:8.2f}-{out_t:8.2f} ({out_t-in_t:6.2f}s) | {head} ... {tail}")

total = sum(r["end"] - r["start"] for r in ranges_out)
print(f"\nranges: {len(ranges_out)}  kept: {total:.1f}s = {total/60:.1f} min  (raw 4131s)")
print("\nFLAGS:")
for f in flags:
    print(" -", f)

edl = {
    "sources": {"C1511": str(BASE / "C1511.MP4")},
    "grade": "",  # filled after color analysis
    "ranges": ranges_out,
}
json.dump(edl, open(Path(__file__).parent / "edl.json", "w"), indent=1)
print("\nwrote edl.json")
