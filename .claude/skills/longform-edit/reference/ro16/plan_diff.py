import json
FPS=30000/1001
def fr(t): return int(round(t*FPS))
W="/Volumes/Extreme/_edit_work/ro16"
a=json.load(open(W+'/round3-plan/before/plan_resolved.json')); b=json.load(open(W+'/plan_resolved.json'))
def exp(f): return 0 if f<=8979 else (-30 if f<20982 else -13)
bad=0; rep=[]
assert [x['id'] for x in a]==[x['id'] for x in b]
for x,y in zip(a,b):
    kx={k:v for k,v in x.items() if k not in('t0','t1','reveal_t')}; ky={k:v for k,v in y.items() if k not in('t0','t1','reveal_t')}
    if kx!=ky: bad+=1; print('FIELDS',x['id'])
    for k in('t0','t1'):
        if x[k] is None:
            if y[k] is not None: bad+=1; print('NONE',x['id'])
            continue
        d=fr(y[k])-fr(x[k])
        if d!=exp(fr(x[k])): bad+=1; print('SHIFT',x['id'],k,x[k],y[k],d)
    for u,v in zip(x.get('reveal_t',[]),y.get('reveal_t',[])):
        if fr(v)-fr(u)!=exp(fr(u)): bad+=1; print('REVEAL',x['id'],u,v)
    rep.append(dict(id=x['id'],kind=x['kind'],r2=[x['t0'],x['t1']],r3=[y['t0'],y['t1']],shift_frames=fr(y['t0'])-fr(x['t0'])))
sa=json.load(open(W+'/round3-plan/before/shots.json')); sb=json.load(open(W+'/shots.json'))
sd=[(x['id'],x['src_f0'],x['src_f1'],y['src_f0'],y['src_f1']) for x,y in zip(sa,sb) if (x['src_f0'],x['src_f1'],x['framing'])!=(y['src_f0'],y['src_f1'],y['framing'])]
print('items',len(a),'findings',bad,'| shots',len(sa),len(sb),'changed:',sd,'framing same:',[x['framing'] for x in sa]==[y['framing'] for y in sb])
json.dump(dict(items=rep,findings=bad,shots_changed=sd,frames=[sa[-1]['out_f1'],sb[-1]['out_f1']]),open(W+'/round3/plan_diff.json','w'),indent=1)
for x in rep:
    if x['r2'][1] and (x['r2'][0]<=300.6<=x['r2'][1] or x['r2'][0]<=700.1<=x['r2'][1]): print('spans a join:',x)
