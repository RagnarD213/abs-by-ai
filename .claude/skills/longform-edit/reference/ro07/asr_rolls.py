"""medium.en word-level transcript of each roll's lav (the sidecar words are Whisper small: mapping only)."""
import json, sys, whisper
W = "/Volumes/Extreme/_edit_work/ro07"
m = whisper.load_model("medium.en")
for roll in sys.argv[1:]:
    r = m.transcribe(f"{W}/lav/{roll}.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
    json.dump(r, open(f"{W}/asr_{roll}_medium.json", "w"))
    print(roll, "done", sum(len(s["words"]) for s in r["segments"]), "words", flush=True)
print("ASR COMPLETE", flush=True)
