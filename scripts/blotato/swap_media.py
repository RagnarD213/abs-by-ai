#!/usr/bin/env python3
"""Swap the media file on queued Blotato posts without changing anything else.

Blotato cannot edit a scheduled post's media, so a swap is create-then-delete: recreate the
post with the identical account, target (cover, first comment, privacy flags), caption and
scheduledTime but the new mediaUrl, confirm the new schedule exists, then delete the old id.
Verify afterwards by DOWNLOADING the new media and MD5-matching the master — Blotato re-hosts
under a new UUID so URL comparison proves nothing.

    python3 scripts/blotato/swap_media.py MAP.json            # dry run
    python3 scripts/blotato/swap_media.py MAP.json --apply

MAP.json: {"<old schedule id>": "<new public media url>", ...}
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402

mapping = json.load(open(sys.argv[1])); apply = "--apply" in sys.argv
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swap_backup")
key = api_key(); items = {str(i["id"]): i for i in fetch_schedules(key)}
print(f"queue: {len(items)} scheduled")
for old_id, new_url in mapping.items():
    it = items.get(old_id)
    if not it:
        print(f"{old_id}: NOT IN QUEUE (already swapped?)"); continue
    d = it["draft"]; body = {"post": {"accountId": d["accountId"], "target": d["target"],
            "content": {**d["content"], "mediaUrls": [new_url]}}, "scheduledTime": it["scheduledAt"]}
    print(f"{old_id}: {it['account'].get('username') or d['accountId']} {it['scheduledAt']} {d['content']['platform']} -> {new_url.split('/')[-1]}")
    if not apply: continue
    # The Starter plan caps the queue at 200 and refuses creates with a 422 (code 20010) at the
    # cap, so at the cap the swap has to delete first. The old post's full body is written to
    # disk before the delete so a failed create can be replayed by hand.
    os.makedirs(BACKUP, exist_ok=True)
    json.dump(it, open(os.path.join(BACKUP, f"{old_id}.json"), "w"), indent=1)
    call("DELETE", f"/schedules/{old_id}", key); print("   deleted old (backup on disk)")
    res = call("POST", "/posts", key, body); print("   created:", res)
    time.sleep(3)
    after = fetch_schedules(key)
    new = [s for s in after if s["draft"]["accountId"] == d["accountId"] and s["scheduledAt"] == it["scheduledAt"]
           and s["draft"]["content"].get("mediaUrls") == [new_url]]
    if not new:
        print(f"   !! new schedule not found -- replay {BACKUP}/{old_id}.json by hand"); continue
    print(f"   verified new schedule id {new[0]['id']}")
