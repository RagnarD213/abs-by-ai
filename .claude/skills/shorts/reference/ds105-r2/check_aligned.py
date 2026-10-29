from pathlib import Path
import sys,json,subprocess,os,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');F=R/'Media/video_edit/bin/ffmpeg';os.environ['PATH']=str(F.parent)+':'+os.environ['PATH'];E=W/'evidence/finishing';E.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as A
sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech,landing
v=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p - aligned.mp4';sha=hashlib.sha256(v.read_bytes()).hexdigest();dur=1917*1001/30000;shots=json.load(open(W/'records/shots.json'));CP=json.load(open(W/'records/context-plan.json'))
def run(args,log):
 with (E/log).open('w') as o:r=subprocess.run(list(map(str,args)),stdout=o,stderr=subprocess.STDOUT)
 print(log,'exit',r.returncode,flush=True);return r.returncode
def ff(args):subprocess.run([str(F),'-nostdin','-v','error','-y']+list(map(str,args)),check=True)
# Shared selftest already passed for this work session; no chain/code change.
ss,dd=A.analysis_window(str(v));A.stash_untreated(str(v),A.pcm(str(W/'audio/cut-raw.wav'),ss=ss,dur=dd,ac=1),'Exact untreated full-cut selected lav audio. Same source map as approved Voice A.')
run([sys.executable,R/'.claude/skills/_shared/audio/audio_gate.py',v,'--ab',W/'review/media/voice-reference-comparison.mp4'],'FULL-audio.log')
# ASR runs locally, with no paid provider calls.
heard,where=speech.transcribe(str(v),quiet=False);words=json.load(open(W/'records/full-words.json'))
(E/'FULL-delivered-words.json').write_text(json.dumps(dict(sha256=sha,source=where,words=heard),indent=2))
plan=dict(evidence_contract=dict(version=2,video_sha256=sha),target_seconds=dur,target_frames=1917,joins=[s['a'] for s in shots[1:]],audio_joins=[p['out'] for p in json.load(open(W/'edit-plan.json'))['pieces'][1:]],punch=[[s['a'],s['b'],'FAR' if i%2==0 else 'NEAR'] for i,s in enumerate(shots)],punch_covered=[False]*len(shots),covered=[],cards=[],graphics=[dict(name=g['id'],beat=[g['a'],g['b']],mov=str(W/f'hf/renders/{g["id"]}.mov')) for g in CP['graphics']],ai_inserts=[],real_photos=[],captions_ass=str(W/'records/FULL-aligned.ass'),source_audio=str(W/'audio/cut-raw.wav'),talking_head_windows=[dict(beat=[0,dur],rect=[0,310,1080,1920],motion='tracking')],graphic_regions=[dict(beat=[0,dur],rect=[0,0,1080,310])]+[dict(beat=[g['a'],g['b']],rect=[68,1130,1012,1378]) for g in CP['graphics']],source_picture=str(W/'picture/FULL-graded.mp4'),words=[dict(w=x['w'],t=x['t0'],e=x['t1']) for x in words],transcript_words=[dict(w=x['w']) for x in heard],speech_words=heard,speech_words_evidence=dict(method='delivered_asr',video_sha256=sha))
plan.update(banned_source='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4',banned_times=[12.,18.,288.])
pp=E/'FULL-plan.json';pp.write_text(json.dumps(plan,indent=2));watch=E/'FULL-watch.json'
run([sys.executable,R/'.claude/skills/_shared/deliver/watch.py',v,'--plan',pp,'--out',E/'FULL-watch','--log',watch,'--clips'],'FULL-watch.log');plan['watch_log']=str(watch);pp.write_text(json.dumps(plan,indent=2))
pcm=E/'FULL-exact.wav';ff(['-i',v,'-vn','-ac',1,'-ar',48000,'-c:a','pcm_s16le',pcm]);jp=E/'FULL-joins.json';jp.write_text(json.dumps(plan['audio_joins']));run([sys.executable,R/'.claude/skills/_shared/audio/seamscan.py',pcm,'--joins',jp,'--out',E/'FULL-seams.json'],'FULL-seams.log')
# Dense actual hair masks independently remeasured for both exact copies; invalid detection stays unresolved.
reports=[]
for tag,video in [('FULL-1080',v),('FULL-540',W/'review/media/Why I Wear A Mouthpiece For SFC R2 - REVIEW 540p - aligned.mp4')]:
 D=Path('/tmp/absbyai-scratch/DS-105-R2')/tag/sha[:8];D.mkdir(parents=True,exist_ok=True);ff(['-i',video,'-vf','scale=540:960:in_color_matrix=bt709:in_range=tv',D/'frame-%04d.jpg']);paths=sorted(D.glob('frame-*.jpg'));assert len(paths)==1917
 z=subprocess.run([str(Path.home()/'.cache/absbyai/facebox')]+list(map(str,paths)),capture_output=True,text=True,check=True);faces=[];invalid=[]
 for i,line in enumerate(z.stdout.splitlines()):
  _,box=line.split('\t');faces.append(None if box in ['none','error'] else list(map(int,box.split())))
 assert len(faces)==1917
 M=D/'masks';M.mkdir(exist_ok=True)
 for k in range(0,len(paths),80):subprocess.run([str(R/'.claude/skills/shorts/reference/recentre/personmask'),str(M)]+list(map(str,paths[k:k+80])),check=True,capture_output=True)
 rows=[]
 for i,(p,box) in enumerate(zip(paths,faces)):
  if box is None:invalid.append(i);continue
  mask=np.array(Image.open(M/(p.stem+'.mask.png')).convert('L'));cc,lab,stats,_=cv2.connectedComponentsWithStats((mask>127).astype('uint8'),8)
  if cc<2:invalid.append(i);continue
  comp=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]));x0,y0,x1,y1=box;cx=(x0+x1)/2;fw=x1-x0;lo=max(0,int(cx-.4*fw));hi=min(540,int(cx+.4*fw));ys=np.where((lab[:,lo:hi]==comp).mean(1)>.2)[0]
  if len(ys)==0:invalid.append(i);continue
  hair=int(ys[0]);rows.append(dict(n=i,t=i*1001/30000,hair=hair,clearance=hair*2-310,face=box,head_x=cx*2))
 minimum=min(x['clearance'] for x in rows);rec=dict(video=str(video),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),valid=not invalid and minimum>=20,native_frames=len(paths),actual_hair_mask_frames=len(rows),invalid_frames=invalid,min_actual_hair_below_picture_top=minimum,method='Actual rendered head-band person mask on EVERY native frame with independent face box, analysis540x960/native cadence;20px bound at1080width. R1 proxy failures preserved separately.',rows=rows)
 (E/f'{tag}-hair-every-frame.json').write_text(json.dumps(rec,indent=2));worst=sorted(rows,key=lambda x:x['clearance'])[:12];im=Image.new('RGB',(1080,1308),'#132236');dr=ImageDraw.Draw(im)
 for q,row in enumerate(worst):
  img=Image.open(paths[row['n']]);dd=ImageDraw.Draw(img);dd.line((0,row['hair'],540,row['hair']),fill='magenta',width=2);img=img.crop((60,120,480,480)).resize((360,309));x=q%3*360;y=q//3*327;im.paste(img,(x,y+18));dr.text((x+6,y+2),f'{row["t"]:.3f}s hair {row["clearance"]}px',fill='white')
 im.save(E/f'{tag}-hair-every-frame-proof.jpg');reports.append({k:v for k,v in rec.items() if k!='rows'});print('DENSE_HAIR',tag,minimum,'invalid',len(invalid),flush=True)
(E/'hair-every-frame-summary.json').write_text(json.dumps(reports,indent=2))
# Motion statistics are from approved shared-landing positions, paired with measured source head track.
track=json.load(open(W/'records/source-track.json'));tt=np.array([x['t'] for x in track]);xx=np.array([x['source_x'] for x in track]);motion=[]
for i,s in enumerate(shots):
 n=np.arange(s['n']);raw=np.interp(s['source_in']+n*1001/30000,tt,xx);motion.append(dict(shot=i,beat=[s['a'],s['b']],stats=landing.motion_stats(n,raw,np.array(s['centre']),[dict(n0=0,n1=s['n'])],s['crop'][0],30000/1001)))
(E/'motion-stats.json').write_text(json.dumps(motion,indent=2))
# Full shared gate runs after the fresh exact-hash watch findings are folded.
state=json.load(open(W/'execution-state.json'));state.update(checkpoint='self_checks_complete_pending_independent_review');(W/'execution-state.json').write_text(json.dumps(state,indent=2));print('SELF_CHECKS_COMPLETE',flush=True)
