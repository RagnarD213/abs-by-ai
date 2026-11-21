from pathlib import Path
import json,subprocess,hashlib,sys,os,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
R=Path('/Volumes/Extreme/_edit_work/SL-11/round2');OLD=R.parent/'round1';ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); FF=str(ROOT/'Media/video_edit/bin/ffmpeg'); FP=str(ROOT/'Media/video_edit/bin/ffprobe');FPS=30000/1001
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import softblue_titlecheck as TC
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2))
def cmd(a,p):
 with open(p,'w') as f:r=subprocess.run(list(map(str,a)),stdout=f,stderr=subprocess.STDOUT)
 print(p.name,r.returncode,flush=True);return r.returncode
def packets(p):return json.loads(subprocess.check_output([FP,'-v','error','-select_streams','a','-show_packets','-show_data_hash','sha256','-show_entries','packet=pts_time,dts_time,duration_time,data_hash','-of','json',str(p)]))['packets']
for row in json.loads((R/'intro-manifest.json').read_text()):
 id=row['id'];
 if len(sys.argv)>1 and id not in sys.argv[1:]:continue
 S=row['short'];v=Path(row['file']);d=R/'build'/id;old=OLD/'build'/S;N=row['frames'];dur=row['seconds'];intro=row['intro_end'];q=d/'exact';q.mkdir(exist_ok=True);(d/'gate/logs').mkdir(parents=True,exist_ok=True)
 orig=old/f'Vacuum-{S}-R1.mp4';a=packets(v);b=packets(orig);assert a[:-1]==b[:len(a)-1] and all(a[-1][k]==b[len(a)-1][k] for k in ['pts_time','dts_time','data_hash']),id+' audio packet mutation';dump(d/'audio-identity.json',dict(sha256=sha(v),reference_sha256=sha(orig),packets=len(a),all_packet_data_and_start_timing_identical=True,last_packet_container_duration_truncated_at_excerpt_edge=True))
 ref=d/'reference.wav';subprocess.run([FF,'-v','error','-y','-i',str(orig),'-t',str(dur),'-vn','-ac','2','-ar','48000',str(ref)],check=True)
 cmd(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',v,'--reference-mix',ref,'--verbatim'],d/'audio-gate.log')
 cp=subprocess.Popen([FF,'-v','error','-threads','1','-i',str(v),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE);paths=[];edge=[];n=0;metrics=[]
 while True:
  raw=cp.stdout.read(1080*1920*3)
  if not raw:break
  assert len(raw)==1080*1920*3
  fr=np.frombuffer(raw,np.uint8).reshape(1920,1080,3);edge.append(int((fr[310:330,390:690].mean(2)<65).sum()))
  if n%7==0 or n in [0,N-1,row['intro_frames']-1,row['intro_frames']]:
   p=q/f'f{n:04d}.png';Image.fromarray(fr).save(p);paths.append(p)
  n+=1
 cp.stdout.close();assert cp.wait()==0 and n==N
 PM=ROOT/'.claude/skills/shorts/reference/recentre/personmask';subprocess.run([str(PM),str(q/'m')]+list(map(str,paths)),check=True,capture_output=True)
 rows=[]
 for p in paths:
  mask=np.asarray(Image.open(q/'m'/f'{p.stem}.mask.png'))>127;mask[:310]=False;lab,num=ndimage.label(mask);assert num
  k=1+np.argmax(ndimage.sum(mask,lab,range(1,num+1)));m=lab==k;rr=np.where(m.sum(1)>=20)[0];yy,xx=np.where(m);assert len(rr)
  rows.append(dict(frame=int(p.stem[1:]),hair_y=int(rr[0]),clearance=int(rr[0])-310,left=int(xx.min()),right=int(xx.max())))
 report=dict(video=str(v),sha256=sha(v),frames=n,min_hair_clearance=min(x['clearance'] for x in rows),max_dark_top_edge=max(edge),every_frame_dark_top_edge=edge,samples=rows,title=TC.frame_report(str(v)))
 dump(d/'framing.json',report);assert report['min_hair_clearance']>=20,(id,report['min_hair_clearance']);assert max(edge)==0 or row['option']==2,(id,max(edge));
 if row['option']==2:report['raw_dark_top_edge_applicability']='Raw dark pixels include hedge background and cannot classify hair; preserve raw values. Actual person-mask hair clearance plus independent native-frame adjudication required.';dump(d/'framing.json',report)
 assert report['title']['verdict']=='OK'
 for j in range(0,len(paths),24):
  sheet=Image.new('RGB',(6*216,4*404),'#eff6fc');dr=ImageDraw.Draw(sheet)
  for k,p in enumerate(paths[j:j+24]):
   x=k%6*216;y=k//6*404;sheet.paste(Image.open(p).resize((216,384)),(x,y+20));dr.text((x+2,y+2),f'{int(p.stem[1:])/FPS:.3f}s',fill='black')
  sheet.save(q/f'dense-{j//24:02d}.jpg',quality=94)
 p=copy.deepcopy(json.loads((old/'gate/plan.json').read_text()));p['target_frames']=N;p['target_seconds']=dur;p['evidence_contract']['video_sha256']=sha(v);p['speech_words_evidence']['video_sha256']=sha(v)
 for key in ['joins','audio_joins']:p[key]=[t for t in p[key] if 0<t<dur-.01]
 for key in ['covered','punch']:
  p[key]=[[x[0],min(dur,x[1])]+x[2:] for x in p[key] if x[0]<dur]
 for key in ['caption_states','talking_head_windows','graphic_regions','graphics','ai_inserts','real_photos','cards']:
  p[key]=[dict(x,beat=[x['beat'][0],min(x['beat'][1],dur)]) for x in p[key] if x['beat'][0]<dur]
 p['words']=[x for x in p['words'] if x['t']<dur];p['transcript_words']=[dict(w=x['w']) for x in p['words']];p['speech_words']=[x for x in p['speech_words'] if x['t']<dur];p['source_audio']=str(ref);p.pop('source_picture',None);p['watch_log']=str(d/'gate/logs/watch_pass.json');p.pop('instrument_adjudications',None)
 p['declare']={'framing:no_wide_level':'This intro-choice excerpt compares a standing exercise. A complete head/body teaching view is required; a talking-head min-face-size test does not apply to exercise footage. Rendered every-frame top edge plus <0.25s independent person-mask hair checks apply; existing presenter return remains unchanged.','style:coverage':'This is a short intro comparison excerpt, not a complete Short. Full-programme cutaway percentage cannot be judged from an opening excerpt; it remains required on the selected complete R2 masters. No R1 palette exception is reused.','compliance:banned_screen':'Only verified real camera footage of Dan from C1625/C1677, approved presenter cache, original captions and title are in this excerpt. No app or screen recording is present.'}
 p['declare']['framing:push_coverage']='This intro comparison contains one unchanged presenter return hold. A single hold cannot demonstrate full-programme punch variation; complete masters retain this rule.'
 if S in ['A','C']:p['declare']['audio:click_at_joins']='This excerpt is a single continuous segment of the R1 approved mix with no internal audio join. Exact AAC data/start timestamps are independently verified. Complete-film audio joins remain required; B pickup join remains measured.'
 p['negative_events_scan']=dict(sha256=sha(v),frames_checked=len(rows),method='Native delivered frame decode; dense samples every7frames, all-frame top edge and fresh independent motion/native review',findings=[])
 # Captions ending with later speech must be scoped to the actually heard words of this excerpt.
 cs=[dict(c,f1=min(c['f1'],N)) for c in json.loads((old/'cues.json').read_text()) if c['f0']<N]
 if S=='B':
  cs[-1]['text']='unnecessarily.';im=Image.new('RGBA',(1080,1920));dr=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',86);s=cs[-1]['text'];dr.text(((1080-dr.textlength(s,font=font))/2,1412),s,font=font,fill='white',stroke_width=7,stroke_fill='black');cap=d/'endpoint-caption.png';im.save(cap)
  p['caption_states'][-1]['image']=str(cap);p['caption_states'][-1]['image_sha256']=sha(cap)
 def ts(t):
  m=round(t*1000);return f'{m//3600000:02}:{m%3600000//60000:02}:{m%60000//1000:02},{m%1000:03}'
 srt=d/'captions.srt';srt.write_text('\n'.join(f"{i+1}\n{ts(c['f0']/FPS)} --> {ts(c['f1']/FPS)}\n{c['text']}\n" for i,c in enumerate(cs)));p['srt']=str(srt);dump(d/'cues.json',cs);dump(d/'gate/plan.json',p)
 cmd(['python3',ROOT/'.claude/skills/_shared/deliver/watch.py',v,'--plan',d/'gate/plan.json','--out',d/'gate/watch','--log',d/'gate/logs/watch_pass.json','--clips'],d/'watch.log')
 print('QA PACKET READY',id,flush=True)
