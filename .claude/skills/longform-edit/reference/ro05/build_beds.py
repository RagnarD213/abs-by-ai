"""Music bed (Pixabay 'Organic Flow', looped with 3 s crossfades) + synthesised SFX track, both on the delivered timeline."""
import json,subprocess,numpy as np,wave,sys
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import sfxlib as S
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg";SR=48000;FPS=30000/1001
TL=json.load(open('timeline.json'));PLAN=json.load(open('gfx-plan.json'))
TOTAL=TL['pieces'][-1]['out_f1']+round(4.0*FPS);N=round(TOTAL/FPS*SR)
def wav(p,x):
    x=np.clip(x,-1,1);w=wave.open(p,'w');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((np.repeat(x[:,None],2,1) if x.ndim==1 else x).astype(np.float32).__mul__(32767).astype('<i2').tobytes());w.close()
b=subprocess.run([FF,'-nostdin','-v','error','-i','/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3','-ac','2','-ar','48000','-f','f32le','-'],capture_output=True).stdout
m=np.frombuffer(b,np.float32).reshape(-1,2);xf=3*SR;L=len(m)
bed=np.zeros((N,2),np.float32);pos=0;ramp=np.linspace(0,1,xf)[:,None]
while pos<N:
    seg=m.copy()
    if pos>0:seg[:xf]*=ramp
    seg[-xf:]*=ramp[::-1]
    e=min(N,pos+L);bed[pos:e]+=seg[:e-pos];pos+=L-xf
# dynamic bed: swell +8 dB where nobody talks (sped-up action, end card), 0.5 s ramps; ducked under speech by the chain
env=np.ones(N,np.float32);up=10**(8/20)
spans=[(p['out_f0']/FPS,p['out_f1']/FPS) for p in TL['pieces'] if p['speed']!=1]+[(TL['pieces'][-1]['out_f1']/FPS,N/SR)]
for a,b in spans:
    i,j=int((a+0.15)*SR),int((b-0.15)*SR);r=int(0.5*SR)
    if j-i<2*r:continue
    env[i:j]=np.maximum(env[i:j],up)
    env[i:i+r]=np.maximum(env[i:i+r]*0+1,np.linspace(1,up,r));env[j-r:j]=np.linspace(up,1,r)
bed*=env[:,None]
fo=int(1.2*SR);bed[-fo:]*=np.linspace(1,0.25,fo)[:,None]
wav('audio/bed.wav',bed)
sfx=np.zeros(N,np.float32)
def put(t,y,g):
    i=int(max(0,t)*SR);e=min(N,i+len(y));sfx[i:e]+=y[:e-i]*g
for g in PLAN['graphics']:
    k=g['kind']
    if k=='title':put(g['a']-0.10,S.riser(0.6),0.22);put(g['a']+0.1,S.whoosh(0.42),0.30)
    elif k in('ingredient','number','keypoint','lower','solid','left-list'):put(g['a']-0.05,S.whoosh(0.30,f0=600,f1=3000),0.16)
    elif k=='speed':put(g['a']-0.08,S.whoosh(0.35,f0=300,f1=2400),0.14)
for c in PLAN['cutaways']:
    if c['key'].startswith('b-'):put(c['a']-0.10,S.whoosh(0.32,f0=500,f1=3400),0.10)
wav('audio/sfx.wav',sfx)
print('bed+sfx',N/SR,'s; peak sfx',round(float(np.abs(sfx).max()),3))
