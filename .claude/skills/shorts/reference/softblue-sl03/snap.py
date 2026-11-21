"""SL-03: snap every editorial in/out to measured silence on the dry voice track (no music bed).
Ground truth = 10 ms RMS envelope of ro05 round4 voice_raw.wav (same timeline as MASTER, lag 0.0 ms at 10 points)."""
import json, wave, numpy as np, sys
VR="/Volumes/Extreme/_edit_work/ro05-fable/round4/full/voice_raw.wav"
W=json.load(open("/Volumes/Extreme/_edit_work/ro05-fable/round4/full/mapped-words.json"))
w=wave.open(VR); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
hop=int(sr*0.01); n=len(a)//hop; env=20*np.log10(np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))+1e-7)
sp=np.percentile(env,90); thr=sp-26
sil=env<thr
# silence intervals >= 50 ms
iv=[]; i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        if (j-i)>=5: iv.append((i*0.01,j*0.01))
        i=j
    else: i+=1
json.dump({"speech_p90_db":float(sp),"thr_db":float(thr),"intervals":iv},open("silence.json","w"))
print("speech p90 %.1f dB thr %.1f dB, %d silences"%(sp,thr,len(iv)))
def near(t,lo,hi):
    c=[(s,e) for s,e in iv if e>lo and s<hi]
    return c
def word_at(t): 
    return [x for x in W if x['t0']-0.01<=t<=x['t1']+0.01]
def show(t,span=1.3):
    ws=[x for x in W if x['t1']>t-span and x['t0']<t+span]
    print("   words:"," ".join("%s[%.2f-%.2f]"%(x['w'],x['t0'],x['t1']) for x in ws))
    print("   sil:"," ".join("(%.2f-%.2f)"%(s,e) for s,e in near(t,t-span,t+span)))
if __name__=="__main__":
    for t in map(float,sys.argv[1:]):
        print("@",t); show(t)
