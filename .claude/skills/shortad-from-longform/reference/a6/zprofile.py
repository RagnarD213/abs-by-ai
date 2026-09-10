#!/usr/bin/env python3
"""Dense acoustic offset profile of Zeeshan's mix against the raw lav (skill: 'Recovering the EDL when word runs are
not enough'). Step his cut in 0.10 s hops, lock each 0.70 s window (300-3400 Hz) against the raw within +-1.5 s of the
word-derived offset. Every step in the locked offset is one of his audio cuts. Writes offset_profile.json."""
import json, wave, numpy as np
SR=16000
def rd(p):
    w=wave.open(p); return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)/32768
H=rd('his_mix16.wav'); R=rd('raw_lav16.wav')
def bp(x):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<300)|(f>3400)]=0; return np.fft.irfft(X,len(x))
HB=bp(H); RB=bp(R); RC=np.concatenate([[0.0],np.cumsum(RB**2)])
P=json.load(open('wordpairs.json'))
pt=np.array([p[0] for p in P]); po=np.array([p[2]-p[0] for p in P])
def guess(t):
    j=np.searchsorted(pt,t); cand=[k for k in (j-1,j) if 0<=k<len(pt)]
    return po[min(cand,key=lambda k:abs(pt[k]-t))]
HOP,WIN,SEARCH=0.10,0.70,1.5
prof=[]; DUR=len(H)/SR
for t in np.arange(0,DUR-WIN,HOP):
    hb=HB[int(t*SR):int((t+WIN)*SR)]
    if np.sqrt((H[int(t*SR):int((t+WIN)*SR)]**2).mean())<0.003: prof.append((t,None,0.0)); continue
    g=t+guess(t); r0=max(0,int((g-SEARCH)*SR)); r1=min(len(RB),int((g+WIN+SEARCH)*SR)); r=RB[r0:r1]
    if len(r)<len(hb)+10: prof.append((t,None,0.0)); continue
    N=1<<int(np.ceil(np.log2(len(r)+len(hb))))
    c=np.fft.irfft(np.fft.rfft(r,N)*np.conj(np.fft.rfft(hb,N)),N)[:len(r)-len(hb)+1]
    e=RC[r0+len(hb):r0+len(r)+1]-RC[r0:r0+len(r)-len(hb)+1]
    nc=c/np.maximum(np.sqrt((hb**2).sum())*np.sqrt(np.maximum(e,0)),1e-9); k=int(np.argmax(nc))
    prof.append((t,(r0+k)/SR-t,float(nc[k])))
json.dump([[round(t,3),(None if o is None else round(o,4)),round(r,3)] for t,o,r in prof],open('offset_profile.json','w'))
ok=[p for p in prof if p[1] is not None and p[2]>0.6]
print(f'{len(prof)} windows, {len(ok)} locked (r>0.60), median r {np.median([p[2] for p in ok]):.2f}')
steps=[]; prev=None
for t,o,r in prof:
    if o is None or r<=0.6: continue
    if prev and abs(o-prev[1])>0.05: steps.append((round(prev[0],2),round(t,2),round(prev[1],3),round(o,3)))
    prev=(t,o,r)
print(len(steps),'offset steps'); print(steps)
