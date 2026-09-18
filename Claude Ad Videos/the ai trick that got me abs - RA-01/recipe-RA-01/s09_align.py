#!/usr/bin/env python3
"""Force-align the cut's words to the FINAL MIX with wav2vec2 CTC.

Whisper's own word timestamps ran ~130 ms early on the approved Ad 1 vertical's mix (sd 150,
p90 +295 ms) -- that is the "highlighted word does not match what is said" Dan rejected on
2026-09-08. Whisper supplies the WORDS; the timings come from this alignment against the audio
that is actually delivered.
"""
import json, re, sys
import subprocess, wave
import numpy as np, torch, torchaudio
CUT = json.load(open("cut.json"))
FIX = {"apps": "abs", "app": "abs", "rip": "ripped"}
raw = []
for w in CUT["words"]:
    t = w["w"].strip()
    if t.startswith("-") and raw:
        raw[-1] = {"w": raw[-1]["w"].rstrip() + t, "t": raw[-1]["t"], "e": w["e"]}
        continue
    raw.append({"w": w["w"], "t": w["t"], "e": w["e"]})
words = []
for w in raw:
    t = w["w"].strip()
    k = re.sub(r"[^a-z]", "", t.lower())
    if k in FIX:
        t = re.sub(re.escape(k), FIX[k], t, flags=re.I) if k in t.lower() else FIX[k]
        t = FIX[k] + ("," if w["w"].strip().endswith(",") else "") + ("." if w["w"].strip().endswith(".") else "")
    words.append({"w": t, "t": w["t"], "e": w["e"]})
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model()
labels = bundle.get_labels()
# torchaudio 2.8 has no wav backend here; decode with the project ffmpeg instead.
SRC = sys.argv[1] if len(sys.argv) > 1 else "mix.wav"
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
raw = subprocess.run([FF, "-nostdin", "-v", "error", "-i", SRC, "-ac", "1",
                      "-ar", str(bundle.sample_rate), "-f", "f32le", "-"],
                     capture_output=True).stdout
wav = torch.from_numpy(np.frombuffer(raw, dtype=np.float32).copy()).unsqueeze(0)
with torch.inference_mode():
    emissions, _ = model(wav)
    emissions = torch.log_softmax(emissions, dim=-1)[0].cpu()
d = {c: i for i, c in enumerate(labels)}
toks, spans = [], []
for i, w in enumerate(words):
    k = re.sub(r"[^A-Z']", "", w["w"].upper())
    if not k: spans.append(None); continue
    spans.append((len(toks), len(toks)+len(k)))
    toks.extend(d[c] for c in k if c in d)
    toks.append(d["|"])
T, N = emissions.size(0), len(toks)
trellis = torch.full((T+1, N+1), -float("inf")); trellis[0, 0] = 0
blank = 0
for t in range(T):
    trellis[t+1, 1:] = torch.maximum(trellis[t, 1:] + emissions[t, blank],
                                     trellis[t, :-1] + emissions[t, toks])
    trellis[t+1, 0] = trellis[t, 0] + emissions[t, blank]
path = [0]*N; j = N; t = T
while t > 0 and j > 0:
    stay = trellis[t-1, j] + emissions[t-1, blank]
    change = trellis[t-1, j-1] + emissions[t-1, toks[j-1]]
    t -= 1
    if change > stay:
        j -= 1; path[j] = t
ratio = wav.size(1)/bundle.sample_rate/T
aligned, bad = [], 0
for i, w in enumerate(words):
    sp = spans[i]
    if sp is None or sp[1] > len(path) or sp[0] >= sp[1]:
        aligned.append({"w": w["w"], "t": w["t"], "e": w["e"], "src": "whisper"}); bad += 1; continue
    t0 = path[sp[0]]*ratio
    t1 = (path[sp[1]-1]+1)*ratio
    if not (0 <= t0 < t1):
        aligned.append({"w": w["w"], "t": w["t"], "e": w["e"], "src": "whisper"}); bad += 1; continue
    aligned.append({"w": w["w"], "t": round(float(t0), 3), "e": round(float(max(t1, t0+0.04)), 3),
                    "src": "ctc"})
off = [a["t"]-w["t"] for a, w in zip(aligned, words) if a["src"] == "ctc"]
print(f"aligned {len(off)}/{len(words)} words by CTC ({bad} fell back to Whisper)")
print(f"CTC minus Whisper: median {np.median(off)*1000:+.0f} ms, p90 {np.percentile(np.abs(off),90)*1000:.0f} ms")
OUT = sys.argv[2] if len(sys.argv) > 2 else "words_aligned.json"
json.dump({"words": aligned, "source": SRC}, open(OUT, "w"), indent=1)
print(OUT, "written")
