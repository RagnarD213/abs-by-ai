"""Reconstruct only the large-watching interval, keeping camera boundaries outside the canvas."""
from pathlib import Path
import sys,json
import numpy as np,cv2
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0,str(W/'recipe'));import house_composite as H,clip_ds35 as CL
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import composite as C
FPS=30000/1001
class Opening:
 def __init__(self,v):
  self.e=json.loads((W/v/'edl.json').read_text());H.configure(json.loads((W/'key/pieces.json').read_text()),'B_warmvivid')
  self.C=C.Compositor(json.loads((B/v/'graphics-manifest.json').read_text()),wh=(1080,1920));self.craig=None;self.nextc=None
  self.photo=np.asarray(Image.open(W/'assets/Daniel-source-inset.png').convert('RGB').resize((425,428),Image.Resampling.LANCZOS))
  self.caps=json.loads((B/'qa'/v/'caption-states.json').read_text())['states'];self.capimgs={}
 def apply(self,g,baseline=None):
  e=self.e
  if g<469:
   c=next(c for c in e['clip']['segs'] if c['n0']<=g<c['n0']+c['frames']);t=c['clip_in']+(g-c['n0'])/FPS
  else:t=e['tr']['clip_in']+(g-469)/FPS
  f=np.zeros((1920,1080,3),np.uint8);f[92:700]=cv2.resize(CL.frame(t),(1080,608),interpolation=cv2.INTER_AREA)*255
  f=self.C.apply(f,g)
  if g<469:
   k=g-284
   if self.craig is None or self.nextc!=k:self.craig=C.reader(str(W/'hf/renders/R3_Craig.mov'),start=k,rgba=True,wh=(480,650))
   ov=next(self.craig);self.nextc=k+1;p=np.zeros((1920,1080,4),np.uint8)
   p[445:895,10:455]=ov[175:625,10:455]
   p[455:883,20:445,:3]=self.photo;p[455:883,20:445,3]=255;p[100:180,8:465]=ov[12:92,8:465]
   ar=Image.fromarray(p);d=ImageDraw.Draw(ar);d.line([(92,192),(92,404),(128,433)],fill=(104,197,255,255),width=7);d.polygon([(128,433),(102,427),(117,410)],fill=(104,197,255,255));f=C.over(f,np.asarray(ar))
  fp,alpha=H.key_frame('W_C3',t+e['clip']['segs'][-1]['roll_minus_clip'])
  f=H.u8(H.place(f.astype(np.float32)/255,fp,alpha,2/3,0,234.66666666666669))
  # Retain the exact always-readable R2 title/header, including the first panel frame.
  if baseline is None:baseline=next(C.reader(str(B/'review/media/dad-bod-r2-scripted.mp4'),start=g,n=1,wh=(1080,1920)))
  f[:92]=baseline[:92]
  for cap in self.caps:
   if cap['beat'][0]<=g/FPS<cap['beat'][1]:
    q=cap['image']
    if q not in self.capimgs:self.capimgs[q]=np.asarray(Image.open(q).convert('RGBA'))
    f=C.over(f,self.capimgs[q])
  return f
if __name__=='__main__':
 out=W/'proofs/callout-v3';out.mkdir(exist_ok=True)
 for v in ['scripted']:
  p=Opening(v)
  for g in [284,350,443,468,484]:Image.fromarray(p.apply(g)).save(out/f'native-{g}.png')
 print('CAMERA_EDGE_REPAIR_STILLS_READY',flush=True)
