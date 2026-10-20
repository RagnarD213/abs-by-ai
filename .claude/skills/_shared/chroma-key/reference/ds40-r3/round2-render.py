import subprocess,sys,time,json,cv2,numpy as np
from pathlib import Path
from key_v2 import key,foreground
from grade import grade
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');SRC='/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R2 hair refinement');cv2.setNumThreads(3)
D=W/'review/media';D.mkdir(parents=True,exist_ok=True)
dec=subprocess.Popen([F,'-v','error','-ss','1413.0116','-i',SRC,'-frames:v','300','-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,format=rgb48le','-f','rawvideo','-'],stdout=subprocess.PIPE)
def encoder(name,w=1080,h=1920):
 return subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{w}x{h}','-framerate','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','17','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(W/f'{name}-picture.mp4')],stdin=subprocess.PIPE)
encs={n:encoder(n) for n in ['wide','dark','oldwide']};encs['hair']=encoder('hair',1080,1200)
flowmaker=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
Y,X=np.mgrid[:700,:1080].astype(np.float32)
def read():
 raw=dec.stdout.read(2160*3840*6)
 if not raw:return None
 im=np.frombuffer(raw,'<u2').reshape(3840,2160,3).astype(np.float32)/65535
 a,bg,hair,top,near,base=key(im)
 gray=cv2.cvtColor((cv2.resize(im[:1400],(1080,700))*255).astype('uint8'),cv2.COLOR_RGB2GRAY)
 return dict(im=im,a=a,bg=bg,hair=hair,top=top,near=near,base=base,gray=gray)
def aligned(other,cur):
 flow=flowmaker.calc(cur['gray'],other['gray'],None)
 amap=cv2.resize(other['a'][:1400],(1080,700),interpolation=cv2.INTER_AREA)
 a=cv2.remap(amap,X+flow[:,:,0],Y+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 g=cv2.remap(other['gray'],X+flow[:,:,0],Y+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 conf=np.exp(-((g.astype('float32')-cur['gray'])/14)**2)
 return cv2.resize(a,(2160,1400)),cv2.resize(conf,(2160,1400))
def premult(cur,a,refined):
 f=foreground(cur['im'],a,cur['bg'])
 if refined:
  h=1400;t=(1-a[:h])*cur['hair'][:h]*.8
  nn=cur['near'][:h].copy();nn[:,:,1]=np.minimum(nn[:,:,1],np.maximum(nn[:,:,0],nn[:,:,2]))
  f[:h]=f[:h]*(1-t[:,:,None])+nn*a[:h,:,None]*t[:,:,None]
 return f

def comp(f,a,c,size=(1080,1920)):
 f=cv2.resize(f,size,interpolation=cv2.INTER_AREA);a=cv2.resize(a,size,interpolation=cv2.INTER_AREA)[:,:,None]
 return np.clip(grade(f/np.maximum(a,.001),'warm')*a+(1-a)*np.array(c,np.float32),0,1)
prev=None;cur=read();nxt=read();t0=time.time();stats=[]
for i in range(300):
 a=cur['a'].copy();acc=a[:1400].copy();weights=np.ones_like(acc)
 for other in [prev,nxt]:
  if other is None:continue
  wa,cf=aligned(other,cur);cf*=np.clip(1-abs(wa-a[:1400])/.22,0,1)*.55
  acc+=cf*wa;weights+=cf
 stable=acc/weights;mask=cur['hair'][:1400];a[:1400]=a[:1400]*(1-mask)+stable*mask
 nf=premult(cur,a,True);of=premult(cur,cur['base'],False)
 light=comp(nf,a,[.84,.87,.89]);dark=comp(nf,a,[.08,.10,.13]);old=comp(of,cur['base'],[.84,.87,.89])
 imgs={}
 for name,o in [('wide',light),('dark',dark),('oldwide',old)]:
  sm=(o*255+.5).astype('uint8');encs[name].stdin.write(sm.tobytes());imgs[name]=sm
 crop=lambda f,aa:comp(f[500:1250,450:1800],aa[500:1250,450:1800],[.84,.87,.89],(1080,600))
 hc=(np.concatenate([crop(of,cur['base']),crop(nf,a)],0)*255+.5).astype('uint8');encs['hair'].stdin.write(hc.tobytes())
 if i in [0,30,90,150,210,270,299]:
  for name,im in imgs.items():cv2.imwrite(str(D/f'{name}-{i:03}.jpg'),im[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,97])
  cv2.imwrite(str(D/f'hair-{i:03}.jpg'),hc[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,97])
 if i%30==0:
  print(i,round(time.time()-t0,1),flush=True);stats.append({'frame':i,'hairtop':cur['top'],'temporal_mean_delta':float(np.mean(abs(a-cur['a']))),'background_alpha_p99':float(np.percentile(a[:300],99))})
 prev,cur=cur,nxt;nxt=read() if i<298 else None
for e in encs.values():e.stdin.close();assert e.wait()==0
assert dec.wait()==0
(W/'key-measurements.json').write_text(json.dumps(stats,indent=2));print('RENDER DONE',flush=True)
