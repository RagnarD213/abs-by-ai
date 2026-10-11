"""loud lav (>= 0.10 s, peak > -30 dB) in the 1.6 s before each piece in that no kept or cut Whisper word accounts for"""
import json, wave, numpy as np
SR=48000; wv=wave.open("/Volumes/Extreme/_edit_work/ro20/lav.wav"); A=np.frombuffer(wv.readframes(wv.getnframes()),np.int16).astype(np.float32)/32768
W=json.load(open("/Volumes/Extreme/_edit_work/ro20/words.json"))["words"]; P=json.load(open("/Volumes/Extreme/_edit_work/ro20/edl.json"))
for p in P:
    a=p["in"]; ts=np.arange(a-1.6,a,0.01); d=np.array([20*np.log10(np.sqrt(np.mean(A[int(t*SR):int((t+0.02)*SR)]**2))+1e-9) for t in ts]); q=d>-43; i=0
    while i<len(q):
        j=i
        while j<len(q) and q[j]==q[i]: j+=1
        if q[i] and ts[j-1]-ts[i]>=0.10 and d[i:j].max()>-30:
            x,y=float(ts[i]),float(ts[j-1])+0.01
            cov=[w["word"].strip() for w in W if w["start"]<y-0.03 and w["end"]>x+0.03]
            print(f"{p['id']:8s} in {a:8.2f}: loud {x:.2f}-{y:.2f} peak {d[i:j].max():.0f}  words there: {' '.join(cov) or 'NONE'}")
        i=j
