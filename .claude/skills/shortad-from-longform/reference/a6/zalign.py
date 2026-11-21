#!/usr/bin/env python3
"""Word-align Zeeshan's cut (ref.whisper.json) against the raw roll C1591 (raw.whisper.json, fresh 2026-09-10).
Apostrophes normalised away on BOTH sides (skill Step 1a). Writes wordpairs.json and prints the constant-offset runs."""
import json, re, numpy as np
def words(p):
    out=[]
    for s in json.load(open(p))['segments']:
        for w in s.get('words',[]):
            t=re.sub(r"[^a-z0-9]", '', w['word'].lower())
            if t: out.append((t, float(w['start']), float(w['end'])))
    return out
RAW=words('raw.whisper.json'); CUT=words('ref.whisper.json')
print('raw words', len(RAW), 'cut words', len(CUT))
n,m=len(CUT),len(RAW); MATCH,MIS,GAPR,GAPC=2.0,-2.0,-0.02,-3.0
prev=np.zeros(m+1); ptr=np.zeros((n+1,m+1),np.int8); ptr[0,:]=1
rw=np.array([w for w,_,_ in RAW])
for i in range(1,n+1):
    cur=np.full(m+1,-1e18); cur[0]=prev[0]+GAPC; ptr[i,0]=2
    sc=np.where(rw==CUT[i-1][0],MATCH,MIS)
    diag=prev[:-1]+sc; up=prev[1:]+GAPC
    # left-gap recurrence needs a scan
    for j in range(1,m+1):
        d=diag[j-1]; l=cur[j-1]+GAPR; u=up[j-1]
        if d>=l and d>=u: cur[j]=d; ptr[i,j]=0
        elif l>=u: cur[j]=l; ptr[i,j]=1
        else: cur[j]=u; ptr[i,j]=2
    prev=cur
j=int(np.argmax(prev)); i=n; pairs=[]
while i>0:
    p=ptr[i,j]
    if p==0:
        if RAW[j-1][0]==CUT[i-1][0]: pairs.append((CUT[i-1][1],CUT[i-1][2],RAW[j-1][1],RAW[j-1][2],CUT[i-1][0]))
        i-=1; j-=1
    elif p==1: j-=1
    else: i-=1
pairs.reverse()
print('matched', len(pairs), f'({100*len(pairs)/n:.1f}% of cut)')
json.dump(pairs, open('wordpairs.json','w'))
offs=[(c0,r0-c0,w) for c0,c1,r0,r1,w in pairs]
runs=[]; cur=[offs[0]]
for x in offs[1:]:
    if abs(x[1]-cur[-1][1])<0.16: cur.append(x)
    else: runs.append(cur); cur=[x]
runs.append(cur)
print('  cut_start cut_end   offset  src_start  nwords  first..last')
for r in runs:
    o=float(np.median([x[1] for x in r]))
    print(f'  {r[0][0]:8.2f} {r[-1][0]:8.2f} {o:+8.2f} {r[0][0]+o:8.2f}  {len(r):3d}  {r[0][2]} .. {r[-1][2]}')
print('runs', len(runs))
