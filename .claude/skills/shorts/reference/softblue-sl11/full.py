"""CONTENT SFL SL-11. Full Shorts from approved RO02 + Dan's explicitly approved ownvoice Natural pickup.
Own work only. Source files read-only. Commands: prepare, gfx, render [A B C]."""
from pathlib import Path
import sys,os,json,math,re,wave,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/hyperframes'));sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'))
import composite as HC,hfbuild as H,vertical as V,renderq
import frames as F,edl as E
E.SHOOT='/Volumes/Expansion/Abs By AI Raw Footage/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose'
FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FPS=30000/1001;SR=48000
MASTER=ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4'
WORDS=json.loads(Path('/Volumes/Extreme/_edit_work/ro02/words_out.json').read_text())
SEG={'A':[(385.106,394.146),(446.586,482.824)],'B':[(487.305,522.724),(575.618,583.538),(590.378,593.157)],'C':[(552.705,599.998)]}
TITLES={'A':['How To Do A Standing','Stomach Vacuum'],'B':['Stop Holding Your Breath','During Stomach Vacuums'],'C':['Start With One','20-Second Vacuum']}
PICKUP="Here's a mistake I see with a lot of beginners when they first start doing stomach vacuums."
FONT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86)
TINY=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rd(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float64).reshape(-1,w.getnchannels())/32768

def wr(p,x):
 with wave.open(str(p),'wb') as w:w.setparams((2,2,SR,0,'NONE','not compressed'));w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
def pcm(a,b):
 z=subprocess.check_output([FF,'-nostdin','-v','error','-ss',str(a),'-i',str(MASTER),'-t',str(b-a),'-vn','-ac','2','-ar',str(SR),'-f','s16le','-'])
 return np.frombuffer(z,'<i2').astype(np.float64).reshape(-1,2)/32768

def words_in(a,b):return [dict(w=z['w'],t=z['t0']-a,e=min(z.get('t1') or z['t0']+.1,b)-a) for z in WORDS if z.get('t0') is not None and a<=z['t0']<b]
def source(t):
 sh=F.shot_at(t);raw=(sh['src_f0']+t*FPS-sh['out_f0'])/FPS
 return sh,raw

def crop(sh,near=False):
 arr=np.array(F.M[sh['piece']]);tops=np.sort(arr[:,1]);med=np.median(tops);good=tops[tops>=med-36] if (tops<med-36).mean()<.15 else tops
 h=840 if near else 1040;y=max(0,min(1080-h,round(float(good.min())-.04*h)));w=round(h*1080/1610);cx=float(np.median(arr[:,2]));x=round(max(0,min(1920-w,cx-w/2)))
 return [x,y,w,h]
def picshots(S,T):
 """Native raw shots; parent's artificial camera punches are not extra raw cuts."""
 N=T['frames'];shots=[];end=N/FPS;demo_end=json.loads((R/'demo-range.json').read_text())['raw_end'] if (R/'demo-range.json').exists() else 58.0
 demo_dur=demo_end-1001/FPS
 if S=='A': blocks=[(0,2.5,'demo',36.0,False),(2.5,T['seg'][1]['a'],'talk',None,True),(T['seg'][1]['a'],13.5,'talk',None,False),(13.5,13.5+demo_dur,'demo',1001/FPS,False),(13.5+demo_dur,T['seg'][1]['a']+477.643833333-446.586,'talk',None,False),(T['seg'][1]['a']+477.643833333-446.586,end,'talk',None,True)]
 elif S=='B':
  rest=T['seg'][2]['a'];start=rest+3.5-demo_dur
  blocks=[(0,180/FPS,'demo',36.0,False),(180/FPS,start,'talk',None,True),(start,rest+3.5,'demo',1001/FPS,False),(rest+3.5,T['seg'][3]['a'],'talk',None,True),(T['seg'][3]['a'],end,'talk',None,False)]
 else:blocks=[(0,2.5,'demo',36.0,True),(2.5,5.5,'talk',None,True),(5.5,5.5+demo_dur,'demo',1001/FPS,False),(5.5+demo_dur,34.98,'talk',None,True),(34.98,end,'talk',None,False)]
 for a,b,kind,raw0,near in blocks:
  f0=round(a*FPS);f1=min(N,round(b*FPS));a=f0/FPS;b=f1/FPS
  if f1<=f0:continue
  if kind=='demo':
   sh=F.shot_at(535);cr=[595,40,698,1040] if not near else [662,40,563,840]
   shots.append(dict(f0=f0,f1=f1,kind=kind,roll='C1625',raw0=raw0,raw1=raw0+(f1-f0)/FPS,crop=cr,lut=F.lut(sh),parent=None,level='EXERCISE',complete=raw0<34))
  else:
   f=f0
   while f<f1:
    seg=next(z for z in T['seg'] if z['a']-1e-5<=f/FPS<z['b']-1e-5)
    assert seg['kind']=='parent'
    t=seg['parent_a']+f/FPS-seg['a'];sh,raw=source(t)
    lim=min(f1,round((seg['a']+sh['out_f1']/FPS-seg['parent_a'])*FPS),round(seg['b']*FPS));assert lim>f
    row=dict(f0=f,f1=lim,kind='talk',roll=sh['roll'],raw0=raw,raw1=raw+(lim-f)/FPS,crop=crop(sh,near),lut=F.lut(sh),parent=t,level='NEAR' if near else 'FAR')
    # Merge only truly contiguous raw frames and identical framing/grade.
    if shots and all(shots[-1].get(k)==row[k] for k in ['kind','roll','crop','lut','level']) and abs(shots[-1]['raw1']-raw)<.001:
     shots[-1]['f1']=lim;shots[-1]['raw1']=row['raw1']
    else:shots.append(row)
    f=lim
 for i,s in enumerate(shots):s['idx']=i
 assert shots[0]['f0']==0 and shots[-1]['f1']==N and all(x['f1']==y['f0'] for x,y in zip(shots,shots[1:]))
 return shots

def prepare(S):
 d=R/'build'/S;d.mkdir(exist_ok=True);pieces=[];seg=[];cursor=0;words=[]
 if S=='B':
  pickup=json.loads((R/'audio/pickup-choice.json').read_text());z=rd(Path(pickup['file']));n=round(math.ceil(len(z)/SR*FPS-1e-8)/FPS*SR);z=np.pad(z,((0,n-len(z)),(0,0)));overlap=2880
  # Match the tested audition: final quiet60ms overlaps the parent's100ms preroll.
  parent=pcm(*SEG[S][0]);z[-overlap:]=z[-overlap:]*np.linspace(1,0,overlap)[:,None]+parent[:overlap]*np.linspace(0,1,overlap)[:,None]
  pieces.append(z);cursor=n/SR;seg.append(dict(kind='pickup',a=0,b=cursor,text=PICKUP,audio_start=0,audio_end=cursor))
 for pi,(a,b) in enumerate(SEG[S]):
  z=pcm(a,b)
  if S=='B' and pi==0:
   z=z[2880:];a+=.06
  # Only tiny fades inside selected audio edges; no compression/EQ on approved parent mix.
  z[:240]*=np.linspace(0,1,240)[:,None];z[-240:]*=np.linspace(1,0,240)[:,None]
  f0=round(cursor*FPS);f1=math.ceil((cursor+len(z)/SR)*FPS-1e-7);dur=(f1-f0)/FPS
  desired=round(dur*SR);z=np.pad(z,((0,max(0,desired-len(z))),(0,0)))[:desired]
  ws=words_in(a,b);seg.append(dict(kind='parent',a=cursor,b=cursor+len(z)/SR,parent_a=a,parent_b=b,text=' '.join(w['w'] for w in ws),audio_start=cursor,audio_end=cursor+len(z)/SR))
  pieces.append(z);cursor+=len(z)/SR
 allx=np.concatenate(pieces);N=math.ceil(len(allx)/SR*FPS-1e-8);need=round(N/FPS*SR);allx=np.pad(allx,((0,max(0,need-len(allx))),(0,0)))[:need];seg[-1]['b']=N/FPS
 wr(d/'his_mix.wav',allx);T=dict(frames=N,seconds=N/FPS,seg=seg,audio_joins=[z['a'] for z in seg[1:]],scope='Parent mix preserved by cuts; B explicit ownvoice pickup choice recorded in audio/pickup-choice.json');dump(d/'timeline.json',T)
 # Inherited source cuts remain audio joins even under continuous exercise cover.
 subprocess.run([sys.executable,str(R/'recipe/audio_joins.py'),S],check=True)
 T=json.loads((d/'timeline.json').read_text())
 # Force-align each exact speech piece. No ASR-selected text or guessed pickup timing.
 import torch,torchaudio,scipy.signal as ss
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H;model=bundle.get_model().eval();L={c:i for i,c in enumerate(bundle.get_labels())}
 out=[];numbers={'20':'TWENTY','20-second':'TWENTY SECOND'}
 for p,z in enumerate(seg):
  tokens=z['text'].split();ids=[];owners=[]
  for k,w in enumerate(tokens):
   w=numbers.get(w.lower().strip('.,'),w);txt=re.sub("[^A-Z' ]",'',w.upper().replace('-',' ')).strip();assert txt,(S,w)
   for c in txt.replace(' ','|'):ids.append(L[c]);owners.append(k)
   ids.append(L['|']);owners.append(-1)
  ids=ids[:-1];owners=owners[:-1];arr=allx[round(z['a']*SR):round(z['b']*SR)].mean(1);xx=torch.from_numpy(ss.resample_poly(arr,1,3).astype(np.float32)).unsqueeze(0)
  with torch.inference_mode():em,_=model(xx);em=em.log_softmax(-1)
  ali,sc=torchaudio.functional.forced_align(em,torch.tensor([ids],dtype=torch.int32),blank=0);spans=torchaudio.functional.merge_tokens(ali[0],sc[0].exp());ratio=xx.shape[1]/em.shape[1]/16000;per={}
  assert len(spans)==len(owners)
  for j,sp in enumerate(spans):
   k=owners[j]
   if k<0:continue
   per.setdefault(k,[z['a']+sp.start*ratio,z['a']+sp.end*ratio,[]]);per[k][1]=z['a']+sp.end*ratio;per[k][2].append(float(sp.score))
  for k,w in enumerate(tokens):out.append(dict(w=w,t=round(per[k][0],4),e=round(per[k][1],4),p=p,score=round(float(np.mean(per[k][2])),3)))
 dump(d/'words.json',out);dump(d/'shots.json',picshots(S,T));print('PREPARED',S,N,N/FPS,len(out),'words',flush=True)

def graphics(S):
 d=R/'build'/S;T=json.loads((d/'timeline.json').read_text());out=d/'hf';cfg=dict(id='TITLE-'+S,dur=math.ceil(T['seconds'])+3,drift=-2,canvas=[1080,310],line_px=68,accent=[64,52,8],eyebrow=dict(x=88,y=38,px=30,s='STOMACH VACUUM'),lines=[])
 while max(H.text_w(s,cfg['line_px']) for s in TITLES[S])>952:cfg['line_px']-=2
 cfg['lines']=[dict(x=64,y=86+i*96,s=s) for i,s in enumerate(TITLES[S])];V.build([(R/'recipe/title-band.template.htm',cfg,())],out,snap=2,check=True)
 def at(parent):
  z=next(s for s in T['seg'] if s['kind']=='parent' and s['parent_a']<=parent<s['parent_b']);return z['a']+parent-z['parent_a']
 rawspec={'A':[('A-step2',453.75,6,'STEP 2','Draw In And Hold',1130),('A-step3',464.95,6,'STEP 3','Use Time, Not Guesswork',1370)],'B':[('B-breaths',507.2,6,'DURING THE HOLD','Small Breaths Through Your Nose',1130),('B-recover',578.5,5,'BETWEEN SETS','Recover With Deep Breaths',1370)],'C':[('C-routine',563.1,7,'BUILD UP GRADUALLY','One Set, Then Two, Then Three',1370),('C-recover',578.5,5,'BETWEEN SETS','Recover With Deep Breaths',1370)]}[S]
 spec=[(id,at(parent),dur,topic,point,y) for id,parent,dur,topic,point,y in rawspec]
 man=[]
 for id,a,dur,topic,point,y in spec:
  cfg=dict(id=id,a=a,b=min(T['seconds'],a+dur),topic=topic,topic_case='preserve',parts=[[point,a+.25]],top_y=y,drift=-4)
  scenes,meta=V.lt_scenes(cfg);V.build(scenes,out,snap=2,check=True);man.append(dict(id=id,a=round(a*FPS)/FPS,b=round(cfg['b']*FPS)/FPS,mov=str(out/'renders'/f'{id}.mov'),mask=str(out/'renders'/f'{id}_mask.mov'),**meta))
 dump(d/'graphics.json',man);print('GRAPHICS',S,flush=True)

def cues(S):
 d=R/'build'/S;ws=json.loads((d/'words.json').read_text());man=json.loads((d/'graphics.json').read_text());T=json.loads((d/'timeline.json').read_text());shots=json.loads((d/'shots.json').read_text());out=[];i=0;(d/'cap').mkdir(exist_ok=True)
 while i<len(ws):
  a=ws[i]['t'];probe=[z for z in ws[i:i+3] if z['p']==ws[i]['p']];probe_end=probe[-1]['e']+.08
  # Choose clearance for the ENTIRE potential cue, including graphics entering mid-caption.
  top=1650 if any(a<m['b']+.15 and probe_end>m['a']-.1 and m['box'][1]>=1300 for m in man) else 1412
  if S=='C' and any(sh['kind']=='talk' and sh['level']=='NEAR' and a<sh['f1']/FPS and probe_end>sh['f0']/FPS for sh in shots):top=1650
  take=2 if top==1650 else 3;sel=ws[i:i+take]
  # Do not let a chunk span speech pieces or the next graphic-position change.
  sel=[z for z in sel if z['p']==ws[i]['p']]
  while len(sel)>1 and ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(' '.join(z['w'] for z in sel),font=FONT)>950:sel=sel[:-1]
  text=' '.join(z['w'] for z in sel);f0=round(a*FPS);f1=round(min(sel[-1]['e']+.08,ws[i+len(sel)]['t'] if i+len(sel)<len(ws) else T['seconds'])*FPS);f1=max(f0+1,f1)
  im=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(im);dr.text(((1080-dr.textlength(text,font=FONT))/2,top),text,font=FONT,fill='white',stroke_width=7,stroke_fill='black');png=d/'cap'/f'cue{len(out):03d}.png';im.save(png)
  out.append(dict(text=text,first_word_index=i,f0=f0,f1=f1,top=top,png=str(png),sha256=sha(png)));i+=len(sel)
 dump(d/'cues.json',out);return out

def encoder(out,N,audio=None,clean=False):
 cmd=[FF,'-nostdin','-v','error','-y','-threads','1','-filter_threads','1','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-']
 if audio:cmd+=['-i',str(audio),'-map','0:v','-map','1:a']
 cmd+=['-frames:v',str(N),'-t',str(N/FPS),'-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','ultrafast' if clean else 'fast','-crf','23' if clean else '20','-threads','1']
 if audio:cmd+=['-c:a','aac','-b:a','320k','-ar','48000','-ac','2']
 cmd+=['-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)]
 return subprocess.Popen(cmd,stdin=subprocess.PIPE)

def render(S):
 d=R/'build'/S;T=json.loads((d/'timeline.json').read_text());shots=json.loads((d/'shots.json').read_text());man=json.loads((d/'graphics.json').read_text());cc=cues(S);N=T['frames'];title=HC.reader(str(d/'hf/renders'/f'TITLE-{S}.mov'),start=30,n=N,wh=(1080,310));enc=encoder(d/f'Vacuum-{S}-R1.mp4',N,d/'his_mix.wav');clean=encoder(d/'source_picture.mp4',N,clean=True)
 capimgs={}
 for c in cc:
  ci=Image.open(c['png']);bb=ci.getbbox();capimgs[c['f0']]=(ci.crop(bb),bb)
 edge=[];(d/'proof').mkdir(exist_ok=True);openlayers={}
 try:
  for sh in shots:
   x,y,w,h=sh['crop'];vf=f"scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,lut3d=file='{sh['lut']}':interp=tetrahedral,crop={w}:{h}:{x}:{y},scale=1080:1610:flags=lanczos,format=rgb24"
   cp=subprocess.Popen([FF,'-nostdin','-v','error','-threads','1','-filter_threads','1','-ss',str(sh['raw0']),'-i',E.src(sh['roll']),'-frames:v',str(sh['f1']-sh['f0']),'-vf',vf,'-f','rawvideo','-'],stdout=subprocess.PIPE)
   try:
    for n in range(sh['f0'],sh['f1']):
     raw=cp.stdout.read(1080*1610*3)
     if len(raw)!=1080*1610*3:raise RuntimeError(('camera short read',S,n,len(raw)))
     frame=np.empty((1920,1080,3),np.uint8);frame[:310]=next(title);frame[310:]=np.frombuffer(raw,np.uint8).reshape(1610,1080,3);clean.stdin.write(frame.tobytes())
     roi=frame[310:330,390:690];edge.append(float((roi.mean(2)<65).mean()))
     for m in man:
      f0=round(m['a']*FPS);f1=round(m['b']*FPS)
      if f0<=n<f1:
       if m['id'] not in openlayers:openlayers[m['id']]=(HC.reader(m['mov'],n=f1-f0,rgba=True,wh=(1080,1920)),HC.reader(m['mask'],n=f1-f0,rgba=True,wh=(1080,1920)))
       ov,mk=openlayers[m['id']];frame=HC.glass(frame,next(mk),m['band']);frame=HC.over(frame,next(ov))
     im=Image.fromarray(frame);dr=ImageDraw.Draw(im);dr.text((64,1800),'AbsByAI.com',font=TINY,fill=(244,250,255),stroke_width=1,stroke_fill=(5,13,28))
     for c in cc:
      if c['f0']<=n<c['f1']:
       ci,bb=capimgs[c['f0']];im.paste(ci,bb,ci);break
     if n%7==0:im.save(d/'proof'/f'f{n:04d}.jpg',quality=93)
     enc.stdin.write(im.tobytes())
   finally:cp.stdout.close();cp.wait()
   print('SHOT',S,sh['idx'],sh['f0'],sh['f1'],sh['kind'],flush=True)
 finally:
  title.close()
  for ov,mk in openlayers.values():ov.close();mk.close()
  enc.stdin.close();clean.stdin.close();rc=enc.wait();rc2=clean.wait()
 assert rc==rc2==0,(rc,rc2)
 dump(d/'edge.json',dict(frames=N,max_dark_share=max(edge),values=edge));dump(d/'render.json',dict(video=str(d/f'Vacuum-{S}-R1.mp4'),sha256=sha(d/f'Vacuum-{S}-R1.mp4'),frames=N,seconds=N/FPS));print('RENDERED',S,flush=True)

if __name__=='__main__':
 stage=sys.argv[1];chosen=sys.argv[2:] or ['A','B','C']
 if stage=='plan':
  for S in chosen:
   d=R/'build'/S;dump(d/'shots.json',picshots(S,json.loads((d/'timeline.json').read_text())))
 else:
  with renderq.slot('Vacuum full Shorts '+stage+' '+','.join(chosen),pool=('light' if stage=='prepare' else 'heavy'),group='SL-11'):
   if stage in ['all','continue']:
    if stage=='all':
     with open(R/'audio/selftest.log','w') as log:
      rc=subprocess.run(['zsh',str(ROOT/'.claude/skills/_shared/audio/selftest.sh')],stdout=log,stderr=subprocess.STDOUT).returncode
     if rc:raise RuntimeError(('Shared audio selftest failed',rc))
    else:
     assert (R/'audio/selftest.log').read_text().strip().endswith('SELFTEST PASS'),'Current batch audio selftest has not passed'
     print('Reusing this batch audio SELFTEST PASS; shared audio module unchanged',flush=True)
    import finish
    for S in chosen:
     prepare(S)
     # Required pre-render junk pass on this exact intended audio, with source-aligned words.
     jd=R/'build'/S
     with open(jd/'pre-render-junk.log','w') as log:
      rc=subprocess.run(['python3',str(ROOT/'.claude/skills/_shared/cut/junk.py'),str(jd/'his_mix.wav'),'--words',str(jd/'words.json'),'--out',str(jd/'pre-render-junk.json')],stdout=log,stderr=subprocess.STDOUT).returncode
     if rc:raise RuntimeError(('pre-render junk scan failed',S,rc))
     graphics(S);render(S);finish.checks(S)
   else:
    for S in chosen:{'prepare':prepare,'gfx':graphics,'render':render}[stage](S)
