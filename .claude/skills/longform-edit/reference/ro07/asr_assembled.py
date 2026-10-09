import json, whisper
W="/Volumes/Extreme/_edit_work/ro07"
r=whisper.load_model("medium.en").transcribe(f"{W}/assembled_untreated.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
json.dump(r, open(f"{W}/asr_assembled_medium.json","w")); print("ASSEMBLED ASR COMPLETE", sum(len(s["words"]) for s in r["segments"]), "words", flush=True)
