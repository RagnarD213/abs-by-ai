"""SL-18: snap every editorial in/out to measured silence on the APPROVED RO-25 master's own mix (master_audio.wav, film clock,
lag 0.0 ms against -ss pulls at 8 points, 2026-10-20). Words: RO-25 round7 plan/full-words.json (bound to master sha 6045ac0e).
Picture joins: round7 plan/full-edit-map.json entries plus their excluded (false-start) spans."""
import json, wave, numpy as np, sys
R7="/Volumes/Extreme/_edit_work/RO-25/round7/plan/"; FPS=30000/1001
W=json.load(open(R7+"full-words.json"))["words"]
E=json.load(open(R7+"full-edit-map.json"))["entries"]
JOINS=[]
for e in E:
    JOINS.append(e["out_seconds"][0])
    if e.get("excluded_original"):
        acc=e["out_seconds"][0]
        for a,b in e["original_kept"][:-1]: acc+=round((b-a)*FPS)/FPS; JOINS.append(acc)
JOINS=sorted(set(round(j,3) for j in JOINS))[1:]
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
    print("speech p90 %.1f dB thr %.1f dB, %d silences; pause floor median %.1f dB"%(sp,thr,len(iv),float(np.median(env[sil]))))
    args=list(map(float,sys.argv[1:]))
    for a_,b_ in zip(args[::2],args[1::2]): print("@@",a_,b_); show(a_,b_)
