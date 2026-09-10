#!/usr/bin/env python3
"""Queue Ad 5 "Every Diet You've Tried Failed for the Same Reason" (Muhammad V3 HD, 3:55) in Blotato.

Dan, 2026-09-10: "upload it to YouTube and set it up on all other platforms in the Blotato queue".
Same shape as abwheel_queue.py's long-form: YouTube is NOT in here — it is scheduled natively by
scripts/youtube/upload.js --publish-at at the same time (full-quality master, no Blotato slot spent).

  * Wed 2026-09-16 14:00Z (9 AM CT) on Facebook, IG @danrosefit, TikTok; the @abs.by.ai mirror a day
    later. 9 AM keeps it off the 5 PM photo/Short slot. Facebook gets NO mediaType (FB Reels cap at 90 s).
  * Media is the untouched 311 MB master (under Blotato's 400 MB cap), uploaded to Blotato storage.
  * IG CTA = ManyChat keyword FOOD (the video is about diets and meal plans — Docs/MANYCHAT_KEYWORDS.md).
  * Links go to the absbyai.com root, not /start, so organic traffic stays out of the /start A/B test.

Idempotent: a post counts as done when a schedule exists for that account at that time whose payload
carries utm_content=ad5-every-diet. Refuses on a slot clash or if the queue would pass the plan cap.

    python3 scripts/blotato/ad5_queue.py            # dry run: plan + checks
    python3 scripts/blotato/ad5_queue.py --apply
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
    "isBrandedContent": False, "isYourBrand": True, "isAiGenerated": True,
}

V = {
    "key": "ad5-longform", "utm": "utm_medium=video&utm_campaign=longform&utm_content=ad5-every-diet",
    "video": MEDIA + "2dbcb385-5ea7-4ac1-9f53-69960366219b.mp4",
    "main": "2026-09-16T14:00:00.000Z", "mirror": "2026-09-17T14:00:00.000Z",
    "hook": "Every diet you've tried failed for the same reason. It isn't willpower.",
    "body": "Day one you're motivated. Day eleven you're tired, your kid is sick, work is a disaster and "
            "there's a pizza in the kitchen. Your diet doesn't lose to a craving, it loses to a bad week. "
            "Here's what kept me on my plan every single day, and why a meal plan built around the foods "
            "you actually like beats any plan you download.",
    "close": "Same eating plan. Same workouts. Two changes.",
    "tags": "#dietplan #mealplan #fatloss #sixpackabs #aifitness",
    "mirror_cta": "More from @danrosefit 👇",
}


def link(source: str) -> str:
    return f"https://absbyai.com/?utm_source={source}&{V['utm']}"


def posts() -> list:
    lede = f"{V['hook']}\n\n{V['body']}\n\n{V['close']}\n\n"
    ig = {"targetType": "instagram", "mediaType": "reel", "shareToFeed": True,
          "firstComment": f"See what you'd look like with a six-pack: {link('instagram')}"}
    return [
        (FACEBOOK, "facebook", V["main"], {"targetType": "facebook", "pageId": FB_PAGE},
         lede + f"See what you'd look like with a six-pack — free AI preview:\n{link('facebook')}\n\n{V['tags']}"),
        (IG_MAIN, "instagram", V["main"], dict(ig),
         lede + f"Comment FOOD and I'll send you the free AI preview 👇\n\n{V['tags']}"),
        (TIKTOK, "tiktok", V["main"], dict(TIKTOK_TARGET),
         lede + f"Free AI preview of your own six-pack — link in bio at AbsByAI.com 👇\n\n{link('tiktok')}\n\n{V['tags']}"),
        (IG_MIRROR, "instagram", V["mirror"], dict(ig),
         lede + f"{V['mirror_cta']}\n\n{V['tags']}"),
    ]


def acct_of(i: dict) -> str:
    return str(i.get("accountId") or i["draft"].get("accountId"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    key = api_key()
    items = fetch_schedules(key)
    marker = f"utm_content={V['utm'].split('utm_content=')[1]}"

    plan, bad = [], 0
    for acct, platform, when, target, text in posts():
        clash = [i for i in items if acct_of(i) == acct and (i.get("scheduledAt") or "")[:16] == when[:16]]
        done = [i for i in clash if marker in json.dumps(i)]
        if done:
            print(f"  done   {platform:9} {acct} {when}  (schedule {done[0]['id']})"); continue
        if clash:
            bad += 1; print(f"  CLASH  {platform:9} {acct} {when}  already holds {clash[0]['id']}"); continue
        plan.append((acct, platform, when, target, text)); print(f"  create {platform:9} {acct} {when}")

    print(f"\nqueue now {len(items)}, to create {len(plan)}, after {len(items) + len(plan)} of {QUEUE_CAP}")
    if bad or len(items) + len(plan) > QUEUE_CAP:
        print("REFUSING: slot clash or over the plan cap"); return 1
    if not args.apply:
        print("dry run — pass --apply to create"); return 0

    for acct, platform, when, target, text in plan:
        body = {"post": {"accountId": acct, "target": target,
                         "content": {"platform": platform, "text": text, "mediaUrls": [V["video"]]}},
                "scheduledTime": when}
        res = call("POST", "/posts", key, body)
        print(f"  created {platform:9} {when}  -> {res.get('postSubmissionId', res)}")

    # Verify against a fresh pull, not the create responses.
    after = fetch_schedules(key); missing = 0
    for acct, platform, when, _t, text in posts():
        hit = [i for i in after if acct_of(i) == acct and (i.get("scheduledAt") or "")[:16] == when[:16]
               and marker in json.dumps(i)]
        ok = len(hit) == 1 and hit[0]["draft"]["content"]["text"] == text and hit[0]["draft"]["content"]["mediaUrls"]
        missing += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {platform:9} {when}  {hit[0]['id'] if hit else '—'}")
    print(f"\nverified: queue {len(after)} of {QUEUE_CAP}, {missing} problem(s)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
