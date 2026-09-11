#!/usr/bin/env python3
"""Dense acoustic offset profile, GCC-PHAT weighted: Muhammad's mix is EQ'd / de-reverbed / compressed, so a plain
band-passed waveform correlation against the raw lav locks at median r 0.61 (Zeeshan's 0.99). PHAT whitens the
cross-spectrum so only PHASE decides, which is what survives an EQ. Same hops/windows; score = PHAT peak height
normalised by the window's own; plus a plain-correlation check at the found lag. Writes offset_profile.json."""
import json, wave, numpy as np
SR=16000
def rd(p):
    w=wave.open(p); return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)/32768
H=rd('his_mix16.wav'); R=rd('raw_lav16.wav')
def bp(x,lo=250,hi=4000):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<lo)|(f>hi)]=0; return np.fft.irfft(X,len(x))
HB=bp(H); RB=bp(R)
P=json.load(open('wordpairs.json'))
pt=np.array([p[0] for p in P]); po=np.array([p[2]-p[0] for p in P])
def guess(t):
    j=np.searchsorted(pt,t); cand=[k for k in (j-1,j) if 0<=k<len(pt)]
    return po[min(cand,key=lambda k:abs(pt[k]-t))]
HOP,WIN,SEARCH=0.10,0.70,1.0
prof=[]; DUR=len(H)/SR
for t in np.arange(0,DUR-WIN,HOP):
    a=int(t*SR); hb=HB[a:a+int(WIN*SR)]
    if np.sqrt((H[a:a+int(WIN*SR)]**2).mean())<0.003: prof.append((t,None,0.0)); continue
    g=t+guess(t); r0=max(0,int((g-SEARCH)*SR)); r1=min(len(RB),int((g+WIN+SEARCH)*SR)); r=RB[r0:r1]
    if len(r)<len(hb)+10: prof.append((t,None,0.0)); continue
    N=1<<int(np.ceil(np.log2(len(r)+len(hb))))
    X=np.fft.rfft(r,N)*np.conj(np.fft.rfft(hb,N)); X/=np.maximum(np.abs(X),1e-9)
    f=np.fft.rfftfreq(N,1/SR); X[(f<250)|(f>4000)]=0
    c=np.fft.irfft(X,N)[:len(r)-len(hb)+1]
    k=int(np.argmax(c)); pk=c[k]/max(np.std(c)*8,1e-9)      # peak in units of 8 sigma
    # plain normalised correlation at that lag, as a sanity value
    x=r[k:k+len(hb)]; nc=float(np.dot(x,hb)/max(np.sqrt((x**2).sum()*(hb**2).sum()),1e-9))
    prof.append((t,(r0+k)/SR-t,float(min(pk,1.0)*0.5+max(nc,0)*0.5)))
json.dump([[round(t,3),(None if o is None else round(o,4)),round(r,3)] for t,o,r in prof],open('offset_profile.json','w'))
ok=[p for p in prof if p[1] is not None and p[2]>0.6]
print(f'{len(prof)} windows, {len(ok)} scored >0.60, median score {np.median([p[2] for p in ok]):.2f}')
# jitter: within stretches of near-constant offset, sd of the offset
offs=np.array([p[1] for p in prof if p[1] is not None]); ts=np.array([p[0] for p in prof if p[1] is not None])
runs=[]; cur=[0]
for i in range(1,len(offs)):
    if abs(offs[i]-offs[i-1])<0.02: cur.append(i)
    else: runs.append(cur); cur=[i]
runs.append(cur)
big=[r for r in runs if len(r)>=8]
print(len(runs),'runs;',len(big),'runs >=8 windows; within-run offset sd (ms): median %.1f p90 %.1f'%(np.median([offs[r].std()*1000 for r in big]),np.percentile([offs[r].std()*1000 for r in big],90)))
steps=[(round(ts[r[0]],2),round(offs[r[0]],3),len(r)) for r in runs if len(r)>=3]
print('runs>=3:',len(steps)); print(steps[:40])
