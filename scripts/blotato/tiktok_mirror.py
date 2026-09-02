#!/usr/bin/env python3
"""Mirror the queued @danrosefit Instagram VIDEOS onto TikTok in Blotato.

Executes Handoffs/handoff-20260902-tiktok-blotato-connect-and-mirror.md.

  * source   = every scheduled post on Instagram @danrosefit (67203) whose media is
               an .mp4 -- photo posts stay on IG/FB, TikTok is video only
  * target   = TikTok @absbyai (58181), same scheduledAt as the Instagram original
  * caption  = the IG hook + body + hashtags; the Instagram-only "Comment ABS" CTA
               (a ManyChat trigger that does nothing on TikTok) becomes a plain
               "link in bio" line, and the absbyai.com link that IG carries in its
               auto first comment is appended with utm_source=tiktok
  * ramp     = at most ONE TikTok post per day for the first RAMP_DAYS after the
               account was connected; surplus videos inside that window are skipped,
               not re-timed (they still post on IG/FB/YouTube as normal)
  * cap      = Blotato's Starter plan silently refuses creates past 200 scheduled
               posts. If the queue has no room, the LATEST Facebook mirrors are
               deleted first (saved to fb_trimmed.json so --restore-fb can put them
               back once the queue has drained). @danrosefit posts are never touched.

Idempotent by construction: a TikTok schedule already carrying the same media url is
"done" and skipped, so re-running never double-posts. No state file.

    python3 scripts/blotato/tiktok_mirror.py                 # dry run
    python3 scripts/blotato/tiktok_mirror.py --apply --limit 1   # smoke test
    python3 scripts/blotato/tiktok_mirror.py --apply
    python3 scripts/blotato/tiktok_mirror.py --restore-fb    # re-add trimmed FB posts
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danrosefit_migration import (  # noqa: E402
    api_key, call, content_key, fetch_schedules, iso, parse,
)

MAIN = "67203"            # Instagram @danrosefit -- the canonical captions
TIKTOK = "58181"          # TikTok @absbyai, connected 2026-09-02
FACEBOOK = "47105"        # the page mirror; its tail is the only thing we trim
QUEUE_CAP = 200           # Blotato Starter plan
CONNECTED_ON = date(2026, 9, 2)
RAMP_DAYS = 7
RAMP_PER_DAY = 1

CTA_IG = "Comment ABS and I'll send you the free AI preview 👇"
CTA_TIKTOK = "Free AI preview of your own six-pack — link in bio at AbsByAI.com 👇"

# Dan's real filmed Shorts: no AI-generated disclosure, comments/duet/stitch open.
TIKTOK_TARGET = {
    "targetType": "tiktok",
    "privacyLevel": "PUBLIC_TO_EVERYONE",
    "disabledComments": False,
    "disabledDuet": False,
    "disabledStitch": False,
    "isBrandedContent": False,
    "isYourBrand": True,
    "isAiGenerated": False,
}

TRIM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fb_trimmed.json")


# --------------------------------------------------------------------------- caption
def tiktok_caption(item: dict) -> str:
    text = item["draft"]["content"]["text"]
    text = text.replace(CTA_IG, CTA_TIKTOK)
    link = None
    fc = item["draft"]["target"].get("firstComment") or ""
    m = re.search(r"https://absbyai\.com/\S*", fc)
    if m:
        link = re.sub(r"utm_source=\w+", "utm_source=tiktok", m.group(0))
    elif "utm_source=" in text:
        text = re.sub(r"utm_source=\w+", "utm_source=tiktok", text)
    else:
        # the backfill reels never carried a first-comment link; keep the UTM scheme
        slug = re.sub(r"[^a-z0-9]+", "-", text.splitlines()[0].lower()).strip("-")[:40]
        link = ("https://absbyai.com/?utm_source=tiktok&utm_medium=reel"
                f"&utm_campaign=backfill&utm_content={slug}")
    if link and link not in text:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                lines.insert(i, link)
                lines.insert(i + 1, "")
                break
        else:
            lines += ["", link]
        text = "\n".join(lines)
    assert len(text) <= 2200, "TikTok caption limit"
    return text


def is_video(item: dict) -> bool:
    urls = item["draft"]["content"].get("mediaUrls") or []
    return bool(urls) and urls[0].lower().endswith(".mp4")


# --------------------------------------------------------------------------- plan
def build_plan(items: list) -> dict:
    src = sorted((i for i in items if i["draft"]["accountId"] == MAIN and is_video(i)),
                 key=lambda x: x["scheduledAt"])
    tt = [i for i in items if i["draft"]["accountId"] == TIKTOK]
    have = {content_key(i) for i in tt}

    ramp_end = CONNECTED_ON + timedelta(days=RAMP_DAYS)
    per_day = defaultdict(int)
    for i in tt:
        per_day[parse(i["scheduledAt"]).date()] += 1

    todo, done, skipped = [], [], []
    for i in src:
        when = parse(i["scheduledAt"])
        row = {"id": i["id"], "when": iso(when),
               "hook": i["draft"]["content"]["text"].splitlines()[0]}
        if content_key(i) in have:
            done.append(row)
            continue
        if when.date() < ramp_end and per_day[when.date()] >= RAMP_PER_DAY:
            skipped.append({**row, "why": f"ramp: {RAMP_PER_DAY}/day until {ramp_end}"})
            continue
        if when <= datetime.now(timezone.utc):
            skipped.append({**row, "why": "in the past"})
            continue
        per_day[when.date()] += 1
        todo.append({**row, "text": tiktok_caption(i),
                     "mediaUrls": i["draft"]["content"]["mediaUrls"]})

    room = QUEUE_CAP - len(items)
    trim = []
    if len(todo) > room:
        fb = sorted((i for i in items if i["draft"]["accountId"] == FACEBOOK),
                    key=lambda x: x["scheduledAt"], reverse=True)
        trim = fb[:len(todo) - room]
    return {"src": src, "tiktok": tt, "todo": todo, "done": done,
            "skipped": skipped, "trim": trim, "room": room}


def check_plan(plan: dict) -> int:
    fails = []

    def check(ok, msg):
        print(("  PASS  " if ok else "  FAIL  ") + msg)
        if not ok:
            fails.append(msg)

    print("\nPLAN CHECK")
    by_day = defaultdict(int)
    for t in plan["tiktok"]:
        by_day[parse(t["scheduledAt"]).date()] += 1
    for t in plan["todo"]:
        by_day[parse(t["when"]).date()] += 1
    ramp_end = CONNECTED_ON + timedelta(days=RAMP_DAYS)
    over = {d: n for d, n in by_day.items() if d < ramp_end and n > RAMP_PER_DAY}
    check(not over, f"max {RAMP_PER_DAY} TikTok post/day inside the ramp window ({over})")
    check(all(t["mediaUrls"] and t["mediaUrls"][0].endswith(".mp4") for t in plan["todo"]),
          "every new post is a video")
    check(all("utm_source=tiktok" in t["text"] for t in plan["todo"]),
          "every caption carries utm_source=tiktok")
    check(all(CTA_IG not in t["text"] for t in plan["todo"]),
          "the Instagram-only Comment-ABS CTA is gone from every caption")
    check(all(len(t["text"]) <= 2200 for t in plan["todo"]), "captions within 2,200 chars")
    check(all(i["draft"]["accountId"] == FACEBOOK for i in plan["trim"]),
          "only Facebook posts are ever trimmed")
    check(len(plan["todo"]) <= plan["room"] + len(plan["trim"]),
          f"queue stays under {QUEUE_CAP} ({plan['room']} free, "
          f"{len(plan['trim'])} FB trims, {len(plan['todo'])} creates)")
    return len(fails)


# --------------------------------------------------------------------------- execute
def save_trimmed(rows: list) -> None:
    old = []
    if os.path.exists(TRIM_PATH):
        with open(TRIM_PATH) as fh:
            old = json.load(fh)
    seen = {r["id"] for r in old}
    old += [r for r in rows if r["id"] not in seen]
    with open(TRIM_PATH, "w") as fh:
        json.dump(old, fh, indent=1, ensure_ascii=False)


def restore_fb(key: str, apply: bool) -> int:
    if not os.path.exists(TRIM_PATH):
        print("nothing to restore")
        return 0
    with open(TRIM_PATH) as fh:
        rows = json.load(fh)
    items = fetch_schedules(key)
    have = {(i["draft"]["accountId"], content_key(i)) for i in items}
    pending = [r for r in rows if (FACEBOOK, content_key(r)) not in have
               and parse(r["scheduledAt"]) > datetime.now(timezone.utc)]
    room = QUEUE_CAP - len(items)
    print(f"trimmed {len(rows)}   still missing {len(pending)}   room {room}")
    for r in pending[:room]:
        print(f"  {r['scheduledAt'][:16]}  {r['draft']['content']['text'].splitlines()[0][:50]!r}")
        if apply:
            body = {"post": {"accountId": FACEBOOK, "target": r["draft"]["target"],
                             "content": r["draft"]["content"]},
                    "scheduledTime": r["scheduledAt"]}
            res = call("POST", "/posts", key, body)
            if not (res.get("postSubmissionId") or res.get("id")):
                raise SystemExit(f"restore not acknowledged: {res}")
    if not apply:
        print("Dry run. Re-run with --apply.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="create at most N (smoke test)")
    ap.add_argument("--restore-fb", action="store_true")
    args = ap.parse_args()
    key = api_key()
    if args.restore_fb:
        return restore_fb(key, args.apply)

    items = fetch_schedules(key)
    plan = build_plan(items)
    todo = plan["todo"][:args.limit] if args.limit else plan["todo"]
    trim = plan["trim"][:max(0, len(todo) - plan["room"])]

    print(f"queue {len(items)}/{QUEUE_CAP}   @danrosefit videos {len(plan['src'])}   "
          f"on TikTok already {len(plan['done'])}   to create {len(todo)}"
          f"{' of ' + str(len(plan['todo'])) if args.limit else ''}   "
          f"skipped {len(plan['skipped'])}   FB trims needed {len(trim)}")
    for s in plan["skipped"]:
        print(f"  SKIP   {s['when'][:16]}  {s['hook'][:50]!r}  ({s['why']})")
    for t in todo:
        print(f"  CREATE {t['when'][:16]}  {t['hook'][:50]!r}")
    for f in trim:
        print(f"  TRIM   {f['scheduledAt'][:16]}  FB "
              f"{f['draft']['content']['text'].splitlines()[0][:50]!r}")
    if todo:
        print("\nsample caption:\n" + "\n".join("    " + l for l in todo[0]["text"].split("\n")))

    fails = check_plan(plan)
    if fails:
        print(f"\nPLAN FAILED {fails} invariant(s) -- nothing written.")
        return 1
    if not args.apply:
        print("\nDry run. Re-run with --apply.")
        return 0

    if trim:
        save_trimmed(trim)
        for f in trim:
            call("DELETE", f"/schedules/{f['id']}", key)
            print(f"  trimmed FB {f['id']} {f['scheduledAt'][:16]}", flush=True)

    for t in todo:
        body = {
            "post": {
                "accountId": TIKTOK,
                "target": TIKTOK_TARGET,
                "content": {"platform": "tiktok", "text": t["text"],
                            "mediaUrls": t["mediaUrls"]},
            },
            "scheduledTime": t["when"],
        }
        res = call("POST", "/posts", key, body)
        if not (res.get("postSubmissionId") or res.get("id")):
            raise SystemExit(f"create for {t['id']} was not acknowledged: {res}")
        print(f"  created TikTok {t['when'][:16]}  {t['hook'][:40]!r}  "
              f"-> {res.get('postSubmissionId') or res.get('id')}", flush=True)

    print(f"\ncreated {len(todo)} TikTok posts, trimmed {len(trim)} Facebook posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
