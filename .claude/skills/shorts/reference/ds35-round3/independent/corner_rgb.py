from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
cv2.setNumThreads(1)
W=Path('/Volumes/Expansion/_edit_work/DS-35/round3');v=sys.argv[1];sys.path.insert(0,str(W/'recipe'));import clip_ds35 as C
sys.path.insert(0,'/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq');import renderq;renderq.hold_until_exit('Independent native corner calibration '+v,pool='quick')
E=json.load(open(W/v/'edl.json'));FPS=30000/1001;out=W/'independent'/v;vid=W/'review/media'/f'dad-bod-r3-{v}.mp4'
p=subprocess.Popen(['/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg','-v','error','-i',str(vid),'-t',str(284/FPS),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24,crop=432:400:0:1280','-f','rawvideo','-'],stdout=subprocess.PIPE)
rows=[]
for g in range(284):
 b=p.stdout.read(432*400*3);assert len(b)==432*400*3;im=np.frombuffer(b,np.uint8).reshape(400,432,3)
 c=next(c for c in E['clip']['segs'] if c['n0']<=g<c['n0']+c['frames']);t=c['clip_in']+(g-c['n0'])/FPS
 ct=t
 if 67<=g<69:t=26.02+(g-69)/FPS;ct=26.02
 ca=next(c for c in C.CAMS if c['a']<=ct<c['b']);h=ca['h'];ww=h*9/16;x=ca['cx']-ww/2
 ex=(cv2.warpAffine(C.frame(t),np.array([[1080/ww,0,-x*1080/ww],[0,1920/h,-1280]],np.float32),(432,400),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)*255).astype(np.uint8)
 r,gg,bb=[im[:,:,i].astype(np.int16) for i in range(3)];diff=np.max(abs(im.astype(np.int16)-ex.astype(np.int16)),2)
 mask=((diff>12)&(im.max(2)<110)&(r-bb>-15)&(r-gg>-18)).astype(np.uint8);mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8));n,l,st,ct=cv2.connectedComponentsWithStats(mask,8)
 ids=[i for i in range(1,n) if st[i,4]>80 and st[i,1]<180 and st[i,0]<330 and st[i,0]+st[i,2]>100];assert ids,(g,'no hair');k=min(ids,key=lambda i:st[i,1]);xx,yy,ww,hh,ar=map(int,st[k]);ys,xs=np.where((l==k)&(np.indices(l.shape)[0]<yy+80));cx=float((xs.min()+xs.max())/2);rows.append(dict(g=g,t=g/FPS,hair_top=yy+1280,head_x=cx,bbox=[xx,yy+1280,ww,hh]))
assert p.wait()==0
res=dict(video_sha256=hashlib.sha256(vid.read_bytes()).hexdigest(),method='Every284 actual native RGB corner frame, crop x0..432 y1280..1680; independently reconstructed original source crop, neutral dark hair intersect residual>12RGB, top connected hair component overlapping head x100..330; minimum80px area. Threshold calibrated on actual76/90/249/281; first residual32 method fragmented hair and is superseded. Core/fringe and source-dark similarity limit exact hair boundary by several pixels.',rows=rows)
a=np.array([r['head_x'] for r in rows]);res['stats']=dict(n=len(rows),min_hair=min(r['hair_top'] for r in rows),max_hair=max(r['hair_top'] for r in rows),median_head=float(np.median(a)),min_head=float(a.min()),max_head=float(a.max()),sd_head=float(a.std()))
(out/'corner-rgb-corrected.json').write_text(json.dumps(res,indent=1));print(v,res['stats'])
