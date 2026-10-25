"""Patch only Dan's two requested picture intervals over the reviewed R2 masters.
Full-film audio is packet-copied. All other picture frames derive from locked R2.
"""
from pathlib import Path
import os,sys,json,subprocess,hashlib
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(k,'1')
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import composite as C
sys.path.insert(0,str(W/'recipe'));import house_composite as H
FPS=30000/1001;F=str(R/'Media/video_edit/bin/ffmpeg');OWNER='01a17430-0acf-72c1-93fa-026651f4da47'
def check():
 j=json.loads((W/'round-controller.json').read_text());assert j['productionOwner']==OWNER and j['phase']=='complete'
class Patch:
 def __init__(self,v):
  self.cached=None;self.nextcache=None;self.v=v;self.rejected=None;self.nextr=None;self.after=None;self.nexta=None
  self.photo=np.asarray(Image.open(W/'assets/Daniel-source-inset.png').convert('RGB').resize((425,428),Image.Resampling.LANCZOS))
  self.caps=json.loads((B/'qa'/v/'caption-states.json').read_text())['states'];self.capimgs={}
 def apply(self,f,g):
  f=f.copy()
  if 284<=g<469:
   if (W/'proofs/craig-context-v2-checked.json').exists():
    k=g-240
    if self.cached is None or self.nextcache!=k:self.cached=C.reader(str(W/'proofs/craig-v2-in-audio-context.mp4'),start=k,wh=(1080,1920))
    self.nextcache=k+1
    return next(self.cached).copy()
   # Preserve the already-correct native photo and foreground from candidate1.
   # Restore only its rejected label/arrow pixels from the locked R2 frame.
   # This is picture evidence only; no rejected verdict or QA is reused.
   if self.rejected is None or self.nextr!=g:
    self.rejected=C.reader(str(W/'rejected-candidate1'/f'dad-bod-r3-{self.v}.mp4'),start=g,wh=(1080,1920))
   old=next(self.rejected).copy();self.nextr=g+1
   label=old[282:362,8:465].copy()
   old[282:362,8:465]=f[282:362,8:465]
   old[375:440,337:403]=f[375:440,337:403]
   old[100:180,8:465]=label
   ar=Image.fromarray(old);d=ImageDraw.Draw(ar)
   d.line([(92,192),(92,404),(128,433)],fill=(104,197,255),width=7)
   d.polygon([(128,433),(102,427),(117,410)],fill=(104,197,255))
   f=np.asarray(ar).copy()
  if self.v=='scripted' and 973<=g<1058:
   k=g-973
   if self.after is None or self.nexta!=k:self.after=C.reader(str(W/'hf/renders/R3_After.mov'),start=k,wh=(1080,1920))
   f=next(self.after).copy();self.nexta=k+1
   t=g/FPS
   for cap in self.caps:
    if cap['beat'][0]<=t<cap['beat'][1]:
     q=cap['image']
     if q not in self.capimgs:self.capimgs[q]=np.asarray(Image.open(q).convert('RGBA'))
     f=C.over(f,self.capimgs[q])
  return f

def render(v,a=0,b=None,outpath=None):
 check();source=B/'review/media'/f'dad-bod-r2-{v}.mp4';out=Path(outpath) if outpath else W/'review/media'/f'dad-bod-r3-{v}.mp4';out.parent.mkdir(parents=True,exist_ok=True)
 n=json.loads((W/v/'edl.json').read_text())['total_frames'];b=b if b is not None else n;n=b-a;p=Patch(v)
 cmd=[F,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-ss',str(a/FPS),'-i',str(source),'-map','0:v:0','-map','1:a:0','-vf','scale=in_range=pc:out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads',os.environ.get('RENDERQ_CORES','4'),'-c:a','copy','-t',str(n/FPS),'-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart',str(out)]
 enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 count=0
 for g,f in enumerate(C.reader(str(source),start=a,n=n,wh=(1080,1920)),start=a):
  enc.stdin.write(np.ascontiguousarray(p.apply(f,g)).tobytes());count+=1
  if g%150==0:print('FRAME',v,g,n,flush=True)
 enc.stdin.close();assert enc.wait()==0 and count==n,(count,n)
 print('R3_COMPLETE',v,out,flush=True)
if __name__=='__main__':
 check()
 if sys.argv[1]=='stills':
  out=W/'proofs';out.mkdir(exist_ok=True)
  for v in ['scripted','off_the_cuff']:
   for t in [9.476133333333333,10,13,14.7814333333,14.8148,14.8481667,14.9,15.2,15.6,15.6489666667]+([33] if v=='scripted' else []):
    g=round(t*FPS);f=next(C.reader(str(B/'review/media'/f'dad-bod-r2-{v}.mp4'),start=g,n=1,wh=(1080,1920)));Image.fromarray(Patch(v).apply(f,g)).save(out/f'{v}-{g:04d}.png')
  print('R3_PROOFS_READY',flush=True)
 elif sys.argv[1]=='contexts':
  render('scripted',240,510,str(W/'proofs/craig-v2-in-audio-context.mp4'))
  render('scripted',910,1100,str(W/'proofs/abs-in-audio-context.mp4'))
 else:render(sys.argv[1])
