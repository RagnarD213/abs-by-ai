import os, sys, time, json, whisper
JOBS = [("spraytan","C1512"),("zepbound","C1513"),("supplements","C1514")]
m = None
for d,b in JOBS:
    wav = f"{d}/{b}.wav"; out = f"{d}/{b}.whisper.json"
    if os.path.exists(out): print("skip", b, flush=True); continue
    # wait for extraction to finish (size stable + ffmpeg job done)
    while True:
        if os.path.exists(wav):
            s1=os.path.getsize(wav); time.sleep(6); s2=os.path.getsize(wav)
            if s1==s2 and s1>0: break
        else: time.sleep(6)
    if m is None: m = whisper.load_model("small")
    t0=time.time()
    r = m.transcribe(wav, word_timestamps=True, language="en", fp16=False, verbose=False)
    json.dump(r, open(out,"w"))
    nw = sum(len(s.get("words",[])) for s in r["segments"])
    print(f"{b}: {time.time()-t0:.0f}s segments={len(r['segments'])} words={nw}", flush=True)
print("TXDONE", flush=True)
