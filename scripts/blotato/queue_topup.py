#!/usr/bin/env python3
"""Weekly top-up: move finished posts from our internal queue into Blotato until the plan cap is full.

Internal queue = studio27_plan.json minus studio27_state.json (approved posts with uploaded media
that Blotato had no room for). Uses the same payloads as studio27_queue.py. Never touches, moves or
deletes existing Blotato posts. A planned slot is kept when it is still in the future and its day is
free on that account; otherwise the item takes the next free Mon/Wed/Fri 5 PM Central slot after
the previous item placed for that account.

    python3 scripts/blotato/queue_topup.py            # dry run
    python3 scripts/blotato/queue_topup.py --apply    # create posts
"""
import json, os, sys, time
from datetime import datetime, timedelta, timezone
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import studio27_queue as s27  # noqa: E402
from danrosefit_migration import call, fetch_schedules  # noqa: E402

CAP = 200
apply = "--apply" in sys.argv
items = fetch_schedules(s27.KEY)
free = CAP - len(items)
state = s27.load_state()
plan = json.load(open(s27.PLAN))
waiting = [o for o in plan if f"{o['account']}|{o['post']}" not in state["created"]]
print(f"queue {len(items)}/{CAP}, free {free}, waiting {len(waiting)}")
occ = {s27.IG: set(), s27.FB: set()}
for i in items:
    a = i["draft"]["accountId"]
    if a in occ:
        occ[a].add(datetime.fromisoformat(i["scheduledAt"].replace("Z", "+00:00")).astimezone(s27.CT).date())
now = datetime.now(timezone.utc)
last = {}
made = 0
for o in waiting:
    if made >= free:
        break
    when = datetime.fromisoformat(o["scheduledTime"].replace("Z", "+00:00"))
    day = when.astimezone(s27.CT).date()
    prev = last.get(o["account"])
    if when <= now + timedelta(hours=2) or day in occ[o["account"]] or (prev and day <= prev):
        day = max(prev + timedelta(days=1) if prev else now.astimezone(s27.CT).date() + timedelta(days=1), day if when > now else now.astimezone(s27.CT).date() + timedelta(days=1))
        while day.weekday() not in (0, 2, 4) or day in occ[o["account"]]:
            day += timedelta(days=1)
        o["scheduledTime"] = s27.utc_for(day).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        o["local"] = f"{day} 17:00 America/Chicago"
        print("  re-slotted", o["post"], o["account"], "->", o["local"])
    day = datetime.fromisoformat(o["scheduledTime"].replace("Z", "+00:00")).astimezone(s27.CT).date()
    print(("create " if apply else "would create "), o["account"], o["post"], o["local"])
    if apply:
        res = call("POST", "/posts", s27.KEY, s27.body(o))
        state["created"][f"{o['account']}|{o['post']}"] = {"response": res, "scheduledTime": o["scheduledTime"], "local": o["local"]}
        s27.save_state(state)
        time.sleep(1.0)
    occ[o["account"]].add(day); last[o["account"]] = day; made += 1
if apply:
    json.dump(plan, open(s27.PLAN, "w"), indent=1)
print("placed", made if apply else f"(dry) {made}")
