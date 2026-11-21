import whisper, json, sys
m = whisper.load_model("medium.en")
out={}
for f,off in [("w1.wav",304.8),("w2.wav",315.0),("w3.wav",252.5)]:
    r = m.transcribe(f, word_timestamps=True, language="en", condition_on_previous_text=False, initial_prompt="Um, uh, so you're actually saving money and you get a car that drives you everywhere. And if you live somewhere with robotaxis.")
    ws=[dict(w=w["word"].strip(),s=round(w["start"]+off,3),e=round(w["end"]+off,3)) for s in r["segments"] for w in s["words"]]
    out[f]=ws; print(f, ' '.join(f"{x['s']:.2f}|{x['w']}|{x['e']:.2f}" for x in ws))
json.dump(out,open("words_windows.json","w"),indent=1)
