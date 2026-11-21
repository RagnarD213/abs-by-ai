#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra01
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"   # ad-edit lesson 44: Whisper shells out to a BARE ffmpeg
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
# usable span only: the script runs 0:27-1:35; take 20-105 s with headroom for orphan/repeat scans
"$P/ffmpeg" -nostdin -v error -y -i lav16.wav -ss 15 -t 95 -c:a pcm_s16le tx/span.wav
python3 tx/whisper_chunked.py tx/span.wav tx/_span.json medium.en 70 60
python3 - <<'PY'
import json
d = json.load(open("tx/_span.json"))
OFF = 15.0
for s in d["segments"]:
    for w in s["words"]:
        w["start"] = round(w["start"] + OFF, 3); w["end"] = round(w["end"] + OFF, 3)
    s["start"] = s["words"][0]["start"]; s["end"] = s["words"][-1]["end"]
json.dump(d, open("tx/c1663.whisper.json", "w"), indent=1)
n = sum(len(s["words"]) for s in d["segments"])
print(f"c1663.whisper.json  {len(d['segments'])} segments  {n} words  "
      f"{d['segments'][0]['start']:.2f}..{d['segments'][-1]['end']:.2f}s")
PY
python3 tx/orphan_scan.py tx/span.wav tx/_span.json | tail -30
echo "--- repeat scan ---"
python3 tx/repeat_scan.py tx/c1663.whisper.json || true
echo "TX_COMPLETE"
