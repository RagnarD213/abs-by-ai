#!/usr/bin/env python3
"""Rewrite the ManyChat CTA keyword in the queued @danrosefit Instagram captions.

Every queued CTA post carried the identical line

    Comment ABS and I'll send you the free AI preview 👇

so every commenter got the same DM and every signup landed on one utm_campaign. This
script swaps ABS for the post's TOPIC keyword, which matches a ManyChat automation whose
DM copy and utm_campaign are topic-specific.

Topics are assigned per schedule id in TOPIC below -- read off each caption's hook, not
guessed from hashtags. Anything in the queue carrying the CTA line but missing from TOPIC
is reported and left alone rather than silently defaulted to ABS.

    python3 scripts/manychat/keyword_split.py            # dry run
    python3 scripts/manychat/keyword_split.py --apply
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blotato"))
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402

CTA = "Comment {kw} and I'll send you the free AI preview 👇"
OLD = CTA.format(kw="ABS")

# schedule id -> ManyChat keyword. ABS entries are listed for completeness/auditing even
# though they need no edit.
TOPIC = {
    "3793974": "ABS",    "3841865": "ABS",    "3793976": "FOOD",   "3841867": "FOOD",
    "3793977": "FOOD",   "3841869": "ABS",    "3794000": "ABS",    "3876738": "ABS",
    "3841871": "COACH",  "3793979": "FOOD",   "3841874": "TRACK",  "3841876": "TRAIN",
    "3841878": "FOOD",   "3794002": "ABS",    "3876742": "FOOD",   "3841880": "FOOD",
    "3793984": "TRACK",  "3841882": "FOOD",   "3876748": "FOOD",   "3841885": "ABS",
    "3841887": "SLEEP",  "3793987": "SLEEP",  "3841895": "TRAIN",  "3876754": "ABS",
    "3841898": "FOOD",   "3841900": "TRACK",  "3841903": "COACH",  "3841905": "TRAIN",
    "3876763": "ABS",    "3841910": "FOOD",   "4066393": "TRAIN",  "3841913": "COACH",
    "3793992": "TRAIN",  "3841916": "SLEEP",  "3841918": "TRAIN",  "4066416": "TRAIN",
    "3841921": "COACH",  "3841924": "FOOD",   "3841931": "FOOD",   "3793994": "ABS",
    "3841933": "TRAIN",  "3841935": "TRACK",  "3793995": "ABS",    "3841937": "SLEEP",
    "3793997": "ABS",    "3841945": "TRACK",  "3793998": "ABS",
}

apply = "--apply" in sys.argv
key = api_key()
items = fetch_schedules(key)
cta = [s for s in items if OLD in s["draft"]["content"].get("text", "")]
print(f"queue: {len(items)} scheduled, {len(cta)} carry the CTA line")

missing = [s["id"] for s in cta if str(s["id"]) not in TOPIC]
if missing:
    print(f"!! not classified, SKIPPED: {missing}")

changed = skipped = 0
for s in sorted(cta, key=lambda x: x["scheduledAt"]):
    sid = str(s["id"])
    kw = TOPIC.get(sid)
    if kw is None:
        continue
    d = s["draft"]
    text = d["content"]["text"]
    new = text.replace(OLD, CTA.format(kw=kw))
    hook = text.split("\n")[0][:58]
    if new == text:
        print(f"  {sid} {s['scheduledAt'][:10]} {kw:<5} unchanged  {hook}")
        skipped += 1
        continue
    print(f"  {sid} {s['scheduledAt'][:10]} ABS->{kw:<5} {hook}")
    changed += 1
    if not apply:
        continue
    # Blotato edits a schedule with PATCH and a `patch.draft` envelope. Probed 2026-09-08:
    # PUT/POST /schedules/{id} are 404, PATCH without `patch` is a 400, and a `patch.post`
    # envelope returns a 500 SQL error rather than a validation message -- so send the whole
    # draft back under `draft`, with only the text swapped.
    call("PATCH", f"/schedules/{sid}", key,
         {"patch": {"draft": {"accountId": d["accountId"], "target": d["target"],
                              "content": {**d["content"], "text": new}}}})

print(f"\n{'APPLIED' if apply else 'DRY RUN'}: {changed} to change, {skipped} already correct")
