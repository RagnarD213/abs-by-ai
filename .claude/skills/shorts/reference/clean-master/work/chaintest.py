#!/usr/bin/env python3
"""Test candidate voice chains against Muhammad's ad on the things Dan can hear.

Three measures, all on the SAME source passage:
  FLOOR  - the spectrum in true silence. Ours sits 6-8 dB above his through the vocal band and
           that is the "weird under sound".
  SPEECH - the octave shape, which the rev-3 chain already matched well. Must not regress.
  TAIL   - how long the room rings after a word. Rev 3 doubled it (65 -> 120 ms).
"""
import subprocess
import numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
PROJ="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OURS=f"{PROJ}/claude edited long form content/03 - The Supplements I Actually Take/CUT_v1_graded_NO-GRAPHICS.mp4"
MUH=f"{PROJ}/Muhammad Ad Videos/Daniel HQ Fitness AD Video v3 HD.mp4"
BANDS=[(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,9000),(9000,14000)]

def load(f,af,t,d):
    p=subprocess.run([FF,'-v','error','-ss',str(t),'-i',f,'-t',str(d),'-vn','-af',af,
                      '-ac','1','-ar','48000','-f','s16le','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.int16).astype(np.float64)/32768.
def metrics(x):
    hop=240; n=len(x)//hop
    e=20*np.log10(np.maximum(1e-9,np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))))
    thr=np.percentile(e,50)-12; q=e<thr
    runs=[];i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)*0.005>=0.30: runs.append((i,j))
            i=j
        else: i+=1
    N=2048
    sil=np.concatenate([x[a*hop:b*hop] for a,b in sorted(runs,key=lambda r:-(r[1]-r[0]))[:14]]) if runs else x[:N*2]
    m=(len(sil)-N)//N
    Sn=(np.abs(np.fft.rfft(sil[:max(1,m)*N].reshape(max(1,m),N)*np.hanning(N),axis=1))**2).mean(0)
    idx=np.arange(960)[None,:]+(np.arange((len(x)-960)//480)*480)[:,None]
    fr=x[idx]; rms=np.sqrt((fr**2).mean(1))
    loud=fr[rms>np.percentile(rms,80)]
    Ss=(np.abs(np.fft.rfft(loud*np.hanning(960),axis=1))**2).mean(0)
    fn=np.fft.rfftfreq(N,1/48000); fs=np.fft.rfftfreq(960,1/48000)
    nb=lambda a,b:10*np.log10(max(1e-14,Sn[(fn>=a)&(fn<b)].mean()))
    prof=np.array([10*np.log10(max(1e-14,Ss[(fs>=a)&(fs<b)].mean())) for a,b in BANDS])
    dec=[]
    for a,_ in runs:
        if a<8: continue
        w=e[a-4:a+50]
        if len(w)<54: continue
        pk=w[:4].max(); tail=w[6:50]
        bl=np.where(tail<pk-20)[0]
        if len(bl): dec.append(bl[0]*0.005)
    return np.array([nb(80,250),nb(250,1000),nb(1000,4000),nb(4000,16000)]), prof, (np.median(dec)*1000 if dec else float('nan'))

mf,mp,mt = metrics(load(MUH,'anull',5,220))
mp = mp-mp.max()
print(f"MUHAMMAD ad: floor 80-250 {mf[0]:.1f} | 250-1k {mf[1]:.1f} | 1-4k {mf[2]:.1f} | 4-16k {mf[3]:.1f}   tail {mt:.0f} ms")

AIR="equalizer=f=1800:width_type=o:width=1.2:g=-2.0,equalizer=f=3500:width_type=o:width=1.2:g=3.0,highshelf=f=6000:g=7.5,equalizer=f=11000:width_type=o:width=1.0:g=4.0,deesser=i=0.40"
HP="pan=mono|c0=c1,highpass=f=75:p=2"
# Our TRUE-silence level measures -47.5 dBFS, so afftdn's nf estimate should sit near there,
# not at the -38..-42 the earlier sweeps guessed. A gentle gate on top, with a release long
# enough to leave the room's own 65ms decay intact.
G="agate=threshold=0.022:ratio=3:range=0.30:attack=8:release=220:knee=8"
CANDS={
 'rev 3 (shipped)': open('work/voicechain.txt').read().strip(),
 'S nf-47 nr25 + soft gate': f"{HP},afftdn=nr=25:nf=-47:tn=1,{G},{AIR}",
 'T nf-47 nr35 + soft gate': f"{HP},afftdn=nr=35:nf=-47:tn=1,{G},{AIR}",
 'U nf-50 nr40 + soft gate': f"{HP},afftdn=nr=40:nf=-50:tn=1,{G},{AIR}",
 'V nf-47 nr35, NO gate':    f"{HP},afftdn=nr=35:nf=-47:tn=1,{AIR}",
 'W nf-47 nr35 + gate rel180':f"{HP},afftdn=nr=35:nf=-47:tn=1,agate=threshold=0.026:ratio=4:range=0.22:attack=8:release=180:knee=8,{AIR}",
}
print(f"\n{'chain':30s} {'80-250':>7s} {'250-1k':>7s} {'1-4k':>7s} {'4-16k':>7s} {'tail':>6s} {'speech vs his':>14s}")
for lab,af in CANDS.items():
    x=np.concatenate([load(OURS,af,t,60) for t in (300,1000)])
    fl,pr,tl=metrics(x); pr=pr-pr.max()
    d=mp-pr; d=d-d.mean()
    print(f"{lab:30s} {fl[0]:7.1f} {fl[1]:7.1f} {fl[2]:7.1f} {fl[3]:7.1f} {tl:5.0f}ms {float(np.sqrt((d**2).mean())):13.2f}")
print(f"{'TARGET (Muhammad)':30s} {mf[0]:7.1f} {mf[1]:7.1f} {mf[2]:7.1f} {mf[3]:7.1f} {mt:5.0f}ms {0.0:13.2f}")
