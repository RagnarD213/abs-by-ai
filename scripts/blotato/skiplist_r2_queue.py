#!/usr/bin/env python3
"""Queue the Skip List Carousel R2 ("7 things I'd skip if I started over at 40") once on Instagram.

Executes Handoffs/handoff-20261020-skip-list-carousel-redesign.md after Dan picked cover A (navy gym stack),
kept "at 40" and approved Saturday 2026-10-24 at noon Central (2026-10-20).
Organic photo carousel: Instagram @danrosefit (67203) only, 9 slides in order. Never touches other queue items.
Resumable: every write is saved in skiplist_r2_state.json.

    python3 scripts/blotato/skiplist_r2_queue.py upload    # upload the 9 JPEGs once, hash-verify the re-hosted copies
    python3 scripts/blotato/skiplist_r2_queue.py create    # snapshot the queue, check the slot, create the one post
    python3 scripts/blotato/skiplist_r2_queue.py verify    # re-read the queue: others untouched, ours exact
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
# The Blotato key lives in the main project folder (Business/), so import the helpers from there.
MAIN = os.path.expanduser("~/Documents/Claude/Projects/Abs By AI/scripts/blotato")
sys.path.insert(0, MAIN if os.path.isdir(MAIN) else HERE)
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402
import ad_guard  # noqa: E402

CT = ZoneInfo("America/Chicago")
IG = "67203"
SLOT = datetime(2026, 10, 24, 12, 0, tzinfo=CT).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
SRC = os.path.expanduser(
    "~/Documents/Claude/Projects/Abs By AI/Short-form video content/instagram-danrosefit/carousel-skip-list-r2")
FILES = [f"skip-list-r2_{i:02d}.jpg" for i in range(1, 10)]
STATE = os.path.join(HERE, "skiplist_r2_state.json")
BEFORE = os.path.join(HERE, "skiplist_r2_queue_before.json")
# Caption from Docs/INSTAGRAM_danrosefit_STEP1_AND_WEEK1.md, "Delivered: the Wednesday carousel", unchanged.
CAPTION = (
    "7 things I'd skip if I started over at 40.\n\n"
    "Every one of these cost me time, money or both. The last one is the one that actually changed the result.\n\n"
    "Save this before you spend another dollar on the first one.\n\n"
    "Comment ABS and I'll send you the free AI preview \U0001F447\n\n"
    "#over40 #sixpackabs #fatloss #fitnessover40 #aifitness"
)
KEY = api_key()


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"uploads": {}, "created": None}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, STATE)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def checks():
    assert "—" not in CAPTION and "–" not in CAPTION, "long dash in caption"
    assert CAPTION.count("#") <= 5, "more than 5 hashtags"
    ad_guard.assert_organic({"content_type": "organic", "slug": "skip-list-carousel-r2"},
                            texts=[CAPTION], sources=[os.path.join(SRC, f) for f in FILES])


def upload():
    s = load_state()
    for f in FILES:
        data = open(os.path.join(SRC, f), "rb").read()
        if f in s["uploads"] and s["uploads"][f]["sha256"] == sha(data):
            continue
        r = call("POST", "/media/uploads", KEY, {"filename": f})
        req = urllib.request.Request(r["presignedUrl"], data=data, method="PUT", headers={"Content-Type": "image/jpeg"})
        urllib.request.urlopen(req).read()
        back = urllib.request.urlopen(r["publicUrl"]).read()
        assert sha(back) == sha(data), "re-hosted bytes differ: " + f
        s["uploads"][f] = {"url": r["publicUrl"], "sha256": sha(data)}
        save_state(s)
        print("uploaded", f, flush=True)
        time.sleep(1.2)
    print("uploads:", len(s["uploads"]), "of", len(FILES))


def media(s):
    return [s["uploads"][f]["url"] for f in FILES]


def same_slides(urls, s):
    """Blotato re-hosts media under new links when a post is created, so compare bytes, not URLs."""
    want = [s["uploads"][f]["sha256"] for f in FILES]
    return [sha(urllib.request.urlopen(u).read()) for u in urls] == want


def create():
    checks()
    s = load_state()
    if s["created"]:
        print("already created:", s["created"]["response"])
        return
    assert len(s["uploads"]) == len(FILES), "run upload first"
    items = fetch_schedules(KEY)
    json.dump(items, open(BEFORE, "w"))
    clash = [i["id"] for i in items if i["draft"]["accountId"] == IG and i["scheduledAt"] == SLOT]
    assert not clash, f"Instagram already has a post at {SLOT}: {clash}"
    dup = [i["id"] for i in items if i["draft"]["content"]["text"].startswith("7 things I'd skip")]
    assert not dup, f"this carousel is already queued: {dup}"
    body = {"post": {"accountId": IG, "target": {"targetType": "instagram"},
                     "content": {"platform": "instagram", "text": CAPTION, "mediaUrls": media(s)}},
            "scheduledTime": SLOT}
    res = call("POST", "/posts", KEY, body)
    s["created"] = {"response": res, "scheduledTime": SLOT, "local": "2026-10-24 12:00 America/Chicago"}
    save_state(s)
    print("created", res, "for", SLOT, "(existing before:", len(items), ")")


def verify():
    s = load_state()
    items = fetch_schedules(KEY)
    before = json.load(open(BEFORE))
    after = {i["id"]: i for i in items}
    ok = True
    for b in before:
        a = after.get(b["id"])
        if not a:
            print("missing (published or removed since the snapshot):", b["id"], b["scheduledAt"])
            if b["scheduledAt"] > datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"):
                ok = False
        elif a["scheduledAt"] != b["scheduledAt"] or a["draft"] != b["draft"]:
            ok = False
            print("CHANGED existing", b["id"])
    new = [i for i in items if i["id"] not in {b["id"] for b in before}]
    ours = [i for i in new if i["draft"]["content"]["text"] == CAPTION]
    print("existing before:", len(before), "after:", len(items), "new:", len(new), "ours:", len(ours))
    if len(ours) != 1:
        ok = False
    for i in ours:
        d = i["draft"]
        order = same_slides(d["content"]["mediaUrls"], s)
        good = (d["accountId"] == IG and i["scheduledAt"] == SLOT and order
                and d["content"]["platform"] == "instagram" and not d["target"].get("mediaType"))
        print("ours:", i["id"], i["scheduledAt"], d["accountId"], len(d["content"]["mediaUrls"]), "slides,",
              "byte-identical and in order" if order else "ORDER/MEDIA MISMATCH")
        ok = ok and good
        if good:
            s["verified"] = {"scheduleId": i["id"], "scheduledAt": i["scheduledAt"], "at": datetime.now(timezone.utc).isoformat()}
            save_state(s)
    clash = [i["id"] for i in items if i["draft"]["accountId"] == IG and i["scheduledAt"] == SLOT]
    print("Instagram posts at the slot:", clash)
    print("RESULT", "OK" if ok and len(clash) == 1 else "PROBLEMS")


if __name__ == "__main__":
    {"upload": upload, "create": create, "verify": verify}[sys.argv[1]]()
