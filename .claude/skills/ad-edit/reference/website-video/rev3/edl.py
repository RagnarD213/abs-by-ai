#!/usr/bin/env python3
"""Website video EDL: kept spans across TWO rolls (C1650 = script through 'charged a dime',
C1651 = the price line re-read at $19.99 + the close). Edges are placed on Whisper WORD
boundaries (in = first word start - 0.12, out = last word end + 0.08) and VALIDATED
against a measured -40 dB envelope of the lav; any edge not inside/near silence is flagged.
The tight pass removes the intra-range pauses later; this only removes retakes + slates."""
import json, re, wave
import numpy as np
SRCDIR=("/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, "
        "scripted long form content/main camera")
ROLLS={"C1650":f"{SRCDIR}/C1650.MP4","C1651":f"{SRCDIR}/C1651.MP4"}
# (roll, first-phrase, after, last-phrase, note)
SPANS=[
 ("C1650","Congratulations on visualizing",  0.0,"how to customize the program for you", "intro through the first 'customize' line; the aborted 'by telling our AI,' at 138-141 is cut"),
 ("C1650","And you can make the program even better",141.0,"And that's just the beginning", "retake of the 'even better' line through 'just the beginning' (first occurrence 194.9)"),
 ("C1650","We also have an AI sleep coach",201.0,"you won't be charged a dime", "second 'sleep coach' take (the 196.5 one restarts) through 'charged a dime'; the $20 price line at 236-240 is WRONG and cut"),
 ("C1651","But if the app helps you",0.0,"the body that they always wanted", "price line re-read at $19.99 + the close"),
 ("C1651","Try abs by AI for free",39.0,"to get started", "CTA take 2 (take 1 at 33.6 is equally clean; later fluent take wins)"),
]
norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower()).split()
def words(roll):
    d=json.load(open(f"tx/{roll}.whisper.json"))
    return [w for s in d["segments"] for w in s["words"]]
def env(roll):
    w=wave.open(f"audio/{roll}.16k.wav"); sr=w.getframerate()
    a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float64)/32768
    HOP=0.005; N=int(HOP*sr); n=len(a)//N
    db=20*np.log10(np.sqrt((a[:n*N].reshape(n,N)**2).mean(1))+1e-9)
    return db,HOP
def find(ws,phrase,after):
    toks=norm(phrase); seq=[norm(w["word"]) for w in ws]; seq=[t[0] if t else "" for t in seq]
    for i,w in enumerate(ws):
        if w["start"]<after: continue
        if seq[i:i+len(toks)]==toks: return i
    raise KeyError(phrase)
def in_silence(db,HOP,t,win=0.08,thr=-40):
    i0=max(0,int((t-win)/HOP)); i1=int((t+win)/HOP)+1
    return bool((db[i0:i1]<thr).any())
ranges=[]; flags=[]
for roll,p0,after,p1,note in SPANS:
    ws=words(roll); db,HOP=env(roll)
    i=find(ws,p0,after); j=find(ws,p1,ws[i]["start"])+len(norm(p1))-1
    a=round(ws[i]["start"]-0.12,3); b=round(ws[j]["end"]+0.08,3)
    # clamp to neighbours so the pad never bites an adjacent word
    if i>0: a=max(a,round(ws[i-1]["end"]+0.02,3))
    if j+1<len(ws): b=min(b,round(ws[j+1]["start"]-0.02,3))
    for edge,t in (("in",a),("out",b)):
        if not in_silence(db,HOP,t): flags.append((roll,edge,t))
    ranges.append({"source":ROLLS[roll],"roll":roll,"start":a,"end":b,
                   "head":" ".join(w["word"].strip() for w in ws[i:i+4]),
                   "tail":" ".join(w["word"].strip() for w in ws[j-3:j+1]),"note":note})
for r in ranges: print(f"{r['roll']} {r['start']:8.3f}-{r['end']:8.3f} ({r['end']-r['start']:6.2f}s)  [{r['head']} ... {r['tail']}]")
print("total",round(sum(r["end"]-r["start"] for r in ranges),2),"s")
print("FLAGS (edge not in -40dB silence within 80ms):",flags)
json.dump({"fps":"30000/1001","ranges":ranges},open("edl.json","w"),indent=1)
