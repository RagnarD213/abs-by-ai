#!/usr/bin/env python3
"""Daily video top-up: queue every finished video that is waiting for Blotato room (Dan, 2026-10-11).

ONE routine queues all waiting videos. Never make a scheduled task for a single video.

The waiting list is scripts/blotato/video_waitlist.json, in release order:
    [{"config": "scripts/blotato/configs/<slug>.json", "kind": "longform" | "short",
      "job": "RO-07", "label": "Why You MUST Work Out Every Day", "added": "2026-10-11"}, ...]
A setup that cannot queue because the plan cap is full adds its entry here and stops. Each entry
needs a finished config (media uploaded, thumbnail, captions) that the normal helper accepts.

For each waiting entry, in order, while the queue has room for its 4 posts:
  - long-form: keeps the config's Sunday if it is still free and at least 2 days away, otherwise takes
    the first free Sunday after the last queued long-form. 9 AM America/Chicago. The other platforms
    follow on Monday (longform_queue.py does that). One long-form per Sunday.
  - short: keeps the config's slot if it is still free and in the future, otherwise takes the next
    free Tuesday, Thursday or Saturday at 9 AM America/Chicago with no other YouTube post that day.
Then it runs the normal helper (longform_queue.py or organic_short_queue.py) with --apply, which
verifies on a fresh pull. Entries never jump the line: if the first waiting one does not fit, nothing
behind it is queued. Never touches, moves or deletes existing Blotato posts. Photo posts
(queue_topup.py) wait while any video is waiting.

    python3 scripts/blotato/video_topup.py            # dry run
    python3 scripts/blotato/video_topup.py --apply
    python3 scripts/blotato/video_topup.py --pending  # prints the number still waiting
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
WAITLIST = os.path.join(HERE, "video_waitlist.json")
CAP, NEED = 200, 4
CT = ZoneInfo("America/Chicago")
YOUTUBE, ACCOUNTS = "46963", ("47105", "67203", "58181", "46963")
IG_MAX_BYTES = 300_000_000
HELPER = {"longform": "longform_queue.py", "short": "organic_short_queue.py"}


def load() -> list:
    return json.load(open(WAITLIST)) if os.path.exists(WAITLIST) else []


def pending(entries: list) -> list:
    return [e for e in entries if not e.get("queued")]


def utc(day: date) -> str:
    local = datetime(day.year, day.month, day.day, 9, 0, tzinfo=CT)
    return local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def local_day(iso: str) -> date:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(CT).date()


def acct(i: dict) -> str:
    return str(i.get("accountId") or (i.get("draft") or {}).get("accountId"))


def head_bytes(url: str) -> int | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            return int(r.headers.get("Content-Length") or 0) or None
    except Exception:
        return None


def main() -> int:
    apply = "--apply" in sys.argv
    entries = load()
    if "--pending" in sys.argv:
        print(len(pending(entries))); return 0
    if not pending(entries):
        print("video top-up: nothing waiting"); return 0

    from danrosefit_migration import api_key, fetch_schedules
    items = fetch_schedules(api_key())
    blob = [json.dumps(i) for i in items]
    free = CAP - len(items)
    if not apply and "--assume-free" in sys.argv:  # test the slotting on a full queue; dry run only
        free = int(sys.argv[sys.argv.index("--assume-free") + 1])
    now = datetime.now(timezone.utc); today = now.astimezone(CT).date()

    yt_days, longform_sundays, minutes = set(), set(), set()
    for i in items:
        when = i.get("scheduledAt") or ""
        minutes.add((acct(i), when[:16]))
        if acct(i) == YOUTUBE:
            yt_days.add(local_day(when))
            text = ((i.get("draft") or {}).get("content") or {}).get("text") or ""
            if "utm_campaign=longform" in text:
                longform_sundays.add(local_day(when))

    queued_now, problem = [], None
    print(f"queue {len(items)}/{CAP}, free {free}, videos waiting {len(pending(entries))}")
    for e in pending(entries):
        path = os.path.join(ROOT, e["config"]); v = json.load(open(path))
        marker = f"utm_content={v['slug']}"
        have = sum(1 for b in blob if marker in b)
        if have >= NEED:
            e["queued"] = {"found": str(today), "main": v["main"]}
            print(f"  already queued  {e['job']} {e['label']}"); continue
        if have:
            problem = f"{e['job']} is partly queued ({have} of {NEED} posts): finish it by hand"; break
        if free < NEED:
            print(f"  no room yet     {e['job']} {e['label']} (needs {NEED}, free {free})"); break

        for key in ("video_url", "tiktok_video_url", "youtube_cover_url", "instagram_video_url"):
            if v.get(key) and not head_bytes(v[key]):
                problem = f"{e['job']}: media {key} no longer downloads, re-upload it"; break
        if problem: break
        if e["kind"] == "longform" and (head_bytes(v.get("instagram_video_url", v["video_url"])) or 0) > IG_MAX_BYTES:
            problem = f"{e['job']}: Instagram copy is over 300 MB, add instagram_video_url to the config"; break

        want = local_day(v["main"])
        if e["kind"] == "longform":
            ok = want.weekday() == 6 and want >= today + timedelta(days=2) and want not in longform_sundays
            if not ok:
                want = max(max(longform_sundays, default=today), today + timedelta(days=1)) + timedelta(days=1)
                while want.weekday() != 6 or want in longform_sundays:
                    want += timedelta(days=1)
            main = utc(want)
        else:
            main = v["main"]
            clash = any((a, main[:16]) in minutes for a in ACCOUNTS)
            if datetime.fromisoformat(main.replace("Z", "+00:00")) < now + timedelta(hours=2) or clash:
                want = max(want, today) + timedelta(days=1)
                while (want.weekday() not in (1, 3, 5) or want in yt_days
                       or any((a, utc(want)[:16]) in minutes for a in ACCOUNTS)):
                    want += timedelta(days=1)
                main = utc(want)
        moved = main != v["main"]
        print(f"  {'queue ' if apply else 'would queue'}  {e['job']} {e['label']}: {e['kind']} on "
              f"{local_day(main):%a %Y-%m-%d} 9 AM Central{' (re-slotted)' if moved else ''}")
        if apply:
            if moved:
                v["main"] = main; open(path, "w").write(json.dumps(v, indent=2, ensure_ascii=False) + "\n")
            run = subprocess.run([sys.executable, os.path.join(HERE, HELPER[e["kind"]]), path, "--apply"],
                                 capture_output=True, text=True)
            print("    " + run.stdout.strip().replace("\n", "\n    "))
            if run.returncode != 0:
                problem = f"{e['job']}: {HELPER[e['kind']]} failed: {(run.stderr or run.stdout).strip()[-300:]}"; break
            e["queued"] = {"date": str(today), "main": main}
            json.dump(entries, open(WAITLIST, "w"), indent=1)
        queued_now.append(e["job"])
        free -= NEED
        day = local_day(main); yt_days.add(day)
        if e["kind"] == "longform":
            longform_sundays.add(day)
        for a in ACCOUNTS:
            minutes.add((a, main[:16]))

    if apply:
        json.dump(entries, open(WAITLIST, "w"), indent=1)
    left = len(pending(entries)) - (0 if apply else len(queued_now))
    print(f"{'queued' if apply else '(dry) would queue'}: {', '.join(queued_now) or 'none'}; still waiting: {left}")
    if problem:
        print("PROBLEM: " + problem); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
