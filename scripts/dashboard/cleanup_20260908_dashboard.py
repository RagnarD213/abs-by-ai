#!/usr/bin/env python3
"""Victory Dashboard sweep (2026-09-08) — Dan asked for every done / superseded
handoff row to come off the board.

Writes through the live API (GET, edit, POST with allowDeletes) rather than the
local todos.json, so it can never clobber a concurrent server write. Keyed on
EXACT task text; a row that is already gone is reported, not an error.

Usage:  python3 scripts/dashboard/cleanup_20260908_dashboard.py [--apply]
Needs DASH_SECRET in ~/.absbyai-secrets.env.
"""
import json, os, sys, urllib.request, pathlib

BASE = "https://absbyai.com"

REMOVE = [
    # --- executed / verified in AI_COORDINATION.md ---
    ("Set up ManyChat comment-to-DM on @danrosefit (33 queued posts already promise it)",
     "DONE — live on every @danrosefit post/reel (Pro), verified end to end comment→reply→DM→button→absbyai.com"),
    ("Send Muhammad the Ad 3 round-1 revisions (already in his Batch-2 doc) and the next ads that are ready for him",
     "DONE — Ad 3 r2 / Ad 4 r1 / Ad 5 r1 all sent 09-03; his V3 + Ads 6-8 first drafts are back and in today's sweep"),
    ("Review Zeshan's video cut and send round-1 revisions",
     "DONE — round 1 sent, round 2 reviewed 09-02, round 3 in today's editor sweep"),
    ("Execute handoff: Google Ads engagement champion — $5 test ad per new video in all 3 DGEN campaigns, one champion per campaign",
     "EXECUTED 09-03 — brain deployed (scripts/ads/ytads, 88 tests), Ads Script 12241942 installed; replaced by a single switch-on row below"),
    # --- superseded ---
    ("Start paid advertising for the @danrosefit Instagram (follower campaigns)",
     "SUPERSEDED — the @danrosefit profile-visits campaign has been LIVE since 09-02 at $6.50/day via the API script (Ads Manager can't run @danrosefit ads; the API can). The 09-01 ad-identity handoff is dead."),
    ("Build AI animations for the workout program exercises",
     "SUPERSEDED — 33 demos built and installed 8/21-22, batch 4's 9 candidates are on the board as their own review row"),
    ("Decide whether both Meta ad campaigns being toggled OFF was intentional",
     "SUBSUMED — Dan answered on 9/2 ('I've got to get my Meta engagement campaign working'); the 'Get the Meta engagement campaign running' row carries it"),
    ("Launch Google DGEN engagement ads for the newest videos (ab-wheel shorts + 3-min workout) per the 8/31 launch-spec artifact",
     "SUBSUMED — this is exactly what the engagement-champion automation does on its first live run; carried by the switch-on row"),
    # --- automated away ---
    ("Post on TikTok",
     "AUTOMATED — Blotato mirrors every reel to @absbyai; four posts published on schedule 09-03..09-08, zero failures. (Recurring row; deleted with allowDeletes.)"),
]

REWRITE_WHY = {
    "Execute handoff: fill danrosefit + abs.by.ai image-post gap days (write captions, schedule in Blotato)":
        "handoff-20260826-danrosefit-abs-image-gap-fill.md — 63 of 70 live. The last 7 need Blotato queue room: it sits at 200/200 and drains ~2/day, so a session can re-run scripts/blotato/iggap_fill.py --apply from ~09-12 with no decision from Dan.",
    "Execute handoff: RevenueCat restore-behavior audit (one Apple ID, multiple accounts)":
        "handoff-20260812-revenuecat-restore-behavior-audit.md — fire the day Apple approves (IN_REVIEW since 09-08)",
    "Execute handoff: Let users purchase before creating an account (iOS)":
        "handoff-20260812-purchase-before-account.md — fire AFTER approval and AFTER the RevenueCat audit",
}

ADD = [
    {"text": "Switch on the YouTube engagement champion: Dan authorizes Ads Script 12241942 (hourly) + creates the MCC developer token, then a session sets YTADS_ENABLED=1",
     "priority": "key",
     "why": "Built + deployed 09-03 (scripts/ads/ytads, Docs/YTADS.md). Two Dan clicks are the only blocker; the follow-up session refines headline-style.md, pins the tier-1/RMKTG ids, shows the dry-run pause list, then flips it live and watches the first hour.",
     "addedAt": "2026-09-08"},
]

def key():
    for line in pathlib.Path(os.path.expanduser("~/.absbyai-secrets.env")).read_text().splitlines():
        if line.startswith("DASH_SECRET="):
            return line.split("=", 1)[1].strip()
    sys.exit("DASH_SECRET not found")

def req(path, body=None):
    r = urllib.request.Request(BASE + path, headers={"X-Dash-Key": key(), "Content-Type": "application/json"},
                               data=json.dumps(body).encode() if body is not None else None,
                               method="POST" if body is not None else "GET")
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read())

def main():
    apply = "--apply" in sys.argv
    d = req("/api/todos")
    biz = d.get("business", [])
    by_text = {t.get("text"): t for t in biz}
    removed, missing = [], []
    for text, reason in REMOVE:
        (removed if text in by_text else missing).append((text, reason))
    kill = {t for t, _ in removed}
    d["business"] = [t for t in biz if t.get("text") not in kill]
    rewritten = []
    for t in d["business"]:
        if t.get("text") in REWRITE_WHY:
            t["why"] = REWRITE_WHY[t["text"]]; rewritten.append(t["text"])
    have = {t.get("text") for t in d["business"]}
    added = []
    for row in ADD:
        if row["text"] not in have:
            d["business"].append(row); added.append(row["text"])

    print(f"business: {len(biz)} -> {len(d['business'])}")
    print(f"\nREMOVED ({len(removed)}):")
    for t, r in removed: print(f"  - {t}\n      {r}")
    if missing:
        print(f"\nALREADY GONE ({len(missing)}):")
        for t, _ in missing: print(f"  - {t}")
    print(f"\nWHY REWRITTEN ({len(rewritten)}):")
    for t in rewritten: print(f"  ~ {t}")
    print(f"\nADDED ({len(added)}):")
    for t in added: print(f"  + {t}")

    if not apply:
        print("\n(dry run — pass --apply to write)"); return
    d["allowDeletes"] = [f"business::{t}" for t in kill]
    res = req("/api/todos", d)
    print("\nPOST:", json.dumps(res)[:300])
    back = req("/api/todos")
    still = [t for t in kill if any(x.get("text") == t for x in back.get("business", []))]
    print("VERIFY business count:", len(back.get("business", [])), "| still present:", still or "none")

if __name__ == "__main__":
    main()
