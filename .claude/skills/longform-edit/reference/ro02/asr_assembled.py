import whisper, json
W = "/Volumes/Extreme/_edit_work/ro02"
m = whisper.load_model("medium.en")
r = m.transcribe(f"{W}/assembled_untreated.wav", word_timestamps=True, condition_on_previous_text=False, language="en")
json.dump(r, open(f"{W}/asr_assembled_medium.json", "w")); print("ASR DONE", len(r["segments"]), flush=True)
