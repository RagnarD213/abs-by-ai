#!/usr/bin/env python3
"""SL-06 round 2: blind Gemini listen of the pickup joins with two film-internal joins as controls (SL-07 lesson:
a blind listener flags any edit, so the controls say how much a "heard" join means). Quality review, about $0.02.
  listen_joins.py   -> round2/listen/clip_<k>.wav, key.json, gemini.json"""
import json, os, random, base64, wave, urllib.request, sys
import numpy as np
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/rolls")
from roll_sidecar import secret_value
import plans as P, batch as Bt
L = Bt.WORK + "/round2/listen"
def rd(p):
    w = wave.open(p); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, w.getnchannels()); return x, sr
items = [(S, "pickup", Bt.head(S)) for S in "ABCDE"] + [("B", "control", 13.11), ("E", "control", 13.07)]
random.seed(616); random.shuffle(items); key = []
for k, (S, kind, j) in enumerate(items):
    x, sr = rd(f"{Bt.D(S)}/audio.wav"); a = max(0, int((j - 3.0) * sr)); b = int((j + 3.0) * sr)
    w = wave.open(f"{L}/clip_{k + 1}.wav", "w"); w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x[a:b].tobytes()); w.close()
    key.append(dict(clip=k + 1, short=S, kind=kind, join_at=round(j - a / sr, 2)))
json.dump(key, open(f"{L}/key.json", "w"), indent=1)
prompt = ("These are 7 short clips of the same man talking, each about 6 seconds. Some clips contain an edit where two "
          "separate recordings are joined; some may not. For EACH clip, listen carefully and answer: (1) is there a point where "
          "the voice changes in loudness, tone, closeness to the mic, room sound or background sound, as if two recordings were "
          "joined? yes or no; (2) if yes, at about what second, and what changes; (3) how noticeable it would be to a casual viewer "
          "on a phone: not at all, slightly, clearly. Be strict; do not guess an edit where none is audible. "
          "Reply as JSON: [{\"clip\":1,\"edit_heard\":true,\"at_s\":2.9,\"what\":\"...\",\"noticeable\":\"slightly\"}, ...]")
parts = [{"text": prompt}]
for k in range(len(items)):
    parts += [{"text": f"Clip {k + 1}:"}, {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(open(f"{L}/clip_{k + 1}.wav", "rb").read()).decode()}}]
key_ = (secret_value("GEMINI_API_KEY") or "").strip().strip(chr(34)); model = "gemini-3.1-pro-preview"
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key_}",
      data=json.dumps({"contents": [{"parts": parts}], "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}}).encode(), headers={"Content-Type": "application/json"})
body = json.loads(urllib.request.urlopen(req, timeout=300).read()); txt = "".join(p.get("text", "") for c in body["candidates"] for p in c["content"]["parts"])
res = json.loads(txt); json.dump(dict(model=model, usage=body.get("usageMetadata"), result=res), open(f"{L}/gemini.json", "w"), indent=1)
for r in res:
    k = key[r["clip"] - 1]; print(f"clip {r['clip']}: {k['short']} {k['kind']:7s} join at {k['join_at']}s | heard={r.get('edit_heard')} at {r.get('at_s')} {r.get('noticeable')}: {r.get('what')}")
print(body.get("usageMetadata"))
