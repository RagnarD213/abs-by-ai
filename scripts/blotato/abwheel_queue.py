#!/usr/bin/env python3
"""Queue "The $17 Ab Wheel Beats Every Crunch" (Muhammad's cut) + its 5 approved Shorts in Blotato.

Dan, 2026-09-10: "set this up in our blotato queue on all platforms". YouTube is NOT in here —
it gets the full-quality master straight from scripts/youtube/upload.js at the same times,
because Blotato caps uploads at 400 MB (the master is 1.1 GB) and every YouTube post through
Blotato would also spend one of the plan's 200 scheduled slots.

  * long-form  Sun 2026-09-13 14:00Z (9 AM CT) on Facebook, IG @danrosefit, TikTok; the
               @abs.by.ai mirror a day later. 9 AM keeps it off the 5 PM photo/Short slot.
               Facebook gets NO mediaType (FB Reels cap at 90 s; a long-form is a plain video).
  * shorts     5 PM CT, Tue/Thu/Sat, appended where the Reels queue ends (Oct 24) so no slot
               is shared on ANY platform, YouTube's native Shorts queue included: Oct 27 / 29 /
               31, Nov 3 / 5 — one every 2-3 days. (Oct 3 and Oct 15 have no Reel, but
               @danrosefit has a photo in both 5 PM slots — this script's clash check caught
               it.) The @abs.by.ai mirror posts the next day, as every other mirror does.
               5 PM is 22:00Z until Nov 1 and 23:00Z after (CDT -> CST).
  * captions   house format of the live queue: hook / body / closer / CTA / 5 hashtags.
               IG CTA = ManyChat keyword ABS (ab training), link in the auto first comment;
               the mirror points at @danrosefit; FB and TikTok carry the link in the text.

Idempotent: a post counts as done when a schedule already exists for that account at that
time whose payload carries this batch's utm_content. Blotato re-hosts media under a new UUID
on create, so a media-URL comparison cannot be used for that. Refuses to create anything if
a planned slot is already taken or the queue would pass the plan cap.

    python3 scripts/blotato/abwheel_queue.py            # dry run: plan + checks
    python3 scripts/blotato/abwheel_queue.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402

QUEUE_CAP = 200
FACEBOOK, FB_PAGE = "47105", "1294282227094660"
IG_MAIN, IG_MIRROR, TIKTOK = "67203", "65632", "58181"
MEDIA = "https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/"

TIKTOK_TARGET = {
    "targetType": "tiktok", "privacyLevel": "PUBLIC_TO_EVERYONE",
    "disabledComments": False, "disabledDuet": False, "disabledStitch": False,
    "isBrandedContent": False, "isYourBrand": True, "isAiGenerated": False,
}

LONGFORM = {
    "key": "longform", "utm": "utm_medium=video&utm_campaign=longform&utm_content=abwheel",
    "video": MEDIA + "80eb9e28-60b4-4159-b4f2-bd5f840da8e6.mp4", "cover": None,
    "main": "2026-09-13T14:00:00.000Z", "mirror": "2026-09-14T14:00:00.000Z",
    "hook": "This $17 infomercial gimmick beats every crunch.",
    "body": "The ab wheel keeps your abs under tension for the whole rep, scales from total beginner "
            "to advanced, and hits every ab muscle at once. Here's exactly how to use it: flat back, "
            "locked-out arms, slow rollouts, and how far to roll at your level.",
    "close": "Three live sets at the end so you can see the pace.",
    "tags": "#abwheel #abworkout #homeworkout #sixpackabs #fitnessover40",
    "mirror_cta": "More ab workouts from @danrosefit 👇",
}

SHORTS = [
    {"n": 1, "video": "3d16c448-f21a-4176-b71b-3781e8b6d543.mp4", "cover": "020b1770-8b0e-4e8d-a38b-6e57a9fc8572.png",
     "main": "2026-10-27T22:00:00.000Z", "mirror": "2026-10-28T22:00:00.000Z",
     "hook": "Your abs never get a break on the ab wheel.",
     "body": "A crunch has two built-in rest stops, at the top and at the bottom. The ab wheel keeps your "
             "abs working through the entire rep, and time under tension is what builds them.",
     "close": "The $17 infomercial gimmick that actually works.",
     "tags": "#abwheel #abs #abworkout #homeworkout #sixpackabs"},
    {"n": 2, "video": "4632a717-59b6-40cb-b823-2c51a55c2a45.mp4", "cover": "d684371b-667b-426f-9e5d-eb6dfc62466c.png",
     "main": "2026-10-29T22:00:00.000Z", "mirror": "2026-10-30T22:00:00.000Z",
     "hook": "The biggest ab wheel mistake is an arched back.",
     "body": "Keep your back flat, then lock your arms out straight with your knuckles facing the ground. "
             "Bend your arms and your chest takes over the work your abs should be doing.",
     "close": "Two fixes, and the same rollout gets a lot harder.",
     "tags": "#abwheel #abworkout #formcheck #homeworkout #sixpackabs"},
    {"n": 3, "video": "471e0e0b-0908-4e9e-bd14-98e7bd2768f2.mp4", "cover": "82b6415b-8550-45fa-96db-1fa8363d7d65.png",
     "main": "2026-10-31T22:00:00.000Z", "mirror": "2026-11-01T23:00:00.000Z",
     "hook": "How far should you roll out on the ab wheel?",
     "body": "Beginners go a few inches and come back. Intermediate goes farther. Advanced goes nose to "
             "the ground. At every level your arms stay locked and the pace stays slow.",
     "close": "Add an inch or two each workout until you reach full extension.",
     "tags": "#abwheel #abworkout #beginnerworkout #homeworkout #sixpackabs"},
    {"n": 4, "video": "df3e814f-e03a-40b7-bf1a-e0763c22de4b.mp4", "cover": "1e1fc72e-7b32-44e6-9f65-dd344c7708e2.png",
     "main": "2026-11-03T23:00:00.000Z", "mirror": "2026-11-04T23:00:00.000Z",
     "hook": "You're rolling out too fast.",
     "body": "A fast rep skips the tension that actually works your abs. Roll out slow and controlled "
             "and every rep gives you twice the time under tension.",
     "close": "Same wheel, same exercise, a lot more work.",
     "tags": "#abwheel #abworkout #timeundertension #homeworkout #sixpackabs"},
    {"n": 5, "video": "2366fad0-b0f6-471c-b7de-058c1e18c202.mp4", "cover": "327ac691-eb8d-4bc8-88a5-6656cf4c6fcb.png",
     "main": "2026-11-05T23:00:00.000Z", "mirror": "2026-11-06T23:00:00.000Z",
     "hook": "Crunches mostly train one ab muscle.",
     "body": "The ab wheel hits your rectus abdominis, your transverse abdominis and your obliques at "
             "the same time, and works your chest, shoulders and arms on top of that.",
     "close": "One $17 tool, every ab muscle.",
     "tags": "#abwheel #crunches #abworkout #homeworkout #sixpackabs"},
]
for s in SHORTS:
    s.update(key=f"abwheel-short{s['n']}", video=MEDIA + s["video"], cover=MEDIA + s["cover"],
             utm=f"utm_medium=reel&utm_campaign=abwheel&utm_content=abwheel-short{s['n']}",
             mirror_cta="Full breakdown from @danrosefit 👇")


def link(v: dict, source: str) -> str:
    return f"https://absbyai.com/?utm_source={source}&{v['utm']}"


def posts_for(v: dict) -> list:
    lede = f"{v['hook']}\n\n{v['body']}\n\n{v['close']}\n\n"
    is_short = v["key"] != "longform"
    ig = {"targetType": "instagram", "mediaType": "reel", "shareToFeed": True,
          "firstComment": f"See what you'd look like with a six-pack: {link(v, 'instagram')}"}
    if v["cover"]:
        ig["coverImageUrl"] = v["cover"]
    fb = {"targetType": "facebook", "pageId": FB_PAGE}
    if is_short:
        fb["mediaType"] = "reel"
    return [
        (FACEBOOK, "facebook", v["main"], fb,
         lede + f"See what you'd look like with a six-pack — free AI preview:\n{link(v, 'facebook')}\n\n{v['tags']}"),
        (IG_MAIN, "instagram", v["main"], dict(ig),
         lede + f"Comment ABS and I'll send you the free AI preview 👇\n\n{v['tags']}"),
        (TIKTOK, "tiktok", v["main"], dict(TIKTOK_TARGET),
         lede + f"Free AI preview of your own six-pack — link in bio at AbsByAI.com 👇\n\n{link(v, 'tiktok')}\n\n{v['tags']}"),
        (IG_MIRROR, "instagram", v["mirror"], dict(ig),
         lede + f"{v['mirror_cta']}\n\n{v['tags']}"),
    ]


def marker(v: dict) -> str:
    return v["utm"].split("utm_content=")[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    key = api_key()
    items = fetch_schedules(key)

    def existing(acct: str, when: str) -> list:
        return [i for i in items if str(i.get("accountId") or i["draft"].get("accountId")) == acct
                and (i.get("scheduledAt") or "")[:16] == when[:16]]

    plan, bad = [], 0
    for v in [LONGFORM] + SHORTS:
        for acct, platform, when, target, text in posts_for(v):
            clash = existing(acct, when)
            done = [i for i in clash if f"utm_content={marker(v)}" in json.dumps(i)]
            if done:
                print(f"  done   {v['key']:16} {platform:9} {acct} {when}  (schedule {done[0]['id']})")
                continue
            if clash:
                bad += 1
                print(f"  CLASH  {v['key']:16} {platform:9} {acct} {when}  already holds {clash[0]['id']}")
                continue
            plan.append((v, acct, platform, when, target, text))
            print(f"  create {v['key']:16} {platform:9} {acct} {when}")

    print(f"\nqueue now {len(items)}, to create {len(plan)}, after {len(items) + len(plan)} of {QUEUE_CAP}")
    if bad or len(items) + len(plan) > QUEUE_CAP:
        print("REFUSING: slot clash or over the plan cap")
        return 1
    if not args.apply:
        print("dry run — pass --apply to create")
        return 0

    for v, acct, platform, when, target, text in plan:
        body = {"post": {"accountId": acct, "target": target,
                         "content": {"platform": platform, "text": text, "mediaUrls": [v["video"]]}},
                "scheduledTime": when}
        res = call("POST", "/posts", key, body)
        print(f"  created {v['key']:16} {platform:9} {when}  -> {res.get('postSubmissionId', res)}")

    # Verify against a fresh pull, not the create responses.
    after = fetch_schedules(key)
    missing = 0
    for v in [LONGFORM] + SHORTS:
        for acct, platform, when, _t, text in posts_for(v):
            hit = [i for i in after if str(i.get("accountId") or i["draft"].get("accountId")) == acct
                   and (i.get("scheduledAt") or "")[:16] == when[:16]
                   and f"utm_content={marker(v)}" in json.dumps(i)]
            ok = len(hit) == 1 and hit[0]["draft"]["content"]["text"] == text and hit[0]["draft"]["content"]["mediaUrls"]
            missing += 0 if ok else 1
            print(f"  {'OK  ' if ok else 'FAIL'} {v['key']:16} {platform:9} {when}  {hit[0]['id'] if hit else '—'}")
    print(f"\nverified: queue {len(after)} of {QUEUE_CAP}, {missing} problem(s)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
