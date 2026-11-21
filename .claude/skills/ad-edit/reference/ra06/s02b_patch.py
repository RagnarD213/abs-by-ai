#!/usr/bin/env python3
"""RA-06: Replicate large-v3 returns CONTIGUOUS word times (a word's end = the next word's start), which hides every
pause inside a word and lets the 60 % overlap rule drop real words when a pause is cut. Re-time from the 5 ms envelope:
each silence run (< -40 dB, >= 0.10 s) inside the take span ends the word before it and starts the word after it.
Also restores the take-2 "That's" Whisper skipped (340.7 s). Idempotent: reads tx/c1664.whisper.orig.json."""
import json, os, shutil
P, O = "tx/c1664.whisper.json", "tx/c1664.whisper.orig.json"
if not os.path.exists(O): shutil.copy(P, O)
d = json.load(open(O)); W = d["segments"][0]["words"]
env = json.load(open("env.json")); H, DB = env["hop"], env["db"]
SIL, MIN = -40.0, 0.10
runs, i0 = [], None
for k in range(int(305/H), int(372/H)):
    q = DB[k] < SIL
    if q and i0 is None: i0 = k
    if not q and i0 is not None:
        if (k-i0)*H >= MIN: runs.append((i0*H, k*H))
        i0 = None
# restore the missing word first: onset of the speech after the 339.8 take break
brk = next(r for r in runs if r[0] < 340.3 < r[1] or 339.6 < r[0] < 340.6)
j = next(k for k, w in enumerate(W) if w["start"] >= 341.0 and w["word"].strip() == "why")
W.insert(j, {"word": " That's", "start": round(brk[1], 3), "end": W[j]["start"]})
print(f"inserted That's at {brk[1]:.3f}")
fixed = 0
for s0, s1 in runs:
    before = [w for w in W if w["start"] < s0 - 0.03]
    after = [w for w in W if w["end"] > s1 + 0.03]
    if not before or not after: continue
    a, b = before[-1], after[0]
    if a is b: continue           # silence INSIDE one word (a stop consonant): leave it
    if a["end"] > s0: a["end"] = round(s0, 3); fixed += 1
    if b["start"] < s1: b["start"] = round(s1, 3); fixed += 1
for w in W:
    assert w["end"] > w["start"], w
W[0]["start"] = 313.38   # "What's": breath 313.00, the word's onset 313.38 (envelope, 40 ms steps)
# caption text: both "replaced ... with AI" lines stay as the long pass heard them ("them"); the independent reviewer's
# three Whisper passes heard "them" at 0:22.6 at 0.93-0.97 confidence (one isolated pass of mine heard "him")
json.dump(d, open(P, "w"), indent=1)
print(f"{len(runs)} silence runs, {fixed} edges moved, {len(W)} words")
for w in W:
    if w["end"]-w["start"] > 0.7: print("  still long:", w)
