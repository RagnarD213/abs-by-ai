import sys,json,time,subprocess,cv2,numpy as np
from pathlib import Path
W=Path(__file__).parent
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared'))
import buildcap
from key_v2 import key as bodykey,foreground
from key_v3 import key as hairkey,stabilize,composite
from grade import grade
F=str(R/'Media/video_edit/bin/ffmpeg');P=json.loads((W/'plan.json').read_text());FPS=P['fps']
cv2.setNumThreads(2)
buildcap.wait('Bill Maher R4 native body and approved five-frame hair')
maker=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
flowbody=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
Y,X=np.mgrid[:700,:1080].astype(np.float32)
def fit_screen(p):
 cs=[]
 for i in range(0,p['frames'],45):
  cmd=[F,'-v','error','-ss',str(p['source_start']+i/FPS),'-i',P['source'],'-frames:v','1','-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,scale=135:240,format=rgb48le','-f','rawvideo','-']
  s=np.frombuffer(subprocess.check_output(cmd),'<u2').reshape(240,135,3).astype(np.float32)/65535
  y,x=np.mgrid[:240,:135].astype(np.float32);x/=135;y/=240;r,g,b=s.transpose(2,0,1);sel=(g-r>.14)&(g-b>.14)
  M=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1);c=np.linalg.lstsq(M[sel],s[sel],rcond=None)[0]
  for _ in range(3):
   res=np.linalg.norm(s-M@c,axis=2);keep=sel&(res<np.percentile(res[sel],85));c=np.linalg.lstsq(M[keep],s[keep],rcond=None)[0]
  cs.append(c)
 c=np.median(cs,axis=0);np.save(W/(p['id']+'-screen-coefs.npy'),cs)
 y,x=np.mgrid[400:1300,350:1850].astype(np.float32);x/=2160;y/=3840;M=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1)
 return M@c
def encoder(path):
 return subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(path)],stdin=subprocess.PIPE)
def align(other,cur):
 flow=flowbody.calc(cur['gray'],other['gray'],None)
 wa=cv2.remap(cv2.resize(other['a'][:1400],(1080,700),interpolation=cv2.INTER_AREA),X+flow[:,:,0],Y+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 wg=cv2.remap(other['gray'],X+flow[:,:,0],Y+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 return cv2.resize(wa,(2160,1400)),cv2.resize(np.exp(-((wg.astype(np.float32)-cur['gray'])/14)**2),(2160,1400))
for p in P['key_pieces']:
 out=W/(p['id']+'-light.mp4')
 if out.exists() and (W/(p['id']+'-key-complete.json')).exists():continue
 bg=fit_screen(p)
 dec=subprocess.Popen([F,'-v','error','-ss',str(p['source_start']),'-i',P['source'],'-frames:v',str(p['frames']),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb48le','-f','rawvideo','-'],stdout=subprocess.PIPE)
 encs=[encoder(out),encoder(W/(p['id']+'-dark.mp4'))]
 cache={};nextframe=0;t=time.time();stats=[]
 def read(j):
  raw=dec.stdout.read(2160*3840*6);assert len(raw)==2160*3840*6,(p['id'],j,len(raw))
  im=np.frombuffer(raw,'<u2').reshape(3840,2160,3).astype(np.float32)/65535
  a,screen,hair,top,near,base=bodykey(im)
  gray=cv2.cvtColor((cv2.resize(im[:1400],(1080,700))*255).astype('uint8'),cv2.COLOR_RGB2GRAY)
  hh=hairkey(im[400:1300,350:1850],bg)
  return dict(im=im,a=a,bg=screen,hair=hair,top=top,near=near,gray=gray,hh=hh)
 for i in range(p['frames']):
  lo=max(0,i-2);hi=min(p['frames'],i+3)
  while nextframe<hi:cache[nextframe]=read(nextframe);nextframe+=1
  for j in list(cache):
   if j<lo:del cache[j]
  cur=cache[i];a=cur['a'].copy();acc=a[:1400].copy();weights=np.ones_like(acc)
  for j in [i-1,i+1]:
   if j not in cache:continue
   wa,cf=align(cache[j],cur);cf*=np.clip(1-abs(wa-a[:1400])/.22,0,1)*.55;acc+=cf*wa;weights+=cf
  a[:1400]=a[:1400]*(1-cur['hair'][:1400])+(acc/weights)*cur['hair'][:1400]
  f=foreground(cur['im'],a,cur['bg']);blend=(1-a[:1400])*cur['hair'][:1400]*.8
  nn=cur['near'][:1400].copy();nn[:,:,1]=np.minimum(nn[:,:,1],np.maximum(nn[:,:,0],nn[:,:,2]));f[:1400]=f[:1400]*(1-blend[:,:,None])+nn*a[:1400,:,None]*blend[:,:,None]
  aa=stabilize([cache[j]['hh'] for j in range(lo,hi)],i-lo,maker)
  y=np.arange(400,1300,dtype=np.float32)[:,None];handover=np.broadcast_to(np.clip((1120-y)/160,0,1),(900,1500))
  handover=cv2.resize(handover,(750,450),interpolation=cv2.INTER_AREA)[:,:,None]
  # R2 grades the downsampled reconstructed body, R3 grades native hair then downsamples.
  # Preserve that exact order while avoiding redundant full-native grading per field.
  fs=cv2.resize(f,(1080,1920),interpolation=cv2.INTER_AREA)
  smalla=cv2.resize(a,(1080,1920),interpolation=cv2.INTER_AREA)[:,:,None]
  gf=grade(fs/np.maximum(smalla,.001),'warm')*smalla
  for e,field in zip(encs,[[.84,.87,.89],[.08,.10,.13]]):
   rgb=gf+(1-smalla)*np.array(field,np.float32)
   hc=cv2.resize(composite(cur['hh'],aa,bg,field,grade),(750,450),interpolation=cv2.INTER_AREA)
   rgb[200:650,175:925]=rgb[200:650,175:925]*(1-handover)+hc*handover
   e.stdin.write((np.clip(rgb,0,1)*255+.5).astype('uint8').tobytes())
  if i%30==0:
   stats.append({'frame':i,'hair_top':cur['top'],'seconds':round(time.time()-t,2)})
   print(p['id'],i,p['frames'],round(time.time()-t,1),flush=True)
 for e in encs:e.stdin.close();assert e.wait()==0
 assert dec.wait()==0
 (W/(p['id']+'-key-complete.json')).write_text(json.dumps({'frames':p['frames'],'stats':stats},indent=2))
 print(p['id'],'DONE',flush=True)
print('ALL KEYED',flush=True)
