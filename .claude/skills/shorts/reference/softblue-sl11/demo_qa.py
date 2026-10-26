import sys,json,hashlib,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
from scipy import ndimage
R=Path(__file__).resolve().parents[1];ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
v=R/'review/context/whole-exercise-source.mp4';d=R/'qa-exact/demo';d.mkdir(parents=True,exist_ok=True)
with renderq.slot('Vacuum source demonstration framing QA',pool='quick',group='SL-11'):
 cp=subprocess.Popen([str(ROOT/'Media/video_edit/bin/ffmpeg'),'-nostdin','-v','error','-i',str(v),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE);paths=[];edges=[];n=0
 while True:
  b=cp.stdout.read(1080*1920*3)
  if not b:break
  assert len(b)==1080*1920*3
  a=np.frombuffer(b,np.uint8).reshape(1920,1080,3);edges.append(int((a[:20,300:780].mean(2)<65).sum()))
  if n%7==0:
   p=d/f'f{n:04d}.png';Image.fromarray(a).save(p);paths.append(p)
  n+=1
 assert cp.wait()==0
 subprocess.run([str(ROOT/'.claude/skills/shorts/reference/recentre/personmask'),str(d/'m')]+list(map(str,paths)),check=True,capture_output=True)
 rows=[]
 for p in paths:
  a=np.array(Image.open(d/'m'/f'{p.stem}.mask.png'))>127;lab,num=ndimage.label(a);assert num
  k=1+np.argmax(ndimage.sum(a,lab,range(1,num+1)));m=lab==k;yy,xx=np.where(m);rows.append(dict(frame=int(p.stem[1:]),hair=int(yy.min()),left=int(xx.min()),right=int(xx.max())))
 assert min(x['hair'] for x in rows)>=20
 assert max(edges)==0
 out=dict(scope='isolated silent exercise source; framing only, no finished film or audio pass',file=str(v),sha256=hashlib.sha256(v.read_bytes()).hexdigest(),frames=n,samples=rows,top_edge_every_frame_dark_pixels=edges)
 (R/'demo-framing-qa.json').write_text(json.dumps(out,indent=2))
 sheet=Image.new('RGB',(5*270,500),'white');dr=ImageDraw.Draw(sheet)
 for j,i in enumerate([0,14,42,70,len(paths)-1]):
  p=paths[i];im=Image.open(p).resize((270,480));sheet.paste(im,(j*270,20));dr.text((j*270+5,2),f"{int(p.stem[1:])/(30000/1001):.2f}s",fill='black')
 sheet.save(R/'qa-exact/demo-contact.jpg')
 print('PASS',n,'frames; hair min',min(x['hair'] for x in rows),'left min',min(x['left'] for x in rows),'right max',max(x['right'] for x in rows))
