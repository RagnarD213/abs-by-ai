#!/usr/bin/env python3
"""RA-09: C1666's single take hides a restart. Replicate's large-v3 heard one sentence 20.76-26.00 with a 2.5 s "AI"; an isolated
medium.en pass on 21.6-26.2 s (disfluency prompt) hears the WHOLE sentence again from 23.24 s: the first attempt "I'm not just talking
about an" (20.76-22.55) stops, 0.7 s of silence (envelope -60 to -68 dB), then the clean read. The first attempt's words are kept in the
list (the EDL drops them by range); the restatement's words come from the isolated pass. Text fix: "Gut injured" -> "Got injured".
Idempotent: the untouched merge is tx/c1666.whisper.orig.json."""
import json, os, shutil
P = "tx/c1666.whisper.json"; O = "tx/c1666.whisper.orig.json"
if not os.path.exists(O): shutil.copy(P, O)
d = json.load(open(O)); WS = d["segments"][0]["words"]
first = [("I'm", 21.22, 21.40), ("not", 21.40, 21.52), ("just", 21.46, 21.72), ("talking", 21.72, 22.00), ("about", 22.00, 22.24), ("an", 22.24, 22.52)]
again = [("I'm", 23.54, 23.72), ("not", 23.72, 23.92), ("just", 23.92, 24.10), ("talking", 24.10, 24.44), ("about", 24.44, 24.64),
         ("an", 24.64, 24.80), ("AI", 24.80, 25.08), ("-generated", 25.08, 25.58), ("picture.", 25.58, 25.98)]
keep = [w for w in WS if not (20.70 <= w["start"] < 26.00)]
new = [{"word": " " + t, "start": a, "end": b} for t, a, b in first + again]
WS2 = sorted(keep + new, key=lambda w: w["start"])
for w in WS2:
    if w["word"].strip() == "Gut":
        w["word"] = " Got"; w["start"] = max(w["start"], 64.40)   # envelope onset 64.40 (the lip noise at 64.30 is cut, review item 4)
d["segments"][0]["words"] = WS2
json.dump(d, open(P, "w"), indent=1)
print(len(WS), "->", len(WS2), "words")
