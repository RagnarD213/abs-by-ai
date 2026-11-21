"""SL-21: snap every editorial in/out to measured silence on the APPROVED RO-20B round 4 master's own mix (master_audio.wav, film clock).
Words: the film's plan.json words (bound to master sha 88a6314f).
Picture joins: every presenter segment boundary in the film's layout.json, mapped to master time (the master's picture cuts)."""
import json, wave, numpy as np, sys
FPS=30000/1001
PL=json.load(open("src/ro20b_plan.json")); W=[dict(w=x["w"],t0=x["t"],t1=x["e"]) for x in PL["words"]]
L=json.load(open("src/ro20b_layout.json"))
JOINS=set()
for k,p in enumerate(L["parts"]):
    JOINS.add(p["out"][0])
    for s_ in p.get("segments",[]): JOINS.add(s_["o0"])      # RO-20B round 4 v2 layout: segment o0 is already the master's output frame (part 2 starts at o0 789 = out[0]); verified by the frame-difference scan of base.mp4 (scan.py, 2026-11-13)
JOINS=sorted(round(j/FPS,3) for j in JOINS if j>0)
w=wave.open("master_audio.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32).reshape(-1,2).mean(1)/32768
hop=int(sr*0.01); n=len(a)//hop; env=20*np.log10(np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))+1e-7)
sp=np.percentile(env,90); thr=sp-26; sil=env<thr
iv=[]; i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        if (j-i)>=5: iv.append((round(i*0.01,2),round(j*0.01,2)))
        i=j
    else: i+=1
def show(a_,b_):
    ws=[x for x in W if x['t1']>a_ and x['t0']<b_]
    print(" ".join("%s[%.2f-%.2f]"%(x['w'],x['t0'],x['t1']) for x in ws))
    print("  sil:"," ".join("(%.2f-%.2f)"%(s,e) for s,e in iv if e>a_ and s<b_))
    print("  joins:"," ".join("%.3f"%j for j in JOINS if a_<=j<=b_))
    print("  10ms dB:", " ".join("%.2f:%.0f"%(k*0.01,env[k]) for k in range(int(a_*100),int(b_*100))))
if __name__=="__main__":
    json.dump({"speech_p90_db":float(sp),"thr_db":float(thr),"intervals":iv,"joins":JOINS},open("silence.json","w"))
    print("speech p90 %.1f dB thr %.1f dB, %d silences, %d picture joins; pause floor median %.1f dB"%(sp,thr,len(iv),len(JOINS),float(np.median(env[sil]))))
    args=list(map(float,sys.argv[1:]))
    for a_,b_ in zip(args[::2],args[1::2]): print("@@",a_,b_); show(a_,b_)
