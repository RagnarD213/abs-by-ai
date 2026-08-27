#!/usr/bin/env python3
"""Chunked Whisper: the only way to get a COMPLETE transcript of a roll full of retakes.

Whisper drops content two different ways on a teleprompter roll:
  * condition_on_previous_text=True (the default) feeds the last window's text back as a
    prompt, and the decoder skips a retake as "already said" -- on C1592 it discarded a
    whole second hook take (32.2-46.9 s) and emitted one word in its place;
  * with it False, the same roll instead dropped the THIRD take of the closing beat.
Neither pass alone is complete, and the transcript looks clean either way.

Fix: transcribe overlapping windows so every take is decoded with fresh, short context,
then keep each window's words only inside its own non-overlapping span. Verify with
orphan_scan.py -- speech that no word covers is the tell.

  whisper_chunked.py <wav16k> <out.json> [model] [win] [step]
"""
import json, re, subprocess, sys, time, wave
import whisper
FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "small"
WIN = float(sys.argv[4]) if len(sys.argv) > 4 else 70.0
STEP = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0
w = wave.open(src); dur = w.getnframes() / w.getframerate(); w.close()
m = whisper.load_model(model)
t0 = time.time(); segs = []
start = 0.0
while start < dur:
    tmp = "/tmp/_chunk.wav"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(start), "-t", str(WIN),
                    "-i", src, tmp], check=True)
    r = m.transcribe(tmp, word_timestamps=True, language="en", verbose=False,
                     condition_on_previous_text=False)
    hi = dur if start + STEP >= dur else start + STEP
    for s in r["segments"]:
        ws = [{"word": x["word"], "start": round(x["start"] + start, 3),
               "end": round(x["end"] + start, 3)}
              for x in s.get("words", []) if start <= x["start"] + start < hi]
        if ws:
            segs.append({"start": ws[0]["start"], "end": ws[-1]["end"],
                         "text": "".join(x["word"] for x in ws), "words": ws})
    start += STEP
segs.sort(key=lambda s: s["start"])
# De-duplicate across window seams: the same word can be timed 119.9 in one window and
# 120.1 in the next, so a disjoint [start,hi) filter still keeps it twice.
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
allw = [w for s in segs for w in s["words"]]
allw.sort(key=lambda w: w["start"])
keep, drop = [], 0
for w in allw:
    if keep and norm(w["word"]) == norm(keep[-1]["word"]) and w["start"] - keep[-1]["start"] < 0.7:
        drop += 1; continue
    keep.append(w)
kept = {id(w) for w in keep}
for s in segs:
    s["words"] = [w for w in s["words"] if id(w) in kept]
    s["text"] = "".join(w["word"] for w in s["words"])
segs = [s for s in segs if s["words"]]
for s in segs:
    s["start"], s["end"] = s["words"][0]["start"], s["words"][-1]["end"]
print("seam duplicates dropped:", drop)
json.dump({"segments": segs}, open(out, "w"))
print("done %.0fs  segments=%d words=%d" % (time.time() - t0, len(segs),
      sum(len(s["words"]) for s in segs)))
