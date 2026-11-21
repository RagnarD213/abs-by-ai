import json,sys
sl=json.load(open(sys.argv[1])); wj=json.load(open(sys.argv[2]))
ws=[w for s in wj["segments"] for w in s.get("words",[])]
for t in [float(x) for x in sys.argv[3:]]:
    near=[(a,b) for a,b in sl if b>=t-1.2 and a<=t+1.2]
    wn=[(w["word"].strip(),round(w["start"],2),round(w["end"],2)) for w in ws if w["end"]>=t-1.2 and w["start"]<=t+1.2]
    print(f"t={t:.2f}  sil={[(round(a,2),round(b,2)) for a,b in near]}")
    print(f"        words={wn}")
