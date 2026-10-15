#!/usr/bin/env python3
"""Put the designed cover on each Facebook reel right after Blotato publishes it.

WHY THIS EXISTS
---------------
Blotato's Facebook target has no cover field, so a queued reel goes out with whatever frame
Facebook picks (often Dan mid-word under a caption, once a black frame). The Graph API does
take a custom thumbnail, but only on a video that already exists:

    POST /{video-id}/thumbnails  source=<jpg>  is_preferred=true

Proven 2026-09-28 on the published "Never start your day with carbs" reel: the preferred
thumbnail became the uploaded 1080x1920 cover. So this runs on a timer (launchd, every 20 min),
finds newly published page reels whose caption matches an entry in fb_reel_covers.json, sets
the cover once, reads it back, and records it in fb_reel_covers_state.json so it never repeats.

    python3 scripts/blotato/fb_reel_covers.py            # set any due covers
    python3 scripts/blotato/fb_reel_covers.py --dry-run  # show what would be set

Config (fb_reel_covers.json, beside this file): a list of
    {"match": "<first line of the caption>", "cover": "<absolute path to jpg>", "w": 1080, "h": 1920}

RUNS FROM ~/.absbyai/fb-reel-covers/, NOT FROM THIS REPO. macOS blocks launchd from reading
~/Documents ("Operation not permitted"), so the LaunchAgent com.absbyai.fb-reel-covers runs a
copy of this script, its config and the cover JPGs from that folder. After editing the config,
re-run the copy step (see the 2026-09-28 cover installation report) so the live copy matches.
"""
from __future__ import annotations

import argparse
import hashlib
import fcntl
from PIL import Image, ImageChops, ImageStat
import datetime as dt
import io
import json
import os
import re
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "fb_reel_covers.json")
STATE = os.path.join(HERE, "fb_reel_covers_state.json")
PAGE = "1294282227094660"  # Abs by AI page, Blotato account 47105
GRAPH = "https://graph.facebook.com/v21.0"


def token() -> str:
    for line in open(os.path.expanduser("~/.absbyai-secrets.env")):
        m = re.match(r"^FACEBOOK_PAGE_ACCESS_TOKEN=(.*)$", line.strip())
        if m:
            return m.group(1).strip().strip('"').strip("'")
    raise SystemExit("FACEBOOK_PAGE_ACCESS_TOKEN missing from ~/.absbyai-secrets.env")


def get(path: str, tok: str) -> dict:
    sep = "&" if "?" in path else "?"
    return json.load(urllib.request.urlopen(f"{GRAPH}/{path}{sep}access_token={tok}"))


def first_line(text: str) -> str:
    return (text or "").strip().split("\n")[0].strip()


def preferred(vid: str, tok: str) -> dict | None:
    for t in get(f"{vid}?fields=thumbnails{{is_preferred,width,height,uri}}", tok)["thumbnails"]["data"]:
        if t["is_preferred"]:
            return t
    return None


def matches_cover(thumbnail, path):
    """Facebook rescales landscape thumbnails. Compare the actual image, not dimensions."""
    if not thumbnail:
        return False
    with urllib.request.urlopen(thumbnail["uri"], timeout=30) as response:
        actual = Image.open(io.BytesIO(response.read())).convert("RGB")
    expected = Image.open(path).convert("RGB")
    if abs(actual.width / actual.height - expected.width / expected.height) > 0.03:
        return False
    difference = ImageChops.difference(actual.resize((128, 128)), expected.resize((128, 128)))
    return max(ImageStat.Stat(difference).rms) < 15


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    lock = open(STATE + ".lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return 0
    tok = token()
    config = json.load(open(CONFIG))
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    reels = []
    page = get(f"{PAGE}/video_reels?fields=id,description,created_time&limit=100", tok)
    while True:
        reels.extend(page.get("data", []))
        next_url = page.get("paging", {}).get("next")
        if not next_url:
            break
        page = get(next_url.split(GRAPH + "/", 1)[1], tok)
    for r in reels:
        line = first_line(r.get("description"))
        hit = next((c for c in config if first_line(c["match"]) == line), None)
        if not hit:
            continue
        digest = hashlib.sha256(open(hit["cover"], "rb").read()).hexdigest()
        if state.get(r["id"], {}).get("cover_sha256") == digest:
            continue
        before = preferred(r["id"], tok)
        if matches_cover(before, hit["cover"]):
            state[r["id"]] = {"caption": line, "cover": hit["cover"], "cover_sha256": digest, "verified_at": dt.datetime.now(dt.timezone.utc).isoformat()}
            if not a.dry_run:
                json.dump(state, open(STATE, "w"), indent=1)
            continue
        print(f"{r['created_time'][:16]} {r['id']} {line[:50]} -> {os.path.basename(hit['cover'])}")
        if a.dry_run:
            continue
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{GRAPH}/{r['id']}/thumbnails",
             "-F", f"source=@{hit['cover']}", "-F", "is_preferred=true", "-F", f"access_token={tok}"],
            capture_output=True, text=True).stdout
        ok = '"success":true' in out
        pref = preferred(r["id"], tok) if ok else None
        good = matches_cover(pref, hit["cover"])
        print(f"   set={ok} preferred={pref and (pref['width'], pref['height'])} {'VERIFIED' if good else 'CHECK'}")
        if good:
            state[r["id"]] = {"caption": line, "cover": hit["cover"],
                              "cover_sha256": digest, "set_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            json.dump(state, open(STATE, "w"), indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
