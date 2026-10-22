#!/usr/bin/env python3
"""Phase 3 of Handoffs/handoff-20261021-instagram-carousels-batch-1.md (Dan's picks, 2026-10-22).

Instagram @danrosefit (67203) and Facebook Page Abs by AI (47105), image slots Mon/Wed/Fri 5 PM America/Chicago.
Uses igtemplate_queue.py's batch file, uploads and state (igtemplate_batch.json / igtemplate_state.json), so a retry never
duplicates. Steps, each resumable:

    python3 scripts/blotato/igtemplate_phase3.py backup     # snapshot the whole queue (swap_backup/, git-ignored)
    python3 scripts/blotato/igtemplate_phase3.py retire     # every unreleased Codex studio post -> photo_reserve.json, off the schedule
    python3 scripts/blotato/igtemplate_phase3.py swap       # C1: new last slide (create new, then delete old); C3 -> workout-06 on Oct 28
    python3 scripts/blotato/igtemplate_phase3.py place      # batch posts with a "slot" go into that slot on both accounts
    python3 scripts/blotato/igtemplate_phase3.py refresh ID # slides of a queued post changed: re-upload, create new, delete old
    python3 scripts/blotato/igtemplate_phase3.py verify     # re-read: ours exact, studio gone, nothing else changed

Studio image files and studio27_state.json are never deleted. The reserve is used only if the image queue would run dry.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import igtemplate_queue as q  # noqa: E402  (loads batch, state helpers, studio captions)
from danrosefit_migration import call, fetch_schedules  # noqa: E402

KEY = q.KEY
IG, FB = q.IG, q.FB
RESERVE = os.path.join(HERE, "photo_reserve.json")
BACKUP = os.path.join(HERE, "swap_backup", "queue_before_igtemplate_phase3.json")
STUDIO_STATE = os.path.join(HERE, "studio27_state.json")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def items_now():
    return fetch_schedules(KEY)


def future(i):
    return i["scheduledAt"] > q.iso(datetime.now(timezone.utc))


def backup():
    items = items_now()
    if os.path.exists(BACKUP):
        print("backup already exists, keeping it:", BACKUP)
    else:
        json.dump(items, open(BACKUP, "w"))
        print("backed up", len(items), "schedules to", BACKUP)


def retire():
    items = items_now()
    studio = [i for i in items if i["draft"]["accountId"] in (IG, FB) and q.is_image(i) and q.studio_id(i) and future(i)]
    st = json.load(open(STUDIO_STATE))
    res = json.load(open(RESERVE)) if os.path.exists(RESERVE) else {
        "note": "Retired Codex studio photo posts (Dan, 2026-10-21/22). Use ONLY if the Mon/Wed/Fri image queue would "
                "otherwise run dry. Media URLs are Blotato-hosted; image files and studio27_state.json are untouched.",
        "posts": {}}
    man = {p["id"]: p for p in json.load(open(q.STUDIO_MANIFEST))["posts"]}
    for i in sorted(studio, key=lambda x: x["scheduledAt"]):
        pid = q.studio_id(i)
        e = res["posts"].setdefault(pid, {"caption": man[pid]["caption"], "title": man[pid].get("title"),
                                          "images": [{"relative_path": im["relative_path"], "sha256": im["sha256"],
                                                      "uploaded_url": st["uploads"].get(im["relative_path"])}
                                                     for im in man[pid]["images"]],
                                          "removed": {}})
        e["removed"][i["draft"]["accountId"]] = {"scheduleId": i["id"], "wasScheduledAt": i["scheduledAt"],
                                                 "mediaUrls": i["draft"]["content"]["mediaUrls"]}
        json.dump(res, open(RESERVE, "w"), indent=1, ensure_ascii=False)  # record before deleting
        call("DELETE", f"/schedules/{i['id']}", KEY)
        print("retired", i["draft"]["accountId"], pid, q.local(i["scheduledAt"]).strftime("%a %m-%d"), flush=True)
        time.sleep(0.8)
    print("studio posts retired this run:", len(studio), "| reserve holds", len(res["posts"]), "posts")


def post_body(p, acct, when, s):
    return q.body(p, acct, when, s)


def swap():
    s = q.load_state()
    posts = {p["id"]: p for p in q.batch["posts"]}
    items = items_now()
    # C1: same slot, same caption, slide 5 replaced. Create first, then delete the old one.
    c1 = posts["C1-the-fix-01-v2"]
    for acct in (IG, FB):
        k = f"{acct}|{c1['id']}"
        old_id = s["created"][f"{acct}|C1-the-fix-01"].get("scheduleId")
        when = s["created"][f"{acct}|C1-the-fix-01"]["scheduledTime"]
        if k not in s["created"]:
            res = call("POST", "/posts", KEY, post_body(c1, acct, when, s))
            s["created"][k] = {"response": res, "scheduledTime": when, "local": "Fri 2026-10-23 17:00 CT",
                               "replaces": old_id, "caption_sha256": sha(c1["caption"].encode())}
            q.save_state(s)
            print("created C1 v2", acct, flush=True)
            time.sleep(1.0)
        if old_id and any(i["id"] == old_id for i in items) and not s["created"][f"{acct}|C1-the-fix-01"].get("deleted"):
            call("DELETE", f"/schedules/{old_id}", KEY)
            s["created"][f"{acct}|C1-the-fix-01"]["deleted"] = datetime.now(timezone.utc).isoformat()
            q.save_state(s)
            print("deleted old C1", acct, old_id, flush=True)
    # C3 -> workout-06 (Dan's real 1-minute ab workout; C3 named his Spiderman plank wrong). C3 goes to the reserve.
    w6 = posts["workout-06-ab-rounds"]
    res = json.load(open(RESERVE))
    for acct in (IG, FB):
        old = s["created"][f"{acct}|C3-steal-my-workout-01"]
        old_id, when = old.get("scheduleId"), old["scheduledTime"]
        if old_id and any(i["id"] == old_id for i in items) and not old.get("deleted"):
            r = res.setdefault("c3", {"note": "C3 Steal My Workout 01 (approved R1, but its 'Spiderman plank' is not Dan's "
                                              "move). Replaced on Oct 28 by workout-06. Re-create from igtemplate_batch.json.",
                                      "removed": {}})
            r["removed"][acct] = {"scheduleId": old_id, "wasScheduledAt": when}
            json.dump(res, open(RESERVE, "w"), indent=1, ensure_ascii=False)
            call("DELETE", f"/schedules/{old_id}", KEY)
            old["deleted"] = datetime.now(timezone.utc).isoformat()
            q.save_state(s)
            print("removed C3", acct, old_id, flush=True)
        k = f"{acct}|{w6['id']}"
        if k not in s["created"]:
            q.checks(w6)
            r = call("POST", "/posts", KEY, post_body(w6, acct, when, s))
            s["created"][k] = {"response": r, "scheduledTime": when, "local": "Wed 2026-10-28 17:00 CT",
                               "caption_sha256": sha(w6["caption"].encode())}
            q.save_state(s)
            print("created workout-06", acct, flush=True)
            time.sleep(1.0)


def next_free(acct, day, items):
    """The planned day if it is still ahead and free on this account, else the next free Mon/Wed/Fri 5 PM."""
    from datetime import timedelta
    today = datetime.now(q.CT).date()
    busy = {q.local(i["scheduledAt"]).date() for i in items if i["draft"]["accountId"] == acct
            and q.is_image(i) and q.local(i["scheduledAt"]).hour == 17}
    while day <= today or day.weekday() not in (0, 2, 4) or day in busy:
        day += timedelta(days=1)
    return day


def place(cap=200):
    """Create every batch post that has a "slot" and is not yet queued. Waits politely at Blotato's cap: run again
    later (queue_topup.py does, once no video is waiting). A slot that has passed or filled rolls to the next free one."""
    s = q.load_state()
    items = items_now()
    left = 0
    for p in q.batch["posts"]:
        if not p.get("slot"):
            continue
        q.checks(p)
        assert all(f"{p['id']}/{f}" in s["uploads"] for f in p["files"]), "upload first: " + p["id"]
        for acct in (IG, FB):
            k = f"{acct}|{p['id']}"
            if k in s["created"]:
                continue
            if len(items) >= cap:
                left += 1
                continue
            day = next_free(acct, datetime.fromisoformat(p["slot"]).date(), items)
            when = q.slot(day)
            r = call("POST", "/posts", KEY, post_body(p, acct, when, s))
            s["created"][k] = {"response": r, "scheduledTime": when, "local": f"{day} 17:00 CT",
                               "caption_sha256": sha(p["caption"].encode())}
            q.save_state(s)
            items.append({"draft": {"accountId": acct, "target": {}, "content": {"text": p["caption"]}}, "scheduledAt": when, "id": "new"})
            print("placed", acct, p["id"], day, flush=True)
            time.sleep(1.0)
    print("template image placements still waiting for room:", left)
    return left


def verify():
    s = q.load_state()
    posts = {p["id"]: p for p in q.batch["posts"]}
    items = items_now()
    before = json.load(open(BACKUP))
    after = {i["id"]: i for i in items}
    removed = {e["scheduleId"] for r in json.load(open(RESERVE))["posts"].values() for e in r["removed"].values()}
    removed |= {e["scheduleId"] for e in json.load(open(RESERVE)).get("c3", {}).get("removed", {}).values()}
    removed |= {v.get("scheduleId") for k, v in s["created"].items() if v.get("deleted")}
    removed |= {r["deleted"] for r in s.get("refreshed", [])}
    ok = True
    for b in before:
        a = after.get(b["id"])
        if b["id"] in removed:
            if a:
                ok = False
                print("STILL QUEUED (should be removed):", b["id"])
            continue
        if not a:
            if future(b):
                ok = False
                print("MISSING existing:", b["id"], b["scheduledAt"])
            continue
        if a["scheduledAt"] != b["scheduledAt"] or a["draft"] != b["draft"]:
            ok = False
            print("CHANGED existing:", b["id"])
    left = [i for i in items if i["draft"]["accountId"] in (IG, FB) and q.is_image(i) and q.studio_id(i) and future(i)]
    print("studio posts still queued:", len(left))
    ok = ok and not left
    seen = 0
    for k, v in s["created"].items():
        if v.get("deleted") or k.split("|")[1] not in posts:
            continue
        acct, pid = k.split("|")
        p = posts[pid]
        hit = [i for i in items if i["draft"]["accountId"] == acct and i["scheduledAt"] == v["scheduledTime"]
               and i["draft"]["content"]["text"] == p["caption"]]
        if not hit:
            if v["scheduledTime"] > q.iso(datetime.now(timezone.utc)):
                ok = False
                print("NOT FOUND:", k, v["scheduledTime"])
            continue
        good = q.same_slides(hit[0]["draft"]["content"]["mediaUrls"], p, s) and len(hit) == 1
        print("ours:", acct, pid, q.local(v["scheduledTime"]).strftime("%a %m-%d %H:%M"), len(p["files"]), "slides",
              "OK" if good else "MISMATCH")
        ok = ok and good
        seen += good
        v["scheduleId"] = hit[0]["id"]
    q.save_state(s)
    from collections import Counter
    cnt = Counter((i["draft"]["accountId"], i["scheduledAt"]) for i in items if i["draft"]["accountId"] in (IG, FB) and q.is_image(i))
    dup = [k for k, v in cnt.items() if v > 1]
    print("queue", len(before), "->", len(items), "| our posts verified:", seen, "| duplicate image slots:", dup)
    print("RESULT", "OK" if ok and not dup else "PROBLEMS")


def refresh(pid):
    """A queued post's slides were re-rendered (e.g. colour correction). Same slot and caption; create, then delete."""
    q.upload()  # re-uploads any file whose bytes changed
    s = q.load_state()
    p = {x["id"]: x for x in q.batch["posts"]}[pid]
    items = items_now()
    for acct in (IG, FB):
        k = f"{acct}|{pid}"
        old = s["created"][k]
        hit = [i for i in items if i["draft"]["accountId"] == acct and i["scheduledAt"] == old["scheduledTime"]
               and i["draft"]["content"]["text"] == p["caption"]]
        assert len(hit) == 1, f"{k}: expected one queued post, found {len(hit)}"
        if q.same_slides(hit[0]["draft"]["content"]["mediaUrls"], p, s):
            print("already current", k)
            continue
        r = call("POST", "/posts", KEY, post_body(p, acct, old["scheduledTime"], s))
        call("DELETE", f"/schedules/{hit[0]['id']}", KEY)
        s.setdefault("refreshed", []).append({"key": k, "deleted": hit[0]["id"], "at": datetime.now(timezone.utc).isoformat()})
        s["created"][k] = dict(old, response=r, scheduleId=None, refreshed=True)
        q.save_state(s)
        print("refreshed", k, "old", hit[0]["id"], flush=True)
        time.sleep(1.0)


if __name__ == "__main__":
    if sys.argv[1] == "refresh":
        refresh(sys.argv[2])
    else:
        {"backup": backup, "retire": retire, "swap": swap, "place": place, "verify": verify}[sys.argv[1]]()
