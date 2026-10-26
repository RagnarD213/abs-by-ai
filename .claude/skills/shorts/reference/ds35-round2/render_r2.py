"""Complete paired R2 films, source mapped. Keys/repairs remain read-only in R1."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(k,'1')
from pathlib import Path
import sys,json,argparse,subprocess,math
import numpy as np,cv2
from PIL import Image
from multiprocessing import Pool
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0,str(W/'recipe'));sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'))
import house_composite as H,clip_ds35 as CL,composite as CM
F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;FR=lambda x:round(x*FPS)
class Video:
 def __init__(self,v):
  self.D=W/v;self.e=json.loads((self.D/'edl.json').read_text());self.L=json.loads((self.D/'r2-layout.json').read_text());self.shots=json.loads((self.D/'shots.json').read_text());self.crops=json.loads((self.D/'framing-frames.json').read_text());self.keys=json.loads((W/'key/pieces.json').read_text());H.configure(self.keys,'B_warmvivid');self.C=CM.Compositor(json.loads((self.D/'graphics-manifest.json').read_text()),wh=(1080,1920));self.bg=None;self.nxt=None
  self.compare=np.asarray(Image.open(W/'comparison-real-source-photos.png').convert('RGB'));self.v=v
  self.geom=json.loads((W/'panel-geometry.json').read_text())[v]
 def field(self,g):
  if self.bg is None or self.nxt!=g:self.bg=CM.reader(str(W/'hf-field/renders/DS35_Field.mov'),start=g,wh=(1080,1920))
  self.nxt=g+1;f=next(self.bg,None);assert f is not None;return f.astype(np.float32)/255
 def key(self,k,t):return H.key_frame(k,t)
 def source_t(self,g):
  if g<469:
   c=next(c for c in self.e['clip']['segs'] if c['n0']<=g<c['n0']+c['frames']);return c['clip_in']+(g-c['n0'])/FPS,c
  c=self.e['clip']['segs'][-1];return self.e['tr']['clip_in']+(g-469)/FPS,c
 def render(self,g):
  e=self.e;L=self.L;ca,cb=L['comparison']
  if ca<=g<cb:
   out=np.zeros((1920,1080,3),np.uint8);out[230:1230,60:1020]=self.compare;return self.C.apply(out,g)
  if self.C.opaque(g):return self.C.apply(None,g)
  if g<L['panel_start']:
   t,c=self.source_t(g);pic=CL.view(26.02+(g-69)/FPS,camera_t=26.02) if 67<=g<69 else CL.view(t)
   fp,a=self.key('W_'+c['id'],t+c['roll_minus_clip']);fp,a=H.feather(fp,a,fw=21)
   return self.C.apply(H.u8(H.place(pic,fp,a,.40*1080/1620,0,1152)),g)
  if g<L['panel_end']:
   t,c=self.source_t(g) if g<485 else (self.e['tr']['clip_in']+(g-469)/FPS,None)
   out=np.zeros((1920,1080,3),np.uint8);out[92:700]=cv2.resize(CL.frame(t),(1080,608),interpolation=cv2.INTER_AREA)*255
   out=self.C.apply(out,g).astype(np.float32)/255
   if g<485:
    k='W_C3';rt=t+e['clip']['segs'][-1]['roll_minus_clip'];sc=1080/1620;xo=self.geom['watch']['x'];yo=self.geom['watch']['y']
   else:
    p=e['pieces'][0];k='S' if self.v=='scripted' else 'O1';rt=p['start']+(g-p['n0'])/FPS;sc=.82
    sh=self.shots[0];x,y,cw,ch=self.crops[sh['id']][g-sh['n0']];xo=-x*1080/cw;yo=self.geom['response']['y']
   fp,a=self.key(k,rt);return H.u8(H.place(out,fp,a,sc,xo,yo))
  out=self.field(g);sh=next(s for s in self.shots if s['n0']<=g<s['n1']);p=next(p for p in e['pieces'] if p['id']==sh['piece']);rt=p['start']+(g-p['n0'])/FPS
  fp,a=self.key(sh['key'],rt);x,y,cw,ch=self.crops[sh['id']][g-sh['n0']]
  if sh['card']:
   # Post-comparison presenter now fills the screen. Source card has exited permanently.
   m=np.load(W/'framing-cache'/(sh['key']+'.npy'));ix=g-p['n0'];cw=1000 if sh['size']=='T' else 1240;ch=cw*16/9
   lo=sh['n0']-p['n0'];hi=sh['n1']-p['n0'];y=float(m[lo:hi,0].min())-.035*ch
   # Original land/hold normalized head centre is retained through its changed scale.
   cx=x+sh['crop_w']/2;x=cx-cw/2
  return self.C.apply(H.u8(H.place(out,fp,a,1080/cw,-x*1080/cw,-y*1080/cw)),g)
def chunk(task):
 v,a,b,path=task;os.environ['RENDERQ_CORES']='1';cv2.setNumThreads(1);video=Video(v);ass=W/v/'captions.ass'
 vf=f"setpts=PTS+{a},ass='{ass}',setpts=PTS-STARTPTS,scale=in_range=pc:out_color_matrix=bt709:out_range=tv,format=yuv420p"
 enc=subprocess.Popen([F,'-v','error','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-an','-vf',vf,'-c:v','libx264','-threads','1','-preset','fast','-crf','16','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',path],stdin=subprocess.PIPE)
 for g in range(a,b):
  enc.stdin.write(np.ascontiguousarray(video.render(g)).tobytes())
  if (g-a)%60==0:print('FRAME',v,g,b,flush=True)
 enc.stdin.close();assert enc.wait()==0;print('PART_DONE',v,a,b,flush=True);return path
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('v',choices=['scripted','off_the_cuff']);ap.add_argument('--start',type=float,default=0);ap.add_argument('--end',type=float);ap.add_argument('--out',required=True);ap.add_argument('--stills');z=ap.parse_args()
 e=json.loads((W/z.v/'edl.json').read_text());a=FR(z.start);b=FR(z.end) if z.end is not None else e['total_frames'];out=Path(z.out);out.parent.mkdir(parents=True,exist_ok=True)
 j=json.loads((W/'round-controller.json').read_text());assert j['productionOwner']=='01a1737b-0b58-7110-b12e-e7b5daa91dda' and j['phase']=='complete'
 if z.stills:
  sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq;renderq.hold_until_exit('Dad Bod R2 native internal proofs',pool='quick')
  v=Video(z.v);out.mkdir(exist_ok=True)
  for t in map(float,z.stills.split(',')):
   g=FR(t);subprocess.run([F,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-vf',f"setpts=PTS+{g},ass='{W/z.v/'captions.ass'}'",'-frames:v','1',str(out/f'{g:04d}.png')],input=v.render(g).tobytes(),check=True)
  sys.exit()
 cores=min(int(os.environ.get('RENDERQ_CORES',4)),max(1,(b-a)//90));tmp=out.parent/(out.stem+'-parts');tmp.mkdir(exist_ok=True);bounds=[round(a+(b-a)*i/cores) for i in range(cores+1)]
 tasks=[(z.v,bounds[i],bounds[i+1],str(tmp/f'part{i}.mp4')) for i in range(cores)]
 with Pool(cores) as pool:parts=pool.map(chunk,tasks)
 li=tmp/'concat.txt';li.write_text(''.join("file '"+p+"'\n" for p in parts))
 subprocess.run([F,'-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(li),'-ss',str(a/FPS),'-i',str(W/z.v/'mix-C_Balanced.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-t',str((b-a)/FPS),'-movflags','+faststart',str(out)],check=True)
 print('R2_RENDER_COMPLETE',z.v,out,flush=True)
