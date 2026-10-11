"""dump a word list as timestamped lines (new line at a gap >= 0.5 s or a sentence end). usage: dump.py words.json out.txt"""
import json, sys
d = json.load(open(sys.argv[1]))
if "words" in d: W = d["words"]
else: W = [w for s in d["segments"] for w in s["words"]]
out = []; cur = []; 
def flush():
    global cur
    if cur:
        longw = [f"{w['word'].strip()}({w['end']-w['start']:.1f})" for w in cur if w['end']-w['start'] > 0.9]
        out.append(f"{cur[0]['start']:7.2f}-{cur[-1]['end']:7.2f} " + "".join(w["word"] for w in cur).strip() + ("   <<LONG " + " ".join(longw) + ">>" if longw else ""))
    cur = []
for i, w in enumerate(W):
    if cur and w["start"] - cur[-1]["end"] >= 0.5:
        g = w["start"] - cur[-1]["end"]; flush(); 
        if g >= 1.5: out.append(f"        [gap {g:.1f}s]")
    cur.append(w)
    if w["word"].strip()[-1:] in ".?!": flush()
flush()
open(sys.argv[2], "w").write("\n".join(out) + "\n"); print(len(out), "lines")
