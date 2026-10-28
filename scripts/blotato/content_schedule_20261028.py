#!/usr/bin/env python3
"""Content schedule overhaul, Dan approved 2026-10-28 (Handoffs/handoff-20261028-content-schedule-overhaul.md).

Data + checker + one-time applier:
  python3 content_schedule_20261028.py check           # validate the whole plan against release_phases.py and the live queue
  python3 content_schedule_20261028.py apply-live      # re-date the live Blotato schedules (time-only PATCH, nothing deleted)
  python3 content_schedule_20261028.py apply-waitlist  # re-date waitlist configs, set flags, sort the waiting list

Every action is a re-date: no schedule is deleted or recreated. A video's four posts keep their content and media.
Kitchen = Dan on the fridge/cabinet kitchen set (checked by frame, 2026-10-28; table in Docs/LONGFORM_RELEASE_CALENDAR.md).
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import release_phases as rp  # noqa: E402

CT = ZoneInfo("America/Chicago")
YOUTUBE = "46963"
D = date

# --- live Blotato schedules to re-date: slug -> (new local date, "HH:MM") of the main/YouTube post.
# Long-forms (kind LF): YouTube at 9 AM on the date, Facebook/Instagram/TikTok next day at noon.
LIVE_SHORTS = {
    "sl05-short5": (D(2026, 11, 26), "18:00"),  # kitchen (Zeeshan Stop Deadlifting set) out of phase 1
    "sl05-short3": (D(2026, 12, 3), "18:00"),   # kitchen
    "ds35-dad-bod": (D(2026, 10, 31), "09:00"),
    "ds44-hormozi-fat-guy": (D(2026, 11, 3), "09:00"),
    "ds31-ai-homework": (D(2026, 11, 16), "09:00"),
    "sl18-short2": (D(2026, 11, 20), "09:00"),
    "sl09-short1": (D(2026, 11, 30), "18:00"),  # kitchen (Oura review set), after the Oura review Nov 29
    "sl09-short2": (D(2026, 12, 3), "09:00"),
    "sl09-short3": (D(2026, 12, 7), "09:00"),
    "sl09-short4": (D(2026, 12, 12), "09:00"),
    "sl09-short5": (D(2026, 12, 14), "18:00"),
}
LIVE_LONGFORMS = {
    "ro10-calories-not-losing-weight": D(2027, 1, 17),  # YouTube only (socials went out Oct 8)
    "oura-ring-review": D(2026, 11, 29),                # kitchen
    "ro16-belly-fat-90-days": D(2026, 12, 27),
    "ro02-the-vacuum": D(2027, 1, 15),
    "ro03-vacuum-workout": D(2027, 1, 22),
    "ro11-calories-dont-matter": D(2027, 1, 27),
}

# --- waiting list: config basename (no .json) -> new main (local date, "HH:MM"); long-forms use 09:00.
WAIT = {
    # phase 1 Shorts (poolside, not kitchen)
    "ds22-how-to-use-the-ab-wheel": (D(2026, 11, 5), "09:00"),
    "ds33-ronaldo-ab-belt": (D(2026, 11, 11), "09:00"),
    "ds14-3-ways-to-reduce-alcohol": (D(2026, 11, 12), "09:00"),
    "ds40-bill-maher-fat-90-year-old": (D(2026, 11, 13), "09:00"),
    "ds24-how-to-do-rear-delt-flys": (D(2026, 11, 19), "09:00"),
    # phase 2
    "ds21-how-to-do-hammer-curls": (D(2026, 11, 26), "09:00"),
    "ro08-intermittent-fasting": (D(2026, 11, 27), "09:00"),
    "sl16-short1-just-skip-breakfast": (D(2026, 11, 28), "18:00"),
    "ro07-work-out-every-day": (D(2026, 12, 2), "09:00"),
    "sl16-short2-why-carbs-destroy-your-productivity": (D(2026, 12, 1), "18:00"),
    "ro19-my-first-spray-tan": (D(2026, 12, 4), "09:00"),
    "sl15-short1-why-you-look-less-ripped-in-photos": (D(2026, 12, 5), "18:00"),
    "abs-at-40-vs-25": (D(2026, 12, 6), "09:00"),
    "sl16-short3-never-break-your-fast-with-alcohol": (D(2026, 12, 7), "18:00"),
    "sl15-short2-get-a-tan-without-sun-damage": (D(2026, 12, 8), "18:00"),
    "ro20-invest-in-your-health": (D(2026, 12, 9), "09:00"),
    "ds20-five-levels-of-pushups": (D(2026, 12, 10), "09:00"),
    "ro20b-what-to-cut": (D(2026, 12, 11), "09:00"),
    "sl16-short4-why-you-need-a-simple-nutrition-plan": (D(2026, 12, 12), "18:00"),
    "ro17-3-healthy-foods": (D(2026, 12, 13), "09:00"),
    "sl19-short1-coconut-water-is-just-sugar-water": (D(2026, 12, 14), "09:00"),
    "sl19-short2-trail-mix-more-calories-than-a-big-mac": (D(2026, 12, 15), "09:00"),
    "ds02-getting-abs-looksmaxxes-your-face": (D(2026, 12, 15), "18:00"),
    "ro20c-what-to-buy": (D(2026, 12, 16), "09:00"),
    "ds03-3-most-important-supplements-for-men": (D(2026, 12, 17), "09:00"),
    "ds07-top-3-ways-to-use-ai-to-get-abs": (D(2026, 12, 17), "18:00"),
    "sl19-short3-my-4-high-protein-snacks": (D(2026, 12, 19), "09:00"),
    "ds11-why-you-must-weigh-yourself-daily": (D(2026, 12, 19), "18:00"),
    "ro13-alcohol-and-abs": (D(2026, 12, 20), "09:00"),
    # phase 3
    "sl07-short1-stop-trying-to-lose-1-pound-a-week": (D(2026, 12, 28), "09:00"),
    "sl07-short2-weigh-yourself-every-morning": (D(2026, 12, 29), "09:00"),
    "sl07-short3-work-out-every-morning": (D(2026, 12, 31), "09:00"),
    "sl07-short4-the-3-pound-rule": (D(2027, 1, 2), "09:00"),
    "sl07-short5-track-your-calories-with-a-photo": (D(2027, 1, 4), "09:00"),
    "ro04-arms-shoulders-workout-only": (D(2027, 1, 6), "09:00"),       # unchanged (Dan approved Oct 25)
    "ds13-the-1-change-i-made-to-get-abs-at-40": (D(2027, 1, 7), "09:00"),
    "ro18-make-time-for-exercise": (D(2027, 1, 13), "09:00"),           # unchanged (Dan approved Oct 27)
    "ds06-what-every-body-fat-percentage-looks-like": (D(2027, 1, 14), "09:00"),
    "sl08-short1-why-i-fast-until-2-pm-every-day": (D(2027, 1, 18), "09:00"),
    "sl08-short2-eat-a-salad-first-to-eat-less": (D(2027, 1, 19), "09:00"),
    "ds10-top-3-non-weight-loss-benefits-of-zepbound": (D(2027, 1, 21), "09:00"),
    "sl08-short3-stop-drinking-your-calories": (D(2027, 1, 21), "18:00"),
    "sl08-short4-snack-on-protein-not-carbs": (D(2027, 1, 23), "09:00"),
    "sl08-short5-make-fasting-easier-with-black-coffee": (D(2027, 1, 25), "09:00"),
    "ds01-top-5-ab-exercises": (D(2027, 1, 28), "09:00"),
}
# Entries that keep an explicit approval and are not touched: DS-05 (Dec 10, 5 PM), DS-20 keeps 9 AM Dec 10 (in WAIT above).
KITCHEN_CONFIGS = {"ro07-work-out-every-day", "ro08-intermittent-fasting", "ro19-my-first-spray-tan", "abs-at-40-vs-25",
                   "ro20-invest-in-your-health", "ro20b-what-to-cut", "ro20c-what-to-buy",
                   "sl15-short1-why-you-look-less-ripped-in-photos", "sl15-short2-get-a-tan-without-sun-damage",
                   "sl16-short1-just-skip-breakfast", "sl16-short2-why-carbs-destroy-your-productivity",
                   "sl16-short3-never-break-your-fast-with-alcohol", "sl16-short4-why-you-need-a-simple-nutrition-plan"}
LONGFORM_CONFIGS = {"ro08-intermittent-fasting", "ro07-work-out-every-day", "ro19-my-first-spray-tan", "abs-at-40-vs-25",
                    "ro20-invest-in-your-health", "ro20b-what-to-cut", "ro20c-what-to-buy", "ro17-3-healthy-foods",
                    "ro13-alcohol-and-abs", "ro04-arms-shoulders-workout-only", "ro18-make-time-for-exercise"}
# parent long-form config basename for waitlist Shorts that need one (added to entries as "after"/"parent_config")
PARENTS = {
    "sl07": "ro16-belly-fat-90-days",
    "sl19": "ro17-3-healthy-foods",
}
# configs whose "main" is only a parent reference for Shorts slotting (live long-forms moved above)
PARENT_MAIN = {"ro16-belly-fat-90-days": (D(2026, 12, 27), "09:00"), "ro10-calories-not-losing-weight": (D(2027, 1, 17), "09:00"),
               "oura-ring-review": (D(2026, 11, 29), "09:00"), "ro02-the-vacuum": (D(2027, 1, 15), "09:00"),
               "ro03-vacuum-workout": (D(2027, 1, 22), "09:00"), "ro11-calories-dont-matter": (D(2027, 1, 27), "09:00"),
               "ro06-home-workout-budget": (D(2026, 11, 25), "09:00")}


def to_utc(day: date, hhmm: str) -> str:
    local = datetime(day.year, day.month, day.day, int(hhmm[:2]), int(hhmm[3:]), tzinfo=CT)
    return local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def local_of(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(CT)


def acct(i: dict) -> str:
    return str(i.get("accountId") or (i.get("draft") or {}).get("accountId"))


def slug_items(items: list, slug: str) -> list:
    pat = re.compile(r"utm_content=" + re.escape(slug) + r"(?![\w-])")
    return [i for i in items if pat.search(json.dumps(i))]


def live_actions(items: list) -> list:
    """[(schedule id, account, platform, old ISO, new ISO, slug)] for every live re-date."""
    out = []
    for slug, (day, hhmm) in LIVE_SHORTS.items():
        found = slug_items(items, slug)
        if len(found) != 4:
            raise SystemExit(f"{slug}: expected 4 live schedules, found {len(found)}")
        for i in found:
            out.append((i["id"], acct(i), i["draft"]["target"]["targetType"], i["scheduledAt"], to_utc(day, hhmm), slug))
    for slug, day in LIVE_LONGFORMS.items():
        found = slug_items(items, slug)
        want = 1 if slug.startswith("ro10") else 4
        if len(found) != want:
            raise SystemExit(f"{slug}: expected {want} live schedules, found {len(found)}")
        for i in found:
            new = to_utc(day, "09:00") if acct(i) == YOUTUBE else to_utc(day + timedelta(days=1), "12:00")
            out.append((i["id"], acct(i), i["draft"]["target"]["targetType"], i["scheduledAt"], new, slug))
    return out


def final_calendar(items: list, actions: list) -> dict:
    """Final state per local (day, hh:mm) of YouTube posts: {(day, hhmm): [labels]} for live + waitlist, plus long-form days."""
    moved = {a[0]: a[4] for a in actions}
    cal: dict = {}
    for i in items:
        if acct(i) != YOUTUBE:
            continue
        iso = moved.get(i["id"], i["scheduledAt"])
        t = local_of(iso)
        m = re.search(r"utm_content=([\w-]+)", json.dumps(i))
        lf = "utm_campaign=longform" in json.dumps(i)
        cal.setdefault((t.date(), t.strftime("%H:%M")), []).append((m.group(1) if m else "?", "LF" if lf else "S", "live"))
    for name, (day, hhmm) in WAIT.items():
        cfg = json.load(open(os.path.join(HERE, "configs", name + ".json")))
        cal.setdefault((day, hhmm), []).append((cfg["slug"], "LF" if name in LONGFORM_CONFIGS else "S", "wait"))
    return cal


def check(items: list) -> list:
    problems = []
    actions = live_actions(items)
    cal = final_calendar(items, actions)
    lf_days = {}
    for (day, hhmm), rows in sorted(cal.items()):
        if len(rows) > 1:
            problems.append(f"{day} {hhmm}: two YouTube posts {rows}")
        for slug, kind, src in rows:
            if kind == "LF":
                if not rp.longform_allowed(day) or hhmm != "09:00":
                    problems.append(f"{day} {hhmm} {slug}: not a long-form day/time")
                if day in lf_days:
                    problems.append(f"{day}: two long-forms {lf_days[day]} and {slug}")
                lf_days[day] = slug
    for (day, hhmm), rows in sorted(cal.items()):
        for slug, kind, src in rows:
            if kind != "S":
                continue
            exceptions = {("ds55-five-minute-exercises", "12:00"), ("ds-05", "17:00")}
            if (slug, hhmm) in exceptions:
                continue
            if not rp.is_short_slot(day, hhmm, day in lf_days):
                problems.append(f"{day} {hhmm} {slug}: not a Short slot of its phase")
            base = {"kitchen": slug_is_kitchen(slug)}
            if rp.blocked_by_content(day, base, slug):
                problems.append(f"{day} {hhmm} {slug}: kitchen footage in a no-kitchen phase")
    for name in KITCHEN_CONFIGS:
        day, _ = WAIT[name]
        slug = json.load(open(os.path.join(HERE, "configs", name + ".json")))["slug"]
        if rp.phase_for(day).name in ("1", "3") and not rp.is_kitchen_exempt(slug):
            problems.append(f"{name}: kitchen waitlist entry on {day} (phase {rp.phase_for(day).name})")
    # parent before Shorts
    parent_day = {"sl05": D(2026, 10, 11), "sl09": PARENT_MAIN["oura-ring-review"][0], "sl16": WAIT["ro08-intermittent-fasting"][0],
                  "sl15": WAIT["ro19-my-first-spray-tan"][0], "sl19": WAIT["ro17-3-healthy-foods"][0],
                  "sl07": PARENT_MAIN["ro16-belly-fat-90-days"][0], "sl08": PARENT_MAIN["ro10-calories-not-losing-weight"][0],
                  "sl06": D(2026, 11, 8), "sl03": D(2026, 11, 1), "sl17": D(2026, 10, 25), "sl18": D(2026, 10, 18)}
    for (day, hhmm), rows in sorted(cal.items()):
        for slug, kind, src in rows:
            pre = slug[:4]
            if kind == "S" and pre in parent_day and day <= parent_day[pre]:
                problems.append(f"{day} {slug}: not after its parent ({parent_day[pre]})")
    return problems


KITCHEN_SLUG_PREFIXES = ("sl05-short", "sl09-short", "sl15-short", "sl16-short", "sl03-short")


def slug_is_kitchen(slug: str) -> bool:
    return slug.startswith(KITCHEN_SLUG_PREFIXES)


def main() -> int:
    from danrosefit_migration import api_key, call, fetch_schedules
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    key = api_key(); items = fetch_schedules(key)
    problems = check(items)
    print(f"queue {len(items)}; plan problems: {len(problems)}")
    for p in problems:
        print("  PROBLEM", p)
    if mode == "check":
        return 1 if problems else 0
    if problems:
        return 1
    if mode == "apply-live":
        actions = live_actions(items)
        log = []
        for sid, a, plat, old, new, slug in actions:
            if old[:16] == new[:16]:
                continue
            call("PATCH", f"/schedules/{sid}", key, {"patch": {"scheduledTime": new}})
            log.append({"id": sid, "account": a, "platform": plat, "slug": slug, "old": old, "new": new})
            print(f"  moved {slug:34} {plat:9} {sid}: {local_of(old):%a %m-%d %H:%M} -> {local_of(new):%a %m-%d %H:%M}")
        path = os.path.join(ROOT, "Docs", "CONTENT_SCHEDULE_MOVE_LOG_20261028.json")
        json.dump(log, open(path, "w"), indent=1)
        after = {i["id"]: i for i in fetch_schedules(key)}
        bad = [x for x in log if after.get(x["id"], {}).get("scheduledAt", "")[:16] != x["new"][:16]]
        print(f"verified {len(log) - len(bad)} of {len(log)} moves on a fresh pull; wrote {path}")
        return 1 if bad else 0
    if mode == "apply-waitlist":
        apply_waitlist()
        return 0
    return 2


def apply_waitlist() -> None:
    wl_path = os.path.join(HERE, "video_waitlist.json")
    entries = json.load(open(wl_path))
    base = lambda e: os.path.basename(e["config"])[:-5]  # noqa: E731
    for e in entries:
        name = base(e)
        if e.get("queued") or name not in WAIT:
            continue
        day, hhmm = WAIT[name]
        cpath = os.path.join(ROOT, e["config"]); cfg = json.load(open(cpath))
        cfg["main"] = to_utc(day, hhmm)
        json.dump(cfg, open(cpath, "w"), indent=2, ensure_ascii=False); open(cpath, "a").write("\n")
        if name in KITCHEN_CONFIGS:
            e["kitchen"] = True
        prefix = name[:4]
        if prefix in PARENTS and e["kind"] == "short":
            e["parent_config"] = f"scripts/blotato/configs/{PARENTS[prefix]}.json"
            e["after"] = e["parent_config"]
        if e["kind"] == "short" and not e.get("approved_release"):
            e["planned"] = f"{day} {hhmm}"
    for name, (day, hhmm) in PARENT_MAIN.items():
        cpath = os.path.join(HERE, "configs", name + ".json")
        cfg = json.load(open(cpath)); cfg["main"] = to_utc(day, hhmm)
        json.dump(cfg, open(cpath, "w"), indent=2, ensure_ascii=False); open(cpath, "a").write("\n")
    # release order: queued first (kept), then everything waiting by its planned date and time
    def key(e):
        if e.get("queued"):
            return (0, "", 0)
        cfg = json.load(open(os.path.join(ROOT, e["config"])))
        return (1, cfg["main"], 0 if e["kind"] == "longform" else 1)
    entries.sort(key=key)
    json.dump(entries, open(wl_path, "w"), indent=1)
    print(f"waitlist re-dated and sorted: {sum(1 for e in entries if not e.get('queued'))} waiting")


if __name__ == "__main__":
    sys.exit(main())
