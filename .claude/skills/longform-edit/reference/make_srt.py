#!/usr/bin/env python3
"""Build an SRT timed to the FINAL EDIT by mapping source word timestamps
through the EDL. Words that fell on the cutting-room floor are dropped."""
import json, sys

P="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot"
BEATS=[(0.78,15.14),(33.70,47.86),(48.96,59.96),(60.42,65.00),(66.32,68.92),
       (71.36,72.52),(74.60,77.66),(81.76,83.48),(86.94,88.12),(88.82,97.66),
       (100.86,115.20),(117.04,144.66),(146.50,157.06),(160.64,162.58),
       (172.58,179.52),(201.98,233.36),(237.96,265.62),(288.08,296.32),
       (299.58,305.08),(308.68,340.24)]
# render offsets accumulate exactly as the build did (durations rounded to 3dp)
offs=[]; acc=0.0
for cs,ce in BEATS:
    offs.append(acc); acc+=round(ce-cs,3)
TOTAL=acc

words=[w for w in json.load(open(f"{P}/edit/transcripts/C1541.json"))["words"]
       if w["type"]=="word"]

def to_render(t):
    for (cs,ce),o in zip(BEATS,offs):
        if cs-0.02 <= t <= ce+0.02:
            return o + max(0.0, t-cs)
    return None

mapped=[]
for w in words:
    a=to_render(w["start"]); b=to_render(w["end"])
    if a is None: continue
    if b is None or b<a: b=a+0.25
    mapped.append({"t":w["text"],"a":a,"b":b})

MAXCHARS=84   # 2 lines x 42
cues=[]; cur=[]
def flush():
    global cur
    if not cur: return
    txt=" ".join(x["t"] for x in cur).strip()
    a=cur[0]["a"]; b=max(cur[-1]["b"], a+0.8)
    cues.append((a,b,txt)); cur=[]
for i,w in enumerate(mapped):
    if cur:
        gap=w["a"]-cur[-1]["b"]
        cand=len(" ".join(x["t"] for x in cur))+1+len(w["t"])
        # break on a real pause, on sentence end, on length, or on max duration
        if gap>=0.45 or cand>MAXCHARS or (w["a"]-cur[0]["a"])>5.5 or cur[-1]["t"].endswith((".","?","!")):
            flush()
    cur.append(w)
flush()

# clamp overlaps and the tail
out=[]
for i,(a,b,t) in enumerate(cues):
    if i+1<len(cues): b=min(b, cues[i+1][0]-0.04)
    b=min(b, TOTAL); 
    if b-a < 0.5: b=min(a+0.5, TOTAL)
    if b>a: out.append((a,b,t))

def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=int(x%60); ms=int(round((x-int(x))*1000))
    if ms==1000: s+=1; ms=0
    return "%02d:%02d:%02d,%03d"%(h,m,s,ms)

def wrap(t,width=42):
    if len(t)<=width: return t
    ws=t.split(); l1=""
    for i,w in enumerate(ws):
        if len(l1)+len(w)+1>width and l1: return l1+"\n"+" ".join(ws[i:])
        l1=(l1+" "+w).strip()
    return t

dst=f"{P}/roughcuts/SPLITSCREEN_v3_graphics.srt"
with open(dst,"w") as f:
    for i,(a,b,t) in enumerate(out,1):
        f.write("%d\n%s --> %s\n%s\n\n"%(i,ts(a),ts(b),wrap(t)))
print("cues:",len(out),"-> ",dst)
print("last cue ends %.2fs of %.2fs"%(out[-1][1],TOTAL))
print("words kept %d of %d (rest were cut)"%(len(mapped),len(words)))
