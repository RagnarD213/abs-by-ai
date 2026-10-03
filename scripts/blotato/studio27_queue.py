#!/usr/bin/env python3
"""Queue the approved 27 studio photo posts (54 placements) in Blotato.

Executes Handoffs/handoff-20261003-approved-studio-posts-27-blotato.md.
Organic feed photos / carousels only: Instagram @danrosefit (67203) and Facebook Page Abs by AI (47105).
Never touches existing queue items. Resumable: every write is saved in studio27_state.json.

    python3 scripts/blotato/studio27_queue.py upload          # upload the 51 JPEGs once, hash-verify
    python3 scripts/blotato/studio27_queue.py plan            # write studio27_plan.json (no writes)
    python3 scripts/blotato/studio27_queue.py create [--max N]  # create posts from the plan
    python3 scripts/blotato/studio27_queue.py verify          # re-read queue, check everything
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402
import ad_guard  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
MANIFEST = os.path.join(ROOT, "Handoffs", "handoff-20261003-approved-studio-posts-27-blotato.json")
STATE = os.path.join(HERE, "studio27_state.json")
PLAN = os.path.join(HERE, "studio27_plan.json")
CT = ZoneInfo("America/Chicago")
IG, FB, FB_PAGE = "67203", "47105", "1294282227094660"
START = datetime(2026, 10, 5).date()  # first Monday after today (2026-10-03)

man = json.load(open(MANIFEST))
posts = {p["id"]: p for p in man["posts"]}
KEY = api_key()


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"uploads": {}, "created": {}}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, STATE)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def upload():
    s = load_state()
    for p in man["posts"]:
        for im in p["images"]:
            rel = im["relative_path"]
            if rel in s["uploads"]:
                continue
            path = os.path.join(man["root"], rel)
            data = open(path, "rb").read()
            assert sha(data) == im["sha256"], rel
            r = call("POST", "/media/uploads", KEY, {"filename": os.path.basename(rel)})
            req = urllib.request.Request(r["presignedUrl"], data=data, method="PUT",
                                         headers={"Content-Type": "image/jpeg"})
            urllib.request.urlopen(req).read()
            back = urllib.request.urlopen(r["publicUrl"]).read()
            assert sha(back) == im["sha256"], "re-hosted bytes differ: " + rel
            s["uploads"][rel] = r["publicUrl"]
            save_state(s)
            print("uploaded", rel, flush=True)
            time.sleep(1.2)
    print("uploads:", len(s["uploads"]))


def utc_for(day):
    return datetime(day.year, day.month, day.day, 17, 0, tzinfo=CT).astimezone(timezone.utc)


def plan():
    items = fetch_schedules(KEY)
    json.dump(items, open(os.path.join(HERE, "studio27_queue_before_20261003.json"), "w"))
    occ = {IG: set(), FB: set()}
    for i in items:
        acct = i["draft"]["accountId"]
        if acct in occ:
            occ[acct].add(datetime.fromisoformat(i["scheduledAt"].replace("Z", "+00:00")).astimezone(CT).date())
    s = load_state()
    out = []
    for acct in (IG, FB):
        day = START
        for pid in man["suggested_rotation"]:
            while day.weekday() not in (0, 2, 4) or day in occ[acct]:
                day += timedelta(days=1)
            p = posts[pid]
            out.append({"post": pid, "account": acct, "platform": "instagram" if acct == IG else "facebook",
                        "local": f"{day} 17:00 America/Chicago", "scheduledTime": utc_for(day).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "media": [s["uploads"][im["relative_path"]] for im in p["images"]]})
            occ[acct].add(day)
            day += timedelta(days=1)
    json.dump(out, open(PLAN, "w"), indent=1)
    print("planned", len(out), "placements;", len(items), "existing")
    for o in out:
        print(o["account"], o["post"], o["local"], len(o["media"]))


def body(o):
    p = posts[o["post"]]
    ad_guard.assert_organic({"content_type": "organic"}, texts=[p["caption"], p["title"], o["post"]], sources=[])
    if o["account"] == IG:
        target = {"targetType": "instagram"}
    else:
        target = {"targetType": "facebook", "pageId": FB_PAGE}
    return {"post": {"accountId": o["account"], "target": target,
                     "content": {"platform": o["platform"], "text": p["caption"], "mediaUrls": o["media"]}},
            "scheduledTime": o["scheduledTime"]}


def create(maxn):
    s = load_state()
    n = 0
    for o in json.load(open(PLAN)):
        k = f"{o['account']}|{o['post']}"
        if k in s["created"]:
            continue
        if n >= maxn:
            break
        res = call("POST", "/posts", KEY, body(o))
        s["created"][k] = {"response": res, "scheduledTime": o["scheduledTime"], "local": o["local"]}
        save_state(s)
        n += 1
        print("created", k, o["local"], res.get("postSubmissionId"), flush=True)
        time.sleep(1.0)
    print("created this run:", n, "total:", len(s["created"]))


def verify():
    items = fetch_schedules(KEY)
    before = json.load(open(os.path.join(HERE, "studio27_queue_before_20261003.json")))
    after = {i["id"]: i for i in items}
    ok = True
    for b in before:  # existing untouched
        a = after.get(b["id"])
        if not a or a["scheduledAt"] != b["scheduledAt"] or a["draft"] != b["draft"]:
            ok = False
            print("CHANGED/MISSING existing", b["id"])
    new = [i for i in items if i["id"] not in {b["id"] for b in before}]
    print("existing before:", len(before), "after:", len(items), "new:", len(new))
    exp = {(o["account"], o["scheduledTime"], o["post"]): o for o in json.load(open(PLAN))}
    seen = set()
    for i in new:
        d = i["draft"]
        cap = d["content"]["text"]
        pid = next((p["id"] for p in man["posts"] if p["caption"] == cap), None)
        key = (d["accountId"], i["scheduledAt"], pid)
        o = exp.get(key)
        if not o:
            ok = False
            print("UNEXPECTED new", i["id"], key)
            continue
        if d["content"]["mediaUrls"] != o["media"] or d["content"]["platform"] != o["platform"]:
            ok = False
            print("MEDIA/PLATFORM MISMATCH", key)
        if d["target"].get("mediaType"):
            ok = False
            print("mediaType set", key)
        seen.add(key)
    print("verified", len(seen), "of", len(exp), "planned placements")
    ok = ok and len(seen) == len(exp)
    # no duplicate account/time among new + existing photo posts
    from collections import Counter
    c = Counter((i["draft"]["accountId"], i["scheduledAt"]) for i in items
                if i["draft"]["accountId"] in (IG, FB) and not i["draft"]["target"].get("mediaType"))
    dup = [k for k, v in c.items() if v > 1]
    print("duplicate account/time photo slots:", dup)
    print("RESULT", "OK" if ok and not dup else "PROBLEMS")
    json.dump(items, open(os.path.join(HERE, "studio27_queue_after.json"), "w"))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "upload":
        upload()
    elif cmd == "plan":
        plan()
    elif cmd == "create":
        create(int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 999)
    elif cmd == "verify":
        verify()
