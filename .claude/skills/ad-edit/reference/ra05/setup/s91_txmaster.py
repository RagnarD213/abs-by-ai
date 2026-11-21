#!/usr/bin/env python3
"""RA-05 setup: transcribe the FINISHED master, what the file actually says (RA-04 round 4 s15_txmaster.py).
   python3 s91_txmaster.py <master>   -> setup/transcript_9x16.json"""
import json, os, subprocess, sys
BIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
os.environ["PATH"] = BIN + ":" + os.environ["PATH"]          # ad-edit lesson 44: Whisper calls the project ffmpeg
import whisper
MASTER = sys.argv[1]; OUT = "/Volumes/Extreme/_edit_work/ra05/setup"
wav = f"{OUT}/_tx_9x16.wav"
subprocess.run([f"{BIN}/ffmpeg", "-nostdin", "-v", "error", "-y", "-i", MASTER, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav], check=True)
r = whisper.load_model("medium.en").transcribe(wav, word_timestamps=True, language="en", verbose=False, condition_on_previous_text=False)
words = [w["word"].strip() for s in r["segments"] for w in s.get("words", []) if w["word"].strip()]
json.dump({"words": words, "text": r["text"].strip(), "media": os.path.abspath(MASTER)}, open(f"{OUT}/transcript_9x16.json", "w"), indent=1)
print(f"transcript_9x16.json  {len(words)} words")
print(r["text"].strip()[:500])
