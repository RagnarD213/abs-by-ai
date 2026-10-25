import os
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(v,'1')
import sys,json,subprocess,hashlib,time,bisect,cv2,numpy as np
from pathlib import Path
from PIL import Image
from layer import clean,place,hair
W=Path(__file__).parent;O=W.parent/'round4';R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;N=1944;OP=588;BA=1274;BB=1818;PANEL=120;PANEL_END=906
cv2.setNumThreads(1)
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));from composite import Compositor,reader,over
D=W/'review/media';D.mkdir(parents=True,exist_ok=True)
M=json.loads((W/'graphics-manifest.json').read_text());C=Compositor(M,wh=(1080,1920));field=reader(str(W/'hf/renders/G00.mov'),wh=(1080,1920))
# The existing caption PNGs and acoustic onsets remain exact. Only their spatial placement changes.
caps=json.loads((O/'caption-states.json').read_text())
for c in caps:
 c['pos']=[40,920 if c['beat'][0]<4.004 else 1440];h=c['rect'][3]-c['rect'][1];c['rect']=[40,c['pos'][1],1040,c['pos'][1]+h]
(W/'caption-states.json').write_text(json.dumps(caps,indent=2));starts=[c['beat'][0] for c in caps];active=-1;capimg=None
(D/'bill-maher-fat-90-year-old-r5.srt').write_bytes((O/'review/media/bill-maher-fat-90-year-old-r4.srt').read_bytes())
# Dense alpha-based hair measurements establish fixed panel overlap and safe framing; every keyed frame is measured.
hairs={};centres={};report={}
for p in json.loads((W/'plan.json').read_text())['pieces']:
 name=p['id'];a=[];cx=[]
 for k in range(p['n']):
  d=np.load(W/'key'/name/'c15'/f'f{k:04d}.npy');top,x=hair(d[...,3]);a.append(top);cx.append(x)
 hairs[name]=np.array(a);centres[name]=np.array(cx)
 report[name]={'frames_measured':p['n'],'hair_top_min':min(a),'hair_top_max':max(a),'hair_top_each_frame':a,'hair_centre_each_frame':cx}
# One fixed offset per continuous take. The lowest posture overlaps the panel by 28 px; no top-frame hair clipping.
ywatch=700-28-int(hairs['watching'].max());yresponse=700-28-round(hairs['response'].max()*1.25)
report['panel']={'rect':[0,92,1080,608],'foreground_offsets':{'watching':ywatch,'response':yresponse},'minimum_hair_overlap':28,'method':'full real alpha foreground composited last'}
(W/'hair-source-measurements.json').write_text(json.dumps(report,indent=2))
# Main portrait cuts: static windows, all from the complete source picture. Hair-top drives Y, never face boxes.
framing=[]
def crop_layer(name,k,width):
 height=round(width*16/9);hh=hairs[name];cy=min(260,int(hh.min())-45);cx=int(round(np.median(centres[name])));x=max(0,min(1080-width,cx-width//2));
 assert cy>=0 and cy+height<=1920
 Fp,a=clean(np.load(W/'key'/name/'c15'/f'f{k:04d}.npy'))
 Fp=Fp[cy:cy+height,x:x+width];a=a[cy:cy+height,x:x+width]
 framing.append({'g':g,'name':name,'crop':[x,cy,width,height],'hair_clearance':float((hh[k]-cy)*1920/height)})
 return cv2.resize(Fp,(1080,1920),interpolation=cv2.INTER_CUBIC),cv2.resize(a,(1080,1920),interpolation=cv2.INTER_CUBIC)
bill=subprocess.Popen([F,'-v','error','-ss','134','-i',str(O/'bill-maher-source.f398.mp4'),'-frames:v',str(PANEL_END),'-an','-vf','scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
pic=W/'full-picture.mp4';enc=subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads',os.environ.get('RENDERQ_CORES','4'),'-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(pic)],stdin=subprocess.PIPE)
table=np.asarray(Image.open(O/'bmi-table.png').convert('RGB'));proof=[];t0=time.time();bgframe=None;checks=[]
for g in range(N):
 t=g/FPS
 if g<PANEL_END:
  raw=bill.stdout.read(1280*720*3);assert len(raw)==1280*720*3;bf=np.frombuffer(raw,np.uint8).reshape(720,1280,3)
 if g<PANEL:
  # Full-screen source crop centred on Bill; Dan remains flush left/bottom with laptop.
  frame=cv2.resize(bf[:,417:822],(1080,1920),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
  Fp,a=clean(np.load(W/'key/watching/c15'/f'f{g:04d}.npy'));frame=place(frame,Fp,a,.4,0,1152,fade=(14+34*min(1,max(0,(g-94)/6))) if g>=94 else 14)
 elif g<PANEL_END:
  frame=np.zeros((1920,1080,3),np.uint8);frame[92:700]=cv2.resize(bf,(1080,608),interpolation=cv2.INTER_CUBIC)
  frame=C.apply(frame,g).astype(np.float32)/255
  name='watching' if g<OP else 'response';k=g if g<OP else g-OP
  Fp,a=clean(np.load(W/'key'/name/'c15'/f'f{k:04d}.npy'));oy=ywatch if name=='watching' else yresponse
  scale=1. if name=='watching' else 1.25
  ox=0 if name=='watching' else round(540-np.median(centres[name])*scale)
  frame=place(frame,Fp,a,scale,ox,oy)
  checks.append({'g':g,'hair_top':int(round(hairs[name][k]*scale))+oy,'panel_bottom':700,'overlap':700-int(round(hairs[name][k]*scale))-oy})
 elif g<BA or g>=BB:
  bgframe=next(field);frame=bgframe.astype(np.float32)/255
  name='response' if g<BA else 'ending';k=g-OP if g<BA else g-BB
  width=900 if g<971 or (g>=1139 and g<BA) or g>=BB else 800
  Fp,a=crop_layer(name,k,width);frame=place(frame,Fp,a)
  frame=C.apply((np.clip(frame,0,1)*255+.5).astype(np.uint8),g).astype(np.float32)/255
 else:
  frame=np.zeros((1920,1080,3),np.uint8);frame[240:1360,36:1044]=table
  # After viewers locate their height/weight, enlarge the category already printed in the table.
  if g>=1530:
   j=2 if g<1671 else 3;xx=24+j*246;crop=table[925:1029,xx:xx+228]
   # Table remains above; the category receives the emphasis at the words that name it.
   frame[240:1360,36:1044]=table[0,0]
   small=cv2.resize(table[:900],(1008,810),interpolation=cv2.INTER_AREA);frame[240:1050,36:1044]=small
   focus=cv2.resize(crop,(584,266),interpolation=cv2.INTER_CUBIC);frame[1068:1334,248:832]=focus
  frame=C.apply(frame,g).astype(np.float32)/255
 frame=(np.clip(frame,0,1)*255+.5).astype(np.uint8)
 ci=bisect.bisect_right(starts,t)-1
 if ci>=0 and t<caps[ci]['beat'][1]:
  if ci!=active:capimg=np.asarray(Image.open(caps[ci]['image']).convert('RGBA'));active=ci
  x,y=caps[ci]['pos'];h,w=capimg.shape[:2];frame[y:y+h,x:x+w]=over(frame[y:y+h,x:x+w],capimg)
 enc.stdin.write(np.ascontiguousarray(frame).tobytes())
 if g%30==0 or g in [119,120,587,588,905,906,970,971,1138,1139,1273,1274,1529,1530,1670,1671,1817,1818,1943]:
  p=D/f'frame-{g:04d}.jpg';cv2.imwrite(str(p),frame[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,96]);proof.append({'frame':g,'t':t,'path':str(p)})
 if g%120==0:print('render',g,N,round(time.time()-t0,1),flush=True)
enc.stdin.close();assert enc.wait()==0;assert bill.wait()==0
master=D/'bill-maher-fat-90-year-old-r5.mp4'
subprocess.run([F,'-y','-v','error','-i',str(pic),'-i',str(O/'review/media/bill-maher-fat-90-year-old-r4.mp4'),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(master)],check=True)
(W/'framing.json').write_text(json.dumps({'all_measured':True,'minimum_clearance':min(x['hair_clearance'] for x in framing),'frames':framing,'panel_foreground':checks},indent=2))
(W/'assembly.json').write_text(json.dumps({'master':str(master),'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'frames':N,'fps':FPS,'duration':N/FPS,'proof':proof,'visible_boundaries':[120/FPS,OP/FPS,906/FPS,971/FPS,1139/FPS,BA/FPS,1530/FPS,1671/FPS,BB/FPS],'audio_joins':[19.6196,55.7474],'audio':'AAC copied verbatim from R4 master; exact elementary-stream identity must be checked'},indent=2))
print('R5_RENDER_COMPLETE',flush=True)
