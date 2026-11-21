"""Full-film shared QA preparation, actual delivered ASR/CTC and watch. No bounded exceptions."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(k,'1')
from pathlib import Path
import sys,json,hashlib,subprocess,re,math
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FPS=30000/1001
os.environ['PATH']=str(R/'Media/video_edit/bin')+os.pathsep+os.environ.get('PATH','');os.environ['GATE_GROUP']='DS-35'
FF=str(R/'Media/video_edit/bin/ffmpeg');FP=str(R/'Media/video_edit/bin/ffprobe')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=1))
def ff(args):subprocess.run([FF,'-v','error','-nostdin','-y']+list(map(str,args)),check=True)
def video(v):return W/'review/media'/('dad-bod-r2-'+v+'.mp4')
def prep(v):
 d=W/v;q=W/'qa'/v;q.mkdir(parents=True,exist_ok=True);vid=video(v);h=sha(vid);e=json.loads((d/'edl.json').read_text());shots=json.loads((d/'shots.json').read_text());L=json.loads((d/'r2-layout.json').read_text());m=json.loads((d/'graphics-manifest.json').read_text());ca,cb=L['comparison'];dur=e['total_seconds']
 probe=json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(vid)]));vs=next(x for x in probe['streams'] if x['codec_type']=='video');assert int(vs['nb_frames'])==e['total_frames'];assert(vs['width'],vs['height'],vs['r_frame_rate'])==(1080,1920,'30000/1001');write(q/'probe.json',probe)
 joins={67/FPS,284/FPS,469/FPS,485/FPS,ca/FPS,cb/FPS};joins.update(s['a'] for s in shots);joins.update(c['film0'] for c in e['clip']['segs']);cameras=[x['exact_after_pts'] for x in json.loads((O/'native-camera-pairs.json').read_text())]
 for c in e['clip']['segs']:
  for t in cameras:
   if c['clip_in']<t<c['clip_out']:joins.add((c['n0']+math.ceil((t-c['clip_in'])*FPS-1e-7))/FPS)
 # The continuing silent panel has its own native source cuts.
 for x in json.loads((W/'silent-panel-native-cuts.json').read_text()):
  if 485<x['output_after_frame']<ca:joins.add(x['output_after_seconds'])
 for t in cameras:
  g=469+math.ceil((t-e['tr']['clip_in'])*FPS-1e-7)
  if 485<g<ca:joins.add(g/FPS)
 covered=[[ca/FPS,cb/FPS]];windows=[];punch=[]
 for c in e['clip']['segs']:
  a=c['film0'];b=min(284/FPS,(c['n0']+c['frames'])/FPS)
  if a<b:windows.append(dict(name='Silent synced real corner '+c['id'],beat=[a,b],rect=[0,1250,432,670],motion='fixed-wide'))
 windows.append(dict(name='Large watching in foreground',beat=[284/FPS,485/FPS],rect=[0,530,1080,1390],motion='fixed-wide'))
 windows.append(dict(name='Response in foreground',beat=[485/FPS,ca/FPS],rect=[0,520,1080,1400],motion='tracking'))
 for s in shots:
  a,b=max(s['n0'],cb)/FPS,s['n1']/FPS
  if b<=a:continue
  if s['kind']=='photo':covered.append([a,b]);continue
  windows.append(dict(name=s['id'],beat=[a,b],rect=[0,0,1080,1920],motion='tracking'))
 for s in shots:punch.append([s['a'],s['b'],s['id']+'-'+s['size']])
 gfx=[];regions=[];scenes=[];photos=[];labels=[]
 for x in m:
  beat=[x['a'],x['b']];gfx.append(dict(name=x['id'],beat=beat,mov=x['mov']));scenes.append(dict(id=x['id'],beat=beat,reference=x['mov'],reference_sha256=sha(x['mov']),expected=x['words'],kind=x['kind'],photo_reference=x.get('photo'),photo_sha256=sha(x['photo']) if x.get('photo') else None))
  if x['id']=='R2_SourcePanel':regions.extend([dict(name='Source Title',beat=beat,rect=[30,10,1020,70]),dict(name='Horizontal Source',beat=beat,rect=[0,92,1080,608])])
  elif x['id'].startswith('R2_Compare'):
   regions.append(dict(name=x['id'],beat=beat,rect=[50,100,980,1150]));covered.append(beat)
  elif x['kind']=='glass':
   x0,y0,x1,y1=x['box'];regions.append(dict(name=x['id'],beat=beat,rect=[x0,y0-4,x1-x0,y1-y0+44]))
  else:
   for name,rect in [('photo',[80,150,920,880]),('disclosure',[80,1070,920,80]),('fact',[80,1165,920,300])]:regions.append(dict(name=x['id']+' '+name,beat=beat,rect=rect))
   chip=q/(x['id']+'-component-label.png');ff(['-ss',str((x['b']-x['a'])*.62),'-i',x['mov'],'-frames:v','1','-vf','scale=in_color_matrix=bt601:in_range=tv:out_range=pc,format=rgba,crop=892:80:94:1070',chip]);photos.append(dict(name=x['id'],beat=beat,chip=str(chip),pos=[94,1070]));labels.append(dict(name=x['id']+' disclosure',kind='real',beat=beat,image=str(chip),image_sha256=sha(chip),rect=[94,1070,892,80]))
 words=json.loads((d/'words_out.json').read_text());plan=dict(scope='CONTENT SFC R2 FULL COMPLETE FILM, no bounded preview exceptions',video_sha256=h,target_frames=e['total_frames'],target_seconds=dur,version=v,joins=sorted(x for x in joins if 0<x<dur),audio_joins=[x['film0'] for x in e['clip']['segs'][1:]]+[469/FPS]+[p['film0'] for p in e['pieces']],covered=covered,punch=punch,punch_covered=[any(a<=p[0] and b>=p[1] for a,b in covered) for p in punch],graphics=gfx,graphic_regions=regions,talking_head_windows=windows,words=[dict(w=x['w'],t=x['t0'],e=x['t1']) for x in words],captions_ass=str(d/'captions.ass'),srt=str(d/'captions.srt'),cards=[],ai_inserts=[],real_photos=photos,label_tracks=labels,evidence_contract=dict(version=2,video_sha256=h),source_audio=str(d/'mix-untreated.wav'),watch_log=str(q/'watch_pass.json'),banned_source='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4',banned_times=[26.5,27.5,29.5,31.0],independent_scenes=scenes,caption_source=dict(ass=str(d/'captions.ass'),sha256=sha(d/'captions.ass')))
 write(q/'plan.json',plan);ff(['-xerror','-i',vid,'-f','null','-']);print('FULL_QA_PREP',v,h,flush=True)
def asr(v):
 import torch,whisper
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES',4)));q=W/'qa'/v;vid=video(v);p=json.loads((q/'plan.json').read_text());assert p['video_sha256']==sha(vid)
 wav=q/'delivered-16k.wav';ff(['-i',vid,'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',wav]);model=whisper.load_model('medium.en');r=model.transcribe(str(wav),language='en',fp16=False,word_timestamps=True,temperature=0)
 rec=dict(video_sha256=p['video_sha256'],model='medium.en',method='Full actual final AAC retranscribed independently of expected script/captions',text=r['text'],words=[dict(w=t['word'].strip(),t=t['start'],e=t['end']) for s in r['segments'] for t in s.get('words',[])])
 write(q/'delivered-asr.json',rec);p.update(transcript_words=[dict(w=x['w']) for x in rec['words']],speech_words=rec['words'],speech_words_evidence=dict(method='delivered_asr',video_sha256=p['video_sha256']));write(q/'plan.json',p);print('FULL_ASR',v,flush=True)
def watch(v):
 q=W/'qa'/v;subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(video(v)),'--plan',str(q/'plan.json'),'--out',str(q/'watch'),'--log',str(q/'watch_pass.json'),'--clips'],check=True)
def gate(v):
 q=W/'qa'/v;ret=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(video(v)),'--format','short','--plan',str(q/'plan.json'),'--json',str(q/'gate-raw.json')]);print('FULL_GATE',v,ret.returncode,flush=True)
if __name__=='__main__':
 action,v=sys.argv[1:];sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq;renderq.hold_until_exit('Dad Bod full '+action+' '+v,pool='heavy' if action=='asr' else 'light');globals()[action](v)
