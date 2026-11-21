#!/usr/bin/env python3
"""Replace DS-17's approved cover without changing its release plan.

Blotato cannot edit a scheduled post's target or media in place, so each affected
schedule is recreated byte-for-byte with only the cover field (Instagram/YouTube)
or frame-zero cover derivative (TikTok) changed. The old record is deleted only
after the replacement is visible in a fresh schedule readback.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ad_guard import AdGuardError, assert_organic  # noqa: E402
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402


IMAGE_URL = (
    "https://database.blotato.io/storage/v1/object/public/public_media/"
    "a836fa29-cde6-464e-8712-36d8a0de9f32/"
    "0fb79dba-515a-428a-974f-385bd241ae8c.png"
)
TIKTOK_VIDEO_URL = (
    "https://database.blotato.io/storage/v1/object/public/public_media/"
    "a836fa29-cde6-464e-8712-36d8a0de9f32/"
    "30c44b24-630e-4a9f-9b8e-3f4f14b8f92c.mp4"
)
SOURCE = "Short-form video content/ds-17_how-to-jump-rope.mp4"
OLD_IDS = {
    "4557024": "instagram",
    "4557025": "tiktok",
    "4557026": "instagram",
    "4557027": "youtube",
}
BACKUP = os.path.join(HERE, "cover_backup")


def replacement(item: dict) -> dict:
    draft = item["draft"]
    target = dict(draft["target"])
    content = dict(draft["content"])
    platform = content["platform"]
    if platform == "instagram":
        target["coverImageUrl"] = IMAGE_URL
    elif platform == "youtube":
        target["thumbnailUrl"] = IMAGE_URL
    elif platform == "tiktok":
        target["videoCoverTimestamp"] = 0
        content["mediaUrls"] = [TIKTOK_VIDEO_URL]
    else:
        raise ValueError(f"unexpected platform {platform}")
    return {
        "post": {
            "accountId": draft["accountId"],
            "target": target,
            "content": content,
        },
        "scheduledTime": item["scheduledAt"],
    }


def matches(item: dict, body: dict) -> bool:
    draft = item["draft"]
    post = body["post"]
    actual_content = dict(draft["content"])
    expected_content = dict(post["content"])
    # Blotato re-hosts a newly submitted TikTok MP4 under a second public URL
    # after schedule creation. Compare the rest of the post exactly; the caller
    # verifies the re-hosted bytes against the approved derivative by SHA-256.
    if actual_content.get("platform") == "tiktok":
        actual_media = actual_content.pop("mediaUrls", [])
        expected_content.pop("mediaUrls", None)
        media_ok = (
            len(actual_media) == 1
            and str(actual_media[0]).startswith("https://")
            and str(actual_media[0]).endswith(".mp4")
        )
    else:
        media_ok = True
    return (
        item["scheduledAt"] == body["scheduledTime"]
        and draft["accountId"] == post["accountId"]
        and draft["target"] == post["target"]
        and actual_content == expected_content
        and media_ok
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    key = api_key()
    items = {str(item["id"]): item for item in fetch_schedules(key)}
    missing = [sid for sid in OLD_IDS if sid not in items]
    if missing:
        print("REFUSING: expected schedules are missing: " + ", ".join(missing))
        return 1

    plans = []
    for sid, expected_platform in OLD_IDS.items():
        item = items[sid]
        platform = item["draft"]["content"]["platform"]
        if platform != expected_platform:
            print(f"REFUSING: {sid} is {platform}, expected {expected_platform}")
            return 1
        try:
            assert_organic(
                {"content_type": "organic", "source": SOURCE},
                texts=[item["draft"]["content"].get("text", "")],
                sources=[SOURCE],
            )
        except AdGuardError as exc:
            print(f"REFUSING: ad guard rejected {sid}: {exc}")
            return 1
        body = replacement(item)
        plans.append((sid, item, body))
        print(
            f"{sid}: {platform:9} {item['scheduledAt']} -> "
            + (TIKTOK_VIDEO_URL if platform == "tiktok" else IMAGE_URL).rsplit("/", 1)[-1]
        )

    if not args.apply:
        print("dry run — pass --apply to recreate and verify")
        return 0

    os.makedirs(BACKUP, exist_ok=True)
    replacements = {}
    for sid, item, body in plans:
        with open(os.path.join(BACKUP, f"{sid}-ds17-c2.json"), "w") as handle:
            json.dump(item, handle, indent=1)
        result = call("POST", "/posts", key, body)
        print(f"{sid}: created replacement submission {result.get('postSubmissionId', result)}")
        found = []
        for _ in range(10):
            time.sleep(3)
            found = [candidate for candidate in fetch_schedules(key) if matches(candidate, body)]
            if len(found) == 1:
                break
        if len(found) != 1:
            print(f"REFUSING TO DELETE {sid}: found {len(found)} matching replacements")
            return 1
        new_id = str(found[0]["id"])
        replacements[sid] = new_id
        call("DELETE", f"/schedules/{sid}", key)
        print(f"{sid}: replacement {new_id} verified; old schedule deleted")

    final = {str(item["id"]): item for item in fetch_schedules(key)}
    failures = []
    for old_id, _, body in plans:
        new_id = replacements[old_id]
        if new_id not in final or not matches(final[new_id], body) or old_id in final:
            failures.append(old_id)
    print(json.dumps({"replacements": replacements, "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
