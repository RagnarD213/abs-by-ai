"""RO-05 output timeline: EDL ranges -> frame-exact pieces (speed-split), word map."""
import json,importlib.util
FPS=30000/1001
spec=importlib.util.spec_from_file_location('r','ranges.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
E=json.load(open('edl.json'))['ranges']
M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
pieces=[]
for r in E:
    b=r['beat'];a,z=max(0.0,r['start']),r['end']
    if b in m.TAILSPEED:
        t0,f=m.TAILSPEED[b];parts=[(a,t0,1,b),(t0,z,f,b+'~tl')]
    else:parts=[(a,z,m.SPEED.get(b,1),b)]
    for (x,y,sp,bb) in parts:pieces.append(dict(source=r['source'],src_in=x,src_out=y,speed=sp,beat=bb,range_beat=b))
t=0.0
for p in pieces:
    d=(p['src_out']-p['src_in'])/p['speed']
    f0=round(t*FPS);t+=d;f1=round(t*FPS)
    p['out_f0']=f0;p['out_f1']=f1;p['frames']=f1-f0
    p['src_dur']=p['frames']/FPS*p['speed']   # exact source span consumed by the picture
words=[]
for i,p in enumerate(pieces):
    if p['speed']!=1:continue
    W=json.load(open(f"{M}{p['source']}.roll/words.json"))['words']
    for w in W:
        mid=(w['start']+w['end'])/2
        if p['src_in']<mid<p['src_in']+p['src_dur']:
            o=p['out_f0']/FPS-p['src_in']
            words.append(dict(w=w['word'].strip(),t0=max(p['out_f0']/FPS,w['start']+o),t1=min(p['out_f1']/FPS,w['end']+o),piece=i,beat=p['beat'],src=p['source'],st=w['start']))
json.dump(dict(fps='30000/1001',total_frames=pieces[-1]['out_f1'],pieces=pieces),open('timeline.json','w'),indent=1)
json.dump(words,open('mapped-words.json','w'),indent=0)
print(len(pieces),'pieces',pieces[-1]['out_f1'],'frames =',round(pieces[-1]['out_f1']/FPS,2),'s',len(words),'words')
