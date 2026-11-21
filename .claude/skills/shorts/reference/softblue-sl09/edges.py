import json, wave, numpy as np, sys
W=json.load(open("asr_words.json")); W2=json.load(open("asr_words2.json"))
words=sorted([w for v in W.values() for w in v]+W2["V"],key=lambda w:w["t"])
G=json.load(open("gaps.json"))
w=wave.open("master_mono.wav"); SR=48000; x=np.frombuffer(w.readframes(w.getnframes()),"<i2").astype(np.float32)/32768
import scipy.signal as ss
bv=ss.butter(4,[300,3400],btype="band",fs=SR,output="sos"); bs=ss.butter(4,[5000,12000],btype="band",fs=SR,output="sos")
def env(t0,t1):
    s=x[int(t0*SR):int(t1*SR)]; v=ss.sosfilt(bv,s); h=ss.sosfilt(bs,s); n=int(0.02*SR)
    k=len(s)//n; f=lambda y:20*np.log10(np.sqrt((y[:k*n].reshape(k,n)**2).mean(1))+1e-9)
    return f(v),f(h)
EDGES=[("A in",682.08),("A out",739.3),("H1 in",976.34),("H1 out",984.85),("H2 in",928.46),("H2 out",976.3),("I1 in",989.1),("I1 out",1035.5),("I2 in",1056.36),("I2 out",1065.2),("J in",1067.0),("J out",1113.4),("K in",195.0),("K out",237.95)]
for name,t in EDGES:
    print("=====",name,t)
    print("  words:"," ".join(f"{w['w']}@{w['t']:.2f}-{w['e']:.2f}" for w in words if t-2.5<w["t"]<t+2.0))
    print("  gaps:"," ".join(f"[{a:.2f}-{b:.2f}]" for a,b in G if t-2.5<b and a<t+2.0))
    v,h=env(t-1.0,t+1.0)
    print("  voice dB/20ms from",f"{t-1.0:.2f}:"," ".join(f"{q:.0f}" for q in v))
    print("  hiss  dB/20ms      :"," ".join(f"{q:.0f}" for q in h))
