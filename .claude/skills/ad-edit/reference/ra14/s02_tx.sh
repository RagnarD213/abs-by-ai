#!/bin/bash
set -e
cd /Volumes/Extreme/_edit_work/ra14
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"   # ad-edit lesson 44: Whisper shells out to a BARE ffmpeg
P="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
# usable span only: the RA-14 script runs 5:40-6:54 on C1667; take 322 s to the end of the roll
"$P/ffmpeg" -nostdin -v error -y -i lav16.wav -ss 322 -t 97.4 -c:a pcm_s16le tx/span.wav
python3 tx/whisper_chunked.py tx/span.wav tx/_span.json medium.en 70 60
python3 - <<'PY'
import json
d = json.load(open("tx/_span.json"))
OFF = 322.0
for s in d["segments"]:
    for w in s["words"]:
        w["start"] = round(w["start"] + OFF, 3); w["end"] = round(w["end"] + OFF, 3)
    s["start"] = s["words"][0]["start"]; s["end"] = s["words"][-1]["end"]
json.dump(d, open("tx/c1667.whisper.json", "w"), indent=1)
n = sum(len(s["words"]) for s in d["segments"])
print(f"c1667.whisper.json  {len(d['segments'])} segments  {n} words  "
      f"{d['segments'][0]['start']:.2f}..{d['segments'][-1]['end']:.2f}s")
PY
echo "TX_COMPLETE"
