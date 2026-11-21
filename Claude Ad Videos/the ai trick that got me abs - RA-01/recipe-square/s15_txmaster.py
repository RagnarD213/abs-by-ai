#!/usr/bin/env python3
"""Transcribe the FINISHED render — what the file actually says.  s15_txmaster.py 9x16 <master>"""
import json, os, subprocess, sys
os.environ["PATH"] = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:"
                      + os.environ["PATH"])          # ad-edit lesson 44
import whisper
KEY, MASTER = sys.argv[1], sys.argv[2]
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
wav = f"_tx_{KEY}.wav"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", MASTER, "-ac", "1", "-ar", "16000",
                "-c:a", "pcm_s16le", wav], check=True)
m = whisper.load_model("medium.en")
r = m.transcribe(wav, word_timestamps=True, language="en", verbose=False,
                 condition_on_previous_text=False)
words = [w["word"].strip() for s in r["segments"] for w in s.get("words", []) if w["word"].strip()]
json.dump({"words": words, "text": r["text"].strip()}, open(f"transcript_{KEY}.json", "w"), indent=1)
print(f"transcript_{KEY}.json  {len(words)} words")
print(r["text"].strip()[:400])
