"""HIS PICTURE CUT at every audio splice inside a talk beat.

The audio EDL says where his SOUND switches takes. His PICTURE switches on a frame of his own
choosing near it (a J- or L-cut on a pose-matched frame: at 96.00 s the picture leads the audio
by 8 frames). For each splice, render both takes from the raw at the grade over +-15 frames,
fit each rendered frame to his framing (scale / fy search, like cover.py) and match against his
frame with a high-passed NCC. The crossover frame -- last frame that matches the OUTGOING take,
first that matches the INCOMING one -- is his picture cut. Writes piccuts.json."""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageFilter
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RAW=("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, "
     "outdoor workout content | jeff chagrin | dan rose/C1592.MP4")
FPS=30000/1001; GRADE=open('grade.txt').read().strip()
E=json.load(open('edl_final.json'))
sys.path.insert(0,'.'); import beats as BT
tl,_=BT.timeline()
def kind_at(t):
    for b in tl:
        if b['t0']<=t<b['t1']: return b['kind']
    return '?'
W=15; H,Wd=270,480
SC=[1.0,1.05,1.1,1.15,1.2,1.25,1.3]; FY=[0.30,0.42,0.50]
def frames_from(cmd, n):
    b=subprocess.run(cmd+['-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    a=np.frombuffer(b[:n*H*Wd],np.uint8).reshape(-1,H,Wd).astype(np.float32)
    return a
def hp(a):
    return a-np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),dtype=np.float32)
def ncc(a,b):
    a=a-a.mean(); b=b-b.mean(); return float((a*b).sum()/max(np.sqrt((a*a).sum()*(b*b).sum()),1e-6))
def best_match(his_hp, our):
    best=-9
    for s in SC:
        nh,nw=int(H/s),int(Wd/s)
        for fy in FY:
            y0=int((H-nh)*fy); x0=(Wd-nw)//2
            r=np.asarray(Image.fromarray(our[y0:y0+nh,x0:x0+nw].astype(np.uint8)).resize((Wd,H)),dtype=np.float32)
            v=ncc(his_hp[30:200,120:360], hp(r)[30:200,120:360])
            if v>best: best=v
    return best
out=[]
for i in range(1,len(E)):
    cur,prev=E[i],E[i-1]
    if kind_at(cur['cut_in'])!='talk' or kind_at(cur['cut_in']-0.05)!='talk': continue
    n0=round(cur['cut_in']*FPS); pn0=round(prev['cut_in']*FPS)
    t0=(n0-W)/FPS; N=2*W+1
    his=frames_from([FF,'-v','error','-ss',f'{t0:.4f}','-i','reference.mp4','-frames:v',str(N),'-vf',f'scale={Wd}:{H}'],N)
    a_src=prev['src_in']+(n0-W-pn0)/FPS
    b_src=cur['src_in']-W/FPS
    A=frames_from([FF,'-v','error','-ss',f'{a_src:.4f}','-i',RAW,'-frames:v',str(N),'-vf',f'{GRADE},scale={Wd}:{H}'],N)
    B=frames_from([FF,'-v','error','-ss',f'{b_src:.4f}','-i',RAW,'-frames:v',str(N),'-vf',f'{GRADE},scale={Wd}:{H}'],N)
    if len(his)<N or len(A)<N or len(B)<N:
        print(f'splice {cur["cut_in"]:.3f}: short extraction his {len(his)} A {len(A)} B {len(B)}'); continue
    ra=[]; rb=[]
    for k in range(N):
        h=hp(his[k]); ra.append(best_match(h,A[k])); rb.append(best_match(h,B[k]))
    ra=np.array(ra); rb=np.array(rb); d=rb-ra
    # crossover: first k where B beats A and stays ahead for >=3 frames
    cross=None
    for k in range(N-2):
        if d[k]>0 and d[k+1]>0 and d[k+2]>0 and (k==0 or d[k-1]<=0):
            cross=k; break
    rel=(cross-W) if cross is not None else None
    conf=float(min(ra[:max(1,cross-1)].mean() if cross and cross>1 else ra[0], rb[cross:cross+5].mean())) if cross is not None else 0.0
    out.append(dict(i=i, cut=cur['cut_in'], n0=n0, pic_rel=rel, pic_frame=(n0+rel) if rel is not None else None,
                    confidence=round(conf,3), ra=[round(float(v),3) for v in ra], rb=[round(float(v),3) for v in rb]))
    tag = f'{rel:+d} frames' if rel is not None else 'NO CROSSOVER'
    print(f'splice {cur["cut_in"]:8.3f} (f{n0})  his picture cut at {tag}   A-before {ra[:W].mean():.2f}  B-after {rb[W:].mean():.2f}   conf {conf:.2f}', flush=True)
json.dump(out, open('piccuts.json','w'), indent=1)
print(len(out),'splices written to piccuts.json')
