#!/usr/bin/env python3
"""Queue ONE finished long-form video on Facebook, IG @danrosefit, TikTok and the IG @abs.by.ai mirror
(next day) through Blotato, from a small JSON config. The generic form of ad5_queue.py / abwheel_queue.py,
used by the /video-setup skill.

YouTube is NOT in here: it is scheduled natively with scripts/youtube/upload.js --publish-at (full-quality
master, no Blotato slot, no 400 MB cap). Facebook gets no mediaType (FB Reels cap at 90 s).

Config (JSON):
  {
    "content_type": "organic",                 # REQUIRED. Ads never go organic - scripts/blotato/ad_guard.py
    "slug": "abwheel-workout",                 # utm_content + idempotency marker
    "video_url": "https://database.blotato.io/...mp4",   # from blotato_create_presigned_upload_url + PUT
    "main": "2026-09-20T14:00:00.000Z",        # FB / IG main / TikTok
    "mirror": "2026-09-21T14:00:00.000Z",      # IG @abs.by.ai
    "keyword": "ABS",                          # ManyChat keyword, Docs/MANYCHAT_KEYWORDS.md
    "ai_generated": true,                      # TikTok isAiGenerated (any AI image on screen)
    "hook": "...", "body": "...", "close": "...",
    "tags": "#a #b",
    "mirror_cta": "More from @danrosefit 👇",
    "source": "Zeeshan Content Videos/.../file.mp4"   # optional; checked against the ad folders
  }

Idempotent: a post counts as done when a schedule exists for that account at that time whose payload
carries utm_content=<slug>. Refuses on a slot clash or if the queue would pass the plan cap.

    python3 scripts/blotato/longform_queue.py CONFIG.json           # dry run
    python3 scripts/blotato/longform_queue.py CONFIG.json --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ad_guard import AdGuardError, assert_organic  # noqa: E402
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402

QUEUE_CAP = 200
FACEBOOK, FB_PAGE = "47105", "1294282227094660"
IG_MAIN, IG_MIRROR, TIKTOK = "67203", "65632", "58181"


def posts(v: dict) -> list:
    utm = f"utm_medium=video&utm_campaign=longform&utm_content={v['slug']}"
    link = lambda source: f"https://absbyai.com/?utm_source={source}&{utm}"  # noqa: E731
    lede = f"{v['hook']}\n\n{v['body']}\n\n{v['close']}\n\n"
    ig = {"targetType": "instagram", "mediaType": "reel", "shareToFeed": True,
          "firstComment": f"See what you'd look like with a six-pack: {link('instagram')}"}
    tiktok = {"targetType": "tiktok", "privacyLevel": "PUBLIC_TO_EVERYONE",
              "disabledComments": False, "disabledDuet": False, "disabledStitch": False,
              "isBrandedContent": False, "isYourBrand": True, "isAiGenerated": bool(v["ai_generated"])}
    return [
        (FACEBOOK, "facebook", v["main"], {"targetType": "facebook", "pageId": FB_PAGE},
         lede + f"See what you'd look like with a six-pack — free AI preview:\n{link('facebook')}\n\n{v['tags']}"),
        (IG_MAIN, "instagram", v["main"], dict(ig),
         lede + f"Comment {v['keyword']} and I'll send you the free AI preview 👇\n\n{v['tags']}"),
        (TIKTOK, "tiktok", v["main"], tiktok,
         lede + f"Free AI preview of your own six-pack — link in bio at AbsByAI.com 👇\n\n{link('tiktok')}\n\n{v['tags']}"),
        (IG_MIRROR, "instagram", v["mirror"], dict(ig),
         lede + f"{v['mirror_cta']}\n\n{v['tags']}"),
    ]


def acct_of(i: dict) -> str:
    return str(i.get("accountId") or i["draft"].get("accountId"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    v = json.load(open(args.config))

    # Ads are never published organically (Dan, 2026-09-17). Runs before any API call, on the
    # captions that are actually going out - not on the config's good intentions.
    try:
        assert_organic(v, texts=[v.get("hook"), v.get("body"), v.get("close"),
                                 v.get("title"), v.get("mirror_cta")],
                       sources=[v["source"]] if v.get("source") else [])
    except AdGuardError as exc:
        print(f"REFUSING - ad_guard: {exc}")
        return 1

    key = api_key()
    items = fetch_schedules(key)
    marker = f"utm_content={v['slug']}"

    plan, bad = [], 0
    for acct, platform, when, target, text in posts(v):
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
                         "content": {"platform": platform, "text": text, "mediaUrls": [v["video_url"]]}},
                "scheduledTime": when}
        res = call("POST", "/posts", key, body)
        print(f"  created {platform:9} {when}  -> {res.get('postSubmissionId', res)}")

    # Verify against a fresh pull, not the create responses.
    after = fetch_schedules(key); missing = 0
    for acct, platform, when, _t, text in posts(v):
        hit = [i for i in after if acct_of(i) == acct and (i.get("scheduledAt") or "")[:16] == when[:16]
               and marker in json.dumps(i)]
        ok = len(hit) == 1 and hit[0]["draft"]["content"]["text"] == text and hit[0]["draft"]["content"]["mediaUrls"]
        missing += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {platform:9} {when}  {hit[0]['id'] if hit else '—'}")
    print(f"\nverified: queue {len(after)} of {QUEUE_CAP}, {missing} problem(s)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
