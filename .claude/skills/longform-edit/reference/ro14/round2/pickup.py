"""RO-14 round 2: the 10/15 pickup (roll C1722, take 342.36-350.86 s, lav LEFT channel) replaces the filmed opening line that
says "five hidden reasons" (film 16.62-26.06, under the full-screen G02 "In this video" card).

PICKUP: film window [A, B) takes the tone- and level-matched pickup (pickup/match.py) from P0 on; the film's own pause after
"genetics." (16.00-16.62) and before "Then" (26.06-26.16) stay, so the total length is unchanged and nothing after B moves.
Pauses: "genetics." -> "I'm" 0.82 s, "angry." -> "Then" 0.85 s (Dan's own pauses on this roll run 0.6-0.7 s).
`python3 pickup.py words` rewrites words_out.json (film words inside [A, B) out, pickup words in, mapped to film time)."""
import json, sys
W = "/Volumes/Extreme/_edit_work/RO-14/round2"
A, B = 16.62, 26.06                 # film seconds replaced
P0 = 342.16                         # pickup roll second that lands on A (0.20 s before the onset of "I'm", 342.36)
MATCHED = f"{W}/pickup/pickup_matched.wav"; MATCHED_T0 = 342.10     # pickup_matched.wav starts at this roll second
XF = 0.030                          # crossfade at both joins (room to room)
# heard words (Gemini verbatim listen 2026-10-20 + medium.en times on the matched take; "you are" as medium.en and the independent reviewer hear it)
TEXT = ("I'm going to give you the four ways you are eating more calories than you think. Then four hidden reasons why you're "
        "eating them in the first place. And some of those four are going to make you angry.")

def words():
    wo = json.load(open(f"{W}/words_out.json"))
    pk = json.load(open(f"{W}/pickup/pickup_words_medium.json"))
    pk[0]["t0"] = 342.36                                   # medium.en clamps the first word to the clip start; the onset is 342.36
    toks = TEXT.split()
    assert len(toks) == len(pk), (len(toks), len(pk))
    new = [dict(w=t, src0=p["t0"], src1=p["t1"], t0=round(A + p["t0"] - P0, 3), t1=round(A + p["t1"] - P0, 3), pickup="C1722")
           for t, p in zip(toks, pk)]
    assert new[-1]["t1"] < B - 0.5, new[-1]
    # medium.en stamped the film's "I" at 16.10 though its onset is 16.74 (level strip): it is inside the replaced audio
    keep = [w for w in wo if w["t0"] is None or not (A <= w["t0"] < B or (w["w"] == "I" and 16.0 < w["t0"] < A))]
    out = sorted(keep + new, key=lambda w: (w["t0"] is None, w["t0"] or 0))
    json.dump(out, open(f"{W}/words_out.json", "w"), indent=1)
    print(f"words_out: {len(wo) - len(keep)} film words out, {len(new)} pickup words in; last pickup word ends {new[-1]['t1']:.2f}")

if __name__ == "__main__" and sys.argv[1:] == ["words"]: words()
