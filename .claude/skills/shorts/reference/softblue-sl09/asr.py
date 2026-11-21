import whisper, wave, numpy as np, json, sys, scipy.signal as ss
w=wave.open("master_audio.wav"); SR=48000; x=np.frombuffer(w.readframes(w.getnframes()),"<i2").reshape(-1,2).mean(1).astype(np.float32)/32768
m=whisper.load_model("medium.en")
out={}
for name,a,b in [("K",190,242),("A",676,743),("HIJ",922,1118)]:
    seg=ss.resample_poly(x[int(a*SR):int(b*SR)],1,3).astype(np.float32)
    r=m.transcribe(seg,language="en",word_timestamps=True,fp16=False,condition_on_previous_text=False)
    ws=[dict(w=wd["word"].strip(),t=round(a+wd["start"],3),e=round(a+wd["end"],3)) for s_ in r["segments"] for wd in s_["words"]]
    out[name]=ws; print(name,len(ws),flush=True)
json.dump(out,open("asr_words.json","w"),indent=0)
