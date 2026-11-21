#!/usr/bin/env python3
"""TURN DAN'S BLIND ANSWERS INTO CORPUS ENTRIES -- his words verbatim, the sha256 of the exact file he
watched, the verdict from his pick, whichever way it went.

  python3 record_verdict.py --dir DIR [--date YYYY-MM-DD] [--prefix kit9x16-ad1-blind]   -> prints the entries as JSON

DIR holds key.json (sealed mapping) and answers.json (what the page saved). For each pair the two files
get one entry each: the picked side `approved` ("blind pick"), the other `rejected` ("blind: not picked"),
a tie `approved-with-notes` on both. Nothing is written into corpus.json by this script -- a person
reads the entries, checks `must_pass` / `must_trigger` make sense for the kit's file, and adds them
in the same session (AGENTS.md: a new rejection becomes a corpus entry in the same session it happens).
"""
import argparse
import datetime
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--prefix", default="kit9x16-ad1-blind")
    a = ap.parse_args()
    key = json.load(open(os.path.join(a.dir, "key.json")))
    ans_p = os.path.join(a.dir, "answers.json")
    if not os.path.exists(ans_p):
        raise SystemExit("no answers.json yet -- Dan has not answered")
    answers = json.load(open(ans_p))
    latest = {}
    for x in answers:                                  # the last answer per pair stands
        latest[x["pair"]] = x
    out = []
    for p in key["pairs"]:
        x = latest.get(p["pair"])
        if not x:
            print(f"pair {p['pair']}: no answer")
            continue
        pick = x["pick"]
        for side in ("left", "right"):
            f = p[side]
            if pick == "tie":
                verdict, note = "approved-with-notes", "blind A/B: a tie"
            elif pick == side:
                verdict, note = "approved", "blind A/B: Dan's pick"
            else:
                verdict, note = "rejected", "blind A/B: not picked"
            out.append(dict(
                id=f"{a.prefix}-{p['pair'].lower()}-{f['name']}", verdict=verdict, date=a.date,
                root="repo" if f["source"].startswith("/Users/") else "ssd",
                path=f["source"], sha256=f["sha256"],
                dan=x.get("why", "").strip() or "(no words given)",
                dan_pick=pick, blind_pair=p["pair"], blind_side=side, blind_title=p["title"],
                must_trigger=[], must_pass=[],
                measured=f"{note}; the file served as `{f['served']}` (order randomised, labels hidden); answered {x.get('when')}",
                notes="Phase 4 blind test (handoff-20260916-vqc-phase4-locked-kit.md). must_pass / must_trigger to be "
                      "filled by the session that records it, from the gate rows of this exact file.",
            ))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
