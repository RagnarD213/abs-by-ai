"""Hand fixes after patch_words.py (run after it): the 303.62 patch lost 'by' (Whisper's region start); the abandoned
'stayed...' (307.64, a stretched word of the stopped 99% read) overlaps the next piece by 0.14 s and is dropped."""
import json
W = "/Volumes/Expansion/_edit_work/ro28/round1"; P = f"{W}/words.json"
d = json.load(open(P)); WJ = d["words"]
WJ = [w for w in WJ if not (abs(w["start"] - 307.64) < 0.02 and w["word"].strip().startswith("stayed"))]
if not any(abs(w["start"] - 303.60) < 0.05 and w["word"].strip() == "by" for w in WJ):
    WJ.append(dict(word=" by", start=303.60, end=303.80, p=0.9, patched=True))
WJ.sort(key=lambda w: w["start"]); json.dump(dict(words=WJ), open(P, "w")); print(len(WJ), "words")
