"""SL-19: snap every editorial in/out to measured silence on the film's dry voice (RO-17 final/RO17_MASTER.mp4.untreated.wav, film clock).
Words: RO-17 round3 words_out.json (t0/t1 film). Joins: round3 shots.json (out_f0)."""
import json, wave, numpy as np, sys
RO="/Volumes/Extreme/_edit_work/RO-17/round3/"; FPS=30000/1001
W=[x for x in json.load(open(RO+"words_out.json")) if x["t0"] is not None and x["t1"] is not None]
S=json.load(open(RO+"shots.json")); JOINS=[s["out_f0"]/FPS for s in S][1:]
w=wave.open(RO+"final/RO17_MASTER.mp4.untreated.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
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
    print("  joins:"," ".join("%.2f"%j for j in JOINS if a_<=j<=b_))
if __name__=="__main__":
    json.dump({"speech_p90_db":float(sp),"thr_db":float(thr),"intervals":iv,"joins":JOINS},open("silence.json","w"))
    print("speech p90 %.1f dB thr %.1f dB, %d silences"%(sp,thr,len(iv)))
    args=list(map(float,sys.argv[1:]))
    for a_,b_ in zip(args[::2],args[1::2]): print("@@",a_,b_); show(a_,b_)
