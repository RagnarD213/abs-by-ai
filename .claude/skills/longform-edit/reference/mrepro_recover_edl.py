#!/usr/bin/env python3
"""Recover Muhammad's ab-wheel EDL: align his cut's words against 4 raw rolls,
then segment on (roll, offset) runs. Output: edl_voice.json (speech segments only)."""
import json, re, numpy as np

BASE='/Volumes/Extreme/_edit_work/abwheel'

def words(p):
    d=json.load(open(p)); out=[]
    for s in d['segments']:
        for w in s.get('words',[]):
            t=re.sub(r"[^a-z0-9']", '', w['word'].lower()).replace("'","")
            if t: out.append((t, float(w['start']), float(w['end'])))
    return out

CUT=words(f'{BASE}/ref_muhammad/m.whisper.json')
ROLLS={r: words(f'{BASE}/{r}.whisper.json') for r in ['C1630','C1631','C1632','C1633']}

def align(cut, raw):
    """NW: global-ish in cut (cheap cut-gap so unmatched regions skip), local in raw."""
    n,m=len(cut),len(raw)
    MATCH,MIS,GAPR,GAPC=2.0,-2.0,-0.02,-0.6
    prev=np.zeros(m+1); ptr=np.zeros((n+1,m+1),dtype=np.int8); ptr[0,:]=1
    rawws=[w for w,_,_ in raw]
    for i in range(1,n+1):
        cw=cut[i-1][0]
        sc=np.array([MATCH if rw==cw else MIS for rw in rawws])
        diag=prev[:-1]+sc
        up=prev[1:]+GAPC
        cur=np.empty(m+1); cur[0]=prev[0]+GAPC
        p=np.zeros(m+1,dtype=np.int8); p[0]=2
        for j in range(1,m+1):
            d=diag[j-1]; l=cur[j-1]+GAPR; u=up[j-1]
            if d>=l and d>=u: cur[j]=d; p[j]=0
            elif l>=u: cur[j]=l; p[j]=1
            else: cur[j]=u; p[j]=2
        ptr[i]=p; prev=cur
    j=int(np.argmax(prev)); i=n
    match={}  # cut index -> (raw_t0, raw_t1)
    while i>0 and j>=0:
        p=ptr[i,j]
        if p==0:
            if raw[j-1][0]==cut[i-1][0]:
                match[i-1]=(raw[j-1][1],raw[j-1][2])
            i-=1; j-=1
        elif p==1: j-=1
        else: i-=1
    return match

cands={}
for rname,raw in ROLLS.items():
    m=align(CUT,raw)
    print(rname,'matched',len(m),'of',len(CUT))
    for ci,(r0,r1) in m.items():
        cands.setdefault(ci,[]).append((rname,r0,r1))

# resolve to runs: DP over cut words choosing candidate that continues (roll, offset)
# state = (roll, offset bucket); switch penalty
INF=1e18
seq=[None]*len(CUT)
# greedy with lookahead: walk words; keep current (roll, offset); continue if a candidate fits
def fits(c,roll,off,t):
    return c[0]==roll and abs((c[1]-t)-off)<0.25
i=0; cur=None; out=[]
for i in range(len(CUT)):
    w,t0,t1=CUT[i]
    cl=cands.get(i,[])
    if not cl: seq[i]=None; continue
    if cur and any(fits(c,cur[0],cur[1],t0) for c in cl):
        c=[c for c in cl if fits(c,cur[0],cur[1],t0)][0]
        cur=(c[0], c[1]-t0)
        seq[i]=(c[0],c[1],c[2])
    else:
        # score each candidate by how many of next 8 words continue it
        best=None;bests=-1
        for c in cl:
            roll,off=c[0],c[1]-t0
            s=0
            for k in range(i+1,min(i+9,len(CUT))):
                if any(fits(cc,roll,off,CUT[k][1]) for cc in cands.get(k,[])): s+=1
            if s>bests: bests=s; best=c
        cur=(best[0],best[1]-t0)
        seq[i]=(best[0],best[1],best[2])

# build segments: runs of same roll + slowly-varying offset
segs=[]
curseg=None
for i,(entry) in enumerate(seq):
    w,ct0,ct1=CUT[i]
    if entry is None: continue
    roll,r0,r1=entry
    off=r0-ct0
    if curseg and curseg['roll']==roll and abs(off-curseg['off_last'])<0.25:
        curseg['cut_out']=ct1; curseg['src_out']=r1; curseg['off_last']=off
        curseg['nw']+=1
    else:
        if curseg: segs.append(curseg)
        curseg={'roll':roll,'cut_in':ct0,'cut_out':ct1,'src_in':r0,'src_out':r1,
                'off_last':off,'nw':1}
segs.append(curseg)
print('\nsegments:',len(segs))
unmatched=[i for i in range(len(CUT)) if seq[i] is None]
print('unmatched words:',len(unmatched), [CUT[i][0] for i in unmatched][:30])
for s in segs:
    s['offset']=round(s['src_in']-s['cut_in'],3)
    print("cut %7.2f-%7.2f  %s %8.2f-%8.2f  off %8.2f  nw %d"%(
        s['cut_in'],s['cut_out'],s['roll'],s['src_in'],s['src_out'],s['offset'],s['nw']))
json.dump(segs,open(f'{BASE}/mrepro/edl_voice_raw.json','w'),indent=1)
