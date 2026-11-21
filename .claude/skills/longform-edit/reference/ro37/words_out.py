"""Map each roll's medium.en words into film time through shots.json -> words_out.json [{w, t0, t1, roll, src}]."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
W = B.W; FPS = B.FPS
S = json.load(open(f"{W}/shots.json")); out = []
for s in S:
    for w in B.words(s["roll"]):
        mid = (w["t"] + w["e"]) / 2
        if w["e"] > s["src0"] + 0.06 and w["t"] < s["src1"] - 0.06 and (w["t"] >= s["src0"] - 0.35):
            o = s["out_f0"] / FPS - s["src0"]
            out.append(dict(w=w["w"].strip(), t0=round(w["t"] + o, 3), t1=round(w["e"] + o, 3), roll=s["roll"], src=w["t"]))
json.dump(out, open(f"{W}/words_out.json", "w"))
print(len(out), "words;", " ".join(x["w"] for x in out[:40]))
