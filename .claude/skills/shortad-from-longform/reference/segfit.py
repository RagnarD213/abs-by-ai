import numpy as np, wave, json
from numpy.lib.stride_tricks import sliding_window_view
SR=16000; NFFT=512; HOP=160
def rd(p):
    w=wave.open(p,'rb'); return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768.
def melspec(x):
    n=1+(len(x)-NFFT)//HOP; win=np.hanning(NFFT).astype(np.float32)
    idx=np.arange(NFFT)[None,:]+HOP*np.arange(n)[:,None]
    S=np.abs(np.fft.rfft(x[idx]*win,axis=1)); f=np.linspace(0,SR/2,S.shape[1])
    e=np.linspace(2595*np.log10(1+200/700),2595*np.log10(1+6500/700),26); hz=700*(10**(e/2595)-1)
    B=np.zeros((n,24),np.float32)
    for i in range(24):
        m=(f>=hz[i])&(f<hz[i+2]); B[:,i]=S[:,m].mean(1) if m.any() else 0
    B=np.log(B+1e-6); B-=B.mean(1,keepdims=True); B/=(B.std(1,keepdims=True)+1e-6); return B
MC=melspec(rd('m.wav')); MR=melspec(rd('raw_R.wav'))
NR=len(MR)

def match(ci,co,guess,search=500):
    a=int(round(ci*100)); b=min(int(round(co*100)), len(MC))
    w=MC[a:b]; W=len(w)
    if W<8: return None
    lo=max(0,int(round(guess*100))-search); hi=min(NR-W, int(round(guess*100))+search)
    if hi<=lo: return None
    sw=sliding_window_view(MR[lo:hi+W],(W,24))[:,0]
    sc=(sw*w[None]).sum(axis=(1,2))/(W*24)
    k=int(np.argmax(sc))
    # per-frame agreement profile at the best offset
    prof=(MR[lo+k:lo+k+W]*w).sum(1)/24
    return (lo+k)/100.0, float(sc[k]), prof

S=json.load(open('his_edl.json'))
work=[(s['cut_in'],s['cut_out'],s['src_in']) for s in S]
final=[]; MINSC=0.60; MINDUR=0.30
it=0
while work and it<4000:
    it+=1
    ci,co,g=work.pop(0)
    r=match(ci,co,g)
    if r is None: final.append((ci,co,g,0.0)); continue
    src,sc,prof=r
    if sc>=MINSC or (co-ci)<=MINDUR:
        final.append((ci,co,src,sc)); continue
    # split at the worst-agreement frame (interior only)
    n=len(prof); m=max(int(0.15*n),8)
    if n<=2*m: final.append((ci,co,src,sc)); continue
    k=int(np.argmin(np.convolve(prof,np.ones(5)/5,'same')[m:n-m]))+m
    cs=ci+k/100.0
    work.insert(0,(cs,co,src+ (cs-ci)))
    work.insert(0,(ci,cs,src))
final.sort()
# merge adjacent segments that are actually continuous
merged=[]
for ci,co,src,sc in final:
    if merged and abs((merged[-1][2]+(merged[-1][1]-merged[-1][0])) - src) < 0.045:
        merged[-1]=(merged[-1][0], co, merged[-1][2], min(merged[-1][3],sc))
    else: merged.append((ci,co,src,sc))
segs=[dict(i=i,cut_in=round(a,4),cut_out=round(b,4),dur=round(b-a,4),
           src_in=round(s,4),src_out=round(s+(b-a),4),score=round(q,3))
      for i,(a,b,s,q) in enumerate(merged)]
json.dump(segs,open('edl_final.json','w'),indent=1)
q=np.array([x['score'] for x in segs])
print(f'iters {it}  segments {len(segs)}  total {sum(x["dur"] for x in segs):.3f}s')
print(f'score: min {q.min():.3f} p10 {np.percentile(q,10):.3f} mean {q.mean():.3f}   segs<0.6: {(q<0.6).sum()}   segs<0.4s: {sum(1 for x in segs if x["dur"]<0.4)}')
tr=[segs[i+1]['src_in']-segs[i]['src_out'] for i in range(len(segs)-1)]
sm=[x for x in tr if 0<=x<2.5]
print(f'pause trims {len(sm)} removing {sum(sm):.2f}s median {np.median(sm):.3f}s   backwards/odd {sum(1 for x in tr if x<0)}   take jumps {sum(1 for x in tr if x>=2.5)}')
