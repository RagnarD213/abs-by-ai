import whisper, json, sys
m = whisper.load_model("medium.en")
r = m.transcribe(sys.argv[1], word_timestamps=True, language="en", condition_on_previous_text=False, initial_prompt="Tesla, Model 3, Camry, Kelley Blue Book, robotaxis, Austin, self-driving car.")
off = float(sys.argv[3])
words=[]
for s in r["segments"]:
    for w in s.get("words",[]):
        words.append({"w":w["word"].strip(),"s":round(w["start"]+off,3),"e":round(w["end"]+off,3),"p":round(w.get("probability",0),3)})
json.dump({"text":r["text"],"words":words}, open(sys.argv[2],"w"), indent=1)
print(r["text"])
