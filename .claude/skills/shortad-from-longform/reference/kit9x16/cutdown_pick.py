#!/usr/bin/env python3
"""THE <=0:59 CUTDOWN'S ONE MODEL CALL: which sentences make the hook, problem, AI demo, payoff and CTA.

  python3 cutdown_pick.py --build B [--ai gemini] [--max 57.5] [--ledger B/ai_ledger.jsonl]

Reads the full vertical's word timings (B/words_ctc.json, else m.whisper.json) and beat sheet (B/beats.json), numbers
the sentences, and asks ONE text-only question: which sentence ranges, in order, tell the whole story in under
--max seconds (skill Step 8: hook, problem, AI demo, payoff, CTA; the final CTA always last; <= 4 ranges; every seam
a sentence AND thought boundary). Everything after the answer is scripted: the ranges become times, a range never
opens inside a lower third or CTA pill whose start it cuts away (lesson A6.15), and kit_cutdown.py snaps, pads,
cuts and proves the seams. Writes B/cutdown_ranges.json with the sentences and the model's reasons.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_calls  # noqa: E402


def load_words(B):
    p = os.path.join(B, "words_ctc.json")
    if os.path.exists(p):
        return [(w["word"].strip(), float(w["start"]), float(w["end"])) for w in json.load(open(p)) if w["word"].strip()]
    d = json.load(open(os.path.join(B, "m.whisper.json")))
    return [(w["word"].strip(), float(w["start"]), float(w["end"])) for s in d["segments"] for w in s["words"] if w["word"].strip()]


def sentences(W):
    out, cur = [], []
    for i, (w, a, b) in enumerate(W):
        cur.append((w, a, b))
        gap = W[i + 1][1] - b if i + 1 < len(W) else 9
        if re.search(r"[.?!]$", w) or gap > 0.9:
            out.append(dict(text=" ".join(x[0] for x in cur), t0=cur[0][1], t1=cur[-1][2]))
            cur = []
    if cur:
        out.append(dict(text=" ".join(x[0] for x in cur), t0=cur[0][1], t1=cur[-1][2]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--ai", default="gemini")
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--max", type=float, default=57.5)
    ap.add_argument("--ledger")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    W = load_words(B)
    S = sentences(W)
    bj = json.load(open(os.path.join(B, "beats.json")))
    dur = float(bj["dur"])
    overlays = bj.get("lower_thirds", []) + bj.get("ctas", [])
    flashes = [(float(f[0]), float(f[1])) for f in bj.get("flashes", [])]
    AI = ai_calls.provider(a.ai, a.ledger or os.path.join(B, "ai_ledger.jsonl"))
    # ---- what the PICTURE allows at each sentence edge (plan.json of the judged full vertical): a seam needs a
    #      change of picture or of framing level across it, and may not sit in a flash or a graphic's fade
    pj = os.path.join(B, "plan.json")
    P = json.load(open(pj)) if os.path.exists(pj) else {}
    inserts = [tuple(x) for x in (P.get("cards") or []) + (P.get("covered") or [])]
    punch = [(float(x[0]), float(x[1]), x[2]) for x in P.get("punch") or []]

    def level_at(t):
        if any(a_ <= t < b_ for a_, b_ in inserts):
            return "picture"
        return next((lv for a_, b_, lv in punch if a_ <= t < b_), "FAR")

    def edges(x, y):
        """-> (t0, t1, problem or None) for the sentence range x..y, snapped clear of flashes and overlay fades."""
        prob = None
        t0 = max(0.0, S[x]["t0"] - 0.06)
        prev_end = S[x - 1]["t1"] if x > 0 else 0.0
        t0 = max(t0, (prev_end + S[x]["t0"]) / 2) if x > 0 else 0.0
        t1 = dur if y == len(S) - 1 else min(S[y]["t1"] + 0.05, (S[y]["t1"] + S[y + 1]["t0"]) / 2)
        # never open inside an overlay whose start is cut away: open on the overlay's own start instead
        for o in overlays:
            if o["t0"] < t0 < o["t1"] and t0 - o["t0"] < 3.0:
                t0 = o["t0"]
        # never cut INSIDE his flash: it is baked into the picture, so a seam in it leaves two frames of ramp-up and
        # a hard cut (AV-09 cutdown seam at 19.94 s, flash 19.91-20.35, judged a truncated graphic). The range takes
        # the whole flash when no word starts inside it, else it stops where the flash begins.
        for f0, f1 in flashes:
            if f0 < t1 < f1:
                nxt_w = min([w_[1] for w_ in W if w_[1] > S[y]["t1"] + 0.01] or [dur])
                t1 = f1 if nxt_w >= f1 - 0.02 else max(f0, S[y]["t1"] + 0.005)
            if f0 < t0 < f1:
                prv_w = max([w_[2] for w_ in W if w_[2] < S[x]["t0"] - 0.01] or [0.0])
                t0 = f0 if prv_w <= f0 + 0.02 else f1
        # ... nor inside an overlay's fade-out (its last 0.4 s): a sentence that ends there cannot end a range
        # (AV-09 cutdown seam 3: "Abs In Less Than 10 Seconds" lost the last 3 frames of its fade; running on past
        # the fade left 4 frames at the next shot's own level, a jump cut by the gate's measure)
        if y < len(S) - 1:
            for o in overlays:
                if o["t1"] - 0.4 < t1 < o["t1"] + 0.02:
                    prob = f"sentence {y} ends inside the fade-out of an on-screen graphic, so a range cannot end on it"
        return round(t0, 3), round(t1, 3), prob

    def seam_problems(R_):
        out = []
        E_ = [edges(x, y) for x, y in R_]
        for (x, y), (t0, t1, pr) in zip(R_, E_):
            if pr:
                out.append(pr)
        for i in range(len(R_) - 1):
            a_out, b_in = level_at(E_[i][1] - 0.03), level_at(E_[i + 1][0] + 0.03)
            if E_[i + 1][0] - E_[i][1] < 0.5:
                continue                                  # contiguous sentences: no seam
            if a_out != "picture" and b_in != "picture" and a_out == b_in:
                out.append(f"the cut from sentence {R_[i][1]} to sentence {R_[i + 1][0]} joins two talking shots at the "
                           f"same zoom level ({a_out}): a jump cut. End on a sentence marked with a different level "
                           f"than the next range's first sentence, or one that ends or starts on a picture")
        return out, E_

    def tag(i):
        t0, t1, pr = edges(i, i)
        return (f" <starts {level_at(t0 + 0.03)}; ends {level_at(t1 - 0.03)}"
                + ("; a range CANNOT END here" if pr else "") + ">")
    listing = "\n".join(f"[{i}] ({s['t0']:.1f}-{s['t1']:.1f}s, {s['t1'] - s['t0']:.1f}s) {s['text']}{tag(i)}" for i, s in enumerate(S))
    prompt = (
        "You are cutting a <=0:59 vertical cutdown of a finished paid video ad for Abs By AI (an app that generates a "
        "picture of you with six-pack abs, then builds the workout and nutrition plan). Below is the ad's transcript as "
        "numbered sentences with their times. Pick sentence RANGES, in the original order, that tell the complete "
        "story in under " + f"{a.max:.0f}" + " seconds total: a hook (the first lines of the ad, normally), the problem, "
        "the AI demo (the moment he generates / sees the picture of himself with abs: it MUST be in the cut, it is what "
        "the ad sells), the payoff (what it did for him), and the call to action. Use most of the time you have: a "
        "cutdown under 45 s has thrown away story it could keep. Rules: at most "
        "4 ranges; each range is a run of consecutive sentences; every seam must be a sentence AND a thought boundary "
        "(the cut must read as natural prose, no dangling 'and'/'so'/'this' referring to something cut away); the "
        "LAST sentences of the ad (the final CTA) must be the last range; never end on a half-finished list. Prefer "
        "fewer, longer ranges. Sum the durations yourself and stay under the limit. PICTURE RULE: each sentence is "
        "tagged with what is on screen where it starts and ends (FAR / NEAR = the talking head at that zoom level, "
        "picture = a photo, clip or text card). Where one range ends and the next begins, the two tags must differ "
        "(FAR to NEAR, NEAR to FAR) or at least one must be 'picture'; never FAR to FAR or NEAR to NEAR. Never end a "
        "range on a sentence tagged 'a range CANNOT END here'.\n\n" + listing +
        '\n\nAnswer JSON: {"ranges": [[first_sentence, last_sentence], ...], "total_seconds": <sum>, '
        '"story": "<the cutdown read as prose>", "why": "<one line per range: hook/problem/demo/payoff/CTA>"}')
    res, E_ = None, None
    for attempt in range(5):
        res = AI.text(prompt, purpose="cutdown", model=a.model)
        if not res or "ranges" not in res:
            continue
        R = [(max(0, int(x)), min(len(S) - 1, int(y))) for x, y in res["ranges"]]
        tot = sum(S[y]["t1"] - S[x]["t0"] + 0.15 for x, y in R)
        probs, E_ = seam_problems(R) if R else (["no ranges"], None)
        if tot > a.max + 1.0:
            probs.append(f"it measures {tot:.1f}s (limit {a.max:.0f}s)")
        if not (R and R[-1][1] == len(S) - 1):
            probs.append("it does not end on the final sentence")
        if not probs:
            break
        prompt += f"\n\nYour last answer {res['ranges']} is not usable: " + "; ".join(probs) + ". Fix it."
    else:
        raise SystemExit("cutdown_pick: no valid selection after 5 answers (escalate)")
    ranges = [[t0, t1] for t0, t1, _ in E_]
    # contiguous or overlapping neighbours merge
    merged = [ranges[0]]
    for r in ranges[1:]:
        if r[0] <= merged[-1][1] + 0.02:
            merged[-1][1] = max(merged[-1][1], r[1])
        else:
            merged.append(r)
    total = sum(b - a_ for a_, b in merged)
    out = dict(ranges=merged, seconds=round(total, 3), sentences=[[x, y] for x, y in R],
               story=res.get("story"), why=res.get("why"), model=a.model,
               text=[" ".join(S[i]["text"] for i in range(x, y + 1)) for x, y in R])
    json.dump(out, open(os.path.join(B, "cutdown_ranges.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("AI", AI.ledger.total())
    if total > 59.0:
        raise SystemExit(f"selection is {total:.1f}s > 59 s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
