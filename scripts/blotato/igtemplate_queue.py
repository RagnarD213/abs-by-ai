#!/usr/bin/env python3
"""Queue the new-template Instagram/Facebook carousels (The Fix, Receipts, Steal My Workout, cheat sheets).

Executes Handoffs/handoff-20261021-instagram-carousels-batch-1.md.
Organic image posts only: Instagram @danrosefit (67203) and Facebook Page Abs by AI (47105), Mon/Wed/Fri 5 PM CT.
Never the retired @abs.by.ai account. Resumable: every write is saved in igtemplate_state.json, keyed by
"<account>|<post id>", so a retry never duplicates.

Phase 1 (2026-10-21): C1, C2, C3 take the next three image slots (Fri Oct 23, Mon Oct 26, Wed Oct 28); the studio posts
that held them move to the next free Mon/Wed/Fri 5 PM slots after the last studio post.

    python3 scripts/blotato/igtemplate_queue.py upload     # upload each post's JPEGs once, hash-verify the re-hosted copy
    python3 scripts/blotato/igtemplate_queue.py plan       # snapshot the queue, write igtemplate_plan.json (no writes)
    python3 scripts/blotato/igtemplate_queue.py apply      # move displaced studio posts, then create ours
    python3 scripts/blotato/igtemplate_queue.py verify     # re-read the queue: ours exact, moves done, nothing else changed
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
BATCH = os.path.join(HERE, "igtemplate_batch.json")
STATE = os.path.join(HERE, "igtemplate_state.json")
PLAN = os.path.join(HERE, "igtemplate_plan.json")
BEFORE = os.path.join(HERE, "swap_backup", "queue_before_igtemplate_apply.json")
STUDIO_MANIFEST = os.path.join(ROOT, "Handoffs", "handoff-20261003-approved-studio-posts-27-blotato.json")
CT = ZoneInfo("America/Chicago")
IG, FB, FB_PAGE = "67203", "47105", "1294282227094660"
ACCOUNTS = (IG, FB)
KEY = api_key()

batch = json.load(open(BATCH))
studio_caps = {p["caption"]: p["id"] for p in json.load(open(STUDIO_MANIFEST))["posts"]}


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"uploads": {}, "created": {}, "moved": {}}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, STATE)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def path_of(p, f):
    return os.path.join(ROOT, p["dir"], f)


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def local(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(CT)


def slot(day):
    return iso(datetime(day.year, day.month, day.day, 17, 0, tzinfo=CT))


def is_image(i):
    return not i["draft"]["target"].get("mediaType")


def studio_id(i):
    return studio_caps.get(i["draft"]["content"]["text"])


def checks(p):
    cap = p["caption"]
    assert "—" not in cap and "–" not in cap, "long dash in caption: " + p["id"]
    assert cap.count("#") <= 5, "more than 5 hashtags: " + p["id"]
    ad_guard.assert_organic({"content_type": "organic", "slug": p["id"]},
                            texts=[cap, p["id"]], sources=[path_of(p, f) for f in p["files"]])


def upload():
    s = load_state()
    for p in batch["posts"]:
        for f in p["files"]:
            data = open(path_of(p, f), "rb").read()
            k = f"{p['id']}/{f}"
            if k in s["uploads"] and s["uploads"][k]["sha256"] == sha(data):
                continue
            r = call("POST", "/media/uploads", KEY, {"filename": f})
            req = urllib.request.Request(r["presignedUrl"], data=data, method="PUT",
                                         headers={"Content-Type": "image/jpeg"})
            urllib.request.urlopen(req).read()
            back = urllib.request.urlopen(r["publicUrl"]).read()
            assert sha(back) == sha(data), "re-hosted bytes differ: " + k
            s["uploads"][k] = {"url": r["publicUrl"], "sha256": sha(data)}
            save_state(s)
            print("uploaded", k, flush=True)
            time.sleep(1.2)
    print("uploads:", len(s["uploads"]))


def plan():
    """New posts take the earliest future image slots now held by studio posts, in batch order; each displaced
    studio post moves to the next free Mon/Wed/Fri 5 PM day after the account's last image post."""
    s = load_state()
    for p in batch["posts"]:
        checks(p)
        assert all(f"{p['id']}/{f}" in s["uploads"] for f in p["files"]), "run upload first: " + p["id"]
    items = fetch_schedules(KEY)
    json.dump(items, open(BEFORE, "w"))
    now = iso(datetime.now(timezone.utc))
    out = {"created": [], "moves": []}
    for acct in ACCOUNTS:
        mine = [i for i in items if i["draft"]["accountId"] == acct]
        busy = {local(i["scheduledAt"]).date() for i in mine if local(i["scheduledAt"]).hour == 17}
        studio = sorted((i for i in mine if is_image(i) and studio_id(i) and i["scheduledAt"] > now),
                        key=lambda i: i["scheduledAt"])
        todo = [p for p in batch["posts"] if f"{acct}|{p['id']}" not in s["created"]]
        last = max(local(i["scheduledAt"]).date() for i in mine if is_image(i) and local(i["scheduledAt"]).hour == 17)
        day = last + timedelta(days=1)
        for p, held in zip(todo, studio):
            out["created"].append({"post": p["id"], "account": acct, "scheduledTime": held["scheduledAt"],
                                   "local": local(held["scheduledAt"]).strftime("%a %Y-%m-%d %H:%M CT")})
            while day.weekday() not in (0, 2, 4) or day in busy:
                day += timedelta(days=1)
            out["moves"].append({"scheduleId": held["id"], "studio": studio_id(held), "account": acct,
                                 "from": held["scheduledAt"], "to": slot(day),
                                 "toLocal": day.strftime("%a %Y-%m-%d 17:00 CT")})
            busy.add(day)
        assert len(todo) <= len(studio), "more new posts than studio slots; extend plan() for free slots"
    json.dump(out, open(PLAN, "w"), indent=1)
    for c in out["created"]:
        print("create", c["account"], c["post"], c["local"])
    for m in out["moves"]:
        print("move  ", m["account"], m["studio"], local(m["from"]).strftime("%a %m-%d"), "->", m["toLocal"])


def body(p, acct, when, s):
    target = {"targetType": "instagram"} if acct == IG else {"targetType": "facebook", "pageId": FB_PAGE}
    media = [s["uploads"][f"{p['id']}/{f}"]["url"] for f in p["files"]]
    return {"post": {"accountId": acct, "target": target,
                     "content": {"platform": "instagram" if acct == IG else "facebook",
                                 "text": p["caption"], "mediaUrls": media}},
            "scheduledTime": when}


def apply():
    s = load_state()
    pl = json.load(open(PLAN))
    posts = {p["id"]: p for p in batch["posts"]}
    for m in pl["moves"]:  # free the slot first; a failure leaves a studio post late, never two posts in one slot
        if m["scheduleId"] in s["moved"]:
            continue
        call("PATCH", f"/schedules/{m['scheduleId']}", KEY, {"patch": {"scheduledTime": m["to"]}})
        s["moved"][m["scheduleId"]] = m
        save_state(s)
        print("moved", m["account"], m["studio"], "->", m["toLocal"], flush=True)
        time.sleep(1.0)
    for c in pl["created"]:
        k = f"{c['account']}|{c['post']}"
        if k in s["created"]:
            continue
        p = posts[c["post"]]
        checks(p)
        res = call("POST", "/posts", KEY, body(p, c["account"], c["scheduledTime"], s))
        s["created"][k] = {"response": res, "scheduledTime": c["scheduledTime"], "local": c["local"],
                           "caption_sha256": sha(p["caption"].encode())}
        save_state(s)
        print("created", k, c["local"], res.get("postSubmissionId"), flush=True)
        time.sleep(1.0)


def same_slides(urls, p, s):
    """Blotato re-hosts media when a post is created, so compare bytes, not URLs."""
    want = [s["uploads"][f"{p['id']}/{f}"]["sha256"] for f in p["files"]]
    return [sha(urllib.request.urlopen(u).read()) for u in urls] == want


def verify():
    s = load_state()
    pl = json.load(open(PLAN))
    posts = {p["id"]: p for p in batch["posts"]}
    items = fetch_schedules(KEY)
    before = json.load(open(BEFORE))
    after = {i["id"]: i for i in items}
    moved = {m["scheduleId"]: m for m in pl["moves"]}
    now = iso(datetime.now(timezone.utc))
    ok = True
    for b in before:
        a = after.get(b["id"])
        if not a:
            if b["scheduledAt"] > now:
                ok = False
                print("MISSING existing", b["id"], b["scheduledAt"])
            continue
        want = moved[b["id"]]["to"] if b["id"] in moved else b["scheduledAt"]
        if a["scheduledAt"] != want or a["draft"] != b["draft"]:
            ok = False
            print("CHANGED existing", b["id"], a["scheduledAt"], "expected", want)
    for m in pl["moves"]:
        print("moved ok" if after.get(m["scheduleId"], {}).get("scheduledAt") == m["to"] else "MOVE MISSING",
              m["account"], m["studio"], m["toLocal"])
    new = [i for i in items if i["id"] not in {b["id"] for b in before}]
    exp = {(c["account"], c["scheduledTime"], posts[c["post"]]["caption"]): c for c in pl["created"]}
    seen = set()
    for i in new:
        d = i["draft"]
        key = (d["accountId"], i["scheduledAt"], d["content"]["text"])
        c = exp.get(key)
        if not c:
            print("other new item (not ours):", i["id"], d["accountId"], i["scheduledAt"])
            continue
        p = posts[c["post"]]
        good = (same_slides(d["content"]["mediaUrls"], p, s) and not d["target"].get("mediaType")
                and d["content"]["platform"] == ("instagram" if d["accountId"] == IG else "facebook"))
        print("ours:", i["id"], d["accountId"], c["post"], c["local"], len(d["content"]["mediaUrls"]), "slides,",
              "byte-identical and in order" if good else "MISMATCH")
        ok = ok and good
        if good:
            seen.add(key)
            s["created"][f"{c['account']}|{c['post']}"]["scheduleId"] = i["id"]
    save_state(s)
    from collections import Counter
    cnt = Counter((i["draft"]["accountId"], i["scheduledAt"]) for i in items
                  if i["draft"]["accountId"] in ACCOUNTS and is_image(i))
    dup = [k for k, v in cnt.items() if v > 1]
    print("verified", len(seen), "of", len(exp), "| queue", len(before), "->", len(items),
          "| duplicate image slots:", dup)
    print("RESULT", "OK" if ok and len(seen) == len(exp) and not dup else "PROBLEMS")


if __name__ == "__main__":
    {"upload": upload, "plan": plan, "apply": apply, "verify": verify}[sys.argv[1]]()
