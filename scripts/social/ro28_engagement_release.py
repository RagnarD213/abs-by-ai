#!/usr/bin/env python3
"""Submit the seven RO-28 engagement ads once Blotato's upload is public."""

import argparse
import fcntl
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
import subprocess
from urllib.request import urlopen

from engagement_release import CHANNEL, api_key, instant, save, secrets, youtube_client
from danrosefit_migration import fetch_schedules


REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / "scripts/blotato/configs/ro28-got-abs.json"
RECEIPT = Path("Docs/RO28_GOT_ABS_SETUP_RECEIPT_20261118.md")
SCRIPT = REPO / "scripts/ads/ytads/ro28-release.js"
SCHEDULE = "7163158"
LABEL = "com.absbyai.ro28-engagement-release"
START_MARKER = "<!-- ro28-paid-live:start -->"
END_MARKER = "<!-- ro28-paid-live:end -->"


def public_release(youtube, cfg, now):
    channel = youtube("channels", {"part": "contentDetails", "id": CHANNEL})["items"][0]
    uploads = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    items = youtube("playlistItems", {"part": "snippet,contentDetails", "playlistId": uploads, "maxResults": 20})["items"]
    ids = {row["contentDetails"]["videoId"] for row in items if row["snippet"]["title"] == cfg["title"]}
    if not ids:
        return None
    result = youtube("videos", {"part": "snippet,status", "id": ",".join(sorted(ids))})["items"]
    floor = instant(cfg["main"]) - timedelta(minutes=2)
    matches = [row for row in result if row["status"]["privacyStatus"] == "public"
               and row["snippet"]["channelId"] == CHANNEL
               and row["snippet"]["title"] == cfg["title"]
               and floor <= instant(row["snippet"]["publishedAt"]) <= now
               and "utm_content=" + cfg["slug"] in row["snippet"]["description"]]
    if len(matches) > 1:
        raise RuntimeError("More than one public YouTube upload matches schedule " + SCHEDULE)
    return matches[0] if matches else None


def run_ads(node, video_id, *, journal=None):
    options = ["--apply", video_id, str(journal)] if journal else ["--dry-run", video_id]
    result = subprocess.run(
        [node, str(SCRIPT), *options],
        cwd=REPO, text=True, capture_output=True, timeout=150,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Google Ads command failed")
    if result.stderr:
        print(result.stderr.strip(), flush=True)
    return json.loads(result.stdout)


def preflight(cfg, args):
    [schedule] = [row for row in fetch_schedules(api_key()) if str(row["id"]) == SCHEDULE]
    assert instant(schedule["scheduledAt"]) == instant(cfg["main"])
    assert schedule["draft"]["target"]["title"] == cfg["title"]
    assert schedule["draft"]["target"]["privacyStatus"].lower() == "public"
    assert "utm_content=" + cfg["slug"] in schedule["draft"]["content"]["text"]
    youtube, _, _ = youtube_client(secrets())
    assert public_release(youtube, cfg, datetime.now(timezone.utc)) is None
    for video_id, label, count in (
        ("iA5PXzzaJzI", "new-asset", 8),
        ("cbWKs5CuQd0", "existing-asset", 7),
    ):
        [test_video] = youtube("videos", {"part": "snippet,status", "id": video_id})["items"]
        assert test_video["snippet"]["channelId"] == CHANNEL and test_video["status"]["privacyStatus"] == "public"
        receipt = run_ads(args.node, video_id)
        assert receipt["dryRun"] and receipt["validatedOps"] == count
        assert receipt["newAsset"] == (count == 8)
        assert not receipt["after"]["enabled"] and receipt["after"]["protectedPaused"] == 45
        assert receipt["after"]["tier2"] == {"targetCpaMicros": "50000", "cpcBidMicros": "50000"}
        for url in {url for placement in receipt["plan"] for url in placement["finalUrls"]}:
            with urlopen(url, timeout=15) as page:
                assert page.status == 200 and page.url == url
                assert not re.search(
                    rb"zepbound|ozempic|mounjaro|wegovy|tirzepatide|semaglutide|glp[- ]?1|"
                    rb"\b(?:drugs?|needles?|vials?|syringes?|pharmac\w*)\b",
                    page.read(), re.IGNORECASE,
                ), "Disallowed words in the ad destination"
        save(args.state_dir / f"engagement-dry-run-{label}.json", receipt)
        print(f"Google Ads validateOnly accepted {count} operations in the {label} path.", flush=True)
    print(f"Verified Blotato schedule {SCHEDULE}, owner YouTube access, and both release creation paths.", flush=True)


def receipt_body(result):
    video_id = result["videoId"]
    lines = [
        START_MARKER,
        f"Live readback at {result['checkedAt']} for the released video. [Public YouTube upload](https://www.youtube.com/watch?v={video_id})",
        f"All seven listed ads were the only enabled ads in the five campaigns. All {result['after']['protectedPaused']} "
        "ads from Dan’s pause list still read as paused. Geo tier 2’s target CPA and CPC fields both read 50,000 micros.",
        "",
        "| Suffix | Campaign | Ad group | Google Ads ID | Status | Final URL |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for ad in result["placements"]:
        lines.append(f"| {ad['key']} | {ad['campaign']} | {ad['adGroupId']} | {ad['adId']} | {ad['status']} | {', '.join(ad['finalUrls'])} |")
    if result.get("pausedNewWorkerAds"):
        lines.extend(["", "New ads from the regular worker paused during release verification: "
                      + ", ".join(name.rsplit("/", 1)[-1] for name in result["pausedNewWorkerAds"]) + "."])
    lines.extend([END_MARKER, ""])
    return "\n".join(lines)


def record_receipt(result):
    path = REPO / RECEIPT
    text = path.read_text()
    body = receipt_body(result)
    if START_MARKER in text:
        head, _, tail = text.partition(START_MARKER)
        _, end, tail = tail.partition(END_MARKER)
        assert end, "Missing paid-release receipt end marker"
        updated = head + body.rstrip() + tail
    else:
        updated = text.rstrip() + "\n\n" + body
    if updated != text:
        scratch = path.with_suffix(".ro28-tmp")
        scratch.write_text(updated)
        scratch.replace(path)
    pushed = subprocess.run(
        [str(REPO / "scripts/git/safe-push.sh"), "-m", "Record live RO-28 engagement ads", "--", str(RECEIPT)],
        cwd=REPO, timeout=90,
    )
    if pushed.returncode not in (0, 2):
        raise RuntimeError(f"Receipt written, safe-push exit {pushed.returncode}")
    return pushed.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", required=True)
    parser.add_argument("--state-dir", required=True, type=Path)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--launchd", action="store_true")
    args = parser.parse_args()
    cfg = json.loads(CONFIG.read_text())
    if args.preflight:
        preflight(cfg, args)
        return
    now = datetime.now(timezone.utc)
    if now < instant(cfg["main"]):
        return
    state_file = args.state_dir / "engagement-release.json"
    with (args.state_dir / "engagement-release.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        state = json.loads(state_file.read_text()) if state_file.exists() else {}
        if not state.get("receipt_written"):
            if not state.get("ads", {}).get("verified"):
                youtube, _, _ = youtube_client(secrets())
                video = public_release(youtube, cfg, now)
                if video is None:
                    print(f"{now.isoformat()} Waiting for public YouTube upload {SCHEDULE}.", flush=True)
                    return
                state["youtube"] = {"id": video["id"], "title": cfg["title"], "privacy": "public",
                                    "published_at": video["snippet"]["publishedAt"], "schedule": SCHEDULE}
                try:
                    result = run_ads(args.node, video["id"], journal=args.state_dir / "engagement-submission.json")
                except (RuntimeError, subprocess.TimeoutExpired) as error:
                    state["error"] = str(error)
                    save(state_file, state)
                    raise
                state.pop("error", None)
                state["ads"] = result
                prior_pauses = set(state.get("paused_new_worker_ads", []))
                state["paused_new_worker_ads"] = sorted(prior_pauses | set(result["pausedNewWorkerAds"]))
                save(state_file, state)
                if not result["verified"]:
                    print(f"{now.isoformat()} Incomplete Google Ads readback: {result['after']}", flush=True)
                    return
            result = dict(state["ads"], pausedNewWorkerAds=state.get("paused_new_worker_ads", []))
            state["receipt_pushed"] = record_receipt(result)
            state["receipt_written"] = True
            save(state_file, state)
            print(f"Verified seven enabled RO-28 ads for {result['videoId']} and wrote the receipt.", flush=True)
    if args.launchd:
        subprocess.run(["/bin/launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"], check=True)


if __name__ == "__main__":
    main()
