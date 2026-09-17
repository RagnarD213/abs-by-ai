#!/usr/bin/env python3
"""Refuse to put an AD video on an organic channel. Imported by every Blotato queue script.

WHY THIS EXISTS (2026-09-17). Ad 5 "Every Diet You've Tried Failed for the Same Reason" — a paid
ad — published organically to Facebook, Instagram @danrosefit, the @abs.by.ai mirror and TikTok on
2026-09-16/17, and went Public on YouTube. Nothing was broken: Dan wrote, on 2026-09-10, "This video
is finalized… upload it to YouTube and set it up on all other platforms in the Blotato queue", and
the session did exactly that with `ad5_queue.py`. No rule anywhere said an ad must not go organic —
`/ad-setup` positively ALLOWED it ("If cross-platform organic distribution is separately requested,
queue those platforms through Blotato"). A prose rule would have been read by the next session and
then written around the same way, so the rule is enforced here, in code, on the payload that is
actually about to be sent.

THE RULE (Dan, 2026-09-17): an ad video is never distributed organically — not Facebook, not
Instagram, not TikTok, not YouTube Public — however the request is phrased. Ads run as paid
placements from an UNLISTED YouTube upload (`/ad-setup`) and nowhere else. Only Dan, told plainly
that the video is an ad and answering yes to that, overrides it: that answer is recorded here as a
dated entry in ORGANIC_OVERRIDES, never as a flag on a config file.

Three checks, in the order they fire. A check that cannot run is a FAILURE, never a silent pass
(AGENTS.md, 2026-09-09):

  1. DECLARED     every config must carry "content_type": "organic". Missing, empty or "ad" fails.
  2. SOURCE PATH  any path under a "<Editor> Ad Videos/" folder fails. The filing convention
                  (/editor-deliveries) is the ground truth and needs no maintenance here.
  3. CONTENT      the caption, slug and title are matched against every known ad — titles read live
                  from the ad folders and from Docs/AD_VIDEO_IDS.md — plus every ad's YouTube id.

    python3 scripts/blotato/ad_guard.py --scan        # audit the live Blotato queue
    python3 scripts/blotato/ad_guard.py --list        # show the ad registry it built
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AD_IDS_DOC = os.path.join(ROOT, "Docs", "AD_VIDEO_IDS.md")

# Dan's explicit, per-video "yes, post this AD organically" answers. Empty by design.
# An entry is a dict: {"title": ..., "date": "YYYY-MM-DD", "words": "<what Dan actually said>"}.
ORGANIC_OVERRIDES: list[dict] = []

# A title shorter than this normalises to something too generic to match on safely.
MIN_TITLE_LEN = 18


class AdGuardError(RuntimeError):
    """An ad video was about to be queued organically."""


def norm(s: str) -> str:
    """Lowercase, strip everything but letters, digits and single spaces."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", (s or "").lower())).strip()


def ad_titles() -> list[str]:
    """Every known ad title, normalised. Read live so a new ad is covered the day it is filed."""
    out = set()
    for entry in os.listdir(ROOT):
        if not entry.endswith("Ad Videos"):
            continue
        folder = os.path.join(ROOT, entry)
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            # "every diet you've tried failed for the same reason - ad 5" -> the title half
            title = norm(re.sub(r"\s*-\s*ad\s*\d+\s*$", "", name, flags=re.I))
            if len(title) >= MIN_TITLE_LEN:
                out.add(title)
    try:
        with open(AD_IDS_DOC, encoding="utf-8") as fh:
            for line in fh:
                if not line.startswith("|"):
                    continue
                cell = line.split("|")[1].strip().strip("~")
                title = norm(re.sub(r"^ad\s*\d+\s*", "", cell, flags=re.I))
                if len(title) >= MIN_TITLE_LEN:
                    out.add(title)
    except OSError:
        raise AdGuardError(f"NOT MEASURED: cannot read the ad registry at {AD_IDS_DOC}")
    if not out:
        raise AdGuardError("NOT MEASURED: the ad registry came back empty — refusing to pass anything")
    return sorted(out)


def ad_video_ids() -> set[str]:
    """Every ad's YouTube id, so a caption that links one is caught even if the title was reworded."""
    try:
        doc = open(AD_IDS_DOC, encoding="utf-8").read()
    except OSError:
        raise AdGuardError(f"NOT MEASURED: cannot read the ad registry at {AD_IDS_DOC}")
    return set(re.findall(r"youtu\.be/([A-Za-z0-9_-]{11})", doc))


def _override(text: str) -> dict | None:
    for o in ORGANIC_OVERRIDES:
        if norm(o.get("title", "")) and norm(o["title"]) in text:
            return o
    return None


def assert_organic(config: dict, *, texts: list[str] = (), sources: list[str] = ()) -> None:
    """Raise AdGuardError unless this payload is safe to publish organically.

    config   the queue config (must declare content_type)
    texts    every caption / hook / body / title actually going out
    sources  every local file path the media came from, when the caller knows them
    """
    declared = str(config.get("content_type", "")).strip().lower()
    if declared != "organic":
        raise AdGuardError(
            f'content_type is {declared or "MISSING"!r}, not "organic". Every organic config must '
            'declare content_type: "organic". An ad belongs in /ad-setup (unlisted YouTube + Google '
            "Ads), never in an organic queue."
        )

    for path in sources:
        if re.search(r"ad videos[/\\]", str(path), flags=re.I):
            raise AdGuardError(
                f"source file is filed as an AD: {path}\n"
                "Ads are never published organically. Run /ad-setup instead."
            )

    haystack = norm(" ".join([str(config.get("slug", "")), *(str(t) for t in texts)]))
    for vid in ad_video_ids():
        if vid.lower() in haystack:
            raise AdGuardError(f"the caption links ad video {vid}. Ads are never published organically.")
    for title in ad_titles():
        if title in haystack:
            ok = _override(title)
            if ok:
                print(f"  ad_guard: OVERRIDE {ok['date']} — {ok['words']}")
                continue
            raise AdGuardError(
                f'this is AD content — it matches the ad "{title}".\n'
                "Ads are never published organically (Dan, 2026-09-17), however the request is phrased.\n"
                "If Dan has been told plainly that this is an ad and has said yes anyway, record his\n"
                "words in ORGANIC_OVERRIDES in scripts/blotato/ad_guard.py and re-run."
            )


def scan_queue() -> int:
    """Audit every future Blotato schedule for ad content. Returns the number of hits."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from danrosefit_migration import api_key, fetch_schedules  # noqa: E402

    items = fetch_schedules(api_key())
    titles, vids = ad_titles(), ad_video_ids()
    hits = []
    for item in items:
        text = json.dumps(item)
        hay = norm(text)
        bad = [t for t in titles if t in hay] + [v for v in vids if v.lower() in hay]
        if bad:
            hits.append((item, bad))
    print(f"scanned {len(items)} scheduled posts against {len(titles)} ads and {len(vids)} ad video ids")
    for item, bad in hits:
        draft = item.get("draft", {})
        print(f"  AD IN QUEUE  schedule {item.get('id')}  {item.get('scheduledAt')}  "
              f"{draft.get('content', {}).get('platform')}  matched {bad}")
    print("CLEAN — no ad content scheduled" if not hits else f"\n{len(hits)} AD POST(S) QUEUED — delete them")
    return len(hits)


if __name__ == "__main__":
    if "--list" in sys.argv:
        for t in ad_titles():
            print(" ", t)
        print(f"\n{len(ad_video_ids())} ad video ids")
        sys.exit(0)
    if "--scan" in sys.argv:
        sys.exit(1 if scan_queue() else 0)
    print(__doc__)
