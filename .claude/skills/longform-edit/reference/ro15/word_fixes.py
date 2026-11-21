"""After patch_words.py: the first word of each re-transcribed region is dropped by Whisper (RO-14 trap); add it back from the
level strip, and fix the one region-start word medium.en timed before the piece's in-point. Idempotent."""
import json
W = "/Volumes/Extreme/_edit_work/RO-15/round1"
J = json.load(open(f"{W}/words.json")); WJ = J["words"]
ADD = [(" So", 202.38, 202.58), (" If", 294.20, 294.34), (" My", 373.20, 373.36), (" Once", 439.54, 439.76), (" But", 472.90, 472.98), (" When", 545.70, 545.86)]
for wd, a, b in ADD:
    if not any(abs(w["start"] - a) < 0.05 and w["word"].strip() == wd.strip() for w in WJ):
        WJ.append(dict(word=wd, start=a, end=b, p=1.0, patched=True, by_hand=True))
for w in WJ:                                   # medium.en started "you" (and the dropped "When") early, before the piece's in-point
    if w["word"].strip() == "When" and 545.1 < w["start"] < 545.3: w["start"], w["end"] = 545.0, 545.1    # outside the piece: never mapped
    if w["word"].strip() == "you" and 545.5 < w["start"] < 545.7: w["start"] = 545.86
WJ.sort(key=lambda w: w["start"]); json.dump(dict(words=WJ), open(f"{W}/words.json", "w")); print(len(WJ), "words")
