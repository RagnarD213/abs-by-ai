#!/usr/bin/env python3
"""SL-12 asset-review excerpts only. Reuses Soft Blue HyperFrames title/recap and the exact approved RO-01 master.
Not a final-short renderer. Caption alignment follows softblue-sl09/batch.py (Wav2Vec2 CTC).
"""
from pathlib import Path
import os,sys,json,re,subprocess,wave,math
import numpy as np
from PIL import Image,ImageFont
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
WORK=Path('/Volumes/Extreme/_edit_work/SL-12/round1')
OUT=WORK/'asset-review';OUT.mkdir(exist_ok=True)
SH=ROOT/'.claude/skills/_shared';HF=SH/'hyperframes'
sys.path[:0]=[str(SH),str(HF)]
import hfbuild as H,vertical as V
FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FP=str(ROOT/'Media/video_edit/bin/ffprobe')
MASTER=ROOT/'Codex Content Videos/How To Keep Your Muscle While You Lose Fat - RO-01/How To Keep Your Muscle While You Lose Fat | Codex | 16x9 | RO-01.mp4'
SHEET=json.loads(Path('/Volumes/Extreme/_edit_work/ro01/revision10/full/RO01_MASTER_R10_REVIEW_1080p.mp4.edit-sheet.json').read_text())
FPS=30000/1001
A="Now you don't need to be doing a full hour of weightlifting every day in the gym like me. What I would recommend if you're first starting off is just to do five minutes of home bodyweight resistance training. If you're a beginner and you're untrained right now, just that five minutes a day, every day will be enough to prevent muscle loss."
B="How much protein should you be aiming for? Studies have shown the optimal amount of protein to eat is about 0.8 grams of protein per pound of body weight. So let's say you're 200 pounds. That means aim for 160 grams of protein per day."
CASES=[dict(id='A-intro',S='A',a=0,b=6.006,text='',intro=True,src='/Volumes/Extreme/_edit_work/ro01/assets/dan-curls.mp4'),dict(id='A-training',S='A',a=347.80,b=366.50,text=A,card=[353.353,366.50]),dict(id='B-protein',S='B',a=455.20,b=471.58,text=B,card=[458.1029,472.00]),dict(id='A-movement',S='A',a=366.9666,b=374.7743,picture_src='/Volumes/Extreme/_edit_work/ro01/assets/dan-pushups.mp4',picture_ss=0.1678,text="As you progress, you're gonna have to step it up to ten minutes, fifteen minutes, twenty minutes, et cetera, in order to keep your muscle.",movement=True)]
TITLE={'A':['Weightlifting Is','Mandatory'],'B':['How Much Protein','Do You Need?']}
EYE={'A':'KEEP YOUR MUSCLE','B':'DAILY PROTEIN'}
def run(args):
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-3000:])
 return r

def cfg_header(S,dur):
 # SL-03/SL-15 locked 310px band, font88 and corrected y86/182; render starts 1.5s after template intro.
 c=dict(id='header-'+S,dur=dur+1.6,drift=-2,canvas=[1080,1920],line_px=88,accent=[64,50,7],eyebrow=dict(x=88,y=51,px=34,s=EYE[S]),lines=[dict(x=64,y=104+96*i,s=l,at=-1) for i,l in enumerate(TITLE[S])])
 assert all(H.text_w(l,88)<952 for l in TITLE[S])
 return c

def cards():
 result={}
 specs=[('A',13.15,'START SMALL. BUILD UP.','A Little Every Day',['5 Minutes To Start','Increase As You Progress','10, 15, Then 20 Minutes']),('B',13.55,'DAILY PROTEIN TARGET','A 200-Pound Example',['0.8 Grams Per Pound','200 Pounds × 0.8','160 Grams Per Day'])]
 for S,dur,eye,title,rows in specs:
  scenes,_=V.title_scenes('card-'+S+'-v2',0,dur,eye,title,rows)
  c=scenes[0][1];c['drift']=-4
  # Keep all card content below the persistent title and above subtitles.
  c['accent']=[80,430,78];c['eyebrow'].update(x=80,y=458,px=32)
  c['line_px']=64;c['lines']=[dict(x=76,y=540,s=title,at=0.1)]
  for i,row in enumerate(c['rows']):row.update(y=700+i*180,h=140,w=920,x=80,t=[0.4,6.5,9.8][i] if S=='B' else [0.4,5.5,8.5][i])
  c['row_px']=46;c['row_ty']=37
  out=OUT/'hf';m=out/'renders'/('card-'+S+'-v2.mov')
  if not m.exists():V.build(scenes,out,render=True,snap=dur-1)
  result[S]=m
 return result

def ctc(wav,text,out):
 if out.exists():return json.loads(out.read_text())
 import torch,torchaudio,scipy.signal as ss
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 w=wave.open(str(wav));sr=w.getframerate();ch=w.getnchannels();x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32).reshape(-1,ch).mean(1)/32768
 x=ss.resample_poly(x,16000,sr).astype(np.float32)
 bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H;model=bundle.get_model().eval();labels={c:i for i,c in enumerate(bundle.get_labels())}
 words=text.split();ids=[];owner=[]
 nums={'0.8':'zero point eight','200':'two hundred','160':'one hundred sixty'}
 for k,s in enumerate(words):
  bare=re.sub(r'[^a-zA-Z0-9.\']','',s).strip('.')
  spoken=nums.get(bare,s)
  n=re.sub(r"[^A-Z' ]",'',spoken.upper()).strip()
  for c in n.replace(' ','|'):ids.append(labels[c]);owner.append(k)
  ids.append(labels['|']);owner.append(-1)
 with torch.inference_mode():em,_=model(torch.from_numpy(x).unsqueeze(0));em=torch.log_softmax(em,-1)
 ali,sc=torchaudio.functional.forced_align(em,torch.tensor([ids[:-1]],dtype=torch.int32),blank=0)
 spans=torchaudio.functional.merge_tokens(ali[0],sc[0].exp());ratio=len(x)/em.shape[1]/16000;per={}
 for i,s in enumerate(spans):
  k=owner[i]
  if k<0:continue
  per.setdefault(k,[s.start*ratio,s.end*ratio,[]]);per[k][1]=s.end*ratio;per[k][2].append(float(s.score))
 res=[dict(w=s,t=round(per[k][0],3),e=round(per[k][1],3),score=round(float(np.mean(per[k][2])),3)) for k,s in enumerate(words)]
 out.write_text(json.dumps(res,indent=2)+'\n');return res

def atime(t):
 h=int(t//3600);m=int(t%3600//60);s=t%60;return f'{h}:{m:02d}:{s:05.2f}'
def captions(words,path):
 cur=[];groups=[]
 for w in words:
  if cur and (len(cur)>=3 or w['t']-cur[-1]['e']>.45):groups.append(cur);cur=[]
  cur.append(w)
  if re.search(r'[.!?]$',w['w']):groups.append(cur);cur=[]
 if cur:groups.append(cur)
 lines=['[Script Info]','PlayResX: 1080','PlayResY: 1920','WrapStyle: 0','[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding','Style: Default,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,7,3,8,70,70,1412,1','[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 for i,g in enumerate(groups):
  end=g[-1]['e']+.18
  if i+1<len(groups):end=min(end,groups[i+1][0]['t'])
  txt=' '.join(w['w'] for w in g)
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86)
  if font.getlength(txt)>940 and len(g)>1:
   options=[(' '.join(w['w'] for w in g[:k]),' '.join(w['w'] for w in g[k:])) for k in range(1,len(g))]
   left,right=min(options,key=lambda q:max(font.getlength(q[0]),font.getlength(q[1])))
   assert max(font.getlength(left),font.getlength(right))<1000,txt
   txt=left+r'\N'+right
  lines.append(f"Dialogue: 0,{atime(g[0]['t'])},{atime(end)},Default,,0,0,0,,{{\\pos(540,1412)}}"+txt)
 path.write_text('\n'.join(lines)+'\n')

def cx_expr(a,b):
 arr=[]
 for e in SHEET['edl']:
  if e['out_in']>=b or e['out_out']<=a:continue
  f=next(q for q in SHEET['framing'] if q['name']==e['shot']);cw,ch,x,y=f['crop'];cx=(f['head']['cx']-x)*1920/cw;x0=max(0,min(1196,cx-362));arr.append((max(a,e['out_in'])-a,min(b,e['out_out'])-a,x0))
 expr=str(round(arr[-1][2],2))
 for t0,t1,x in reversed(arr[:-1]):expr=f'if(lt(t,{t1:.6f}),{x:.2f},{expr})'
 return expr

def preview(q,cardpaths):
 ident=q['id'];a=q['a'];dur=q['b']-a;S=q['S'];nf=round(dur*FPS);dur=nf/FPS
 d=OUT/ident;d.mkdir(exist_ok=True);wav=d/'speech.wav'
 if q['text'] and not wav.exists():run([FF,'-v','error','-y','-ss',str(a),'-i',q.get('src',str(MASTER)),'-t',str(dur),'-vn','-c:a','pcm_s16le',str(wav)])
 words=ctc(wav,q['text'],d/'words.json') if q['text'] else []
 if words:captions(words,d/'captions.ass')
 c=cfg_header(S,dur);hp=OUT/'hf'/'renders'/(c['id']+'.mov')
 # Per excerpt header files avoid a shorter reused header ending early.
 c['id']='header-'+q.get('header_id',ident);hp=OUT/'hf'/'renders'/(c['id']+'.mov');header_ss=q.get('header_ss',1.5)
 if not hp.exists():
  # The shared 1.4 line boxes overlap inside a 310px header. Keep the same glyph positions with 1.0 boxes plus half-leading offsets.
  ht=OUT/'header.template.htm';ht.write_text((HF/'title-card/title-card.template.htm').read_text().replace('line-height: 1.4','line-height: 1.0').replace('id="lines"','id="lines" data-layout-allow-overlap="true"').replace('id="eyebrow"','id="eyebrow" data-layout-allow-overlap="true"').replace('height: 8px; border-radius: 3px','height: 36px; border-radius: 3px').replace('sp.textContent = w +', 'sp.setAttribute("data-layout-allow-overlap","true"); sp.textContent = w +'))
  V.build([(ht,c,())],OUT/'hf',render=True,snap=2.0)
 out=OUT/(ident+'-context.mp4')
 if out.exists():return out
 args=[FF,'-v','error','-y','-ss',str(a),'-i',q.get('src',str(MASTER)),'-i',str(hp)]
 if q.get('card'):args+=['-i',str(cardpaths[S])]
 if q.get('picture_src'):args+=['-ss',str(q['picture_ss']),'-i',q['picture_src']]
 picture=("crop=724:1080:644:0,scale=1080:1610:flags=lanczos,eq=gamma=1.2:saturation=1.05" if q.get('intro') else "crop=1440:1080:480:0,scale=1080:810:flags=lanczos" if q.get('movement') else f"crop=724:1080:x='{cx_expr(a,a+dur)}':y=0:exact=1,scale=1080:1610:flags=lanczos")
 pi=2 if q.get('picture_src') else 0
 graph=f"[{pi}:v]setpts=PTS-STARTPTS,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,{picture}[pic];[1:v]trim=start={header_ss},setpts=PTS-STARTPTS,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[bg];[bg][pic]overlay=0:310:eof_action=pass:shortest=1:format=rgb[base];"
 if q.get('card'):
  ca,cb=q['card'];ofs=ca-a
  graph+=f"[2:v]setpts=PTS-STARTPTS+{ofs}/TB,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[card];[base][card]overlay=0:0:eof_action=pass:format=rgb:enable='between(t,{ofs:.6f},{cb-a:.6f})'[withcard];"
  # Cover the card's top with this Short's persistent header, keeping its identity throughout.
  graph+=f"[1:v]trim=start={header_ss},setpts=PTS-STARTPTS,crop=1080:310:0:0,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[header];[withcard][header]overlay=0:0:shortest=1:format=rgb[composed];"
  tag='composed'
 else:tag='base'
 graph+=f"[{tag}]ass='{d/'captions.ass'}',scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]" if words else f'[{tag}]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
 args+=['-filter_complex',graph,'-map','[v]','-map','0:a:0?','-frames:v',str(nf),'-t',str(dur),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-ar','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(out)]
 run(args)
 probe=json.loads(run([FP,'-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames','-of','json',str(out)]).stdout)['streams'][0]
 assert (probe['width'],probe['height'])==(1080,1920),probe
 assert int(probe['nb_frames'])==nf,(probe,nf)
 # Full-res poster: settled graphic or complete-rep view, never a sparse sheet for a timing judgment.
 t=12 if ident=='B-protein' else 10 if ident=='A-training' else 2.3
 run([FF,'-v','error','-y','-ss',str(min(t,dur-1)),'-i',str(out),'-frames:v','1',str(OUT/(ident+'.jpg'))])
 return out
if __name__=='__main__':
 paths=cards()
 for q in CASES:print('BUILT',preview(q,paths),flush=True)
 print('ASSET EXCERPTS COMPLETE; no final Shorts rendered.',flush=True)
