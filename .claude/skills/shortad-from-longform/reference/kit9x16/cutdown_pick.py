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


# AN ORGANIC FILM'S 59 s CUT IS A SHORT, NOT AN AD CUTDOWN (RO-10, 2026-10-03). The ad brief demands the app demo and
# the tap-the-button CTA, which a content video does not have. A short must stand alone and leave the viewer with
# something to do (Dan's standing shorts rules: a reason to watch, a tactic, never a line that points at something the
# cut does not contain). The seam, length and caption rules are the same as the ad's; only the ending is free.
ORGANIC_BRIEF = (
    "You are cutting a <=0:59 vertical Short out of a finished ORGANIC YouTube video by Dan Rose (fitness for men over "
    "40; this is content, not an ad). Below is the video's transcript as numbered sentences with their times. Pick "
    "sentence RANGES, in the original order, that make ONE short that stands on its own in under {max} seconds: the "
    "hook (the first lines of the video), the main claim with its single strongest piece of proof, and the practical "
    "payoff. The viewer must leave with at least one concrete thing to do, stated completely; a recap that lists the "
    "video's tactics is the best payoff when there is one. Never include a line that points at something the cut does "
    "not contain ('the study I just showed you', 'here's the second one', 'number five goes together with...', 'the "
    "next one') unless what it points at is in the cut. End on a complete thought: the recap or the video's closing "
    "line are both good endings, and the cut does NOT have to run to the last sentence. Use most of the time you "
    "have: a cut under 45 s has thrown away story it could keep. Rules: the first range starts at sentence 0 (the hook "
    "is never cut); at most 4 ranges; each range is a run of consecutive sentences; every seam must be a sentence AND "
    "a thought boundary (the cut must read as natural prose, no dangling 'and'/'so'/'this' referring to something cut "
    "away); never end on a half-finished list. Prefer fewer, longer ranges. Sum the durations yourself and stay under "
    "the limit. PICTURE RULE: each sentence is tagged with what is on screen where it starts and ends (FAR / NEAR = "
    "the talking head at that zoom level, picture = a photo, clip or text card). Where one range ends and the next "
    "begins, the two tags must differ (FAR to NEAR, NEAR to FAR) or at least one must be 'picture'; never FAR to FAR "
    "or NEAR to NEAR. Never end a range on a sentence tagged 'a range CANNOT END here', nor start one on 'a range "
    "CANNOT START here'. At least half of the cut's running time must be sentences NOT tagged 'NO CAPTIONS on screen'.\n\n")
ANSWER_JSON = ('\n\nAnswer JSON: {"ranges": [[first_sentence, last_sentence], ...], "total_seconds": <sum>, '
               '"story": "<the cut read as prose>", "why": "<one line per range: hook/proof/payoff/close>"}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--organic", action="store_true", help="the film is content, not an ad: the short's brief (ORGANIC_BRIEF); "
                                                           "the cut need not end on the film's last sentence")
    ap.add_argument("--ai", default="gemini")
    ap.add_argument("--model", default="gemini-3.1-pro-preview",
                    help="one text call, a few cents: Flash 2.5 could not hold the seam rules (out-of-order ranges, a 34 s cut "
                         "without the demo, AV-09 2026-10-01)")
    ap.add_argument("--max", type=float, default=57.5)
    ap.add_argument("--ledger")
    ap.add_argument("--list", action="store_true", help="print the numbered, tagged sentence listing the model sees, and stop")
    ap.add_argument("--ranges", help='a hand selection, e.g. "0-1,9-14,27-27,56-65": no model call, the same checks')
    ap.add_argument("--search", type=int, metavar="N", help="list every selection the checks accept (middle ranges of at most N sentences), no model call")
    ap.add_argument("--must", help='with --search: sentence groups the cut must contain, e.g. "9|14,27|36"')
    ap.add_argument("--why", default="hand-picked by the session after the model's answers failed the seam checks")
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
    inserts = [tuple(x) for x in (P.get("covered") or [])]      # `cards` also lists lower thirds and CTA pills: not pictures
    punch = [(float(x[0]), float(x[1]), x[2]) for x in P.get("punch") or []]

    caps = sorted((float(c["beat"][0]), float(c["beat"][1])) for c in P.get("caption_states") or [])

    def captioned(t0, t1):
        """Seconds of [t0, t1] with a burned caption on screen (the gate's captions:burned row wants 45 % of the
        cutdown's frames; a selection made of labelled pictures, where captions are off, read 44 %: AV-09)."""
        return sum(max(0.0, min(b_, t1) - max(a_, t0)) for a_, b_ in caps)

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
            # the last word's sound needs up to 0.3 s after its CTC end (kit_cutdown pad_tail), so a flash that
            # starts in that tail is cut too: the range takes the whole flash, or the sentence cannot end a range
            # (AV-09 cutdown: stopping at the flash's start still left 2 flash frames once the tail was padded)
            if y < len(S) - 1 and f0 - 0.30 < S[y]["t1"] < f1:
                nxt_w = min([w_[1] for w_ in W if w_[1] > S[y]["t1"] + 0.01] or [dur])
                if nxt_w >= f1 + 0.03:
                    t1 = f1 + 0.01
                else:
                    prob = f"sentence {y} ends against a white flash transition, so a range cannot end on it"
            if x > 0 and f0 < t0 < f1:
                prv_w = max([w_[2] for w_ in W if w_[2] < S[x]["t0"] - 0.01] or [0.0])
                if prv_w <= f0 - 0.30:
                    t0 = f0
                else:
                    prob = f"sentence {x} starts inside a white flash transition, so a range cannot start on it"
        # ... nor inside an overlay's fade-out (its last 0.4 s): a sentence that ends there cannot end a range
        # (AV-09 cutdown seam 3: "Abs In Less Than 10 Seconds" lost the last 3 frames of its fade; running on past
        # the fade left 4 frames at the next shot's own level, a jump cut by the gate's measure)
        if y < len(S) - 1:
            for o in overlays:
                if o["t1"] - 0.4 < t1 < o["t1"] + 0.02:
                    prob = f"sentence {y} ends inside the fade-out of an on-screen graphic, so a range cannot end on it"
        # ... nor a few frames after a zoom change: the word's tail (up to 0.3 s) would carry a sliver of the next
        # level into the seam, which the gate's cut:min_segment row fails (AV-09 cutdown, 2 NEAR frames at 44.18 s)
        pb = sorted({a_ for a_, b_, _ in punch} | {b_ for a_, b_, _ in punch})
        # (a change in the word's own tail is fine: kit_cutdown holds the last frame before it; one BEFORE the word
        # ends would freeze his mouth mid-word)
        if y < len(S) - 1 and any(S[y]["t1"] - 0.20 < q < S[y]["t1"] - 0.02 for q in pb):
            prob = prob or f"sentence {y} ends on a zoom change, so a range cannot end on it"
        if x > 0 and any(t0 + 0.02 < q < t0 + 0.22 for q in pb):
            prob = prob or f"sentence {x} starts just before a zoom change, so a range cannot start on it"
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
                + ("; a range CANNOT END here" if pr and "end" in pr else "")
                + ("; a range CANNOT START here" if pr and "start on" in pr else "")
                + ("; NO CAPTIONS on screen" if caps and captioned(S[i]["t0"], S[i]["t1"]) < 0.4 * (S[i]["t1"] - S[i]["t0"]) else "") + ">")
    listing = "\n".join(f"[{i}] ({s['t0']:.1f}-{s['t1']:.1f}s, {s['t1'] - s['t0']:.1f}s) {s['text']}{tag(i)}" for i, s in enumerate(S))
    prompt = ORGANIC_BRIEF.format(max=f"{a.max:.0f}") + listing + ANSWER_JSON if a.organic else (
        "You are cutting a <=0:59 vertical cutdown of a finished paid video ad for Abs By AI (an app that generates a "
        "picture of you with six-pack abs, then builds the workout and nutrition plan). Below is the ad's transcript as "
        "numbered sentences with their times. Pick sentence RANGES, in the original order, that tell the complete "
        "story in under " + f"{a.max:.0f}" + " seconds total: a hook (the first lines of the ad, normally), the problem, "
        "the AI demo (the moment he generates / sees the picture of himself with abs: it MUST be in the cut, it is what "
        "the ad sells), the payoff (what it did for him), and the call to action. Use most of the time you have: a "
        "cutdown under 45 s has thrown away story it could keep. Rules: the first range starts at sentence 0 (the "
        "hook is never cut); at most "
        "4 ranges; each range is a run of consecutive sentences; every seam must be a sentence AND a thought boundary "
        "(the cut must read as natural prose, no dangling 'and'/'so'/'this' referring to something cut away); the "
        "LAST sentences of the ad (the final CTA) must be the last range; never end on a half-finished list. Prefer "
        "fewer, longer ranges. Sum the durations yourself and stay under the limit. PICTURE RULE: each sentence is "
        "tagged with what is on screen where it starts and ends (FAR / NEAR = the talking head at that zoom level, "
        "picture = a photo, clip or text card). Where one range ends and the next begins, the two tags must differ "
        "(FAR to NEAR, NEAR to FAR) or at least one must be 'picture'; never FAR to FAR or NEAR to NEAR. Never end a "
        "range on a sentence tagged 'a range CANNOT END here', nor start one on 'a range CANNOT START here'. At least half of the cut's running time must be sentences NOT tagged 'NO CAPTIONS on screen'.\n\n" + listing +
        '\n\nAnswer JSON: {"ranges": [[first_sentence, last_sentence], ...], "total_seconds": <sum>, '
        '"story": "<the cutdown read as prose>", "why": "<one line per range: hook/problem/demo/payoff/CTA>"}')
    if a.list:
        print(listing); return 0
    if a.search:
        # every selection the checks below would accept (first range from sentence 0, last to the final sentence, at most
        # 4 ranges of at most --search sentences each), best first: the demo sentence in, then the longest. A
        # session uses this when the model's answers keep failing the seam rules, then passes one with --ranges.
        n = len(S); L = a.search
        ok_end = {y for y in range(n) if not (edges(y, y)[2] or "").count("end")}
        cand = [(x, y) for x in range(1, n - 1) for y in range(x, min(n - 1, x + L)) ]
        dur_ = lambda R_: sum(S[y]["t1"] - S[x]["t0"] + 0.15 for x, y in R_)
        found = []
        firsts = [(0, y) for y in range(0, 12)]
        lasts = [(x, n - 1) for x in range(n - 12, n)]
        import itertools
        for r1 in firsts:
            for r4 in lasts:
                base = dur_([r1, r4])
                if base > a.max + 1.0:
                    continue
                mids = [c for c in cand if c[0] > r1[1] and c[1] < r4[0] and base + dur_([c]) <= a.max + 1.0]
                for k in (0, 1, 2):
                    for M in itertools.combinations(mids, k):
                        if any(M[i + 1][0] <= M[i][1] for i in range(len(M) - 1)):
                            continue
                        R_ = [r1, *M, r4]
                        tot = dur_(R_)
                        if tot < 45.0 or tot > a.max + 1.0:
                            continue
                        probs_, E2 = seam_problems(R_)
                        if probs_:
                            continue
                        real = sum(t1 - t0 for t0, t1, _ in E2) + 0.35 * len(R_)
                        cov = sum(captioned(t0, t1) for t0, t1, _ in E2) / max(1e-6, sum(t1 - t0 for t0, t1, _ in E2))
                        if real > 58.3 or (caps and cov < 0.50):
                            continue
                        found.append((tot, cov, R_))
        if a.must:
            for grp in a.must.split(","):                     # "9|14,27|36": each group needs one of its sentences in the cut
                opts = [int(q) for q in grp.split("|")]
                found = [f for f in found if any(x <= o <= y for o in opts for x, y in f[2])]
        found.sort(key=lambda f: (-f[0]))
        print(f"{len(found)} valid selections")
        for tot, cov, R_ in found[:40]:
            print(f"{tot:5.1f}s  captions {100 * cov:3.0f}%  " + ",".join(f"{x}-{y}" for x, y in R_))
        return 0
    res, E_ = None, None
    for attempt in range(1 if a.ranges else 5):
        res = (dict(ranges=[[int(q.split("-")[0]), int(q.split("-")[1])] for q in a.ranges.split(",")], story="hand-picked", why=a.why)
               if a.ranges else AI.text(prompt, purpose="cutdown", model=a.model))
        if not res or "ranges" not in res:
            continue
        if not all(isinstance(r_, (list, tuple)) and len(r_) == 2 for r_ in res["ranges"]):
            prompt += f"\n\nYour last answer {res['ranges']} is not usable: every range is [first_sentence, last_sentence], two numbers. Fix it."
            continue
        R = [(max(0, int(x)), min(len(S) - 1, int(y))) for x, y in res["ranges"]]
        tot = sum(S[y]["t1"] - S[x]["t0"] + 0.15 for x, y in R)
        probs, E_ = seam_problems(R) if R else (["no ranges"], None)
        real = sum(t1 - t0 for t0, t1, _ in E_) + 0.35 * len(R) if E_ else tot      # + the word-tail pad per range
        if tot > a.max + 1.0 or real > 58.3:
            probs.append(f"it measures {max(tot, real):.1f}s (limit {a.max:.0f}s)")
        if tot < 45.0:
            probs.append(f"it measures only {tot:.1f}s: use at least 45 s of the {a.max:.0f} s")
        if caps and E_:
            cov = sum(captioned(t0, t1) for t0, t1, _ in E_) / max(1e-6, sum(t1 - t0 for t0, t1, _ in E_))
            if cov < 0.50:
                probs.append(f"only {100 * cov:.0f}% of it has captions on screen (at least 50% needed): swap sentences "
                             f"tagged 'NO CAPTIONS on screen' for captioned ones")
        if R and R[0][0] != 0:
            probs.append("the first range must start at sentence 0: the ad's opening hook is never cut")
        if len(R) > 4:
            probs.append(f"it has {len(R)} ranges (at most 4)")
        if any(x > y for x, y in R) or any(R[i + 1][0] <= R[i][1] for i in range(len(R) - 1)):
            probs.append("the ranges must be in the ad's own order and must not overlap")
        if not a.organic and not (R and R[-1][1] == len(S) - 1):
            probs.append("it does not end on the final sentence")
        if not probs:
            break
        prompt += f"\n\nYour last answer {res['ranges']} is not usable: " + "; ".join(probs) + ". Fix it."
    else:
        if a.ranges:
            raise SystemExit("cutdown_pick: the hand selection fails: " + "; ".join(probs))
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
               story=res.get("story"), why=res.get("why"), model=("hand" if a.ranges else a.model),
               text=[" ".join(S[i]["text"] for i in range(x, y + 1)) for x, y in R])
    json.dump(out, open(os.path.join(B, "cutdown_ranges.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("AI", AI.ledger.total())
    if total > 59.0:
        raise SystemExit(f"selection is {total:.1f}s > 59 s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
