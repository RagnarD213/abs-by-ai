"""Measured graphic placement: never over Dan's face or hair; least overlap with his body/hands. Writes placement.json."""
import json,sys,os,subprocess,numpy as np
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared");sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/06-organic-r4")
from deliver.checks import framing as F
import ro05_gfx as G
from PIL import Image
FF="bin/ffmpeg";FPS=30000/1001;M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
PM="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask"
TL=json.load(open('timeline.json'))['pieces'];FR=json.load(open('framing.json'));PL=json.load(open('gfx-plan.json'))
GPD="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/gopro 2/"
def gp_file(t):
    if t<1060.501333:return GPD+'GH010270.MP4',t
    if t<2121.002666:return GPD+'GH020270.MP4',t-1060.501333
    return GPD+'GH030270.MP4',t-2121.002666
def grab(t,out):
    c=next((c for c in PL['cutaways'] if c['a']<=t<c['b']),None)
    if c:
        if c['source'] in('PHONE',):return None
        ss=c['ss']+(t-c['a'])*c.get('speed',1)
        if c['source']=='GP':f,o=gp_file(ss);vf='crop=1280:720:320:0,scale=1920:1080'
        else:f,o=M+c['source']+'.MP4',ss;vf='scale=1920:1080'
    else:
        i=next(k for k,p in enumerate(TL) if p['out_f0']/FPS<=t<p['out_f1']/FPS);p=TL[i]
        if p['source']=='C1541':return None
        o=p['src_in']+(t-p['out_f0']/FPS)*p['speed'];f=M+p['source']+'.MP4';cr=FR[i]['crop']
        vf=(f"crop={cr[2]}:{cr[3]}:{cr[0]}:{cr[1]}," if cr else '')+'scale=1920:1080'
    subprocess.run([FF,'-nostdin','-v','error','-y','-ss',f'{o:.3f}','-i',f,'-frames:v','1','-vf',vf,out]);return out
POS_TALK=['bottom','tl','tr','bl','br'];POS_BUILD=['tl','tr','bl','br']
def layers(g,pos,top_y=56):
    k=g['kind']
    if k=='keypoint':return G.lower(g['text'],pos=pos,keypoint=True,top_y=top_y)[1]
    if k=='lower':return G.lower(g['text'],pos=pos,top_y=top_y)[1]
    if k=='number':return G.lower(g['text'],pos=pos,tab=g['num'],top_y=top_y)[1]
    if k=='solid':return G.solid(g['text'],pos=pos,top_y=top_y)[1]
    if k=='ingredient':return G.ingredient(g['num'],g['text'],g.get('sub'),pos=pos,top_y=top_y)[1]
def bbox(ls):
    b=[l['image'].getbbox() for l in ls];return (min(x[0] for x in b),min(x[1] for x in b),max(x[2] for x in b),max(x[3] for x in b))
os.makedirs('place',exist_ok=True);fm,fd=F._facemesh(),F._facefinder()
todo=[g for g in PL['graphics'] if g['kind'] in('keypoint','lower','number','solid','ingredient') and g.get('pos')!='right']
frames=[]
for g in todo:
    for k,fr in enumerate((0.05,0.25,0.5,0.75,0.95)):
        t=g['a']+fr*(g['b']-g['a']);fn=f"place/{g['key']}_{k}.png"
        if grab(t,fn):frames.append((g['key'],fn))
subprocess.run([PM,'place/m']+[f for _,f in frames],capture_output=True)
FACE={};BODY={}
for key,fn in frames:
    im=np.asarray(Image.open(fn).convert('RGB'));P=F._find_face(fm,fd,im,1920,1080)
    if P is not None:
        xs=[p[0] for p in (P.values() if isinstance(P,dict) else P)];fore,chin=P[10][1],P[152][1];fh=chin-fore;fw=max(xs)-min(xs)
        FACE.setdefault(key,[]).append((min(xs)-0.25*fw-60,fore-0.9*fh-60,max(xs)+0.25*fw+60,chin+0.15*fh+40))
    mp='place/m/'+os.path.basename(fn)[:-4]+'.mask.png'
    if os.path.exists(mp):BODY.setdefault(key,[]).append(np.asarray(Image.open(mp).convert('L').resize((1920,1080)))>127)
out={}
FORCE={}
DISALLOW={'k-chop-late':{'bl','bottom'},'k-measure':{'tl','tr'}}   # auditor: off the tomato box / oil bottle held low
speed_on=lambda g:any(s['kind']=='speed' and s['a']<g['b'] and s['b']>g['a'] for s in PL['graphics'])
for g in todo:
    build=g['a']>150 and g['kind']!='solid' and not g['key'].startswith('l-sub')
    best=None
    if g['key'] in FORCE:
        out[g['key']]=dict(pos=FORCE[g['key']],top_y=56,body=None,face_hit=False,forced=True);continue
    for rank,pos in enumerate([q for q in (POS_BUILD if build else POS_TALK) if q not in DISALLOW.get(g['key'],set())]):
        ty=150 if (pos=='tr' and speed_on(g)) else 56
        x0,y0,x1,y1=bbox(layers(g,pos,ty));area=(x1-x0)*(y1-y0)
        face=sum(max(0,min(x1,f[2])-max(x0,f[0]))*max(0,min(y1,f[3])-max(y0,f[1])) for f in FACE.get(g['key'],[]))
        body=max([m[int(max(0,y0)):int(y1),int(max(0,x0)):int(x1)].mean() for m in BODY.get(g['key'],[])] or [0])
        cost=(1e6 if face>0 else 0)+body*100+rank*4
        if best is None or cost<best[0]:best=(cost,pos,ty,round(float(body),3),face>0)
    out[g['key']]=dict(pos=best[1],top_y=best[2],body=best[3],face_hit=best[4])
json.dump(out,open('placement.json','w'),indent=0)
bad=[k for k,v in out.items() if v['face_hit']];print(len(out),'placed; unavoidable face overlaps:',bad)
import collections;print(collections.Counter(v['pos'] for v in out.values()))
