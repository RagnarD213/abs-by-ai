"""Re-transcribe the kept start of a piece where medium.en folded a restart into one stretched word (the second copy's
words were lost inside it). For each region [a, b] (source s): remove every words.json word overlapping it, transcribe the
lav slice with medium.en word timestamps, insert its words (offset to source time) whose start lies in [a, b).
Also drops listed stray words. Writes words.json (keeps words_orig.json)."""
import json, os, wave, subprocess, numpy as np, whisper
W = "/Volumes/Extreme/_edit_work/RO-14/round1"; SR = 48000
REGIONS = [(209.34, 212.55), (353.02, 355.75), (473.06, 474.70), (483.58, 485.10), (547.20, 549.12)]
DROP = [(601.09, "it")]                     # 'it' of the abandoned 'it is not gonna' (601.1), 0.1 s inside r3b's tail
if not os.path.exists(f"{W}/words_orig.json"): os.rename(f"{W}/words.json", f"{W}/words_orig.json")
WJ = json.load(open(f"{W}/words_orig.json"))["words"]
wv = wave.open(f"{W}/lav.wav"); A = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
m = whisper.load_model("medium.en"); new = []
for a, b in REGIONS:
    s0 = max(0, a - 0.3); x = A[int(s0*SR):int((b + 0.6)*SR)]
    import scipy.signal as ss
    y = ss.resample_poly(x, 1, 3).astype(np.float32)            # 48 k -> 16 k
    r = m.transcribe(y, word_timestamps=True, language="en", condition_on_previous_text=False)
    got = [dict(word=w["word"], start=round(s0 + w["start"], 3), end=round(s0 + w["end"], 3), p=round(w.get("probability", 0), 2), patched=True)
           for sg in r["segments"] for w in sg.get("words", []) if a - 0.05 <= s0 + w["start"] < b]
    print(f"{a}-{b}:", " ".join(f"{g['word'].strip()}[{g['start']:.2f}]" for g in got))
    WJ = [w for w in WJ if not (w["start"] < b and w["end"] > a)]
    new += got
for t, wd in DROP: WJ = [w for w in WJ if not (abs(w["start"] - t) < 0.02 and w["word"].strip().lower() == wd)]
WJ = sorted(WJ + new, key=lambda w: w["start"])
json.dump(dict(words=WJ), open(f"{W}/words.json", "w")); print(len(WJ), "words")
