"""Use native audio/video on the Gemini API when the subscription CLI gives only stills."""
import json
import math
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com"
MODEL = "gemini-3.1-flash-lite"
SAMPLE_FPS = 6
OUTPUT_LIMIT = 2048
MAX_USD = 4.90
# Standard rates as of 2026-11-20. Budget every prompt token at the higher audio
# rate. https://ai.google.dev/gemini-api/docs/pricing#gemini-3.1-flash-lite
VIDEO_RATE, AUDIO_RATE, OUTPUT_RATE = 0.25, 0.50, 1.50


def api_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    for line in (Path.home() / ".absbyai-secrets.env").read_text().splitlines():
        match = re.match(r"""\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["']?([^"'\s]+)""", line)
        if match:
            return match[1]
    raise ValueError("Gemini API key is unavailable for native video fallback")


def call(path, key, data=None, headers=None, method=None):
    url = path if path.startswith(API + "/") else API + path
    request = urllib.request.Request(url, data, {"x-goog-api-key": key, **(headers or {})}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=150) as response:
            body = response.read()
            return (json.loads(body) if body else {}, response.headers)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace").replace(key, "[redacted]")
        raise ValueError(f"Gemini API HTTP {error.code}: {detail[:350]}") from None


def upload(file, key):
    size = str(file.stat().st_size)
    _, headers = call(
        "/upload/v1beta/files", key, json.dumps({"file": {"display_name": file.name}}).encode(),
        {"content-type": "application/json", "x-goog-upload-protocol": "resumable",
         "x-goog-upload-command": "start", "x-goog-upload-header-content-length": size,
         "x-goog-upload-header-content-type": "video/mp4"},
    )
    url = headers["x-goog-upload-url"]
    if not url.startswith(API + "/"):
        raise ValueError("Gemini returned an unexpected upload host")
    with file.open("rb") as stream:
        uploaded, _ = call(url, key, stream,
                           {"content-length": size, "x-goog-upload-offset": "0",
                            "x-goog-upload-command": "upload, finalize"})
    return uploaded["file"]


def budget(parts):
    # Bound even the standard 258-token image rate with 300 tokens/frame and
    # 100/sec for audio and timestamps. No paid retries or tools are enabled.
    total = sum(((math.ceil(end - start) + 2) * (SAMPLE_FPS * 300 + 100) + 1024) * AUDIO_RATE
                + OUTPUT_LIMIT * OUTPUT_RATE for _, start, end in parts) / 1_000_000
    if total >= MAX_USD:
        raise ValueError(f"Gemini input would reserve ${total:.2f}; exceeds the per-run cap")
    return total


def cost(usage):
    prompt = usage.get("promptTokenCount", 0)
    audio = sum(row["tokenCount"] for row in usage.get("promptTokensDetails", [])
                if row["modality"] == "AUDIO")
    output = max(usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0),
                 usage.get("totalTokenCount", 0) - prompt)
    estimate = ((prompt - audio) * VIDEO_RATE + audio * AUDIO_RATE + output * OUTPUT_RATE) / 1_000_000
    upper = (prompt * AUDIO_RATE + output * OUTPUT_RATE) / 1_000_000
    return estimate, upper


def native_review(file, prompt, output, duration):
    key = api_key()
    uploaded = upload(file, key)
    try:
        for _ in range(30):
            if uploaded["state"] != "PROCESSING":
                break
            time.sleep(2)
            uploaded, _ = call("/v1beta/" + uploaded["name"], key)
        if uploaded["state"] != "ACTIVE":
            raise ValueError(f"Gemini could not prepare the video attachment ({uploaded['state']})")
        body = {"contents": [{"parts": [
            {"fileData": {"fileUri": uploaded["uri"], "mimeType": "video/mp4"},
             "videoMetadata": {"fps": SAMPLE_FPS}},
            {"text": prompt + f" The native video input requests sequential sampling at {SAMPLE_FPS} fps."},
        ]}], "generationConfig": {"maxOutputTokens": OUTPUT_LIMIT, "responseMimeType": "application/json",
                                  "mediaResolution": "MEDIA_RESOLUTION_LOW",
                                  "thinkingConfig": {"thinkingLevel": "LOW"} }}
        result, _ = call(f"/v1beta/models/{MODEL}:generateContent", key, json.dumps(body).encode(),
                         {"content-type": "application/json"})
        output.with_suffix(".api.json").write_text(json.dumps(result))
        usage = result["usageMetadata"]
        video_tokens = sum(row["tokenCount"] for row in usage.get("promptTokensDetails", [])
                           if row["modality"] == "VIDEO")
        if video_tokens < duration * 66 * (SAMPLE_FPS - 1):
            raise ValueError("Gemini usage could not confirm higher-frame-rate video input")
        candidate = result["candidates"][0]
        if candidate["finishReason"] != "STOP":
            raise ValueError(f"Gemini response ended early ({candidate['finishReason']})")
        answer = "".join(part["text"] for part in candidate["content"]["parts"] if not part.get("thought"))
        return answer
    finally:
        try:
            call("/v1beta/" + uploaded["name"], key, method="DELETE")
        except (ValueError, OSError):
            pass  # Google deletes temporary uploads after 48 hours.
