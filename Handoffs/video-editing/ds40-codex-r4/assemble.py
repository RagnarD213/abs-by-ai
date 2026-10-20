import sys,json,time,subprocess,hashlib,re,bisect,cv2,numpy as np
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import landing
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));from composite import Compositor,reader,over
sys.path.insert(0,str(R/'.claude/skills'));from _shared.deliver.checks import framing as FT
while not all((W/f).exists() for f in ['preparation-complete.json','response-key-complete.json','ending-key-complete.json']):time.sleep(5)
buildcap.wait('Bill Maher R4 full edit assembly and native crop tracking')
cv2.setNumThreads(2);D=W/'review/media';D.mkdir(parents=True,exist_ok=True)
P=json.loads((W/'plan.json').read_text());OPEN=P['opening_frames'];N=OPEN+686+544+126;BMIA=OPEN+686;BMIB=BMIA+544
M=json.loads((W/'graphics-manifest.json').read_text());M=[dict(m,kind=m.get('kind','overlay')) for m in M];C=Compositor(M,wh=(1080,1920))
def sample_crop(piece,n):
 fm=FT._facemesh();fd=FT._facefinder();samples=[];hair=[]
 for i,frame in enumerate(reader(str(W/(piece+'-light.mp4')),wh=(1080,1920))):
  if i%8 and i!=n-1 and not (piece=='response' and i==383):continue
  sm=cv2.resize(frame,(540,960),interpolation=cv2.INTER_AREA);L=FT._find_face(fm,fd,sm,540,960)
  if L is None:
   samples.append((i,float('nan')));continue
  L={k:(x*2,y*2) for k,(x,y) in L.items()};cx=(L[234][0]+L[454][0])/2;fw=abs(L[454][0]-L[234][0]);fh=L[152][1]-L[10][1]
  samples.append((i,cx));x0=max(0,int(cx-fw*.35));x1=min(1080,int(cx+fw*.35));y0=max(0,int(L[10][1]-fh*.65));y1=int(L[10][1])
  region=frame[y0:y1,x0:x1].astype(np.float32);field=np.median(frame[15:120,15:120].reshape(-1,3),axis=0)
  hit=(np.linalg.norm(region-field,axis=2)>18).mean(1)>.2;ys=np.where(hit)[0]
  if len(ys):hair.append((i,y0+int(ys[0])))
 fm.close();fd.close();nn=np.array([x[0] for x in samples]);xx=np.array([x[1] for x in samples]);assert np.isfinite(xx[0]),'Need actual first-frame head centre'
 holds=[(0,383,803,1426),(383,n,720,1280)] if piece=='response' else [(0,n,803,1426)]
 crops=np.zeros((n,4),float);reports=[]
 for n0,n1,width,height in holds:
  seg=[{'n0':n0,'n1':n1}];dn,centres,heads,info=landing.vertical_dense(nn,xx,seg,width,FPS)
  assert centres.min()-width/2>=0 and centres.max()+width/2<=1080,'Crop exceeds source'
  hh=[top for k,top in hair if n0<=k<n1];y=min(280,int(min(hh))-45);assert y>=0
  for k,cx in zip(dn,centres):crops[int(k)]=[round(cx-width/2),y,width,height]
  reports.append({'n0':n0,'n1':n1,'crop_width':width,'crop_height':height,'crop_y':y,'tracking':info,'statistics':landing.motion_stats(dn,heads,centres,seg,width,FPS)})
 report={'piece':piece,'pixel_space':'1080x1920 keyed source','head_samples':[[i,float(v) if np.isfinite(v) else None] for i,v in samples],'hair_samples':hair,'segments':reports}
 (W/(piece+'-framing.json')).write_text(json.dumps(report,indent=2));return crops
layouts={}
for name,n in [('response',686),('ending',126)]:layouts[name]=sample_crop(name,n)
# Captions are emitted as the actual PNG alpha states used by this compositor.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86)
words=json.loads((W/'words-aligned.json').read_text())['words'];words[0]=dict(words[0],t=.260,src='direct_final_AAC_CTC_and_native_RMS_onset');chunks=[];cur=[]
def clean(ws):
 s=' '.join(x['w'].strip() for x in ws);s=re.sub(r'\s+([.,!?%])',r'\1',s);s=re.sub(r'\bABS\b','abs',s);return s
def wrap(s):
 out=[];line=''
 for w in s.split():
  test=(line+' '+w).strip()
  if font.getlength(test)>910 and line:out.append(line);line=w
  else:line=test
 if line:out.append(line)
 return out
for i,w in enumerate(words):
 if cur and (len(cur)>=4 or (cur[0]['t']<P['opening_seconds'] and font.getlength(clean(cur+[w]))>910) or len(wrap(clean(cur+[w])))>2 or w['t']-cur[-1]['e']>.6):chunks.append(cur);cur=[]
 cur.append(w)
 if re.search(r'[.!?]$',w['w']):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
cd=W/'caption-states';cd.mkdir(exist_ok=True);caps=[]
for i,ch in enumerate(chunks):
 a=ch[0]['t'];nexta=chunks[i+1][0]['t'] if i+1<len(chunks) else N/FPS
 b=min(max(ch[-1]['e']+.10,a+.28),nexta-.008,P['opening_seconds'] if a<P['opening_seconds'] else N/FPS);lines=wrap(clean(ch));height=112*len(lines)+30
 im=Image.new('RGBA',(1000,height));dr=ImageDraw.Draw(im)
 for j,s in enumerate(lines):
  x=(1000-font.getlength(s))/2;y=4+j*112
  dr.text((x+3,y+3),s,font=font,fill=(0,0,0,180),stroke_width=7,stroke_fill=(0,0,0,180))
  dr.text((x,y),s,font=font,fill='white',stroke_width=7,stroke_fill='black')
 path=cd/f'caption-{i:03}.png';im.save(path);pos=[40,850 if a<P['opening_seconds'] else 1440]
 caps.append({'id':i,'beat':[round(a,3),min(round(b,3),int(P['opening_seconds']*1000)/1000) if a<P['opening_seconds'] else round(b,3)],'image':str(path),'image_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pos':pos,'word':clean(ch),'word_indices':[words.index(ch[0]),words.index(ch[-1])],'rect':[pos[0],pos[1],pos[0]+1000,pos[1]+height]})
(W/'caption-states.json').write_text(json.dumps(caps,indent=2))
def srt_time(t):
 z=round(t*1000);return f'{z//3600000:02}:{z//60000%60:02}:{z//1000%60:02},{z%1000:03}'
(D/'bill-maher-fat-90-year-old-r4.srt').write_text('\n\n'.join(f"{i+1}\n{srt_time(c['beat'][0])} --> {srt_time(c['beat'][1])}\n{c['word']}" for i,c in enumerate(caps))+'\n')
watch=reader(str(W/'watching-light.mp4'),wh=(1080,1920));tail=reader(str(W/'watching-tail-light.mp4'),start=2,wh=(1080,1920))
resp=reader(str(W/'response-light.mp4'),wh=(1080,1920));end=reader(str(W/'ending-light.mp4'),wh=(1080,1920))
bill=subprocess.Popen([F,'-v','error','-ss',str(P['bill_source_start']),'-i',str(W/'bill-maher-source.f398.mp4'),'-frames:v',str(OPEN),'-an','-vf','crop=880:720:200:0,scale=1080:884:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
picture=W/'full-picture.mp4';enc=subprocess.Popen([F,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30000/1001','-i','-','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads','3','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE)
table=np.asarray(Image.open(W/'bmi-table.png').convert('RGB'));capstarts=[c['beat'][0] for c in caps];active=-1;capimg=None;t=time.time();proof=[]
for g in range(N):
 if g<OPEN:
  raw=bill.stdout.read(1080*884*3);assert len(raw)==1080*884*3
  frame=np.empty((1920,1080,3),np.uint8);frame[:]=np.array([.84,.87,.89])*255;frame[:884]=np.frombuffer(raw,'uint8').reshape(884,1080,3)
  wf=next(watch) if g<538 else next(tail);field=np.median(wf[20:100,20:100].reshape(-1,3),axis=0);frame[884:]=field;frame[930:1920]=wf[260:1250]
 elif g<BMIA:
  j=g-OPEN;src=next(resp);x,y,w,h=map(int,layouts['response'][j]);frame=cv2.resize(src[y:y+h,x:x+w],(1080,1920),interpolation=cv2.INTER_CUBIC)
 elif g<BMIB:
  frame=np.zeros((1920,1080,3),np.uint8);frame[240:1360,36:1044]=table
 else:
  j=g-BMIB;src=next(end);x,y,w,h=map(int,layouts['ending'][j]);frame=cv2.resize(src[y:y+h,x:x+w],(1080,1920),interpolation=cv2.INTER_CUBIC)
 frame=C.apply(frame,g)
 ci=bisect.bisect_right(capstarts,g/FPS)-1
 if ci>=0 and g/FPS<caps[ci]['beat'][1] and (g<OPEN or caps[ci]['beat'][0]>=P['opening_seconds']):
  if active!=ci:capimg=np.asarray(Image.open(caps[ci]['image']).convert('RGBA'));active=ci
  x,y=caps[ci]['pos'];h,w=capimg.shape[:2];frame[y:y+h,x:x+w]=over(frame[y:y+h,x:x+w],capimg)
 enc.stdin.write(np.ascontiguousarray(frame).tobytes())
 if g%30==0 or g in [OPEN-1,OPEN,BMIA-1,BMIA,BMIB-1,BMIB,N-1]:
  path=D/f'frame-{g:04}.jpg';cv2.imwrite(str(path),frame[:,:,::-1],[cv2.IMWRITE_JPEG_QUALITY,96]);proof.append({'frame':g,'time':g/FPS,'path':str(path)})
 if g%150==0:print('assemble',g,N,round(time.time()-t,1),flush=True)
enc.stdin.close();assert enc.wait()==0;assert bill.wait()==0
master=D/'bill-maher-fat-90-year-old-r4.mp4'
subprocess.run([F,'-y','-v','error','-i',str(picture),'-i',str(W/'mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',str(master)],check=True)
(W/'assembly.json').write_text(json.dumps({'master':str(master),'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'frames':N,'fps':FPS,'duration':N/FPS,'proof':proof,'boundaries':[OPEN/FPS,(OPEN+383)/FPS,BMIA/FPS,BMIB/FPS],'audio_joins':[P['opening_seconds'],P['opening_seconds']+1436.36-1400.2322],'caption_states':str(W/'caption-states.json'),'framing':['response-framing.json','ending-framing.json']},indent=2))
print('FULL EDIT ASSEMBLED',flush=True)
