from pathlib import Path
import os,sys,json,subprocess,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=W/'round2';os.chdir(O)
sys.path.insert(0,str(O/'recipe'));import cards
SH=R/'.claude/skills/_shared';sys.path[:0]=[str(SH),str(SH/'hyperframes'),str(SH/'cut')]
import buildcap,softblue as B,composite as CP,vertical as V,landing
from motionlib import font
FF=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;FD=1/FPS
original_cut=json.load(open(W/'cut.json'));cut=json.loads(json.dumps(original_cut));LEAD_FRAMES=18;LEAD=LEAD_FRAMES/FPS
N=round((cut['dur']+.6)*FPS)-LEAD_FRAMES;end=N/FPS
for pi,p in enumerate(cut['pieces']):
 p['t_in']=max(0,p['t_in']-LEAD);p['t_out']-=LEAD
 if pi==0:p['src_in']+=LEAD
cut['dur']-=LEAD
assert json.load(open(O/'asset-context-review.json'))['verdict']=='PASS','Exact isolated assets must pass editor review first'
T=json.load(open(O/'track-all.json'));ws=[dict(x,t=x['t']-LEAD,e=x['e']-LEAD) for x in json.load(open(O/'words_individual.json'))['words']]
grade=json.load(open(W/'grade-options.json'))['B']['filter'];roll=json.load(open(W/'source/roll.json'))['identity']['current_path']
for d in ('final','seg9','seg16','cap9/png','cap16/png','logs'): (O/d).mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(cmd):subprocess.run(cmd,check=True)
def wait(name):buildcap.wait('RA-13 R2 '+name)
def enc(frames,path,wh):
 p=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{wh[0]}x{wh[1]}','-framerate','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(path)],stdin=subprocess.PIPE)
 for fr in frames:p.stdin.write(np.asarray(fr,dtype=np.uint8).tobytes())
 p.stdin.close();assert p.wait()==0
# Named filming pieces with complete words. P1 covers all of the 0.34-second intermediate take.
A1CFG=json.load(open(O/'analysis-config.json'))[0]
A1A,A1B=A1CFG['a']-LEAD,A1CFG['b']-LEAD
P2B=next(x['t'] for x in ws if x['w'].lower()=='and' and 38.5<x['t']<39.5)
slots=[('cam0',0,0,2.87-LEAD,'FAR'),('cam1',1,2.87-LEAD,14.948-LEAD,'NEAR'),('P1',None,14.948-LEAD,25.759-LEAD,'CARD'),('cam5',5,25.759-LEAD,A1A,'NEAR'),('A1',None,A1A,A1B,'CARD'),('P2',None,A1B,P2B,'CARD'),('cam7',7,P2B,43.21-LEAD,'FAR'),('cam8',8,43.21-LEAD,47.18-LEAD,'NEAR'),('cam9',9,47.18-LEAD,end,'FAR')]
# The narrow slots where source CTC/audio piece edge differs are covered by a card; no presenter flashes.
slots=[dict(name=name,piece=pi,f0=round(a*FPS),f1=round(b*FPS),a=round(a*FPS)/FPS,b=round(b*FPS)/FPS,level=lv) for name,pi,a,b,lv in slots]
for a,b in zip(slots,slots[1:]):assert a['f1']==b['f0']
assert slots[0]['f0']==0 and slots[-1]['f1']==N
# Camera frames are sampled at their ACTUAL new return frame when an asset splits a filmed piece.
def exact_head(src,tag):
 import mediapipe as mp
 raw=subprocess.run([FF,'-nostdin','-v','error','-ss',str(src),'-i',roll,'-frames:v','1','-vf',grade+',scale=1080:1920','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True).stdout
 a=np.frombuffer(raw,np.uint8).reshape(1920,1080,3)
 with mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,min_detection_confidence=.4) as mesh:
  fr=mesh.process(a)
  if fr.multi_face_landmarks:
   lm=fr.multi_face_landmarks[0].landmark;return (lm[234].x+lm[454].x)*1080
  with mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=.4) as detector:
   ds=detector.process(a)
   if not ds.detections:raise RuntimeError('Missing exact cut head '+tag)
   b=ds.detections[0].location_data.relative_bounding_box;cx=(b.xmin+b.width/2)*1080;cy=(b.ymin+b.height/2)*1920;side=max(b.width*1080,b.height*1920)*2.2
   x0,y0=int(max(0,cx-side/2)),int(max(0,cy-side/2));x1,y1=int(min(1080,cx+side/2)),int(min(1920,cy+side/2));fr=mesh.process(np.ascontiguousarray(a[y0:y1,x0:x1]))
   if not fr.multi_face_landmarks:raise RuntimeError('Cannot mesh exact head '+tag)
   lm=fr.multi_face_landmarks[0].landmark;return ((lm[234].x+lm[454].x)/2*(x1-x0)+x0)*2

def crop_expr(ni,x,cw):
 e=str(float(x[-1])-cw/2)
 for j in range(len(ni)-2,-1,-1):
  a,b=int(ni[j]),int(ni[j+1]);xa,xb=float(x[j])-cw/2,float(x[j+1])-cw/2
  e=f'if(lt(n,{b}),{xa:.4f}+({xb-xa:.4f})*(n-{a})/{max(1,b-a)},{e})'
 return e
framing=[]
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 wait('camera segments '+fmt)
 for s in slots:
  if s['piece'] is None:continue
  p=cut['pieces'][s['piece']];src0=p['src_in']+max(0,s['a']-p['t_in']);n=s['f1']-s['f0'];avail=p['src_out']-src0
  close=s['level']=='NEAR';cw,ch=((630,1120) if close else (738,1312)) if fmt=='9' else ((1728,972) if close else (2144,1206))
  vals=[q for q in T if q['piece']==s['piece']];assert vals,'Missing dense source measurements'
  ns=np.array([q['frame']*6 for q in vals]);rawx=np.array([q['cx'] for q in vals]);off=round((src0-original_cut['pieces'][s['piece']]['src_in'])*FPS)
  use=np.arange(0,max(1,min(n,round(avail*FPS))),6);raw=np.interp(use+off,ns,rawx)
  if off:raw[0]=exact_head(src0,s['name'])
  ni,x,info=landing.vertical_track(use,raw,[dict(n0=0,n1=n)],cw,FPS) if fmt=='9' else (use,np.full(len(use),1080.),{})
  if fmt=='9':info.update(landing.motion_stats(ni,np.interp(ni,use,raw),x,[dict(n0=0,n1=n)],cw,FPS))
  hair=min(q['hair'] for q in vals)
  y=1240 if fmt=='9' or not close else 1260
  assert hair-y>=18,f'{s["name"]}: headroom would clip ({hair}, {y}); repair before render'
  vf=grade+f",crop={cw}:{ch}:'{crop_expr(ni,x,cw)}':{y},scale={wh[0]}:{wh[1]}:flags=lanczos,setsar=1"
  if s['name']=='cam9' and avail<n/FPS:vf+=f',tpad=stop_mode=clone:stop_duration={n/FPS-avail+.05}' # only the approved 0.6 s ending after speech
  dst=O/f'seg{fmt}/{s["name"]}.mp4'
  run([FF,'-nostdin','-v','error','-y','-ss',str(src0),'-i',roll,'-vf',vf,'-frames:v',str(n),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv',str(dst)])
  framing.append(dict(format=fmt,name=s['name'],src0=src0,n=n,crop=[cw,ch],y=y,min_hair=hair,min_gap=hair-y,motion=info,path=str(dst)))
json.dump(framing,open(O/'framing.json','w'),indent=2)
# Horizontal phone cards are redrawn from the SAME source frames. Never crop a portrait composite into 16:9.
spec=importlib.util.spec_from_file_location('shared_phone_helpers',R/'.claude/skills/ad-edit/reference/ra14/s63_stills.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
# The common helper builds a credible modern phone; the 16:9 placement uses its same shell.
def phone16(t,screen,chip=None):
 im=B.field(t,1920,1080).convert('RGBA');body=S.phone_shell();scr=screen.resize((518,982),Image.Resampling.LANCZOS)
 mask=Image.new('L',(518,982));ImageDraw.Draw(mask).rounded_rectangle((0,-60,517,981),56,fill=255);body.paste(scr,(48,114),mask)
 body=body.resize((400,827),Image.Resampling.LANCZOS);im.alpha_composite(body,(760,40))
 if chip:B.disclosure(im,chip,xy=(960,888),anchor='mt',size=20)
 return im.convert('RGB')
def decode(path,t,n,wh,crop=None):
 vf='scale=in_color_matrix=bt709:in_range=tv,'+(f'crop={crop},' if crop else '')+f'fps=30000/1001,scale={wh[0]}:{wh[1]},format=rgb24'
 b=subprocess.run([FF,'-nostdin','-v','error','-ss',str(t),'-i',str(path),'-frames:v',str(n),'-vf',vf,'-f','rawvideo','-'],capture_output=True,check=True).stdout
 return np.frombuffer(b,np.uint8).reshape(-1,wh[1],wh[0],3)
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 wait('clean phone cards '+fmt)
 for s in slots:
  if s['name'] not in ('P1','P2'):continue
  n=s['f1']-s['f0'];a=s['a']
  if s['name']=='P1':
   nn=round(1.57*FPS);scr=decode(S.DEMO,2.0,nn,(434,940),'434:940:741:68')
   def gen():
    for i in range(n):
     t=a+i/FPS
     if i<nn:yield cards.phone(t,Image.fromarray(S.square_corners(scr[i])),fmt,'Real picture of me. Not AI-generated.' if 2.0+i/FPS>=2.6 else None,room_for_label=True)[0]
     else:yield cards.goal(1+(i-nn)/FPS,fmt)[0]
  else:
   nn=round(2*FPS);s1=decode(S.TOUR,6,nn,(432,920));s2=decode(S.TOUR,2.05,n-nn,(432,920))
   def gen():
    for i in range(n):yield cards.phone(a+i/FPS,Image.fromarray(s1[i] if i<nn else s2[i-nn]),fmt)[0]
  enc(gen(),O/f'media/{s["name"]}-{fmt}.mp4',wh)
# Build shared CTA in each aspect, at the recorded CTA words. No ending URL.
cta_a=next(x['t'] for x in ws if x['w'].lower()=='tap');cta_b=end;man={}
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 wait('shared CTA '+fmt)
 if fmt=='9':mod=V
 else:
  sp=importlib.util.spec_from_file_location('horizontal_cta_layout',SH/'hyperframes/vertical.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);mod.W,mod.Hh=wh;mod.CANVAS=list(wh);mod.U=2.;import types;mod.B=types.SimpleNamespace(**{**vars(B),'lower_third_default_box':lambda w,h,nlines=1:(430,0,1490,0)})
 # Avoid altering any shared module globals by loading an isolated instance above.
 scenes,meta=mod.cta_scenes('CTA',cta_b-cta_a,'Tap The Button Below','Get Started',hold_out=True)
 layout=json.load(open(O/'cta-layout.json'))[fmt];x,y,bw,bh=layout['box'];toppx,bigpx=layout['top_px'],layout['big_px'];H=mod.H;bx=x+(bw-H.text_w('Get Started',bigpx)-56)/2
 for _,c,_ in scenes:
  c['canvas']=list(wh);c['btn']=[x,y,bw,bh];c['radius']=layout['radius'];c['top']=dict(x=round(x+(bw-H.text_w('Tap The Button Below',toppx))/2),y=y+layout['top_offset'],px=toppx,s='Tap The Button Below');c['big']=dict(x=round(bx),y=y+layout['big_offset'],px=bigpx,s='Get Started');c['arrow']=dict(x=round(bx+H.text_w('Get Started',bigpx)+22),y=y+layout['big_offset'],px=bigpx)
 meta.update(box=[x,y,x+bw,y+bh],band=[y-12,y+bh+12])
 mod.build(scenes,O/f'cta{fmt}',render=True)
 mov=O/f'cta{fmt}/renders/CTA.mov';mask=O/f'cta{fmt}/renders/CTA_mask.mov'
 man[fmt]=[dict(id='A1',a=A1A,b=A1B,kind='opaque',mov=str(O/('hf9/renders/A1.mov' if fmt=='9' else 'hf16/A1.mov'))),dict(id='CTA',a=cta_a,b=cta_b,kind='glass',mov=str(mov),mask=str(mask),**{k:v for k,v in meta.items() if k!='kind'})]
 json.dump(man[fmt],open(O/f'hf-manifest{fmt}.json','w'),indent=2)
# Caption PNG states are the actual compositor input, one highlighted word per state.
def captions(fmt,wh):
 groups=[];g=[]
 for w in ws:
  if g and (len(' '.join(q['w'] for q in g+[w]))>22 or g[-1]['w'].endswith(('.', '?','!'))):groups.append(g);g=[]
  g.append(w)
 if g:groups.append(g)
 F=font(64,'ExtraBold');cy=1400 if fmt=='9' else 930;states=[]
 for gi,g in enumerate(groups):
  stop=min(g[-1]['e']+.7,groups[gi+1][0]['t'] if gi+1<len(groups) else end)
  txt=' '.join(q['w'] for q in g)
  for k,w in enumerate(g):
   a=w['t'];b=g[k+1]['t'] if k+1<len(g) else stop;f0,f1=round(a*FPS),round(b*FPS)
   if f1<=f0:continue
   im=Image.new('RGBA',wh);sh=Image.new('RGBA',wh);tw=F.getlength(txt);x=(wh[0]-tw)/2;baseline=cy+F.getmetrics()[0]
   ImageDraw.Draw(sh).text((int(x),baseline),txt,font=F,fill=(0,0,0,245),anchor='ls');im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)));d=ImageDraw.Draw(im);cx=x
   for j,word in enumerate(txt.split(' ')):
    d.text((int(cx),baseline),word,font=F,fill=((104,197,255) if j==k else (255,255,255))+(255,),anchor='ls');cx+=F.getlength(word+' ')
   path=O/f'cap{fmt}/png/{len(states):04d}.png';im.save(path);states.append(dict(name=f'cap{len(states):04d}',beat=[f0/FPS,f1/FPS],f0=f0,f1=f1,image=str(path),image_sha256=sha(path),rect=[0,0,*wh],word=w['w']))
 json.dump({'states':states},open(O/f'cap{fmt}/caption_states.json','w'),indent=1)
 def ts(t):return f'{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}'.replace('.',',')
 text='\n\n'.join(f'{i+1}\n{ts(g[0]["t"])} --> {ts(min(g[-1]["e"]+.7,groups[i+1][0]["t"] if i+1<len(groups) else end))}\n'+ ' '.join(q['w'] for q in g) for i,g in enumerate(groups))+'\n';(O/f'cap{fmt}/captions.srt').write_text(text)
 return states
json.dump(dict(frames=N,duration=end,lead_trim_frames=LEAD_FRAMES,lead_trim_seconds=LEAD,cut=cut,words=ws,slots=slots,framing=framing,manifests=man,stage='components_ready'),open(O/'build-record.json','w'),indent=2)
mix_ready=False
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 wait('complete composite '+fmt);states=captions(fmt,wh);C=CP.Compositor(man[fmt],wh=wh);g=0;ci=0;cache=None;laststate=None
 def frames():
  global g,ci,cache,laststate
  for s in slots:
   n=s['f1']-s['f0']
   if s['piece'] is not None:path=O/f'seg{fmt}/{s["name"]}.mp4'
   elif s['name']=='A1':path=None
   elif fmt=='9':path=O/f'media/{s["name"]}-9.mp4'
   else:path=O/f'media/{s["name"]}-16.mp4'
   rd=CP.reader(str(path),wh=wh) if path else None
   for i in range(n):
    base=next(rd,None) if rd else np.zeros((wh[1],wh[0],3),np.uint8)
    assert base is not None,f'{s["name"]} missing native frame {i}'
    fr=C.apply(base,g)
    while ci<len(states) and g>=states[ci]['f1']:ci+=1
    if ci<len(states) and states[ci]['f0']<=g<states[ci]['f1']:
     if ci!=laststate:cache=np.array(Image.open(states[ci]['image']).convert('RGBA'));laststate=ci
     fr=CP.over(fr,cache)
    yield fr;g+=1
   if rd:rd.close()
  assert g==N
 pic=O/f'final/picture{fmt}.mp4';enc(frames(),pic,wh)
 if not mix_ready:
  run([FF,'-nostdin','-v','error','-y','-i',str(W/'cut_audio.wav'),'-af',f'atrim=start={LEAD},asetpts=PTS-STARTPTS','-c:a','pcm_s16le',str(O/'audio/cut_trim.wav')])
  assert 'words=[]' in (W/'logs/r2-music-listen.txt').read_text()
  eq=json.load(open(W/'audio-options/lighter-bass.wav.voice_chain.json'))['eq']
  run([sys.executable,str(SH/'audio/voice_chain.py'),'--in',str(O/'audio/cut_trim.wav'),'--out',str(O/'audio/mix.wav'),'--eq',eq,'--bed','/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3','--bed-db','-32','--frame-lock',str(pic),'--work',str(O/'audio/work-mix')])
  mix_ready=True
 target=O/f'final/why do most guys never get abs | codex | {"9x16" if fmt=="9" else "16x9"} | RA-13 R2.mp4'
 run([FF,'-nostdin','-v','error','-y','-i',str(pic),'-i',str(O/'audio/mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(end),'-movflags','+faststart',str(target)])
 print('CANDIDATE',target,N,end,flush=True)
json.dump(dict(frames=N,duration=end,lead_trim_frames=LEAD_FRAMES,lead_trim_seconds=LEAD,cut=cut,words=ws,slots=slots,framing=framing,manifests=man),open(O/'build-record.json','w'),indent=2)
print('FULL CANDIDATES READY',flush=True)
