#!/usr/bin/env python3
"""Queue one finished organic long-form video across all five Abs By AI destinations.

The YouTube Data API holding copy remains Private. Blotato creates the public YouTube
release at the scheduled time. Facebook gets no mediaType because its Reels route is
limited to short videos. TikTok can initially use the shared upload; tiktok_cover.py
then replaces that schedule with the cover-prefixed derivative.

Config (JSON):
  {
    "content_type": "organic",                 # REQUIRED. Ads never go organic - scripts/blotato/ad_guard.py
    "slug": "abwheel-workout",                 # utm_content + idempotency marker
    "title": "Ab Wheel Workout...",            # YouTube title
    "video_url": "https://database.blotato.io/...mp4",   # from blotato_create_presigned_upload_url + PUT
    "youtube_cover_url": "https://database.blotato.io/...jpg",
    "main": "2026-09-20T14:00:00.000Z",        # FB / IG main / TikTok
    "mirror": "2026-09-21T14:00:00.000Z",      # IG @abs.by.ai
    "keyword": "ABS",                          # ManyChat keyword, Docs/MANYCHAT_KEYWORDS.md
    "ai_generated": true,                      # YouTube + TikTok AI label: realistic AI footage only, not a labeled AI still (VIDEO-RULES.md)
    "hook": "...", "body": "...", "close": "...",
    "tags": "#a #b",
    "youtube_description": "...",
    "mirror_cta": "More from @danrosefit 👇",
    "instagram_video_url": "https://...mp4",   # optional smaller copy: Instagram rejects files over about 300 MB
    "tiktok_direct": true,                     # optional: TikTok is uploaded by hand in TikTok Studio (films over Blotato's
                                               # 10 minute TikTok limit, Dan 2026-10-14); no TikTok post is queued here
    "source": "Zeeshan Content Videos/.../file.mp4"   # optional; checked against the ad folders
    "platform_ctas": {"facebook": "Try Abs By AI free for 7 days: {link}"},
    "release_hold": "Previous-video URL and release order not yet verified"  # optional; blocks --apply
  }

Idempotent: a post counts as done when a schedule exists for that account at that time whose payload
carries utm_content=<slug>. Refuses on a slot clash or if the queue would pass the plan cap.

    python3 scripts/blotato/longform_queue.py CONFIG.json           # dry run
    python3 scripts/blotato/longform_queue.py CONFIG.json --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
import os
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ad_guard import AdGuardError, assert_organic  # noqa: E402
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402
import release_phases as rp  # noqa: E402

QUEUE_CAP = 200
FACEBOOK, FB_PAGE = "47105", "1294282227094660"
IG_MAIN, IG_MIRROR, TIKTOK, YOUTUBE = "67203", "65632", "58181", "46963"
CHICAGO = ZoneInfo("America/Chicago")


def check_longform_day(when: str, slug: str, items: list) -> None:
    """Refuse a day that is not a long-form day of its phase (release_phases.py), a wrong time, or a second long-form
    that day. Sun+Wed through Nov 25 2026, Sun+Wed+Fri Nov 26 to Jan 31 (none Dec 25), Sunday from Feb 1 (Dan, 2026-10-28)."""
    try:
        local = datetime.fromisoformat(when.replace("Z", "+00:00")).astimezone(CHICAGO)
    except ValueError as exc:
        raise ValueError(f"invalid main release time: {when}") from exc
    if not rp.longform_allowed(local.date()) or (local.hour, local.minute, local.second) != (9, 0, 0):
        raise ValueError(f"{local:%A %Y-%m-%d} is not a long-form day at 9 AM Chicago time (see release_phases.py): {when}")
    for item in items:
        draft = item.get("draft") or {}
        target = draft.get("target") or {}
        if target.get("targetType") != "youtube":
            continue
        body = (draft.get("content") or {}).get("text") or ""
        if "utm_campaign=longform" not in body:
            continue
        existing = datetime.fromisoformat(item["scheduledAt"].replace("Z", "+00:00")).astimezone(CHICAGO)
        if existing.date() == local.date() and f"utm_content={slug}" not in body:
            raise ValueError(f"{local:%A} {local.date()} already has long-form YouTube schedule {item['id']}")


def social_time(main: str) -> str:
    """Facebook, Instagram and TikTok follow the next day at noon: Monday after a Sunday release, Thursday
    after a Wednesday release, Saturday after a Friday release. 9 AM on those days is a Shorts slot on the same
    accounts (Dan, 2026-10-17; Friday added 2026-10-28)."""
    local = datetime.fromisoformat(main.replace("Z", "+00:00")).astimezone(CHICAGO) + timedelta(days=1)
    local = datetime(local.year, local.month, local.day, 12, 0, tzinfo=CHICAGO)
    return local.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def posts(v: dict) -> list:
    # YouTube releases on Sunday or Wednesday; the other platforms follow the next day.
    social_when = social_time(v["main"])
    utm = f"utm_medium=video&utm_campaign=longform&utm_content={v['slug']}"
    link = lambda source: f"https://absbyai.com/?utm_source={source}&{utm}"  # noqa: E731
    def cta(platform, fallback):
        template = (v.get("platform_ctas") or {}).get(platform, fallback)
        source = "instagram" if platform == "instagram_first_comment" else platform
        return template.replace("{link}", link(source)).replace("{keyword}", v["keyword"])
    lede = f"{v['hook']}\n\n{v['body']}\n\n{v['close']}\n\n"
    ig = {"targetType": "instagram", "mediaType": "reel", "shareToFeed": True,
          "firstComment": cta("instagram_first_comment", "See what you'd look like with a six-pack: {link}")}
    if v.get("instagram_cover_url"):
        ig["coverImageUrl"] = v["instagram_cover_url"]
    tiktok = {"targetType": "tiktok", "privacyLevel": "PUBLIC_TO_EVERYONE",
              "disabledComments": False, "disabledDuet": False, "disabledStitch": False,
              "isBrandedContent": False, "isYourBrand": False, "isAiGenerated": bool(v["ai_generated"])}
    if v.get("tiktok_video_url"):
        tiktok["videoCoverTimestamp"] = 0
    youtube = {"targetType": "youtube", "title": v["title"], "privacyStatus": "public",
               "shouldNotifySubscribers": True, "isMadeForKids": False,
               "containsSyntheticMedia": bool(v["ai_generated"]),
               "thumbnailUrl": v["youtube_cover_url"]}
    out = [
        (FACEBOOK, "facebook", social_when, {"targetType": "facebook", "pageId": FB_PAGE},
         lede + cta("facebook", "See what you'd look like with a six-pack. Free AI preview:\n{link}") + f"\n\n{v['tags']}",
         v["video_url"]),
        (IG_MAIN, "instagram", social_when, dict(ig),
         lede + cta("instagram", "Comment {keyword} and I'll send you the free AI preview 👇") + f"\n\n{v['tags']}",
         v.get("instagram_video_url", v["video_url"])),
        (TIKTOK, "tiktok", social_when, tiktok,
         lede + cta("tiktok", "Free AI preview of your own six-pack, link in bio at AbsByAI.com 👇\n\n{link}") + f"\n\n{v['tags']}",
         v.get("tiktok_video_url", v["video_url"])),
        # @abs.by.ai (65632) retired 2026-09-24: never queue it. No mirror post.
        (YOUTUBE, "youtube", v["main"], youtube, v["youtube_description"], v["video_url"]),
    ]
    # A film TikTok cannot take through Blotato is uploaded directly in TikTok Studio instead (Dan, 2026-10-14).
    return [p for p in out if not (v.get("tiktok_direct") and p[1] == "tiktok")]


def tiktok_caption(v: dict) -> str:
    """The TikTok caption this script would queue; used for a direct TikTok Studio upload."""
    return next(p[4] for p in posts({**v, "tiktok_direct": False}) if p[1] == "tiktok")


def acct_of(i: dict) -> str:
    return str(i.get("accountId") or i["draft"].get("accountId"))


_HEAD_LENGTHS: dict[str, int | None] = {}


def head_length(url: str) -> int | None:
    if url not in _HEAD_LENGTHS:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as resp:
                value = resp.headers.get("Content-Length")
                _HEAD_LENGTHS[url] = int(value) if value else None
        except Exception:
            _HEAD_LENGTHS[url] = None
    return _HEAD_LENGTHS[url]


def same_media(actual_urls: list, source_url: str) -> bool:
    """Blotato re-hosts each post under a new URL; verify type and byte length instead."""
    if len(actual_urls) != 1 or not str(actual_urls[0]).startswith("https://"):
        return False
    actual = actual_urls[0]
    actual_ext = os.path.splitext(urllib.parse.urlparse(actual).path)[1].lower()
    source_ext = os.path.splitext(urllib.parse.urlparse(source_url).path)[1].lower()
    actual_len, source_len = head_length(actual), head_length(source_url)
    return actual_ext == source_ext == ".mp4" and actual_len is not None and actual_len == source_len


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    v = json.load(open(args.config))
    if args.apply and v.get("release_hold"):
        print(f"REFUSING - release hold: {v['release_hold']}")
        return 1

    required = ["content_type", "source", "slug", "title", "video_url",
                "youtube_cover_url", "main", "keyword", "ai_generated",
                "hook", "body", "close", "tags", "youtube_description"]
    missing = [key for key in required if key not in v or v[key] in (None, "")]
    if missing:
        print("REFUSING - missing config fields: " + ", ".join(missing))
        return 1
    url_fields = ["video_url", "youtube_cover_url"]
    if v.get("tiktok_video_url"):
        url_fields.append("tiktok_video_url")
    if v.get("instagram_cover_url"):
        url_fields.append("instagram_cover_url")
    if v.get("instagram_video_url"):
        url_fields.append("instagram_video_url")
    bad_urls = [key for key in url_fields if not str(v[key]).startswith("https://")]
    if bad_urls:
        print("REFUSING - non-HTTPS media fields: " + ", ".join(bad_urls))
        return 1

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
    try:
        check_longform_day(v["main"], v["slug"], items)
    except ValueError as exc:
        print(f"REFUSING - {exc}")
        return 1
    marker = f"utm_content={v['slug']}"

    plan, bad = [], 0
    for acct, platform, when, target, text, media in posts(v):
        clash = [i for i in items if acct_of(i) == acct and (i.get("scheduledAt") or "")[:16] == when[:16]]
        done = [i for i in clash if marker in json.dumps(i)]
        if done:
            print(f"  done   {platform:9} {acct} {when}  (schedule {done[0]['id']})"); continue
        if clash:
            bad += 1; print(f"  CLASH  {platform:9} {acct} {when}  already holds {clash[0]['id']}"); continue
        plan.append((acct, platform, when, target, text, media)); print(f"  create {platform:9} {acct} {when}")

    print(f"\nqueue now {len(items)}, to create {len(plan)}, after {len(items) + len(plan)} of {QUEUE_CAP}")
    if bad or len(items) + len(plan) > QUEUE_CAP:
        print("REFUSING: slot clash or over the plan cap"); return 1
    if not args.apply:
        print("dry run — pass --apply to create"); return 0

    for acct, platform, when, target, text, media in plan:
        body = {"post": {"accountId": acct, "target": target,
                         "content": {"platform": platform, "text": text, "mediaUrls": [media]}},
                "scheduledTime": when}
        res = call("POST", "/posts", key, body)
        print(f"  created {platform:9} {when}  -> {res.get('postSubmissionId', res)}")

    # Verify against a fresh pull, not the create responses.
    after = fetch_schedules(key); missing = 0
    for acct, platform, when, target, text, media in posts(v):
        hit = [i for i in after if acct_of(i) == acct and (i.get("scheduledAt") or "")[:16] == when[:16]
               and marker in json.dumps(i)]
        ok = (len(hit) == 1 and hit[0]["draft"]["content"]["text"] == text
              and same_media(hit[0]["draft"]["content"].get("mediaUrls") or [], media)
              and hit[0]["draft"].get("target") == target)
        missing += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {platform:9} {when}  {hit[0]['id'] if hit else '—'}")
    print(f"\nverified: queue {len(after)} of {QUEUE_CAP}, {missing} problem(s)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
