#!/usr/bin/env python3
"""Build output/social-queue-artifact/queue.json for the Social Queue artifact page.

Reads the live Blotato schedule (every page) plus the not-yet-queued plan files, writes one JSON
the page fetches. Refresh = run this, then republish the artifact with the same url.

    python3 scripts/blotato/queue_artifact_data.py
"""
import json, os, sys
from datetime import datetime, timezone
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from danrosefit_migration import api_key, fetch_schedules  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "output", "social-queue-artifact", "queue.json")
CAP = 200
man = json.load(open(os.path.join(ROOT, "Handoffs", "handoff-20261003-approved-studio-posts-27-blotato.json")))
by_cap = {p["caption"]: p for p in man["posts"]}
items = fetch_schedules(api_key())
rows = []
for i in items:
    d = i["draft"]; c = d["content"]; t = d.get("target", {}); a = i["account"]
    plat = c["platform"]; media = c.get("mediaUrls") or []
    video = bool(media) and media[0].lower().split("?")[0].endswith((".mp4", ".mov", ".m4v"))
    mt = t.get("mediaType")
    kind = "Reel" if mt == "reel" else "Story" if mt == "story" else "Video" if video else ("Carousel" if len(media) > 1 else "Photo")
    sp = by_cap.get(c.get("text"))
    first = (c.get("text") or d.get("title") or "").strip().split("\n")[0]
    rows.append({"id": i["id"], "platform": plat, "when": i["scheduledAt"], "kind": kind,
                 "slides": len(media), "text": first[:110],
                 "batch": ("Studio " + sp["id"]) if sp else ""})
rows.sort(key=lambda r: (r["when"], r["platform"]))
plan = json.load(open(os.path.join(HERE, "studio27_plan.json")))
state = json.load(open(os.path.join(HERE, "studio27_state.json")))["created"]
posts = {p["id"]: p for p in man["posts"]}
waiting = [{"batch": "Studio posts", "platform": o["platform"], "post": o["post"], "title": posts[o["post"]]["title"],
            "planned": o["scheduledTime"], "slides": len(o["media"]),
            "kind": "Carousel" if len(o["media"]) > 1 else "Photo"}
           for o in plan if f"{o['account']}|{o['post']}" not in state]
PIPELINE = [  # hand-kept from AI_COORDINATION.md; edit here, rerun
    {"name": "RO-11 long-form", "state": "Round 1 with Dan", "note": "Waiting on Dan's review before any edit finishes."},
    {"name": "RO-13 long-form", "state": "Round 1 with Dan", "note": "Waiting on Dan's review before any edit finishes."},
    {"name": "SL-03 shorts", "state": "Building", "note": "Round 2 render in progress."},
    {"name": "SL-06 to SL-09 shorts", "state": "Ready to cut", "note": "Shorts from RO-12, RO-16, RO-10 and the Oura review. Not cut yet."},
    {"name": "Zepbound + Supplements shorts (16)", "state": "Parked", "note": "Held until their parent long-form is public."},
    {"name": "Long-forms 02 (Zepbound) and 03 (Supplements)", "state": "On hold", "note": "Dan's call. Not chasing."},
    {"name": "IG photo gap-fill, last 7 of 70", "state": "Needs queue room", "note": "Per the board; run iggap_fill.py --apply once slots free."},
]
json.dump({"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "cap": CAP,
           "scheduled": rows, "waiting": waiting, "pipeline": PIPELINE}, open(OUT, "w"), indent=0)
print(len(rows), "scheduled,", len(waiting), "waiting ->", OUT)
