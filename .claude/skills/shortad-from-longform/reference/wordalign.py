import json, re, numpy as np

def words(p):
    d=json.load(open(p)); out=[]
    for s in d['segments']:
        for w in s.get('words',[]):
            t=re.sub(r"[^a-z0-9']", '', w['word'].lower())
            if t: out.append((t, float(w['start']), float(w['end'])))
    return out

RAW = words('/Volumes/Extreme/_edit_work/ad1-8-14/C1591.whisper.json')
CUT = words('m.whisper.json')
print('raw words', len(RAW), 'cut words', len(CUT))

# Needleman-Wunsch, monotonic, cut fully consumed (global in CUT, local in RAW)
n, m = len(CUT), len(RAW)
MATCH, MIS, GAPR, GAPC = 2.0, -2.0, -0.02, -3.0   # skipping raw words is cheap (unused takes)
prev = np.full(m+1, 0.0)     # free start in RAW
ptr = np.zeros((n+1, m+1), dtype=np.int8)
ptr[0,:] = 1                  # came from left (raw gap)
for i in range(1, n+1):
    cur = np.full(m+1, -1e18)
    cur[0] = prev[0] + GAPC
    ptr[i,0] = 2
    cw = CUT[i-1][0]
    sc = np.fromiter((MATCH if RAW[j][0]==cw else MIS for j in range(m)), dtype=np.float64, count=m)
    for j in range(1, m+1):
        diag = prev[j-1] + sc[j-1]
        left = cur[j-1] + GAPR
        up   = prev[j] + GAPC
        if diag >= left and diag >= up: cur[j]=diag; ptr[i,j]=0
        elif left >= up:                cur[j]=left; ptr[i,j]=1
        else:                           cur[j]=up;   ptr[i,j]=2
    prev = cur
j = int(np.argmax(prev)); i = n
pairs=[]
while i>0:
    p = ptr[i,j]
    if p==0:
        if RAW[j-1][0]==CUT[i-1][0]:
            pairs.append((CUT[i-1][1], CUT[i-1][2], RAW[j-1][1], RAW[j-1][2], CUT[i-1][0]))
        i-=1; j-=1
    elif p==1: j-=1
    else: i-=1
pairs.reverse()
print('matched words', len(pairs), f'({100*len(pairs)/n:.1f}% of cut)')
json.dump(pairs, open('wordpairs.json','w'))

# derive runs of constant offset
offs=[(c0, r0-c0) for c0,c1,r0,r1,w in pairs]
runs=[]; cur=[offs[0]]
for t,o in offs[1:]:
    if abs(o-cur[-1][1])<0.16: cur.append((t,o))
    else: runs.append(cur); cur=[(t,o)]
runs.append(cur)
runs=[r for r in runs if len(r)>=2]
print('\n  cut_start  cut_end   offset   src_start  src_end   nwords')
tot=0
for r in runs:
    o=float(np.median([x[1] for x in r]))
    print(f'  {r[0][0]:8.2f} {r[-1][0]:8.2f}  {o:+8.2f}   {r[0][0]+o:8.2f} {r[-1][0]+o:8.2f}   {len(r)}')
    tot+=len(r)
print('runs',len(runs),'words in runs',tot)
