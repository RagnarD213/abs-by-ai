"""SL-17: snap every editorial in/out to measured silence on the film's dry voice (RO-26 round 5 audio/cut-untreated.wav, film clock).
Words: ro13_words.json (RO-26 recipe finished-asr.json, w/t/e film). Joins: ro13_cut_map.json (out_in)."""
import json, wave, numpy as np, sys
FPS=30000/1001
W=[dict(w=x['w'].strip(),t0=x['t'],t1=x['e']) for x in json.load(open("ro13_words.json"))['words'] if x.get('t') is not None]
JOINS=[c["out_in"] for c in json.load(open("ro13_cut_map.json"))["cuts"]][1:]
w=wave.open("dry_voice.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
if w.getnchannels()==2: a=a.reshape(-1,2).mean(1)
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
    print("  env10ms:"," ".join("%.2f:%d"%(k*0.01,env[k]) for k in range(int(a_*100),int(b_*100)) if k<n))
if __name__=="__main__":
    json.dump({"speech_p90_db":float(sp),"thr_db":float(thr),"intervals":iv,"joins":JOINS},open("silence.json","w"))
    print("speech p90 %.1f dB thr %.1f dB, %d silences"%(sp,thr,len(iv)))
    args=list(map(float,sys.argv[1:]))
    for a_,b_ in zip(args[::2],args[1::2]): print("@@",a_,b_); show(a_,b_)
