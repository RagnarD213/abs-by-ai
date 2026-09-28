#!/usr/bin/env python3
"""THE WATCH-PASS JUDGE AS A MODEL CALL: reads every sheet and strip of watch.py's output against CHECKLIST.md and
writes findings in EXACTLY the format the session judges write (JUDGE_PROMPT.md), so kit_fold.sh and the gate take
it unchanged:  logs/findings_part<N>.json = {"judge", "video", "method", "entries": [{image, verdict, item, t, note}]}

  python3 gemini_judge.py --build B --video NAME.mp4 [--model gemini-3.1-pro-preview] [--batch 16] [--parts 3]
                          [--watch B/watch] [--ledger B/ai_ledger.jsonl]

It is told the design facts the session judges needed (the kit's size steps, ramps, flashes). It must not be LESS
strict than the session judges: proven on Ad 10's rejected builds (their known defects) and its delivered build
(its false alarms) -- see README "Gemini judge". A defect it records blocks delivery like any judge's.
Every call is logged with its cost. Images are sent at their own resolution (no downscale: a jump cut is a
few pixels of a hand).
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_calls  # noqa: E402

DESIGN_FACTS = """DESIGN FACTS OF THIS FORMAT (the kit9x16 vertical). These are EXPECTED, not defects:
- Every bare talk cut (a splice between two takes) carries an instant ~20 % SIZE STEP (a zoom-cut): the framing
  jumps in or out by about a fifth on the cut frame. A size step at a declared boundary is expected.
- Strips whose name contains punch_FAR / punch_NEAR with NO join under them are 0.5 s RAMPS (a gradual push),
  not steps: the five frames change size smoothly.
- A light-leak / white flash on the return from an inserted picture to the talking head is his design.
- Word-timed captions sit in a band over the lower frame; they are suppressed under text plates and under
  labelled pictures of Dan.
- Real photos of Dan carry one chip "Real picture of me - not AI-generated"; AI pictures carry "AI-GENERATED".
  Exactly one label per picture of his physique, never over his face or abs.
A DEFECT is anything on the checklist that is not one of the above: a jump cut where the subject moves between
-1 and 0 with the same framing and the same scene, hair cut by the top edge, a label or caption over his face or
abs, a missing or doubled label, garbled/placeholder/junk text, a black or frozen frame, an AI giveaway (melting
hands, smoke), a wide shot, a declared graphic that is not there, visual junk (a look-away, glasses adjust)."""


def load_items(watch):
    ck = open(os.path.join(watch, "CHECKLIST.md")).read()
    keys = re.findall(r"\*\*`([a-z_]+)`\*\*", ck)
    return ck, keys


def t_of(name):
    m = re.search(r"_(\d\d)-(\d\d\.\d\d)", name)
    return round(int(m.group(1)) * 60 + float(m.group(2)), 2) if m else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--watch")
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    ap.add_argument("--batch", type=int, default=16, help="images per call (a strip and its pair stay together)")
    ap.add_argument("--parts", type=int, default=3, help="write findings_part1..N like three session judges")
    ap.add_argument("--ledger")
    ap.add_argument("--out-dir", help="default B/logs")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    W = a.watch or os.path.join(B, "watch")
    out_dir = a.out_dir or os.path.join(B, "logs")
    os.makedirs(out_dir, exist_ok=True)
    ck, keys = load_items(W)
    AI = ai_calls.provider("gemini", a.ledger or os.path.join(B, "ai_ledger.jsonl"))
    sheets = sorted(glob.glob(os.path.join(W, "sheets", "*.jpg")))
    strips = sorted(glob.glob(os.path.join(W, "strips", "strip_*.jpg")))
    groups = [[p] for p in sheets]
    for s in strips:
        idx = re.search(r"strip_(\d+)_(\d\d-\d\d\.\d\d)", os.path.basename(s))
        pair = os.path.join(W, "strips", f"pair_{idx.group(1)}_{idx.group(2)}.jpg") if idx else None
        groups.append([s] + ([pair] if pair and os.path.exists(pair) else []))
    batches, cur = [], []
    for g in groups:
        if cur and len(cur) + len(g) > a.batch:
            batches.append(cur); cur = []
        cur += g
    if cur:
        batches.append(cur)
    prompt_head = (
        "You are the independent judge of a watch pass on a 9:16 vertical ad (1080x1920). Nobody has looked at it "
        "yet; you are that person. Be skeptical: the build believes it is fine. Judge EVERY image given below, one "
        "entry per image at least (several if an image has several findings).\n\n"
        "A 'sheet' is a contact sheet of exact frames across the runtime: judge framing, hair at the top edge, cards, "
        "labels, captions, junk. A 'strip_*' is five CONSECUTIVE frames at -2/-1/0/+1/+2 around a boundary; its "
        "'pair_*' is the -1|0 pair at half resolution: a jump cut is visible ONLY there (same scene both sides, the "
        "subject jumps). The strip's file name says what the plan declares at that boundary (card in/out, join, "
        "punch_FAR/NEAR, flash, cta, lt, ...).\n\n" + DESIGN_FACTS + "\n\nCHECKLIST:\n" + ck + "\n\n"
        "Answer with JSON only: {\"entries\": [{\"image\": \"<exact file name>\", \"verdict\": \"clean\"|\"defect\"|"
        "\"expected\", \"item\": \"<checklist key for a defect, else empty>\", \"t\": <seconds from the name>, "
        "\"note\": \"<what you saw; for expected, what the plan declares>\"}]}. Use the checklist keys exactly: "
        + ", ".join(keys) + ". When unsure whether something is a defect, call it a defect and say why.")
    entries = []
    for bi, batch in enumerate(batches):
        names = [os.path.basename(p) for p in batch]
        prompt = prompt_head + "\n\nThe images in this call, in order: " + ", ".join(names)
        res = AI.judge(batch, prompt, purpose="judge", model=a.model)
        answered = {e.get("image") for e in (res or {}).get("entries", []) if isinstance(e, dict)}
        missing = [p for p in batch if os.path.basename(p) not in answered]
        if missing:                                       # ask again for the ones it skipped
            res2 = AI.judge(missing, prompt_head + "\n\nThe images in this call, in order: " +
                            ", ".join(os.path.basename(p) for p in missing), purpose="judge", model=a.model)
            res = dict(entries=(res or {}).get("entries", []) + (res2 or {}).get("entries", []))
        for n in names:
            es = [e for e in (res or {}).get("entries", []) if isinstance(e, dict) and e.get("image") == n]
            if not es:                                    # an image the model did not answer for is NOT clean
                es = [dict(image=n, verdict="defect", item="junk_card", t=t_of(n),
                           note="judge returned no verdict for this image: not inspected, re-judge")]
            for e in es:
                e["t"] = float(e.get("t") or t_of(n))
                if e.get("verdict") not in ("clean", "defect", "expected"):
                    e["verdict"] = "defect"; e["note"] = f"unparseable verdict {e.get('verdict')!r}: " + str(e.get("note", ""))
                if e["verdict"] == "defect" and e.get("item") not in keys:
                    e["note"] = f"(item was {e.get('item')!r}) " + str(e.get("note", "")); e["item"] = "junk_card"
                entries.append(dict(image=n, verdict=e["verdict"], item=e.get("item", "") if e["verdict"] == "defect" else "",
                                    t=e["t"], note=str(e.get("note", ""))[:600]))
        print(f"batch {bi + 1}/{len(batches)}: {len(names)} images, "
              f"{sum(1 for e in entries if e['verdict'] == 'defect')} defects so far; spend {AI.ledger.total()['usd']}", flush=True)
    # split into parts like three session judges (kit_fold.sh merges findings_part*.json)
    per = -(-len(entries) // a.parts)
    for i in range(a.parts):
        part = entries[i * per:(i + 1) * per]
        json.dump(dict(judge=f"Gemini judge ({a.model}) part {i + 1}", video=os.path.basename(a.video),
                       method=f"gemini_judge.py: every image, batches of {a.batch}, design facts + CHECKLIST.md",
                       entries=part), open(os.path.join(out_dir, f"findings_part{i + 1}.json"), "w"), indent=1)
    d = [e for e in entries if e["verdict"] == "defect"]
    print(f"gemini judge: {len(entries)} entries, {len(d)} defects; spend {AI.ledger.total()}")
    for e in d:
        print("  DEFECT", e["t"], e["item"], e["image"], e["note"][:160])
    return 0


if __name__ == "__main__":
    sys.exit(main())
