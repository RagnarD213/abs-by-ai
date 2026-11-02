from pathlib import Path
import subprocess,json,sys,hashlib,os,math
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';E=W/'evidence';F=str(R/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-27'
V=Q/'Home Workouts SFC R2 - 1080p.mp4'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):Path(p).write_text(json.dumps(d,indent=2))
def ff(a):subprocess.run([F,'-v','error','-nostdin','-y']+list(map(str,a)),check=True)
def normalize_hyphens(ws):
 out=[]
 for x in ws:
  x=dict(x)
  if x['w'].strip().startswith('-') and out:
   out[-1]['w']=out[-1]['w']+x['w'].strip();out[-1]['e']=x['e']
  else:out.append(x)
 return out
def prep():
 h=sha(V);shots=json.load(open(W/'shots.json'));edl=json.load(open(W/'edl.json'));events=json.load(open(W/'asset-events.json'));gfx=json.load(open(W/'hf/manifest.json'));chunks=json.load(open(W/'caption-chunks.json'))
 sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as A
 A.stash_untreated(str(V),A.pcm(str(W/'untreated-cut.wav'),ac=1),note='Full selected C1719 lav before approved Gentle Bass shared chain; no other mic mixed.')
 ass=W/'build/Home Workouts SFC R2.ass';cues=[]
 sys.path.insert(0,str(R/'.claude/skills/_shared'));from deliver.checks.captions import read_cues
 cues=read_cues(str(ass));cdir=E/'caption-states';cdir.mkdir(exist_ok=True)
 mids=[int(math.ceil((a+b)/2*FPS)) for a,b,_ in cues]
 selection='+'.join(f'eq(n,{n})' for n in mids)
 ff(['-f','lavfi','-i','color=c=black@0.0:s=1080x1920:r=30000/1001:d=61.45,format=rgba','-vf',f"ass='{ass}':alpha=1,select='{selection}'",'-vsync','0','-frames:v',len(mids),cdir/'state-%03d.png'])
 states=[]
 for i,(a,b,txt) in enumerate(cues):
  p=cdir/f'state-{i+1:03}.png';im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox();assert box
  im.crop(box).save(p);states.append(dict(name=f'C{i+1:03}',beat=[a,b],image=str(p),image_sha256=sha(p),pos=list(box[:2]),word=txt.split()[0],text=txt,scope='whole-cue image; first-word onset only'))
 def srt(t):
  n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
 (Q/'Home Workouts SFC R2.srt').write_text('\n'.join(f'{i+1}\n{srt(a)} --> {srt(b)}\n{txt}\n' for i,(a,b,txt) in enumerate(cues)))
 ai=next(x for x in events if x['id']=='A0157');chip=E/'ai-label-from-independent-plate.png';plate=json.load(open(W/'media-plates.json'))['CLIENT']['mov']
 ff(['-ss','2','-i',plate,'-frames:v','1','-vf','crop=408:60:336:1216,format=rgba',chip])
 regions=[dict(name=x['id'],beat=[x['a'],x['b']],rect=[x['box'][0],x['band'][0],x['box'][2]-x['box'][0],x['band'][1]-x['band'][0]]) for x in gfx]
 for name,beat,rect in [('Equipment inset',[823/FPS,1150/FPS],[0,617,1080,606]),('Equipment title',[823/FPS,1150/FPS],[0,520,1080,80]),('Client inset',[ai['a']/FPS,ai['b']/FPS],[0,543,1080,606]),('Client title',[ai['a']/FPS,ai['b']/FPS],[0,445,1080,80]),('AI label',[ai['a']/FPS,ai['b']/FPS],[336,1216,408,60])]:regions.append(dict(name=name,beat=beat,rect=rect))
 covered=[[x['a']/FPS,x['b']/FPS] for x in events];windows=[]
 for s in shots:
  if s['kind']=='equipment':continue
  spans=[(s['n0'],s['n1'])]
  for x in events:
   spans=[v for a,b in spans for v in ([(a,min(b,x['a']))] if a<x['a'] else [])+([(max(a,x['b']),b)] if b>x['b'] else []) if v[1]>v[0]]
  windows += [dict(name=s['id'],beat=[a/FPS,b/FPS],rect=[0,0,1080,1920],motion='tracking') for a,b in spans]
 scenes=[dict(id=x['id'],beat=[x['a']/FPS,x['b']/FPS],reference=x['src'],reference_sha256=sha(x['src']),source_seconds=[x['ss'],x['ss']+(x['b']-x['a'])/FPS],expected={'B0431':'Real kettlebell deadlifts, complete shoes and weight','A0157':'AI client pushups with trainer; complete source height and label'}.get(x['id'],'October15 actual equipment; match named objects'),motion='natural-speed moving source') for x in events]
 joins=sorted(set([s[k]/FPS for s in shots for k in ['n0','n1']]+[x[k]/FPS for x in events for k in ['a','b']]))
 p=dict(target_frames=1841,target_seconds=1841/FPS,captions_ass=str(ass),srt=str(Q/'Home Workouts SFC R2.srt'),source_audio=str(W/'voice.wav'),joins=joins,audio_joins=[x['out'] for x in edl[1:]],covered=covered,punch=[[s['n0']/FPS,s['n1']/FPS,'NEAR' if s['kind']=='tight' else 'FAR'] for s in shots if s['kind']!='equipment'],graphics=[dict(name=x['id'],beat=[x['a'],x['b']],mov=x['mov']) for x in gfx],graphic_regions=regions,caption_states=states,talking_head_windows=windows,words=[dict(w=x['w'],t=x['t0'],e=x['t1']) for x in json.load(open(W/'words_out.json'))],watch_log=str(E/'watch.json'),evidence_contract=dict(version=2,video_sha256=h),ai_inserts=[dict(name='A0157',beat=[ai['a']/FPS,ai['b']/FPS])],real_photos=[],cards=[],label_tracks=[dict(name='A0157 AI disclosure',kind='ai',beat=[ai['a']/FPS,ai['b']/FPS],image=str(chip),image_sha256=sha(chip),rect=[336,1216,408,60])],independent_scenes=scenes,banned_source='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4',banned_times=[26.5,27.5,29.5,31.0])
 write(E/'plan.json',p);print('FULL_QA_PREP',h,flush=True)
def asr():
 sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech
 ws,method=speech.transcribe(str(V),model='small.en');write(E/'delivered-asr-raw-tokens.json',dict(sha256=sha(V),method=method,words=ws));ws=normalize_hyphens(ws);h=sha(V);write(E/'delivered-asr.json',dict(sha256=h,method=method,words=ws));p=json.load(open(E/'plan.json'));p.update(speech_words=ws,speech_words_evidence=dict(method='delivered_asr',video_sha256=h),transcript_words=[dict(w=x['w']) for x in ws]);write(E/'plan.json',p)
 import re,difflib
 expected=json.load(open(W/'words_out.json'));norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
 matcher=difflib.SequenceMatcher(None,[norm(x['w']) for x in expected],[norm(x['w']) for x in ws],autojunk=False)
 pairs=[(i+k,j+k) for i,j,n in matcher.get_matching_blocks() for k in range(n)];mapping=dict(pairs);onsets=[];ci=0
 for chunk in json.load(open(W/'caption-chunks.json')):
  spoken=ws[mapping[ci]] if ci in mapping else None;onsets.append(dict(text=' '.join(x['w'] for x in chunk),expected_start=chunk[0]['t0'],delivered_start=spoken['t'] if spoken else None,offset_ms=round((chunk[0]['t0']-spoken['t'])*1000,1) if spoken else None));ci+=len(chunk)
 write(E/'all-word-caption-alignment.json',dict(sha256=h,method='In-order full-word sequence alignment to fresh delivered AAC small.en ASR; independent inference, same acoustic-model family as R1. Diagnostic, not a perceptual listen.',expected_words=len(expected),delivered_words=len(ws),matched_words=len(pairs),unmatched_expected=[x for i,x in enumerate(expected) if i not in mapping],unmatched_delivered=[x for i,x in enumerate(ws) if i not in set(mapping.values())],cue_onsets=onsets))
 print('FULL_ASR_COMPLETE',len(pairs),'matched words',flush=True)
def audio():
 with open(E/'audio-gate.txt','w') as o:subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),str(V),'--ab',str(Q/'Home Workouts SFC R2 - reference A-B.mp4')],stdout=o,stderr=subprocess.STDOUT)
def watch():
 with open(E/'watch.txt','w') as o:subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(V),'--plan',str(E/'plan.json'),'--out',str(E/'watch'),'--log',str(E/'watch.json'),'--clips'],stdout=o,stderr=subprocess.STDOUT,check=True)
def gate():
 with open(E/'delivery-gate.txt','w') as o:r=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(V),'--format','short','--plan',str(E/'plan.json')],stdout=o,stderr=subprocess.STDOUT)
 print('FULL_GATE_EXIT',r.returncode,flush=True)
if __name__=='__main__':
 if (W/'rebuild-required.txt').exists():raise SystemExit('Repair checkpoint: source edge must be corrected before QA')
 for a in sys.argv[1:]:globals()[a]()
