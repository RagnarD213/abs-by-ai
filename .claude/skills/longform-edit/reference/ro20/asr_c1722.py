#!/usr/bin/env python3
"""RO-20 round 3b: Whisper medium.en word times for the C1722 lav (0 to 192 s, the four RO-20 pickups). Waits for a build slot first."""
import json, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import buildcap; buildcap.wait("RO-20 R3b pickup ASR")
import whisper
D = "/Volumes/Extreme/_edit_work/ro20/round3b/src"
r = whisper.load_model("medium.en").transcribe(f"{D}/c1722_lav_0-192_48k_mono.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
W = [dict(w=w["word"].strip(), t0=round(w["start"], 3), t1=round(w["end"], 3)) for s in r["segments"] for w in s["words"]]
json.dump(dict(model="medium.en", words=W, text=r["text"]), open(f"{D}/c1722_lav.transcript.json", "w"), indent=0); print(len(W), "words")
