#!/usr/bin/env python3
"""HIS time map for the app-demo card (6717-6954: the recording 09_CLIP played inside a phone on his olive card) and his
meal-plan scroll (5422-5635: 12_APP_meal-plan.png in a phone beside him). NCC of his panel against the recording's
frames / the png's rows. Writes media_map.json."""
import json, subprocess, numpy as np, cv2
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
LIB="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD"
APP=f"{LIB}/09_CLIP_app-generate-future-self.mp4"; PNG=f"{LIB}/12_APP_meal-plan.png"
def frames(src,w,h,fps=None):
    vf=([f'fps={fps}'] if fps else [])+[f'scale={w}:{h}','format=gray']
    b=subprocess.run([FF,'-v','error','-i',src,'-vf',','.join(vf),'-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(-1,h,w).astype(np.float32)
def z(a): a=a-a.mean(); return a/max(np.sqrt((a*a).sum()),1e-6)
def grab(n):
    b=subprocess.run([FF,'-v','error','-ss',f'{n/FPS+0.0002:.5f}','-i','ref/ad5_v3_hd.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(1080,1920,3)
def screen_box(im):
    """the phone screen inside his olive card: the region of non-olive, non-field pixels in the centre column"""
    ol=np.array([93,101,60],np.float32); d=np.abs(im.astype(np.float32)-ol).sum(2)>60
    fld=np.abs(im.astype(np.float32)-np.array([9,10,4],np.float32)).sum(2)>40; d&=fld
    d[:, :600]=False; d[:, 1320:]=False; d[:80]=False; d[1000:]=False
    ys,xs=np.nonzero(d)
    if len(xs)<2000: return None
    return int(np.percentile(xs,1)),int(np.percentile(ys,1)),int(np.percentile(xs,99)),int(np.percentile(ys,99))
OUT={}
R=frames(APP,66,144,fps=20); Rz=np.stack([z(r) for r in R])
res=[]
for n in range(6717,6954,4):
    im=grab(n); bx=screen_box(im)
    if bx is None: res.append((n,None,0.0,None)); continue
    x0,y0,x1,y1=bx; g=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_RGB2GRAY).astype(np.float32)
    ph=min(144,int(round(66*(y1-y0)/(x1-x0)))); t=cv2.resize(g,(66,ph),interpolation=cv2.INTER_AREA)
    v=np.array([float((z(r[:ph])*z(t)).sum()) for r in R]); j=int(np.argmax(v)); res.append((n,round(j/20,3),round(float(v[j]),3),bx))
OUT['app']=dict(src=APP,n0=6717,n1=6954,map=res)
print('app:',' '.join(f'{n}->{t}({r:.2f})' for n,t,r,_ in res if t is not None))
print('boxes:',[b for _,_,_,b in res][:3])
pg=cv2.cvtColor(cv2.imread(PNG),cv2.COLOR_BGR2GRAY).astype(np.float32)
sc=[]
for n in range(5422,5635,6):
    im=grab(n); ol=np.array([93,101,60],np.float32)
    # his phone is on the LEFT third here (dan right)
    d=np.abs(im.astype(np.float32)-np.array([9,10,4],np.float32)).sum(2)>60; d[:, 900:]=False; d[:60]=False; d[1040:]=False
    ys,xs=np.nonzero(d)
    if len(xs)<2000: sc.append((n,None)); continue
    x0,y0,x1,y1=int(np.percentile(xs,1)),int(np.percentile(ys,1)),int(np.percentile(xs,99)),int(np.percentile(ys,99))
    g=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_RGB2GRAY).astype(np.float32); s=900/(x1-x0)
    t=cv2.resize(g,(900,int((y1-y0)*s)),interpolation=cv2.INTER_CUBIC)
    if t.shape[0]>=pg.shape[0]: sc.append((n,0,(x0,y0,x1,y1),None)); continue
    rr=cv2.matchTemplate(pg,t,cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(rr); sc.append((n,int(ml[1]),(x0,y0,x1,y1),round(float(mv),3)))
OUT['meal']=dict(src=PNG,n0=5422,n1=5635,offsets=sc)
print('meal:',[(a[0],a[1],a[3] if len(a)>3 else None) for a in sc])
json.dump(OUT,open('media_map.json','w'))
