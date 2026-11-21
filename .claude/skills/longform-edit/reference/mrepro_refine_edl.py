#!/usr/bin/env python3
"""Refine the recovered EDL by direct audio xcorr of his mix vs raw rolls.
Per-1s window offset tracking; segments = runs of constant (roll, offset)."""
import json, wave, numpy as np

BASE='/Volumes/Extreme/_edit_work/abwheel'
SR=16000

def rd(p):
    w=wave.open(p); d=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768; w.close(); return d

def bp(x):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR)
    X[(f<300)|(f>3400)]=0
    return np.fft.irfft(X,len(x)).astype(np.float32)

cut=bp(rd(f'{BASE}/mrepro/cut16k.wav'))
rolls={r: bp(rd(f'{BASE}/{r}.wav')) for r in ['C1630','C1631','C1632','C1633']}
segs=json.load(open(f'{BASE}/mrepro/edl_voice_raw.json'))

def xcorr_best(win, hay):
    """normalized cross-correlation of win against hay; returns (best_idx, score)."""
    n=len(win); m=len(hay)
    if m<n: return None,0
    wz=win-win.mean(); wnorm=np.sqrt((wz**2).sum())+1e-9
    # FFT correlate
    L=1
    while L<m+n: L*=2
    C=np.fft.irfft(np.fft.rfft(hay,L)*np.conj(np.fft.rfft(wz,L)),L)[:m-n+1]
    # local energy of hay windows
    cs=np.cumsum(np.concatenate([[0],hay**2]))
    en=np.sqrt(cs[n:]-cs[:-n])+1e-9
    score=C/(en*wnorm)
    i=int(np.argmax(score))
    return i, float(score[i])

def expected(t):
    """nearest word-recovery segment for cut time t -> (roll, offset)."""
    best=None; bd=1e9
    for s in segs:
        if s['cut_in']-2<=t<=s['cut_out']+2: return s['roll'], s['offset'], 4.0
        d=min(abs(t-s['cut_in']),abs(t-s['cut_out']))
        if d<bd: bd=d; best=s
    return best['roll'], best['offset'], min(20.0, 4.0+bd*2)

track=[]
t=0.25
while t < 417.8:
    i0=int(t*SR); win=cut[i0:i0+SR]
    if len(win)<SR: break
    if t<23.0:
        # hook: search all of C1630
        roll='C1630'; hay=rolls[roll]; base=0
        idx,sc=xcorr_best(win,hay)
        off=(idx/SR)-t if idx is not None else None
    else:
        roll,off0,rad=expected(t)
        hay=rolls[roll]
        lo=max(0,int((t+off0-rad)*SR)); hi=min(len(hay),int((t+off0+rad)*SR)+SR)
        idx,sc=xcorr_best(win,hay[lo:hi])
        off=((lo+idx)/SR)-t if idx is not None else None
    track.append((round(t,2),roll,round(off,3) if off is not None else None,round(sc,3)))
    t+=0.5
json.dump(track,open(f'{BASE}/mrepro/offset_track.json','w'))
# report: runs
prev=None
for (t,roll,off,sc) in track:
    tag='' if sc>=0.30 else '  LOW'
    if prev is None or roll!=prev[0] or off is None or prev[1] is None or abs(off-prev[1])>0.04:
        print(f"t={t:7.2f}  {roll}  off={off}  corr={sc}{tag}")
    prev=(roll,off)
