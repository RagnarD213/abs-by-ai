#!/usr/bin/env python3
"""Transcribe VSL audio files with Whisper (small), one light render-queue slot for the run.

    python3 transcribe.py vsl1.wav vsl2.wav      -> vsl1.txt / vsl1.json next to each file

Get the audio first (audio-only ffmpeg never waits in the render queue):
    FF="<repo>/Media/video_edit/bin/ffmpeg"
    "$FF" -nostdin -loglevel error -y -headers "Referer: https://<sales-page-host>/"$'\r\n' \
          -i "<vidalytics ..._variant.m3u8>" -vn -ac 1 -ar 16000 out.wav
A page can load two Vidalytics streams; one is often a silent background loop ("does not contain any stream").
YouTube ads: yt-dlp -f bestaudio -x --audio-format wav -o "ad_<id>.%(ext)s" https://www.youtube.com/watch?v=<id>
(some downloads come back silent: check with ffmpeg -af volumedetect; mean -91 dB = no sound).
"""
import json, os, sys
REPO = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
sys.path.append(os.path.join(REPO, ".claude/skills/_shared/renderq"))
os.environ["PATH"] = os.path.join(REPO, "Media/video_edit/bin") + ":" + os.environ["PATH"]
try:
    import renderq
    renderq.hold_until_exit("Whisper VSL transcripts", pool="light")
except Exception as e:
    print("renderq skip:", e)
import whisper
m = whisper.load_model("small")
for src in sys.argv[1:]:
    r = m.transcribe(src, language="en", condition_on_previous_text=False, fp16=False)
    base = os.path.splitext(src)[0]
    json.dump(r["segments"], open(base + ".json", "w"))
    with open(base + ".txt", "w") as f:
        for s in r["segments"]:
            t = int(s["start"]); f.write(f"[{t//60:02d}:{t%60:02d}] {s['text'].strip()}\n")
    print("done", src, flush=True)
