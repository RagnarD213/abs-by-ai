#!/usr/bin/env python3
"""Upload a timed SRT to the authorized Dan Rose Fitness YouTube channel.

Usage: python3 scripts/youtube/upload-captions.py VIDEO_ID FILE.srt
Uses YOUTUBE_CAPTIONS_REFRESH_TOKEN from ~/.absbyai-secrets.env.
Never prints OAuth tokens. Does not alter video language or automatic dubbing.
"""

import json
import os
import pathlib
import sys
import uuid

import requests

CHANNEL_ID = "UC236gjadarHAhEhOMYNGJ9g"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
SECRETS = pathlib.Path.home() / ".absbyai-secrets.env"


def secrets():
    values = dict(os.environ)
    for line in SECRETS.read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values.setdefault(key, value.strip().strip('"'))
    return values


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    video_id, filename = sys.argv[1:]
    source = pathlib.Path(filename)
    if not source.is_file() or source.suffix.lower() != ".srt":
        raise SystemExit("Expected an existing .srt file")
    data = source.read_bytes()
    if len(data) > 100_000_000 or b"-->" not in data:
        raise SystemExit("SRT is missing time codes or exceeds YouTube's file limit")

    config = secrets()
    required = ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "YOUTUBE_CAPTIONS_REFRESH_TOKEN")
    missing = [name for name in required if not config.get(name)]
    if missing:
        raise SystemExit("Missing secret keys: " + ", ".join(missing))
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": config["GOOGLE_CLIENT_ID"],
            "client_secret": config["GOOGLE_CLIENT_SECRET"],
            "refresh_token": config["YOUTUBE_CAPTIONS_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    response.raise_for_status()
    access_token = response.json()["access_token"]
    headers = {"Authorization": "Bearer " + access_token}
    info = requests.get(
        "https://oauth2.googleapis.com/tokeninfo",
        params={"access_token": access_token}, timeout=30,
    )
    info.raise_for_status()
    if SCOPE not in info.json().get("scope", "").split():
        raise SystemExit("Caption upload permission is missing")

    channel = requests.get(
        "https://www.googleapis.com/youtube/v3/channels",
        params={"part": "snippet", "mine": "true"}, headers=headers, timeout=30,
    )
    channel.raise_for_status()
    ids = [item["id"] for item in channel.json().get("items", [])]
    if ids != [CHANNEL_ID]:
        raise SystemExit("Authorization belongs to the wrong YouTube channel")

    existing = requests.get(
        "https://www.googleapis.com/youtube/v3/captions",
        params={"part": "snippet", "videoId": video_id}, headers=headers, timeout=30,
    )
    existing.raise_for_status()
    for item in existing.json().get("items", []):
        snippet = item.get("snippet", {})
        if snippet.get("language") == "en" and snippet.get("trackKind", "").lower() != "asr" and not snippet.get("isDraft"):
            print("Manual English caption track already exists:", item["id"])
            return

    boundary = "codex-" + uuid.uuid4().hex
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = (
        ("--" + boundary + "\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n").encode()
        + json.dumps(metadata).encode()
        + ("\r\n--" + boundary + "\r\nContent-Type: application/octet-stream\r\n\r\n").encode()
        + data
        + ("\r\n--" + boundary + "--\r\n").encode()
    )
    result = requests.post(
        "https://www.googleapis.com/upload/youtube/v3/captions",
        params={"uploadType": "multipart", "part": "snippet"},
        headers={**headers, "Content-Type": "multipart/related; boundary=" + boundary},
        data=body, timeout=60,
    )
    if not result.ok:
        raise SystemExit("Caption upload failed: HTTP %s %s" % (result.status_code, result.text[:500]))
    uploaded = result.json()
    print("Uploaded English SRT:", uploaded.get("id"), uploaded.get("snippet", {}).get("status"))


if __name__ == "__main__":
    main()
