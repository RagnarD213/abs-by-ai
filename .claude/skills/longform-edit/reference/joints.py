import json, subprocess, sys, whisper
from pathlib import Path
slug, vid = sys.argv[1], sys.argv[2]; beats = sys.argv[3:]
B = Path(slug); V = B/"roughcuts"/vid
rs = json.load(open(B/"edl.json"))["ranges"]
offs, acc = [], 0.0
for r in rs: offs.append(acc); acc += round(r["end"]-r["start"], 3)
idx = {r["beat"]: i for i, r in enumerate(rs)}
m = whisper.load_model("small")
for beat in beats:
    i = idx.get(beat)
    if i is None: print(f"  {beat}: not found"); continue
    t = offs[i]
    w = B/"_j.wav"
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{max(0,t-2.5):.2f}","-i",str(V),
                    "-t","6","-vn","-ac","1","-ar","16000",str(w)],check=True)
    print(f"  {beat:24s} @{t:8.2f} :: {m.transcribe(str(w), fp16=False, language='en')['text'].strip()}")
    w.unlink()
