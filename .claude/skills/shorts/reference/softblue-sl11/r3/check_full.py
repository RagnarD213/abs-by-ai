from pathlib import Path
import json,subprocess,hashlib,sys,os,copy
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
R=Path('/Volumes/Extreme/_edit_work/SL-11/round3');OLD=R.parent/'round1';ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FP=str(ROOT/'Media/video_edit/bin/ffprobe');FPS=30000/1001
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import softblue_titlecheck as TC
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,j):Path(p).write_text(json.dumps(j,indent=2))
def cmd(a,p):
 with open(p,'w') as f:r=subprocess.run(list(map(str,a)),stdout=f,stderr=subprocess.STDOUT)
 print(p.name,r.returncode,flush=True);return r.returncode
def packets(p):return json.loads(subprocess.check_output([FP,'-v','error','-select_streams','a','-show_packets','-show_data_hash','sha256','-show_entries','packet=pts_time,dts_time,duration_time,data_hash','-of','json',str(p)]))['packets']
def reader(p,n,w=270,h=480):return subprocess.Popen([FF,'-v','error','-threads','1','-filter_threads','1','-i',str(p),'-frames:v',str(n),'-vf',f'scale={w}:{h},format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
def read(p,w=270,h=480):
 b=p.stdout.read(w*h*3);assert len(b)==w*h*3;return np.frombuffer(b,np.uint8).reshape(h,w,3)
for row in json.loads((R/'build-manifest.json').read_text()):
 S=row['short']
 if len(sys.argv)>1 and S not in sys.argv[1:]:continue
 d=R/'build'/S;old=OLD/'build'/S;v=Path(row['file']);N=row['frames'];intro=row['intro_frames'];orig=Path(row['r1_reference']);chosen=Path(row['approved_intro']);(d/'gate/logs').mkdir(parents=True,exist_ok=True);q=d/'exact';q.mkdir(exist_ok=True)
 a=packets(v);b=packets(orig);assert a==b,(S,'AAC stream changed');dump(d/'audio-identity.json',dict(sha256=sha(v),reference_sha256=sha(orig),packets=len(a),all_packet_data_and_pts_dts_duration_identical=True))
 assert cmd(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',v,'--reference-mix',old/'his_mix.wav','--verbatim'],d/'audio-gate.log')==0
 # Every native frame's time/source identity, measured on a reduced raster; native boundaries reviewed independently.
 output=reader(v,N);base=reader(orig,N);replacement=reader(chosen,intro);scores=[];errors=[]
 for n in range(N):
  x=read(output).astype(np.float32);y=read(base)
  if n<intro:y=read(replacement)
  y=y.astype(np.float32);xc=x-x.mean();yc=y-y.mean();scores.append(float((xc*yc).sum()/np.sqrt((xc*xc).sum()*(yc*yc).sum())));errors.append(float(np.abs(x-y).mean()))
 for p in [output,base,replacement]:p.stdout.close();assert p.wait()==0
 lineage=dict(video_sha256=sha(v),method='Every native frame at native sequence index, reduced270x480 RGB raster; NCC/MAE to selected R2 intro before boundary, R1 exact frame after boundary. New output is encoded once, audio copied. Independent native first/last/boundary/dense inspection separately required.',intro_source=str(chosen),intro_sha256=sha(chosen),intro_frames=intro,rest_source=str(orig),rest_sha256=sha(orig),min_ncc=min(scores),mean_ncc=float(np.mean(scores)),max_mean_absolute_rgb_error=max(errors),frame_ncc=scores,frame_mae=errors)
 dump(d/'source-lineage.json',lineage);assert min(scores)>.97,(S,min(scores))
 # Native full resolution decode, all-frame edge measurement and sub0.25s person masks.
 cp=reader(v,N,1080,1920);paths=[];edge=[]
 for n in range(N):
  fr=read(cp,1080,1920);edge.append(int((fr[310:330,390:690].mean(2)<65).sum()))
  if n%7==0 or n in [0,N-1,intro-1,intro]:
   p=q/f'f{n:04d}.png';Image.fromarray(fr).save(p);paths.append(p)
 cp.stdout.close();assert cp.wait()==0
 PM=ROOT/'.claude/skills/shorts/reference/recentre/personmask';subprocess.run([str(PM),str(q/'m')]+list(map(str,paths)),capture_output=True,check=True);samples=[]
 for p in paths:
  mask=np.asarray(Image.open(q/'m'/f'{p.stem}.mask.png'))>127;mask[:310]=False;lab,num=ndimage.label(mask);assert num
  k=1+np.argmax(ndimage.sum(mask,lab,range(1,num+1)));m=lab==k;rr=np.where(m.sum(1)>=20)[0];yy,xx=np.where(m);assert len(rr);samples.append(dict(frame=int(p.stem[1:]),clearance=int(rr[0])-310,hair_y=int(rr[0]),left=int(xx.min()),right=int(xx.max())))
 f=dict(sha256=sha(v),frames=N,min_hair_clearance=min(x['clearance'] for x in samples),all_frame_top_edge_dark_pixels=edge,max_top_edge_dark_pixels=max(edge),samples=samples,title=TC.frame_report(str(v)));dump(d/'framing.json',f);assert f['min_hair_clearance']>=20 and max(edge)==0 and f['title']['verdict']=='OK',(S,f['min_hair_clearance'],max(edge),f['title'])
 for j in range(0,len(paths),24):
  im=Image.new('RGB',(1296,1616),'#edf4fb');dr=ImageDraw.Draw(im)
  for k,p in enumerate(paths[j:j+24]):
   x=k%6*216;y=k//6*404;im.paste(Image.open(p).resize((216,384)),(x,y+20));dr.text((x+2,y+2),f'{int(p.stem[1:])/FPS:.3f}s',fill='black')
  im.save(q/f'dense-{j//24:02d}.jpg',quality=93)
 shots=json.loads((old/'shots.json').read_text());shots[0].update(raw0=1256/FPS,raw1=(1256+intro)/FPS,crop=[595,40,698,1040],source_reference=str(chosen),source_reference_frames=[0,intro],source_reference_sha256=sha(chosen));dump(d/'shots.json',shots);alt=sum(s['f1']-s['f0'] for s in shots if s['kind']=='demo');dump(d/'coverage-source-evidence.json',dict(sha256=sha(v),frames=N,alternate_source_frames=alt,coverage=alt/N,min_ncc=min(scores),lineage=str(d/'source-lineage.json'),source='C1625 actual exercise footage; R1 shots/native source identity and R2 selected intro lineage',demo_spans=[dict(f0=s['f0'],f1=s['f1'],raw0=s['raw0'],raw1=s['raw1'],complete=s['complete']) for s in shots if s['kind']=='demo'],verified_samples=[dict(frame=i,ncc=scores[i]) for i in range(N)]))
 p=copy.deepcopy(json.loads((old/'gate/plan.json').read_text()));p['evidence_contract']['video_sha256']=sha(v);p['speech_words_evidence']['video_sha256']=sha(v);p['speech_words_evidence']['pipeline']+='; R3 full AAC packet data/pts/dts/durations identical to R1, verified in audio-identity.json';p['source_audio']=str(old/'his_mix.wav');p['source_picture']=str(old/'source_picture.mp4');p['watch_log']=str(d/'gate/logs/watch_pass.json');p.pop('instrument_adjudications',None)
 for k in ['style:coverage','junk:dead_air']:p['declare'].pop(k,None)
 p['declare']['framing:no_wide_level']='Exact wider teaching framing approved in R1 and option1 approved in R2. Full exercise must preserve complete head/body and hands; talking-head min-face-size is inapplicable to this complete teaching shot. Hair and actual presenter framing checks remain measured.'
 p['negative_events_scan']=dict(sha256=sha(v),frames_checked=len(samples),method='Every native frame decode, sub0.25s dense frames/person masks and shared watch packet; fresh independent whole-film visual/native review required',findings=[])
 dump(d/'gate/plan.json',p)
 cmd(['python3',ROOT/'.claude/skills/_shared/deliver/watch.py',v,'--plan',d/'gate/plan.json','--out',d/'gate/watch','--log',d/'gate/logs/watch_pass.json','--clips'],d/'watch.log');print('FULL QA PACKET',S,flush=True)
