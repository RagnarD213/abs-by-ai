"""carry a judged watch pass forward by TIME TOKEN (strip names renumber when a boundary is added or removed): an image whose
earlier twin (same time, same size) is pixel-identical and was judged clean/expected keeps its verdicts; everything else is re-judged."""
import sys,os,re,json,glob
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16")
from carry_verdicts import same
B,P=os.path.abspath(sys.argv[1]),os.path.abspath(sys.argv[2])
prev={}; judges=[]
for fp in sorted(glob.glob(P+"/logs/findings_part*.json")):
    d=json.load(open(fp)); judges.append(d.get("judge","?"))
    for e in d["entries"]: prev.setdefault(os.path.basename(str(e.get("image",""))),[]).append(e)
def key(name):
    m=re.match(r"(strip|sheet|pair)_\d+_(\d\d-\d\d\.\d\d)(_to_\d\d-\d\d\.\d\d)?",name)
    return (m.group(1),m.group(2),m.group(3)) if m else None
oldmap={}
for sub in ("sheets","strips"):
    for f in glob.glob(P+f"/watch/{sub}/*.jpg"):
        n=os.path.basename(f)
        oldmap.setdefault(key(n),[]).append((n,f))
carried=[]; redo=[]
for sub in ("sheets","strips"):
    for f in sorted(glob.glob(B+f"/watch/{sub}/*.jpg")):
        n=os.path.basename(f)
        k=key(n); ok=False
        for on,of in oldmap.get(k,[]):
            ents=prev.get(on)
            if ents and all(e.get("verdict") in ("clean","expected") for e in ents) and same(f,of,1.0):
                # the pair image beside it must match too
                if n.startswith("strip_"):
                    pair=lambda nm: re.sub(r"^strip_(\d+_\d\d-\d\d\.\d\d).*$",r"pair_\1.jpg",nm)
                    pn=pair(n); po=os.path.join(P,"watch","strips",pair(on)); pf=os.path.join(B,"watch","strips",pn)
                    if not (os.path.exists(po) and os.path.exists(pf) and same(pf,po,1.0)): continue
                for e in ents: carried.append(dict(e,image=n,note="carried: pixel-identical to the judged round (same time, same size) | "+str(e.get("note",""))))
                ok=True; break
        if not ok: redo.append(n)
os.makedirs(B+"/logs",exist_ok=True)
vid=None
for fp in glob.glob(P+"/logs/findings_part*.json"): vid=json.load(open(fp)).get("video") or vid
json.dump(dict(judge="carried from round 2 ("+" | ".join(judges)+")",video=None,method="carry_by_time.py: entries kept only for images (and their pair images) pixel-identical to the judged round",entries=carried),open(B+"/logs/findings_part0_carried.json","w"),indent=1)
json.dump(redo,open(B+"/logs/rejudge.json","w"),indent=1)
print(len(carried),"entries carried;",len(redo),"images to re-judge")
