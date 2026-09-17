#!/usr/bin/env python3
"""Queue one approved organic Short across the five Abs By AI destinations.

The YouTube Data API holding copy remains Private. Blotato creates the public
release at the scheduled time, which is why the YouTube target below is public.
TikTok receives a one-frame cover-prefixed derivative and pins its cover to 0 ms.

Usage:
    python3 scripts/blotato/organic_short_queue.py CONFIG.json
    python3 scripts/blotato/organic_short_queue.py CONFIG.json --apply
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
IG_MAIN, IG_MIRROR, TIKTOK, YOUTUBE = "67203", "65632", "58181", "46963"


def account_id(item: dict) -> str:
    return str(item.get("accountId") or item.get("draft", {}).get("accountId"))


def post_plan(v: dict) -> list[dict]:
    slug = v["slug"]
    campaign = v["campaign"]
    tags = v["tags"]
    hook, body, close = v["hook"], v["body"], v["close"]
    lede = f"{hook}\n\n{body}\n\n{close}\n\n"

    def link(source: str) -> str:
        return (f"https://absbyai.com/?utm_source={source}&utm_medium=short"
                f"&utm_campaign={campaign}&utm_content={slug}")

    instagram_target = {
        "targetType": "instagram",
        "mediaType": "reel",
        "shareToFeed": True,
        "coverImageUrl": v["instagram_cover_url"],
        "firstComment": f"Try your free Abs By AI preview: {link('instagram')}",
    }
    tiktok_target = {
        "targetType": "tiktok",
        "privacyLevel": "PUBLIC_TO_EVERYONE",
        "disabledComments": False,
        "disabledDuet": False,
        "disabledStitch": False,
        "isBrandedContent": False,
        "isYourBrand": True,
        "isAiGenerated": bool(v["ai_generated"]),
        "videoCoverTimestamp": 0,
    }
    youtube_target = {
        "targetType": "youtube",
        "title": v["title"],
        "privacyStatus": "public",
        "shouldNotifySubscribers": True,
        "isMadeForKids": False,
        "containsSyntheticMedia": bool(v["ai_generated"]),
        "thumbnailUrl": v["youtube_cover_url"],
    }
    return [
        {
            "account": FACEBOOK,
            "platform": "facebook",
            "when": v["main"],
            "target": {"targetType": "facebook", "pageId": FB_PAGE, "mediaType": "reel"},
            "text": lede + f"Try your free Abs By AI preview:\n{link('facebook')}\n\n{tags}",
            "media": v["video_url"],
        },
        {
            "account": IG_MAIN,
            "platform": "instagram",
            "when": v["main"],
            "target": instagram_target,
            "text": lede + f"Comment {v['keyword']} and I'll send you the free preview 👇\n\n{tags}",
            "media": v["video_url"],
        },
        {
            "account": TIKTOK,
            "platform": "tiktok",
            "when": v["main"],
            "target": tiktok_target,
            "text": lede + f"Free Abs By AI preview — link in bio 👇\n\n{link('tiktok')}\n\n{tags}",
            "media": v["tiktok_video_url"],
        },
        {
            "account": IG_MIRROR,
            "platform": "instagram",
            "when": v["mirror"],
            "target": instagram_target,
            "text": lede + f"More from @danrosefit 👇\n\n{tags}",
            "media": v["video_url"],
        },
        {
            "account": YOUTUBE,
            "platform": "youtube",
            "when": v["main"],
            "target": youtube_target,
            "text": v["youtube_description"],
            "media": v["video_url"],
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    with open(args.config) as fh:
        v = json.load(fh)

    required = [
        "content_type", "source", "slug", "campaign", "title", "video_url",
        "tiktok_video_url", "instagram_cover_url", "youtube_cover_url", "main",
        "mirror", "keyword", "ai_generated", "hook", "body", "close", "tags",
        "youtube_description",
    ]
    missing = [key for key in required if key not in v or v[key] in (None, "")]
    if missing:
        print("REFUSING - missing config fields: " + ", ".join(missing))
        return 1
    url_fields = ["video_url", "tiktok_video_url", "instagram_cover_url", "youtube_cover_url"]
    bad_urls = [key for key in url_fields if not str(v[key]).startswith("https://")]
    if bad_urls:
        print("REFUSING - non-HTTPS media fields: " + ", ".join(bad_urls))
        return 1

    try:
        assert_organic(
            v,
            texts=[v["title"], v["hook"], v["body"], v["close"], v["youtube_description"]],
            sources=[v["source"]],
        )
    except AdGuardError as exc:
        print(f"REFUSING - ad_guard: {exc}")
        return 1

    key = api_key()
    items = fetch_schedules(key)
    marker = f"utm_content={v['slug']}"
    plan, problems = [], 0
    for p in post_plan(v):
        same_time = [
            item for item in items
            if account_id(item) == p["account"]
            and (item.get("scheduledAt") or "")[:16] == p["when"][:16]
        ]
        done = [item for item in same_time if marker in json.dumps(item)]
        if done:
            print(f"  done   {p['platform']:9} {p['account']} {p['when']}  schedule {done[0]['id']}")
            continue
        if same_time:
            problems += 1
            print(f"  CLASH  {p['platform']:9} {p['account']} {p['when']}  schedule {same_time[0]['id']}")
            continue
        plan.append(p)
        print(f"  create {p['platform']:9} {p['account']} {p['when']}")

    print(f"\nqueue now {len(items)}, to create {len(plan)}, after {len(items) + len(plan)} of {QUEUE_CAP}")
    if problems or len(items) + len(plan) > QUEUE_CAP:
        print("REFUSING: slot clash or over the plan cap")
        return 1
    if not args.apply:
        print("dry run — pass --apply to create")
        return 0

    for p in plan:
        payload = {
            "post": {
                "accountId": p["account"],
                "content": {"platform": p["platform"], "text": p["text"], "mediaUrls": [p["media"]]},
                "target": p["target"],
            },
            "scheduledTime": p["when"],
        }
        result = call("POST", "/posts", key, payload)
        print(f"  created {p['platform']:9} {p['when']} -> {result.get('postSubmissionId', result)}")

    after = fetch_schedules(key)
    failures = 0
    for p in post_plan(v):
        matches = [
            item for item in after
            if account_id(item) == p["account"]
            and (item.get("scheduledAt") or "")[:16] == p["when"][:16]
            and marker in json.dumps(item)
        ]
        ok = len(matches) == 1
        if ok:
            draft = matches[0]["draft"]
            ok = (draft["content"]["text"] == p["text"]
                  and draft["content"].get("mediaUrls") == [p["media"]]
                  and draft["target"] == p["target"])
        failures += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {p['platform']:9} {p['when']}  {matches[0]['id'] if matches else '—'}")

    print(f"\nverified: queue {len(after)} of {QUEUE_CAP}, {failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
