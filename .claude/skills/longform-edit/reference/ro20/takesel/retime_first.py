"""First words whose Whisper time sits before the measured cut-in (Whisper pads a take's first word back into the pause):
the audio keeps the word (checked: verify5.txt, each piece re-transcribed from its in point) but words_src_out.py drops it by
its midpoint. Write a word_patches.json entry that moves such a word (and any word it then overlaps) to the lav onset."""
import json, sys, wave, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/recipe")
import edl
SR = 48000; A = edl.lav(); W = edl.WORDS
def db(t): x = A[int(t*SR):int((t+0.02)*SR)]; return 20*np.log10(np.sqrt(np.mean(x*x))+1e-9)
P = edl.pieces(); patches = json.load(open(f"{edl.W}/word_patches.json")); n = 0
for p, row in zip(P, edl.PIECES):
    i0, _ = edl.find("C1511", row[2], row[4]); w = W[i0]
    if (w["start"]+w["end"])/2 >= p["in"]: continue
    t = p["in"]
    while t < p["in"]+0.6 and not (db(t) > edl.THR and db(t+0.01) > edl.THR): t += 0.01
    new = []; prev_end = None; k = i0
    while True:
        x = W[k]; s = round(t-0.02, 2) if k == i0 else max(x["start"], prev_end)
        if k > i0 and s == x["start"]: break
        e = round(max(x["end"], s+0.12), 2); new.append((x, s, e)); prev_end = e; k += 1
    for x, s, e in new:
        m = (x["start"]+x["end"])/2
        patches.append(dict(t0=round(m-0.004, 3), t1=round(m+0.004, 3), why=f"piece {p['id']}: '{x['word'].strip()}' moved from {x['start']:.2f}-{x['end']:.2f} to the lav onset (first word of a kept take; heard from the cut-in on a verify window)", words=[[x["word"].strip(), s, e]]))
        print(p["id"], x["word"].strip(), x["start"], x["end"], "->", s, e)
    n += 1
json.dump(patches, open(f"{edl.W}/word_patches.json", "w"), indent=1); print(n, "pieces retimed;", len(patches), "patches in all")
