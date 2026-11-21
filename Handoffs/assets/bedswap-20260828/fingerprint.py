import numpy as np, wave, os, sys, collections

SR=22050; NFFT=1024; HOP=256

def load(p):
    w=wave.open(p,'rb'); n=w.getnframes(); d=w.readframes(n)
    a=np.frombuffer(d,dtype=np.int16).astype(np.float32)/32768.0
    return a

def spec(a):
    win=np.hanning(NFFT).astype(np.float32)
    nf=1+(len(a)-NFFT)//HOP
    if nf<1: return np.zeros((0,NFFT//2+1),np.float32)
    idx=np.arange(NFFT)[None,:]+HOP*np.arange(nf)[:,None]
    fr=a[idx]*win
    S=np.abs(np.fft.rfft(fr,axis=1))
    return 20*np.log10(S+1e-8)

# frequency bands (bin indices) - pick strongest peak per band per frame
BANDS=[(4,10),(10,20),(20,40),(40,80),(80,160),(160,320)]

def peaks(S):
    pk=[]
    for t in range(S.shape[0]):
        row=S[t]
        for lo,hi in BANDS:
            seg=row[lo:hi]
            if seg.size==0: continue
            j=int(np.argmax(seg)); v=float(seg[j])
            pk.append((t,lo+j,v))
    if not pk: return []
    vals=np.array([p[2] for p in pk])
    thr=np.mean(vals)+0.4*np.std(vals)   # keep the stronger half-ish
    return [(t,f) for (t,f,v) in pk if v>=thr]

def hashes(pkl, fan=6, dtmin=1, dtmax=40):
    H=collections.defaultdict(list)
    for i,(t1,f1) in enumerate(pkl):
        c=0
        for (t2,f2) in pkl[i+1:]:
            dt=t2-t1
            if dt<dtmin: continue
            if dt>dtmax: break
            H[(f1,f2,dt)].append(t1); c+=1
            if c>=fan: break
    return H

def fp(path):
    return hashes(peaks(spec(load(path))))

def match(Hq,Hr):
    """count hashes aligning at a consistent offset"""
    off=collections.Counter(); shared=0
    for k,tq in Hq.items():
        tr=Hr.get(k)
        if not tr: continue
        shared+=1
        for a in tq:
            for b in tr:
                off[b-a]+=1
    if not off: return 0,0,0
    best,cnt=off.most_common(1)[0]
    return cnt,shared,best

if __name__=="__main__":
    ref=sys.argv[1]
    files=sorted(os.listdir("wav"))
    Hr=fp(os.path.join("wav",ref))
    print(f"REF {ref}: {len(Hr)} hash keys\n")
    rows=[]
    for f in files:
        if f==ref: continue
        Hq=fp(os.path.join("wav",f))
        cnt,shared,off=match(Hq,Hr)
        # normalise by query size
        score=cnt/max(1,len(Hq))
        rows.append((score,cnt,shared,off,len(Hq),f))
    rows.sort(reverse=True)
    print(f"{'score':>7} {'aligned':>8} {'shared':>7} {'off':>6}  file")
    for s,c,sh,o,n,f in rows:
        print(f"{s:7.4f} {c:8d} {sh:7d} {o:6d}  {f}")
