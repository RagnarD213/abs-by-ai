"""words_out.json straight from the roll transcripts (medium.en on each roll, global source time): a word is kept when its
MIDPOINT is inside a shot; output time = shot out start + (source time - shot source start). Then a 4-word repeat scan."""
import json, re
W="/Volumes/Extreme/_edit_work/ro07"; FPS=30000/1001
WS=json.load(open(f"{W}/words.json"))["words"]; S=json.load(open(f"{W}/shots.json")); out=[]
for sh in S:
    a=sh["src_f0"]/FPS; b=sh["src_f1"]/FPS; o=sh["out_f0"]/FPS
    for w in WS:
        m=(w["start"]+w["end"])/2
        if a<=m<b: out.append(dict(w=w["word"].strip(), src0=w["start"], src1=w["end"], t0=round(o+max(w["start"],a)-a,3), t1=round(o+min(w["end"],b)-a,3), shot=sh["id"]))
json.dump(out,open(f"{W}/words_out.json","w"),indent=0); print(len(out),"words;",round(out[-1]["t1"],1),"s;",round(len(out)/(out[-1]["t1"]/60)),"wpm")
n=lambda s: re.sub(r"[^a-z0-9]","",s.lower()); T=[n(x["w"]) for x in out]; seen={}
for i in range(len(T)-3):
    k=tuple(T[i:i+4])
    if k in seen and out[i]["t0"]-out[seen[k]]["t0"]<30 and i-seen[k]>=4: print(f"  repeat {out[seen[k]]['t0']:7.1f} / {out[i]['t0']:7.1f}: {' '.join(k)}")
    seen[k]=i
