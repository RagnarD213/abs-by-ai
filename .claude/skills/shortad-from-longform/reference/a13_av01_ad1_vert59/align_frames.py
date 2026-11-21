import subprocess, numpy as np, sys, json
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def prof(path, n, size=64):
    raw = subprocess.run([FF,'-nostdin','-v','error','-i',path,'-vf',
        f'scale={size}:{size},format=gray','-fps_mode','passthrough','-f','rawvideo','-'],
        capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, size*size).astype(np.float32)
    print(path, 'frames', a.shape[0], file=sys.stderr)
    d = np.abs(np.diff(a, axis=0)).mean(axis=1)
    return a, d
SQ="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs | claude | 1x1 | ad 1.mp4"
av, dv = prof('picture.mp4', 6977)
aq, dq = prof(SQ, 6976)
np.save('proof/dv.npy', dv); np.save('proof/dq.npy', dq)
# where does the +1 appear? test hypothesis: identity for first k, then vertical shifted by 1
n = min(len(dv), len(dq))
best=[]
for lag in (0,1,-1):
    x = dv[max(0,lag):]; y = dq[max(0,-lag):]
    m = min(len(x), len(y))
    best.append((lag, float(np.corrcoef(x[:m], y[:m])[0,1])))
print('global corr by lag:', best)
# sliding: for each 200-frame window, which lag correlates best
rows=[]
for s in range(0, 6800, 200):
    e=s+200
    r={}
    for lag in (0,1,-1,2,-2):
        x = dv[s+max(0,lag):e+max(0,lag)]; y = dq[s+max(0,-lag):e+max(0,-lag)]
        m=min(len(x),len(y))
        if m<50: continue
        r[lag]=float(np.corrcoef(x[:m],y[:m])[0,1])
    bl=max(r,key=r.get)
    rows.append((s, bl, round(r[bl],4), round(r.get(0,float('nan')),4)))
for r in rows: print(r)
