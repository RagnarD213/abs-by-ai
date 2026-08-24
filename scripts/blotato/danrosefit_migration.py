#!/usr/bin/env python3
"""Build the @danrosefit Instagram posting queue in Blotato.

Executes steps 2-5 of Handoffs/handoff-20260824-instagram-migration-danrosefit.md:

  SURGERY  drop every photo post and the follow-along reel from the Instagram queue
  SYNC     recreate each surviving reel on @danrosefit at the IDENTICAL scheduledTime
           so it lands with its Facebook (and YouTube) sibling
  MIRROR   shift the @abs.by.ai original +24h, same time-of-day, CTA rewritten to
           point at @danrosefit -- @danrosefit always goes first
  BACKFILL drip the 4 previously-published reels onto days no Instagram account posts
  VERIFY   re-read the queue from the API and assert every invariant

Facebook and YouTube are NEVER touched: the stagger exists to protect people who
follow both Instagram accounts, not to desynchronise platforms.

Idempotent. Every write is recorded in STATE_PATH keyed by a stable operation key, so
a re-run resumes instead of double-posting. Blotato has already double-posted once by
accident (2026-08-20), which is why this is not optional.

    python3 scripts/blotato/danrosefit_migration.py --account-id <id>            # dry run
    python3 scripts/blotato/danrosefit_migration.py --account-id <id> --apply    # execute
    python3 scripts/blotato/danrosefit_migration.py --account-id <id> --verify-only
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEY_PATH = os.path.join(ROOT, "Business", "blotato-api-key.txt")
STATE_PATH = os.path.join(ROOT, "Business", "blotato-danrosefit-migration-state.json")
BASE = "https://backend.blotato.com/v2"

ABS_BY_AI = "65632"                     # @abs.by.ai, the mirror
MIRROR_SHIFT = timedelta(days=1)        # Dan's decision, 2026-08-24

CTA_OLD = "Free AI preview of your own six-pack — link in the first comment 👇"
CTA_MAIN = "Comment ABS and I'll send you the free AI preview 👇"
CTA_MIRROR = "Full breakdown from @danrosefit 👇"

# Reels dropped from the Instagram feed. Measured 1.8-2.0 s average watch time on the
# published follow-alongs -- they suppress whatever posts after them. They belong in a
# Highlight and on YouTube. Matched on the caption's opening line, not on an id, so the
# script stays correct if the queue is rebuilt.
DROP_REEL_PREFIXES = [
    "The three-minute total body workout, follow-along version.",
]

# Step 3. Already published to @abs.by.ai; the media is on Blotato's CDN and is reused
# rather than re-uploaded. Best performer first -- the grid is thin after archiving and
# early visitors read the top row. Captions are rewritten, not reposted: a word-for-word
# repost is visible to anyone who saw the original.
BACKFILL = [
    {
        "key": "backfill-night-snacking",
        "source_post_id": "6371472",
        "mediaUrl": "https://database.blotato.io/storage/v1/object/public/public_media/"
                    "a836fa29-cde6-464e-8712-36d8a0de9f32/e2ed7153-4d39-4cc8-a31a-9300a71e64d6.mp4",
        "text": (
            "I lost the weight in the hour I wasn't training.\n\n"
            "Dinner is done, you're on the couch, and nothing about the day has gone "
            "wrong yet. That hour is where most diets actually die — not at the gym, "
            "not at lunch.\n\n"
            "What fixed it for me cost about two dollars.\n\n"
            f"{CTA_MAIN}\n\n"
            "#abs #fatloss #sixpackabs #diettips #aifitness"
        ),
    },
    {
        "key": "backfill-instead-of-crunches",
        "source_post_id": "6315443",
        "mediaUrl": "https://database.blotato.io/storage/v1/object/public/public_media/"
                    "a836fa29-cde6-464e-8712-36d8a0de9f32/4f0f52c1-4c68-4472-896b-5115758fb4ec.mp4",
        "text": (
            "You can have abs and still look wide.\n\n"
            "That is what nobody explains. Crunches build the muscle sitting on top. "
            "They do nothing for the one underneath — the one that actually pulls your "
            "waist in.\n\n"
            "This is what I do instead. No equipment, anywhere, starting today.\n\n"
            f"{CTA_MAIN}\n\n"
            "#abs #absworkout #sixpackabs #coreworkout #aifitness"
        ),
    },
    {
        "key": "backfill-channel-intro",
        "source_post_id": "6274086",
        "mediaUrl": "https://database.blotato.io/storage/v1/object/public/public_media/"
                    "a836fa29-cde6-464e-8712-36d8a0de9f32/613131fe-c14e-41c1-a40d-0e107ce29a41.mp4",
        "text": (
            "I was 200 lbs at 38. I had a real six-pack at 40.\n\n"
            "No trainer, no coach, no program. The AI tools that replaced both of them, "
            "the four ab muscles most workouts never touch, and what I'd skip entirely "
            "if I were starting over at 40 — that is what this account is.\n\n"
            "Nothing to buy. Just the method.\n\n"
            f"{CTA_MAIN}\n\n"
            "#absworkout #sixpackabs #aifitness #over40 #fitnesstips"
        ),
    },
    {
        "key": "backfill-four-ab-muscles",
        "source_post_id": "6332851",
        "mediaUrl": "https://database.blotato.io/storage/v1/object/public/public_media/"
                    "a836fa29-cde6-464e-8712-36d8a0de9f32/3ef7ba6f-fc20-4098-8b0c-c8954cd7f2df.mp4",
        "text": (
            "Hundreds of crunches, and your waist never changed shape.\n\n"
            "Because a crunch trains one of the four muscles down there. You also have "
            "obliques, a transverse abdominis, and the deep stabilisers under all of "
            "it — and the ones you're skipping are the ones that narrow you.\n\n"
            "Three exercises, sixty seconds, all four covered. No equipment.\n\n"
            f"{CTA_MAIN}\n\n"
            "#absworkout #coreworkout #sixpackabs #homeworkout #fitnesstips"
        ),
    },
]

# 17:00 America/Chicago = 22:00 UTC while CDT is in force, which covers the backfill's
# two-to-four-week run. Matches the established reel slot.
BACKFILL_HOUR_UTC = 22
BACKFILL_WEEKDAYS = [0]     # Monday only -- see pick_backfill_days()

# Blotato's auto first-comment currently carries the absbyai.com link on all 88
# Instagram posts (and, despite the handoff's note, on none of the Facebook ones).
# It stays until ManyChat is live, because until then the link is the only working
# path from a reel to the site -- then run with --no-first-comment.
DROP_FIRST_COMMENT = False


# --------------------------------------------------------------------------- http
def api_key() -> str:
    with open(KEY_PATH) as fh:
        return fh.read().strip()


def call(method: str, path: str, key: str, body=None, retries: int = 4):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retries):
        req = urllib.request.Request(
            BASE + path, data=data, method=method,
            headers={"blotato-api-key": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            payload = exc.read().decode(errors="replace")
            if exc.code == 429:
                wait = 30
                m = re.search(r"retry in (\d+)", payload)
                if m:
                    wait = int(m.group(1)) + 2
                print(f"    429, honouring retry-in {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise SystemExit(f"{method} {path} -> {exc.code} {payload}")
    raise SystemExit(f"{method} {path} -> gave up after {retries} attempts")


def fetch_schedules(key: str) -> list:
    items, cursor = [], None
    while True:
        q = "?limit=100" + (f"&cursor={cursor}" if cursor else "")
        page = call("GET", "/schedules" + q, key)
        items += page.get("items", [])
        cursor = page.get("cursor") or page.get("nextCursor")
        if not cursor:
            return items


# --------------------------------------------------------------------------- state
def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as fh:
            return json.load(fh)
    return {"created": {}, "deleted": {}, "shifted": {}}


def save_state(state: dict) -> None:
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
    os.replace(tmp, STATE_PATH)


# --------------------------------------------------------------------------- helpers
def parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def rewrite_cta(text: str, cta: str) -> str:
    """Swap the CTA line. Falls back to inserting one above the hashtags."""
    if cta in text:
        return text
    if CTA_OLD in text:
        return text.replace(CTA_OLD, cta)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "link in the first comment" in line.lower():
            lines[i] = cta
            return "\n".join(lines)
    for i, line in enumerate(lines):
        if line.strip().startswith("#"):
            lines.insert(i, cta)
            lines.insert(i + 1, "")
            return "\n".join(lines)
    return text + "\n\n" + cta


def hashtags(text: str) -> int:
    return len(re.findall(r"#\w+", text))


def is_photo(item: dict) -> bool:
    return not item["draft"]["target"].get("mediaType")


def content_key(item: dict) -> str:
    """Identifies one piece of content WITHIN an account -- the CDN media url."""
    urls = item["draft"]["content"].get("mediaUrls") or []
    return urls[0] if urls else item["draft"]["content"]["text"][:80]


def sibling_key(text: str) -> str:
    """Identifies one piece of content ACROSS platforms.

    Instagram and Facebook carry DIFFERENT media urls for the same post -- each
    platform got its own upload and its own aspect crop -- so 82 of the 88 pairs
    have nothing in common but the copy. The hook line is what is actually shared,
    and it is what makes "synchronized" checkable.
    """
    return re.sub(r"\s+", " ", text.strip().split("\n")[0]).lower()


def pick_backfill_days(busy_days: set, start: datetime, count: int) -> list:
    """Idle days only.

    `busy_days` holds every date carrying an Instagram post on EITHER account after
    the mirror shift. With @danrosefit on Tue/Thu/Sat and the mirror landing
    Wed/Fri/Sun, Monday is the only genuinely idle day -- the handoff's "Monday and
    Friday" was computed before the +1 day stagger was decided, and Friday now carries
    the Thursday mirror. One a week, so the four reels run four weeks.
    """
    picked, day = [], start.date()
    guard = 0
    while len(picked) < count and guard < 400:
        guard += 1
        day += timedelta(days=1)
        if day.weekday() not in BACKFILL_WEEKDAYS:
            continue
        if day in busy_days:
            continue
        picked.append(day)
        busy_days.add(day)
    if len(picked) < count:
        raise SystemExit("could not find enough idle days for the backfill")
    return picked


# --------------------------------------------------------------------------- plan
def build_plan(items: list, account_id: str) -> dict:
    ig = [i for i in items if i["draft"]["target"]["targetType"] == "instagram"]
    mine = [i for i in ig if i["draft"]["accountId"] == ABS_BY_AI]
    already = [i for i in ig if i["draft"]["accountId"] == account_id]

    drop_photos = [i for i in mine if is_photo(i)]
    drop_followalong = [
        i for i in mine
        if not is_photo(i)
        and any(i["draft"]["content"]["text"].startswith(p) for p in DROP_REEL_PREFIXES)
    ]
    dropped_ids = {i["id"] for i in drop_photos} | {i["id"] for i in drop_followalong}
    survivors = sorted((i for i in mine if i["id"] not in dropped_ids),
                       key=lambda x: x["scheduledAt"])

    # Photos leaving the Instagram feed resolves the four photo/reel duplicate pairs
    # the audit found (milk, supplements, daily abs, food photos) -- the reel is what
    # survives in every case. Facebook keeps both; it is a different feed.
    sync, mirror = [], []
    for item in survivors:
        when = parse(item["scheduledAt"])
        tgt = dict(item["draft"]["target"])
        sync.append({
            "key": f"sync::{item['id']}",
            "scheduledTime": iso(when),
            "mirror_of": item["id"],
            "target": {
                "targetType": "instagram",
                "mediaType": tgt.get("mediaType", "reel"),
                "shareToFeed": tgt.get("shareToFeed", True),
                **({"coverImageUrl": tgt["coverImageUrl"]} if tgt.get("coverImageUrl") else {}),
                **({"firstComment": tgt["firstComment"]}
                   if tgt.get("firstComment") and not DROP_FIRST_COMMENT else {}),
            },
            "text": rewrite_cta(item["draft"]["content"]["text"], CTA_MAIN),
            "mediaUrls": item["draft"]["content"]["mediaUrls"],
        })
        mirror.append({
            "id": item["id"],
            "from": iso(when),
            "scheduledTime": iso(when + MIRROR_SHIFT),
            "text": rewrite_cta(item["draft"]["content"]["text"], CTA_MIRROR),
            "target": tgt,
            "mediaUrls": item["draft"]["content"]["mediaUrls"],
        })

    busy = {parse(i["scheduledAt"]).date() for i in ig if i["id"] not in dropped_ids}
    busy |= {parse(m["scheduledTime"]).date() for m in mirror}
    busy |= {parse(i["scheduledAt"]).date() for i in already}

    # Never backfill something the future queue already carries.
    queued_media = {content_key(i) for i in ig if i["id"] not in dropped_ids}
    fresh = [b for b in BACKFILL if b["mediaUrl"] not in queued_media]
    skipped = [b["key"] for b in BACKFILL if b["mediaUrl"] in queued_media]

    start = max(datetime.now(timezone.utc), min(parse(i["scheduledAt"]) for i in ig))
    days = pick_backfill_days(set(busy), start, len(fresh))
    backfill = []
    for spec, day in zip(fresh, days):
        when = datetime(day.year, day.month, day.day, BACKFILL_HOUR_UTC,
                        tzinfo=timezone.utc)
        backfill.append({
            "key": spec["key"],
            "scheduledTime": iso(when),
            "target": {"targetType": "instagram", "mediaType": "reel",
                       "shareToFeed": True},
            "text": spec["text"],
            "mediaUrls": [spec["mediaUrl"]],
        })

    return {
        "delete": [{"id": i["id"], "why": "photo", "when": i["scheduledAt"],
                    "text": i["draft"]["content"]["text"][:60]} for i in drop_photos]
                  + [{"id": i["id"], "why": "follow-along", "when": i["scheduledAt"],
                      "text": i["draft"]["content"]["text"][:60]} for i in drop_followalong],
        "sync": sync,
        "mirror": mirror,
        "backfill": backfill,
        "backfill_skipped": skipped,
        "already_on_target": len(already),
    }


def check_plan(plan: dict, items: list) -> int:
    """Assert the invariants on the PLANNED end state, before anything is written.

    Verifying after the fact is required, but a plan that provably violates an
    invariant should never reach the API in the first place.
    """
    fails = []

    def check(ok, msg):
        print(("  PASS  " if ok else "  FAIL  ") + msg)
        if not ok:
            fails.append(msg)

    print("\nPLAN CHECK")
    deleted = {e["id"] for e in plan["delete"]}
    fb_times = defaultdict(list)
    for i in items:
        if i["draft"]["target"]["targetType"] == "facebook":
            fb_times[sibling_key(i["draft"]["content"]["text"])].append(
                parse(i["scheduledAt"]))

    bad = [s for s in plan["sync"]
           if parse(s["scheduledTime"]) not in fb_times.get(sibling_key(s["text"]), [])]
    check(not bad, f"all {len(plan['sync'])} sync posts land on their Facebook "
                   f"sibling's timestamp")

    origins = {s["mirror_of"]: parse(s["scheduledTime"]) for s in plan["sync"]}
    off = [(m["id"], str(parse(m["scheduledTime"]) - origins[m["id"]]))
           for m in plan["mirror"]
           if m["id"] not in origins or parse(m["scheduledTime"]) - origins[m["id"]] != MIRROR_SHIFT]
    check(not off, f"all {len(plan['mirror'])} mirrors sit exactly +24h behind "
                   f"their original" + (f" -- {off[:3]}" if off else ""))

    per_day = defaultdict(list)
    for s in plan["sync"]:
        per_day[parse(s["scheduledTime"]).date()].append(("main", "sync"))
    for b in plan["backfill"]:
        per_day[parse(b["scheduledTime"]).date()].append(("main", "backfill"))
    for m in plan["mirror"]:
        per_day[parse(m["scheduledTime"]).date()].append(("mirror", "sync"))
    for i in items:
        t = i["draft"]["target"]
        if t["targetType"] == "instagram" and i["id"] not in deleted \
                and i["id"] not in {m["id"] for m in plan["mirror"]}:
            per_day[parse(i["scheduledAt"]).date()].append(("other", "sync"))

    mixed = {d: v for d, v in per_day.items()
             if {k for _, k in v} == {"sync", "backfill"}}
    check(not mixed, f"no day carries both a sync post and a backfill post "
                     f"({sorted(mixed)[:3]})")
    twice = {d: v for d, v in per_day.items()
             if len({a for a, _ in v}) < len(v)}
    check(not twice, f"no account posts twice on one day ({sorted(twice)[:3]})")

    allnew = plan["sync"] + plan["backfill"]
    check(all(x["mediaUrls"] for x in allnew), "every new post has media")
    over = [x["text"].splitlines()[0] for x in allnew if hashtags(x["text"]) > 5]
    check(not over, f"no new caption exceeds 5 hashtags ({over[:2]})")
    check(all(CTA_OLD not in x["text"] for x in allnew + plan["mirror"]),
          "the old link-in-first-comment CTA is gone from every rewritten caption")
    horizon = datetime.now(timezone.utc) + timedelta(days=270)
    late = [x["scheduledTime"] for x in allnew + plan["mirror"]
            if parse(x["scheduledTime"]) > horizon]
    check(not late, f"nothing lands past the 9-month limit ({late[:2]})")
    check(all(parse(x["scheduledTime"]) > datetime.now(timezone.utc)
              for x in allnew + plan["mirror"]),
          "every scheduled time is in the future")
    return len(fails)


# --------------------------------------------------------------------------- execute
def create(plan_item: dict, account_id: str, key: str, state: dict, apply: bool) -> None:
    if plan_item["key"] in state["created"]:
        return
    if not apply:
        return
    body = {
        "post": {
            "accountId": account_id,
            "target": plan_item["target"],
            "content": {
                "platform": "instagram",
                "text": plan_item["text"],
                "mediaUrls": plan_item["mediaUrls"],
            },
        },
        "scheduledTime": plan_item["scheduledTime"],
    }
    res = call("POST", "/posts", key, body)
    state["created"][plan_item["key"]] = {
        "response": res, "scheduledTime": plan_item["scheduledTime"]}
    save_state(state)


def delete(entry: dict, key: str, state: dict, apply: bool) -> None:
    if entry["id"] in state["deleted"] or not apply:
        return
    call("DELETE", f"/schedules/{entry['id']}", key)
    state["deleted"][entry["id"]] = entry
    save_state(state)


def shift(entry: dict, key: str, state: dict, apply: bool) -> None:
    """In-place time change -- one call, and it cannot half-fail into a lost post."""
    if entry["id"] in state["shifted"] or not apply:
        return
    body = {
        "post": {
            "accountId": ABS_BY_AI,
            "platform": "instagram",
            "text": entry["text"],
            "mediaUrls": entry["mediaUrls"],
            **{k: v for k, v in entry["target"].items() if k != "targetType"},
        },
        "scheduledTime": entry["scheduledTime"],
    }
    for method in ("PUT", "PATCH"):
        try:
            call(method, f"/schedules/{entry['id']}", key, body, retries=1)
            state["shifted"][entry["id"]] = entry
            save_state(state)
            return
        except SystemExit as exc:
            last = exc
    raise SystemExit(f"could not shift schedule {entry['id']}: {last}")


# --------------------------------------------------------------------------- verify
def verify(key: str, account_id: str) -> int:
    items = fetch_schedules(key)
    ig = [i for i in items if i["draft"]["target"]["targetType"] == "instagram"]
    fb = [i for i in items if i["draft"]["target"]["targetType"] == "facebook"]
    main = [i for i in ig if i["draft"]["accountId"] == account_id]
    mirror = [i for i in ig if i["draft"]["accountId"] == ABS_BY_AI]
    fb_times = defaultdict(list)
    for i in fb:
        fb_times[sibling_key(i["draft"]["content"]["text"])].append(
            parse(i["scheduledAt"]))

    fails = []

    def check(ok, msg):
        print(("  PASS  " if ok else "  FAIL  ") + msg)
        if not ok:
            fails.append(msg)

    print("\nVERIFY")
    check(all(i["draft"]["accountId"] in (account_id, ABS_BY_AI) for i in ig),
          "every Instagram post targets @danrosefit or @abs.by.ai")
    check(not [i for i in ig if is_photo(i)],
          f"no photo posts remain in the Instagram queue ({len(ig)} posts)")

    # sync: shares its timestamp with the Facebook sibling carrying the same media
    bad = [i for i in main
           if sibling_key(i["draft"]["content"]["text"]) in fb_times
           and parse(i["scheduledAt"])
           not in fb_times[sibling_key(i["draft"]["content"]["text"])]]
    orphan = [i for i in main
              if sibling_key(i["draft"]["content"]["text"]) not in fb_times]
    check(not bad, f"every sync post shares its timestamp with its Facebook sibling "
                   f"({len(main) - len(orphan)} matched, {len(orphan)} backfill/no sibling)")

    # mirror: exactly +24h behind its @danrosefit original, never earlier
    by_media = defaultdict(list)
    for i in main:
        by_media[content_key(i)].append(parse(i["scheduledAt"]))
    off, unpaired = [], []
    for i in mirror:
        origins = by_media.get(content_key(i))
        if not origins:
            unpaired.append(i)
            continue
        delta = parse(i["scheduledAt"]) - min(origins)
        if delta != MIRROR_SHIFT:
            off.append((i["id"], str(delta)))
    check(not off, f"every @abs.by.ai mirror is exactly +24h behind its original "
                   f"({len(mirror) - len(unpaired)} checked)"
                   + (f" -- off: {off[:5]}" if off else ""))
    check(not unpaired, f"every @abs.by.ai post has a @danrosefit original "
                        f"({len(unpaired)} unpaired)")

    # one Instagram post per day per account, and no day mixes sync with backfill
    per_day = defaultdict(list)
    for i in ig:
        per_day[parse(i["scheduledAt"]).date()].append(
            (i["draft"]["accountId"], content_key(i)))
    clash = {d: v for d, v in per_day.items()
             if len({a for a, _ in v}) < len(v)}
    check(not clash, f"no account posts twice on one day ({len(clash)} clashes)")

    backfill_media = {b["mediaUrl"] for b in BACKFILL}
    mixed = {d: v for d, v in per_day.items()
             if any(m in backfill_media for _, m in v)
             and any(m not in backfill_media for _, m in v)}
    check(not mixed, f"no day carries both a sync post and a backfill post "
                     f"({len(mixed)} mixed)")

    check(all(i["draft"]["content"].get("mediaUrls") for i in ig),
          "every Instagram post has media")
    horizon = datetime.now(timezone.utc) + timedelta(days=270)
    late = [i["scheduledAt"] for i in ig if parse(i["scheduledAt"]) > horizon]
    check(not late, f"nothing scheduled past the 9-month limit ({len(late)} late)")
    over = [(i["id"], hashtags(i["draft"]["content"]["text"])) for i in ig
            if hashtags(i["draft"]["content"]["text"]) > 5]
    check(not over, f"no Instagram caption carries more than 5 hashtags ({over[:3]})")
    check(all(CTA_OLD not in i["draft"]["content"]["text"] for i in ig),
          "the link-in-first-comment CTA is gone from every Instagram caption")

    print(f"\n  @danrosefit: {len(main)} posts   @abs.by.ai: {len(mirror)} posts   "
          f"Facebook: {len(fb)} posts (untouched)")
    return len(fails)


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--account-id", default=os.environ.get("DANROSEFIT_ACCOUNT_ID"),
                    help="Blotato accountId for @danrosefit")
    ap.add_argument("--apply", action="store_true", help="actually write")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--no-first-comment", action="store_true",
                    help="drop Blotato's auto first comment (run this once ManyChat "
                         "is live and the Comment-ABS CTA actually works)")
    args = ap.parse_args()

    global DROP_FIRST_COMMENT
    DROP_FIRST_COMMENT = args.no_first_comment
    key = api_key()
    if not args.account_id:
        accounts = call("GET", "/accounts", key)
        found = [a for a in (accounts.get("items") or accounts)
                 if a.get("username", "").lower() == "danrosefit"]
        if not found:
            print("@danrosefit is not connected to Blotato. Dan must add it under "
                  "Settings -> Social accounts, signing in with the Instagram "
                  "credentials rather than through Facebook. Nothing was changed.")
            return 2
        args.account_id = found[0]["id"]
        print(f"resolved @danrosefit -> accountId {args.account_id}")

    if args.verify_only:
        return 1 if verify(key, args.account_id) else 0

    items = fetch_schedules(key)
    plan = build_plan(items, args.account_id)
    state = load_state()

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"=== {mode} === @danrosefit accountId {args.account_id}")
    print(f"\nDELETE {len(plan['delete'])} Instagram posts from @abs.by.ai")
    for e in plan["delete"][:6]:
        print(f"   {e['when'][:10]}  {e['why']:<13} {e['text']!r}")
    if len(plan["delete"]) > 6:
        print(f"   ... and {len(plan['delete']) - 6} more")

    print(f"\nSYNC   create {len(plan['sync'])} posts on @danrosefit at identical times")
    for e in plan["sync"][:4]:
        print(f"   {e['scheduledTime'][:16]}  {e['text'].splitlines()[0]!r}")

    print(f"\nMIRROR shift {len(plan['mirror'])} @abs.by.ai posts +1 day")
    for e in plan["mirror"][:4]:
        print(f"   {e['from'][:16]} -> {e['scheduledTime'][:16]}")

    print(f"\nBACKFILL {len(plan['backfill'])} reels onto idle days"
          + (f" (skipped, already queued: {plan['backfill_skipped']})"
             if plan["backfill_skipped"] else ""))
    for e in plan["backfill"]:
        print(f"   {e['scheduledTime'][:16]}  {e['text'].splitlines()[0]!r}")

    fails = check_plan(plan, items)
    if fails:
        print(f"\nPLAN FAILED {fails} invariant(s) -- nothing was written.")
        return 1

    if plan["already_on_target"]:
        print(f"\nNOTE {plan['already_on_target']} posts already exist on @danrosefit; "
              "the state file decides what is re-created.")

    if not args.apply:
        print("\nDry run. Re-run with --apply to execute.")
        return 0

    print("\nexecuting...")
    for e in plan["delete"]:
        delete(e, key, state, True)
    print(f"  deleted {len(state['deleted'])}")
    for e in plan["sync"]:
        create(e, args.account_id, key, state, True)
    for e in plan["backfill"]:
        create(e, args.account_id, key, state, True)
    print(f"  created {len(state['created'])}")
    for e in plan["mirror"]:
        shift(e, key, state, True)
    print(f"  shifted {len(state['shifted'])}")

    return 1 if verify(key, args.account_id) else 0


if __name__ == "__main__":
    sys.exit(main())
