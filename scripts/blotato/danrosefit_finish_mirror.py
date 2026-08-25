#!/usr/bin/env python3
"""Finish the @danrosefit migration: shift + recaption the @abs.by.ai mirror.

danrosefit_migration.py's shift() assumed the schedule could be rewritten in place.
It cannot. Blotato's /v2/schedules/{id} accepts PATCH with a {"patch": {...}} wrapper
and ONLY honours scheduledTime -- any content-shaped patch body returns a 500 from the
query builder. So the mirror's CTA rewrite has to be a create-then-delete.

Idempotent BY CONSTRUCTION, not by a state file: the target time is recomputed every
run as "the @danrosefit original's time + 24h", so a mirror already sitting at its
target is skipped rather than shifted a second time. Create always precedes delete, so
a failure mid-pair leaves a duplicate (visible, fixable) rather than a lost post.

    python3 scripts/blotato/danrosefit_finish_mirror.py            # dry run
    python3 scripts/blotato/danrosefit_finish_mirror.py --apply
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danrosefit_migration import (  # noqa: E402
    ABS_BY_AI, CTA_MIRROR, MIRROR_SHIFT, api_key, call, content_key,
    fetch_schedules, iso, parse, rewrite_cta,
)

MAIN = "67203"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    key = api_key()

    items = fetch_schedules(key)
    ig = [i for i in items if i["draft"]["target"]["targetType"] == "instagram"]
    main_posts = [i for i in ig if i["draft"]["accountId"] == MAIN]
    mirrors = [i for i in ig if i["draft"]["accountId"] == ABS_BY_AI]

    origin = {}
    for i in main_posts:
        origin.setdefault(content_key(i), []).append(parse(i["scheduledAt"]))

    # Group by media so a half-finished run (created but not yet deleted) is seen as a
    # duplicate pair rather than as two independent posts to rewrite again.
    groups = defaultdict(list)
    orphan = []
    for m in mirrors:
        if content_key(m) in origin:
            groups[content_key(m)].append(m)
        else:
            orphan.append(m)

    todo, done, stale = [], [], []
    for ck, group in groups.items():
        target = min(origin[ck]) + MIRROR_SHIFT
        want_text = rewrite_cta(group[0]["draft"]["content"]["text"], CTA_MIRROR)
        correct = [m for m in group
                   if parse(m["scheduledAt"]) == target
                   and m["draft"]["content"]["text"] == want_text]
        wrong = [m for m in group if m not in correct]
        if correct:
            done.append(correct[0])
            # a previous run created the replacement but died before the delete
            stale += correct[1:] + wrong
            continue
        m = wrong[0]
        todo.append({
            "id": m["id"],
            "from": m["scheduledAt"],
            "to": iso(target),
            "retime": parse(m["scheduledAt"]) != target,
            "recaption": m["draft"]["content"]["text"] != want_text,
            "text": want_text,
            "target": m["draft"]["target"],
            "mediaUrls": m["draft"]["content"]["mediaUrls"],
            "also_delete": [x["id"] for x in wrong[1:]],
        })

    print(f"@danrosefit {len(main_posts)}   @abs.by.ai {len(mirrors)}   "
          f"already correct {len(done)}   to fix {len(todo)}   "
          f"stale duplicates to delete {len(stale)}   orphan {len(orphan)}")
    for o in orphan:
        print(f"  ORPHAN {o['id']} {o['scheduledAt'][:16]} "
              f"{o['draft']['content']['text'].splitlines()[0][:50]!r}")
    for t in todo[:5]:
        print(f"  {t['id']}  {t['from'][:16]} -> {t['to'][:16]}  "
              f"retime={t['retime']} recaption={t['recaption']}")
    if len(todo) > 5:
        print(f"  ... and {len(todo) - 5} more")

    if not args.apply:
        print("\nDry run. Re-run with --apply.")
        return 0

    for t in todo:
        body = {
            "post": {
                "accountId": ABS_BY_AI,
                "target": t["target"],
                "content": {"platform": "instagram", "text": t["text"],
                            "mediaUrls": t["mediaUrls"]},
            },
            "scheduledTime": t["to"],
        }
        res = call("POST", "/posts", key, body)
        # /v2/posts answers with a postSubmissionId, not a schedule id.
        if not (res.get("postSubmissionId") or res.get("id")):
            raise SystemExit(f"create for {t['id']} was not acknowledged: {res}")
        for dead in [t["id"]] + t["also_delete"]:
            call("DELETE", f"/schedules/{dead}", key)
        print(f"  {t['id']} replaced at {t['to'][:16]}", flush=True)

    for m in stale:
        call("DELETE", f"/schedules/{m['id']}", key)
        print(f"  deleted stale duplicate {m['id']}", flush=True)

    print(f"\nrewrote {len(todo)} mirror posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
