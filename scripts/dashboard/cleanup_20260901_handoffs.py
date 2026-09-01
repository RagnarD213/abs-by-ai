#!/usr/bin/env python3
"""One-off Victory Dashboard cleanup (2026-09-01).

Removes business-list rows that are either (a) executed and verified in the
coordination record, or (b) superseded so they no longer need executing.
Keyed on EXACT task text, so it is safe to re-run against a todos.json that has
moved on since it was written: a row that is already gone is simply reported.

Usage:  python3 scripts/dashboard/cleanup_20260901_handoffs.py [--apply]
"""
import json, sys, pathlib

REMOVE = [
    # --- executed handoffs (verified in AI_COORDINATION.md / archive) ---
    ("Execute handoff: Write 4 approved ad outlines + brainstorm 20 skip-stopper-first ideas",
     "batch-4 outlines delivered 8/18; AI_COORDINATION.md names this row as the completed task"),
    ("Execute handoff: Replace stick figures with AI exercise demo videos",
     "superseded by the batch handoffs; 33 demos built and INSTALLED live 8/21-8/22. Remaining exercises are covered by 'Build AI animations for the workout program exercises'"),
    ("Execute handoff: Ad 1 rev-4 (busy-dad clip + tag fix) then 9:16 build",
     "rev-4 shipped 8/21 and the 9:16 exists; was checked off 8/25 and the check was later swept"),
    ("Execute handoff: YouTube subscriber campaign geo restructure (all-countries + tier-1 clone)",
     "Steps 0-2 done 8/22; Step 3 clone confirmed complete 8/26 - tier 1 + RMKTG campaigns are live in the 8/31 pull"),
    ("Execute handoff: Ad 1 vertical ATTEMPT 2 - exact copy of Muhammad's final, then Dan cuts the script",
     "attempt 2 delivered 8/26, then superseded by attempt 3 and revs 1-4"),
    ("Execute handoff: Ad 1 vertical ATTEMPT 3 - indistinguishable from Muhammad's edit",
     "attempt 3 delivered 8/26; rev 4 is the FINAL, QC 16/16"),
    ("Execute handoff: clear the claimed music bed from V5 (workout-only longform)",
     "V5 bed swapped and delivered 8/28; only the YouTube-side decision is left and that is Dan's, not a session's"),
    ("Execute handoff: clear the claimed music bed from V4 (1 Minute Ab Workout longform)",
     "V4 bed swapped and delivered 8/28; same - the YouTube action is Dan's call"),
    ("Execute handoff: cut Shorts from the supplements long-form (03)",
     "eight Shorts delivered through rev 4 (8/30); posting is blocked on the parent long-form's packaging, not on this handoff"),
    ("Execute the Instagram growth plan (7 profile fixes + Blotato queue rework)",
     "migration steps 1-5 executed and verified live 8/25; step 6's four reels are covered by 'Produce short-form CONTENT'"),
    ("Approve Ad 1 rev-1, apply final revisions, finalize the /ad-edit skill",
     "long superseded - our pipeline reached rev-5, then Dan chose Muhammad's cut as the finished Ad 1 (see the 'Launch Google Ads campaigns with finished Ad 1' task). /ad-edit was finalized through lessons 50-61."),
    ("Fix two-mic comb-filter audio on the 4 remaining delivered longform masters (Zepbound, supplements, invest-health, meal prep)",
     "all four delivered and verified 8/23"),

    # --- done / decided, no longer needs executing ---
    ("Send Muhammad the offer on Upwork (editor hire)",
     "Upwork job 2093108552765647365 posted and Muhammad invited 8/27; he has since delivered Ads 1 and 2"),
    ("Decide the video-editing stack: Upwork trial results vs /longform-edit pipeline vs Grokbot (evaluate/sign up)",
     "decided 8/24: in-house pipeline with the gate enforced, plus Muhammad on the 12-ad batch"),
    ("Plan the permanent filming set (studio build vs kitchen)",
     "spec + priced gear list delivered 8/31 (artifact v2). The live follow-on is the 'Order the filming-set gear' task"),
    ("Audit that the newest app features are actually advertised in the Meta + Google Ads engagement campaigns",
     "audited 8/26 - answer is no: trainer/nutritionist/supplement-audit/sleep-coach appear in zero ads. Acting on it is separate creative work"),
    ("Remove backgrounds from the finalized studio photos + test cutout-style thumbnails",
     "all 100 studio finals cut out 8/31, approved by Dan and promoted to the /background-removal skill. The cutout-thumbnail A/B was never run - re-add if you still want it"),
    ("Check Google Ads performance since the 8/18 search launch (spend, clicks, conversions)",
     "covered by the 8/26 paid audit and the 8/31 Aug 26-31 pull"),
    ("Check Meta ad campaigns (spend, results, any disapprovals)",
     "covered by the same two pulls; the one live finding is carried forward as a new task"),
    ("Advertise latest video on Google Ads (engagement campaign) + scope Claude automation for these",
     "the automation scoping produced handoff-20260831-google-ads-api-setup...; launching is covered by the 'Launch Google Ads campaigns with finished Ad 1' task"),
    ("Plan the next photo shoot",
     "the 8/27 Snappr studio shoot happened and produced 100 finished picks"),
    ("Confirm the next video shoot date does NOT collide with the photo shoot",
     "moot - the photo shoot took place 8/27"),
    ("Review the 5 parked video deliverables (3x 8/3 longform, invest-health v2, ab-wheel)",
     "names superseded artifacts (invest-health is on v3 + two cutdowns; ab-wheel was rebuilt and approved). The live remainder is folded into the five-longforms task's note"),
]

# Rows whose `why` no longer matches reality.
REWRITE_WHY = {
    "Execute handoff: Bring the 5 delivered longforms up to the new /longform-edit standard":
        "handoff-20260824-five-longforms-to-new-standard.md - 4 of 5 DONE (05, 01, 02, 03 delivered 8/27). Only 04 invest-health remains and it is blocked on Dan picking a cutdown variant (conservative 43:31 vs sub30 28:25). Also still owed: Dan watching the three rebuilt review copies.",
    "Execute handoff: fill danrosefit + abs.by.ai image-post gap days (write captions, schedule in Blotato)":
        "handoff-20260826-danrosefit-abs-image-gap-fill.md - 63 of 70 scheduled and verified live 8/26. The last 7 are blocked on Blotato's 200-post plan cap: delete queued posts or upgrade the plan, then re-run scripts/blotato/iggap_fill.py --apply (idempotent).",
}

ADD = [
    {"text": "Decide whether both Meta ad campaigns being toggled OFF was intentional",
     "priority": "high",
     "why": "8/31 paid pull: [DAN] [ENGAGEMENT] and [DAN] [ENGAGEMENT] IG GEO are both switched off (IG GEO spent $13.26 then stopped), and 3 unpublished draft edits are still pending. Carried over from the deleted Meta-check task.",
     "addedAt": "2026-09-01"},
]

def main():
    apply = "--apply" in sys.argv
    p = pathlib.Path(__file__).resolve().parents[2] / "todos.json"
    d = json.loads(p.read_text())
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
            t["why"] = REWRITE_WHY[t["text"]]
            rewritten.append(t["text"])

    added = []
    have = {t.get("text") for t in d["business"]}
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

    if apply:
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False))  # byte-match saveTodosToGitHub()
        print("\nWROTE todos.json")
    else:
        print("\n(dry run - pass --apply to write)")

if __name__ == "__main__":
    main()
