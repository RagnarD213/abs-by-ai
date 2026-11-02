from pathlib import Path
import json,subprocess,sys,os,importlib.util,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
S=json.load(open(W/'source.json'))['path'];raw=json.load(open(W/'source-words-corrected.json'));edl=json.load(open(W/'edl.json'));out=0;words=[]
for p in edl:
 p['n0']=out;p['frames']=round((p['end']-p['start'])*FPS);p['n1']=out+p['frames'];p['out']=out/FPS;out+=p['frames']
 for v in raw:
  if p['start']<=v['start']<p['end']:
   text=v['word'].strip();text={'Like':'Light','as':'is'}.get(text,text) if v['start'] in [232.76,254.16] else text
   words.append(dict(w=text,t0=v['start']-p['start']+p['out'],t1=min(v['end'],p['end'])-p['start']+p['out'],src=v['start']))
(W/'edl.json').write_text(json.dumps(edl,indent=2));(W/'words_out.json').write_text(json.dumps(words,indent=2))
print('FILM',out,'frames',out/FPS,'sec',flush=True)
# Dense source hair/head measurement at 4fps and exact planned cut anchors. Coordinates are decoded 540x960.
B=W/'measurements';B.mkdir(exist_ok=True)
if not (B/'head-samples.json').exists():
 cmd=[F,'-v','error','-nostdin','-ss','198.35','-i',S,'-t','71.1','-an','-vf','fps=4,scale=540:960:in_color_matrix=bt709:in_range=tv','-f','rawvideo','-pix_fmt','rgb24','-'];proc=subprocess.Popen(cmd,stdout=subprocess.PIPE);rows=[];n=0
 while True:
  data=proc.stdout.read(540*960*3)
  if len(data)<540*960*3:break
  im=np.frombuffer(data,np.uint8).reshape(960,540,3);lum=im@np.array([.2126,.7152,.0722]);roi=lum[145:300,185:365];counts=(roi<31).sum(1);hits=np.where(counts>20)[0]
  if not len(hits):rows.append(dict(t=198.35+n/4,valid=False))
  else:
   y=145+int(hits[0]);yy,xx=np.where(lum[y+6:y+36,185:365]<34);left=int(xx.min()+185);right=int(xx.max()+185)
   rows.append(dict(t=198.35+n/4,valid=True,hair_y=y*4,head_x=(left+right)*2,hair_box=[left*4,y*4,right*4,(y+40)*4]))
  n+=1
 assert proc.wait()==0
 (B/'head-samples.json').write_text(json.dumps(rows,indent=2))
rows=json.load(open(B/'head-samples.json'));valid=[r for r in rows if r['valid']];print('HAIR',min(r['hair_y'] for r in valid),max(r['hair_y'] for r in valid),'HEADX',min(r['head_x'] for r in valid),max(r['head_x'] for r in valid),'invalid',len(rows)-len(valid),flush=True)
# Timeline source anchors: raw take reset is removed. First review stays at 30s, with isolated narrated contexts later.
def t(src):
 p=next(p for p in edl if p['start']<=src<p['end']);return p['out']+src-p['start']
shots=[]
# Both whole blue fixtures in wide and neither in tight; use exact DS28 pair as starting geometry.
segments=[(198.35,202.16,'tight'),(202.16,206.86,'wide'),(206.86,216.38,'tight'),(219.58,225.53,'wide'),(225.53,229.02,'tight'),(229.02,239.93,'equipment'),(239.93,246.21,'wide'),(248.70,253.0,'tight'),(253.0,256.6,'wide'),(256.6,262.62,'tight'),(266.48,269.36,'wide')]
Lspec=importlib.util.spec_from_file_location('landing',R/'.claude/skills/_shared/cut/landing.py');L=importlib.util.module_from_spec(Lspec);Lspec.loader.exec_module(L);motion=[]
for i,(a,b,mode) in enumerate(segments):
 p=next(p for p in edl if p['start']<=a<p['end']);n0=round((p['out']+a-p['start'])*FPS);n1=min(p['n1'],round((p['out']+b-p['start'])*FPS));s=dict(id=f'T{i+1:02}',src=a,n0=n0,n1=n1,kind=mode)
 if mode!='equipment':
  cw,ch,cy=(2040,3626,214) if mode=='wide' else (1120,1990,740)
  # Exact cut-frame anchor, independently of dense sampling.
  anchor=B/(s['id']+'-anchor.jpg');subprocess.run([F,'-v','error','-nostdin','-y','-ss',str(a),'-i',S,'-frames:v','1','-vf','scale=540:960:in_color_matrix=bt709:in_range=tv',str(anchor)],check=True)
  im=np.array(Image.open(anchor));lum=im@np.array([.2126,.7152,.0722]);hits=np.where((lum[145:300,185:365]<31).sum(1)>20)[0];hy=145+int(hits[0]);_,xx=np.where(lum[hy+6:hy+36,185:365]<34);hx=(int(xx.min())+int(xx.max())+370)*2
  nr=[n0];xr=[hx]
  for r in valid:
   n=n0+round((r['t']-a)*FPS)
   if n0<n<n1:nr.append(n);xr.append(r['head_x'])
  dn,centres,heads,info=L.vertical_dense(nr,xr,[s],cw,FPS);left=centres-cw/2
  if left.min()<0 or left.max()>2160-cw:
   # Wider camera set is bounded by native source. Keep complete lights and document exact residual.
   left=np.clip(left,0,2160-cw)
  s.update(crop=[cw,ch,cy],tracking=[[int(n),round(float(v),3)] for n,v in zip(dn,left)],anchor_head_x=hx,anchor_hair_y=hy*4)
  motion.append(dict(id=s['id'],stats=L.motion_stats(dn,heads,left+cw/2,[s],cw,FPS),minimum_sampled_clearance=min((r['hair_y']-cy)/ch*1920 for r in valid if a<=r['t']<b)))
 shots.append(s)
(W/'shots.json').write_text(json.dumps(shots,indent=2));(W/'motion-stats.json').write_text(json.dumps(motion,indent=2))
# Corrections made against the intended script; timing stays from the actual take.
for w in words:
 if w['src']==232.76:w['w']='Light'
 if w['src']==254.16:w['w']='is'
# Join split hyphen spelling into readable caption token.
for i in range(len(words)-1,0,-1):
 if words[i]['w']=='-minute':words[i-1]['w']+='-minute';words[i-1]['t1']=words[i]['t1'];words.pop(i)
chunks=[];cur=[]
for w in words:
 if cur and (len(cur)>=3 or w['t0']-cur[-1]['t1']>.55):chunks.append(cur);cur=[]
 cur.append(w)
 if w['w'].endswith(('.',',','!','?')):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
def ts(t):return f'{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}'
header='[Script Info]\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,2,70,70,420,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
(W/'captions.ass').write_text(header+''.join(f"Dialogue: 0,{ts(c[0]['t0'])},{ts(min(c[-1]['t1']+.03,chunks[i+1][0]['t0']) if i+1<len(chunks) else c[-1]['t1']+.03)},Default,,0,0,0,,"+' '.join(v['w'] for v in c)+'\n' for i,c in enumerate(chunks)))
(W/'caption-chunks.json').write_text(json.dumps(chunks,indent=2));(W/'words_out.json').write_text(json.dumps(words,indent=2))
# Two distilled graphics, phrase anchored in the cut speech. Full equipment scene shown in the separate context excerpt.
plan=[dict(id='G01',kind='lt',t0=t(206.98),t1=t(211.0),start='Listen',end='you pack',topic='HOME WORKOUTS',point='Skip The Commute',parts=[['Skip The Commute','Listen']]),dict(id='G02',kind='lt',t0=t(221.76),t1=t(225.76),start='driving 15 minutes',end='At home',topic='THE REAL TIME COST',point='30-Minute Workout. 60 Minutes Gone.',parts=[['30-Minute Workout.','driving 15 minutes'],['60 Minutes Gone.','doubles your workout time']])]
(W/'plan_resolved.json').write_text(json.dumps(plan,indent=2));print('PREPARED',flush=True)
