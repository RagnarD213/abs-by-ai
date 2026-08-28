#!/usr/bin/env python3
"""Snap every voice-EDL boundary into an inter-word gap of HIS transcript,
choosing each word's side by xcorr. Adds the C1633-take1 line correction.
Output: edl_final.json"""
import json, wave, numpy as np, re

BASE='/Volumes/Extreme/_edit_work/abwheel'
SR=16000

def rd(p):
    w=wave.open(p); d=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768; w.close(); return d
def bp(x):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<300)|(f>3400)]=0
    return np.fft.irfft(X,len(x)).astype(np.float32)

cut=bp(rd(f'{BASE}/mrepro/cut16k.wav'))
rolls={r: bp(rd(f'{BASE}/{r}.wav')) for r in ['C1630','C1631','C1632','C1633']}

def words(p):
    d=json.load(open(p)); out=[]
    for s in d['segments']:
        for w in s.get('words',[]):
            t=re.sub(r"[^a-z0-9']", '', w['word'].lower()).replace("'","")
            if t: out.append((t, float(w['start']), float(w['end'])))
    return out
CW=words(f'{BASE}/ref_muhammad/m.whisper.json')

segs=[s for s in json.load(open(f'{BASE}/mrepro/edl_voice3.json')) if s['kind']=='voice']
# MANUAL FIXES (all xcorr-verified this session):
# 1. cut 276.96-279.41 = C1633 take-1 line "lets talk about what it looks like live"
#    (off -273.17, corr peak at src 4.13 for cut 277.30; fresh transcript C1633 2.9-6.1)
# 2. cut 290.75-292.00 = C1633 "All right. Let's do it." at 73.58 (off -217.21, corr 0.991)
# 3. the 279.41+ segment (take 2) keeps off -258.01
new=[]
for s in segs:
    if 276.9<=s['cut_in']<292.0:
        continue  # rebuild this region manually
    if s['cut_in']<276.9<s['cut_out']:  # C1632 standing-variation seg: truncate
        s['cut_out']=276.96; s['src_out']=round(276.96+s['off1'],3)
    new.append(s)
segs=new
segs.append({'roll':'C1633','cut_in':276.96,'cut_out':279.41,'off0':-273.17,'off1':-273.17,
             'src_in':round(276.96-273.17,3),'src_out':round(279.41-273.17,3),'kind':'voice'})
segs.append({'roll':'C1633','cut_in':279.41,'cut_out':285.78,'off0':-258.01,'off1':-258.01,
             'src_in':round(279.41-258.01,3),'src_out':round(285.78-258.01,3),'kind':'voice'})
segs.append({'roll':'C1633','cut_in':285.78,'cut_out':290.75,'off0':-246.07,'off1':-246.07,
             'src_in':round(285.78-246.07,3),'src_out':round(290.75-246.07,3),'kind':'voice'})
segs.append({'roll':'C1633','cut_in':290.75,'cut_out':292.00,'off0':-217.21,'off1':-217.21,
             'src_in':round(290.75-217.21,3),'src_out':round(292.00-217.21,3),'kind':'voice'})
segs.sort(key=lambda s:s['cut_in'])

def wscore(w0,w1,roll,off,rad=0.10):
    i0=int((w0-0.04)*SR); i1=int((w1+0.04)*SR)
    win=cut[i0:i1]
    if len(win)<400: return -1
    hay=rolls[roll]
    lo=int((w0-0.04+off-rad)*SR); hi=int((w1+0.04+off+rad)*SR)
    if lo<0 or hi>len(hay): return -1
    seg=hay[lo:hi]
    wz=win-win.mean(); wn=np.sqrt((wz**2).sum())+1e-9
    best=-1
    for st in range(0,len(seg)-len(win),24):
        h=seg[st:st+len(win)]; hz=h-h.mean()
        c=float((wz*hz).sum()/(wn*(np.sqrt((hz**2).sum())+1e-9)))
        if c>best: best=c
    return best

report=[]
for i in range(1,len(segs)):
    A,B=segs[i-1],segs[i]
    t=B['cut_in']
    if B['cut_in']-A['cut_out']>0.5: continue  # not adjacent (music gap) — never stretch across
    if t-A['cut_in']<0.2 or B['cut_out']-t<0.2: continue
    if A['roll']==B['roll'] and abs(A['off1']-B['off0'])<0.05: continue
    cand=[w for w in CW if t-1.0<w[1]<t+1.0]
    if not cand: continue
    sides=[]
    for (w,w0,w1) in cand:
        sa=wscore(w0,w1,A['roll'],A['off1'])
        sb=wscore(w0,w1,B['roll'],B['off0'])
        sides.append((w,w0,w1,sa,sb,'A' if sa>=sb else 'B'))
    # find split: last A-word before first B-word (require monotone-ish)
    lastA=None; firstB=None
    for s_ in sides:
        if s_[5]=='A': lastA=s_
    for s_ in sides:
        if s_[5]=='B': firstB=s_; break
    if lastA and firstB and lastA[2]<=firstB[1]:
        nb=round((lastA[2]+firstB[1])/2,3)
    elif firstB and (not lastA):
        nb=round(firstB[1]-0.06,3)
    elif lastA and (not firstB):
        nb=round(lastA[2]+0.06,3)
    else:
        report.append((t,'CONFLICT',sides)); continue
    if abs(nb-t)>0.02:
        report.append((t,f'-> {nb}',[(x[0],x[5],round(x[3],2),round(x[4],2)) for x in sides]))
    A['cut_out']=nb; B['cut_in']=nb
    A['src_out']=round(nb+A['off1'],3); B['src_in']=round(nb+B['off0'],3)

for r in report:
    print(r[0],r[1])
    for x in r[2]: print('   ',x)

# reassemble: music windows are the gaps between voice segs, source-continuous with
# their neighbours, timelapsed (speed = src span / cut span, all measure ~3x)
allsegs=sorted(segs,key=lambda s:s['cut_in'])
out=[]
gaps=[]
for i in range(1,len(allsegs)):
    a,b=allsegs[i-1],allsegs[i]
    if b['cut_in']-a['cut_out']>1.0:
        gaps.append((a,b))
for (a,b) in gaps:
    m0,m1=a['cut_out'],b['cut_in']
    # window 3 has an internal hard cut at ~379.03 to src ~445.6
    if 363<m0<365:
        cutp=379.03
        srcA_out=279.13
        spA=(srcA_out-a['src_out'])/(cutp-m0)
        out.append({'kind':'set','roll':'C1633','cut_in':m0,'cut_out':cutp,
                    'src_in':a['src_out'],'src_out':srcA_out,'speed':round(spA,4)})
        spB=(b['src_in']-445.55)/(m1-cutp)
        out.append({'kind':'set','roll':'C1633','cut_in':cutp,'cut_out':m1,
                    'src_in':445.55,'src_out':b['src_in'],'speed':round(spB,4)})
    else:
        sp=(b['src_in']-a['src_out'])/(m1-m0)
        out.append({'kind':'set','roll':a['roll'],'cut_in':m0,'cut_out':m1,
                    'src_in':a['src_out'],'src_out':b['src_in'],'speed':round(sp,4)})
for s in allsegs:
    s['speed']=1.0
full=sorted(allsegs+out,key=lambda s:s['cut_in'])
print("\nFINAL EDL:")
for s in full:
    print(f"{s['cut_in']:8.3f} {s['cut_out']:8.3f}  {s['roll']}  {s['src_in']:8.3f}-{s.get('src_out',0):8.3f}  x{s['speed']}  {s['kind']}")
json.dump(full,open(f'{BASE}/mrepro/edl_final.json','w'),indent=1)
