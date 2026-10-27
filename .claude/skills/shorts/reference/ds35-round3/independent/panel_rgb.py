from pathlib import Path
import sys,json,subprocess,hashlib,os
import numpy as np,cv2
from PIL import Image,ImageDraw
cv2.setNumThreads(1)
W=Path('/Volumes/Expansion/_edit_work/DS-35/round3');B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(W/'recipe'));sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'))
sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq;renderq.hold_until_exit('Independent exact native panel '+sys.argv[1],pool='quick')
import opening_v3 as O,house_composite as H,clip_ds35 as CL,composite as C
FPS=30000/1001;F=str(R/'Media/video_edit/bin/ffmpeg')
# Only independent original-source background stages, explicitly before H.place; no candidate-derived subtraction plate.
H.key_frame=lambda *a:(None,None)
H.place=lambda out,*a,**k:out
for v in sys.argv[1:] or ['scripted','off_the_cuff']:
 e=json.loads((W/v/'edl.json').read_text());L=json.loads((W/v/'r2-layout.json').read_text());n=L['panel_end'];out=W/'independent'/v;vid=W/'review/media'/f'dad-bod-r3-{v}.mp4';op=O.Opening(v);bgcomp=C.Compositor(json.loads((B/v/'graphics-manifest.json').read_text()),wh=(1080,1920));rows=[];proofs=[]
 p=subprocess.Popen([F,'-v','error','-ss',str(284/FPS),'-i',str(vid),'-t',str((n-284)/FPS),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
 for g in range(284,n):
  b=p.stdout.read(1080*1920*3);assert len(b)==1080*1920*3;im=np.frombuffer(b,np.uint8).reshape(1920,1080,3)
  if g<485:bg=op.apply(g,np.zeros_like(im))
  else:
   t=e['tr']['clip_in']+(g-469)/FPS;bg=np.zeros_like(im);bg[92:700]=(cv2.resize(CL.frame(t),(1080,608),interpolation=cv2.INTER_AREA)*255).astype(np.uint8);bg=bgcomp.apply(bg,g)
  y0=500;x0=100;roi=im[y0:1000,x0:950];ex=bg[y0:1000,x0:950];rr,gg,bb=[roi[:,:,i].astype(np.int16) for i in range(3)]
  diff=np.max(np.abs(roi.astype(np.int16)-ex.astype(np.int16)),2)
  mask=((rr-bb>-15)&(rr-gg>-18)&(np.max(roi,2)<120)&(diff>30)).astype(np.uint8);mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8));nn,lab,st,ct=cv2.connectedComponentsWithStats(mask,8)
  ids=[i for i in range(1,nn) if st[i,4]>500 and st[i,1]<350 and st[i,0]+st[i,2]>200 and st[i,0]<650];assert ids,(v,g,'no detected hair')
  k=max(ids,key=lambda i:st[i,4]);xx,yy,ww,hh,ar=map(int,st[k]);ys,xs=np.where((lab==k)&(np.indices(lab.shape)[0]<yy+130));cx=float((xs.min()+xs.max())/2+x0);hy=y0+yy;row=dict(g=g,t=g/FPS,population='watching' if g<485 else 'response_panel',hair_top=hy,head_x=cx,bbox=[xx+x0,hy,ww,hh],roi_boundary_hit=bool(yy==0 or xx==0 or xx+ww==850));rows.append(row)
  if g in [284,350,417,425,443,468,478,479,480,481,482,483,484,485,486,487,488,489,490,507,616,640,721]:
   pi=Image.fromarray(im.copy());d=ImageDraw.Draw(pi);d.line((0,hy,1080,hy),fill='lime',width=2);d.line((cx,hy,cx,hy+130),fill='yellow',width=2);path=out/f'panel-corrected-{g:04d}.png';pi.save(path);proofs.append(str(path))
 assert p.wait()==0
 result=dict(video_sha256=hashlib.sha256(vid.read_bytes()).hexdigest(),method='Actual sequential native1080x1920 RGB, independently reconstructed original CL.frame + original R2 SourcePanel HF + R3 Craig/photo background BEFORE any foreground H.place. Neutral dark RGB hair intersected with >30RGB residual, ROI x100..950/y500..1000. This removes source/photo contamination that invalidated the first RGB panel ROIs. No candidate-derived plate, alpha or production geometry used as measurement.',rows=rows,proofs=proofs)
 for kind in ['watching','response_panel']:
  q=[x for x in rows if x['population']==kind];a=np.array([x['head_x'] for x in q]);result[kind]=dict(n=len(q),min_hair=min(x['hair_top'] for x in q),max_hair=max(x['hair_top'] for x in q),median_head=float(np.median(a)),min_head=float(a.min()),max_head=float(a.max()),sd_head=float(a.std()),roi_boundary_hits=[x['g'] for x in q if x['roi_boundary_hit']])
 (out/'panel-rgb-corrected.json').write_text(json.dumps(result,indent=1));print(v,result['watching'],result['response_panel'],flush=True)
