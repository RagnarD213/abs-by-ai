#!/usr/bin/env python3
"""RO-12 "Top 5 Zepbound Tips": the cut. Source = 9/23 roll C1706 only.
SPEECH lists the kept passages in order as approximate source ranges; pieces() snaps each to the lav's measured speech
islands (vad.py) and splits any internal silence over MAX_PAUSE. Take choices (2026-09-30):
  intro      take 3 (100.8-126.2): the only take that pronounces "Zepbound" correctly (Gemini listen, listen/q_intro.txt);
             Dan went "back to the top" after takes 1 and 2; matches his last-clean-take rule.
  restarts   verified verbatim by Gemini on the lav (listen/chunk_*.txt): every abandoned attempt dropped, the complete retake kept.
  dropped    "0.8 grams per pound of body fat" (770.4, a misstatement of lean body mass), "Shoot Thursday evening" (761.7, he
             corrected it to "Inject"), the first closing (787.8-803.6, he rolled back), the drink break (246-259)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vad

ROLL = "C1706"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1706.MP4"
MAX_PAUSE = 0.95      # an internal silence longer than this is tightened (a cut, so a framing change or a cover)
KEEP_PAUSE = (0.22, 0.30)
TAIL = 828.4   # tail / head kept either side of a tightened pause

SPEECH = [
    (101.0, 126.3),   # intro take 3: Here are 5 tips ... glad I took the medication.
    (155.2, 167.2),   # (abandoned "However, I did screw th-" 153.3-154.8 dropped) However, I did screw some things up ... So here's what you need to do when you're on Zepbound.
    (167.4, 210.95),  # TIP 1 ... and that is important.
    (211.1, 241.7),   # I have found ... dial it down to maintain.
    (259.4, 280.99),  # I'm currently taking 1.5 (retake after the drink) ... inject yourself properly with a needle.
    (283.3, 306.3),   # Learn the needle, and you get to run ... for the concentration you have.
    (312.3, 326.8),   # And then you just pull back to that line (retake) ... If you can read a measuring cup, you can do this.
    (326.9, 371.4),   # TIP 2 ... there is no blood.
    (374.3, 379.1),   # If you bled, or if it actually hurt (retake) ... Change something next time.
    (381.45, 385.9),  # You went too deep, or you were in the wrong spot ... too fast. (retake)
    (389.75, 425.5),  # If you are scared of needles (retake) ... there is almost nothing to numb.
    (425.8, 502.4),   # TIP 3 ... waiting a few extra days one time.
    (511.5, 523.7),   # TIP 4 (second title read) ... That's how you avoid the side effects.
    (535.2, 559.0),   # Coming off (script version) ... So here's the process that I use instead.
    (562.0, 599.3),   # instead of going off totally (retake), start by lowering ... hold your new body the entire time.
    (606.5, 611.7),   # Do not white-knuckle (second read) ... jumping off the roof.
    (612.1, 630.7),   # TIP 5 ... by weight training regularly.
    (635.6, 654.45),  # In fact, I have gained muscle ... because of this. ... hit your protein every day.
    (658.7, 683.3),   # What you're aiming for (retake) ... the failure mode here is not obvious.
    (697.0, 703.9),   # If you under-eat protein (third read) ... You will feel like it's working.
    (708.6, 719.45),  # What you will not see (retake) ... now you think you need to bulk.
    (728.2, 753.9),   # Then you regain the fat (retake) ... go and watch that one next.
    (754.1, 761.35),  # WRAP: So those are your 5 tips ... outer thigh.
    (764.1, 770.2),   # Inject Thursday evening. Ramp on slow and taper off slower and guard your protein.
    (778.9, 787.6),   # Zepbound is the most powerful (retake) ... use it the right way.
    (812.0, 827.0),   # (+1.5 s hold after the last word, TAIL below) If you take this medication ... (second closing, after "roll it back") ... as soon as I release them.
]

def _isl(a, b):
    return [(s, e) for s, e in vad.islands(a - 0.5, b + 0.5, min_gap=0.12) if e - s >= 0.08 and e > a + 0.05 and s < b - 0.05]

def pieces():
    """-> list of dict(in, out, speech_idx). Consecutive pieces are separate CUTS (source time skipped)."""
    out = []
    for k, (a, b) in enumerate(SPEECH):
        isl = _isl(a, b)
        assert isl, (a, b)
        s0 = isl[0][0]; e1 = isl[-1][1]
        sil_before = [s for s in vad.silences(s0 - 1.0, s0 + 0.01, 0.05)]
        lo = sil_before[-1][0] + 0.02 if sil_before else s0 - 0.10
        start = max(lo, s0 - 0.10)
        sil_after = vad.silences(e1 - 0.01, e1 + 1.0, 0.05)
        hi = sil_after[0][1] - 0.04 if sil_after else e1 + 0.14
        end = min(hi, e1 + 0.16)
        # split long internal pauses
        cur = start
        for (x0, x1), (y0, y1) in zip(isl, isl[1:]):
            if y0 - x1 > MAX_PAUSE:
                out.append(dict(**{"in": round(cur, 3), "out": round(x1 + KEEP_PAUSE[0], 3)}, speech=k, why=f"pause {y0-x1:.2f}s tightened"))
                cur = y0 - KEEP_PAUSE[1]
        out.append(dict(**{"in": round(cur, 3), "out": round(end, 3)}, speech=k))
    out[-1]["out"] = max(out[-1]["out"], TAIL)   # review r1 N14: room for YouTube's end screen; silent until 829.3 ("There we go")
    return out

if __name__ == "__main__":
    import json
    P = pieces(); tot = sum(p["out"] - p["in"] for p in P)
    w = json.load(open(SRC.replace(".MP4", ".roll/words.json"))); w = w["words"] if isinstance(w, dict) else w
    for p in P:
        txt = " ".join(x["word"].strip() for x in w if p["in"] <= (x["start"] + x["end"]) / 2 < p["out"])
        print(f"{p['in']:8.2f}-{p['out']:8.2f} ({p['out']-p['in']:5.2f}) {p.get('why','')} | {txt[:70]} ... {txt[-50:]}")
    print(len(P), "pieces", round(tot, 1), "s")
