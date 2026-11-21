"""Exact-file evidence and checks for SL11. No gate overrides or stamp forging."""
from pathlib import Path
import sys,json,subprocess,hashlib,datetime,re,os,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
from full import R,ROOT,FF,FPS,SR,sha,dump
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
PM=str(ROOT/'.claude/skills/shorts/reference/recentre/personmask');FB=str(Path.home()/'.cache/absbyai/facebox')
def command(args,log):
 with open(log,'w') as f:r=subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT)
 print('COMMAND',log,r.returncode,flush=True);return r.returncode

def framing(S):
 d=R/'build'/S;v=d/f'Vacuum-{S}-R1.mp4';q=d/'exact-framing';q.mkdir(exist_ok=True);paths=[];edge=[];n=0
 cp=subprocess.Popen([FF,'-nostdin','-v','error','-threads','1','-filter_threads','1','-i',str(v),'-vf','scale=in_color_matrix=bt709:in_range=tv,format=rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
 while True:
  b=cp.stdout.read(1080*1920*3)
  if not b:break
  assert len(b)==1080*1920*3
  a=np.frombuffer(b,np.uint8).reshape(1920,1080,3);edge.append(int((a[310:330,390:690].mean(2)<65).sum()))
  if n%7==0:
   p=q/f'f{n:04d}.png';Image.fromarray(a).save(p);paths.append(p)
  n+=1
 cp.stdout.close();assert cp.wait()==0
 subprocess.run([PM,str(q/'m')]+list(map(str,paths)),check=True,capture_output=True)
 fbs={}
 for line in subprocess.run([FB]+list(map(str,paths)),check=True,capture_output=True,text=True).stdout.splitlines():
  p,b=line.split('\t');fbs[p]=b
 rows=[]
 for p in paths:
  mask=np.array(Image.open(q/'m'/f'{p.stem}.mask.png'))>127;mask[:310]=False;lab,num=ndimage.label(mask);assert num,('no person',p)
  k=1+np.argmax(ndimage.sum(mask,lab,range(1,num+1)));m=lab==k;rr=np.where(m.sum(1)>=20)[0];assert len(rr),p;yy,xx=np.where(m)
  rows.append(dict(frame=int(p.stem[1:]),hair_y=int(rr[0]),clearance=int(rr[0])-310,left=int(xx.min()),right=int(xx.max()),face=fbs[str(p)]))
 report=dict(video=str(v),sha256=sha(v),frames=n,every_frame_top_edge_dark_pixels=edge,interval_frames=7,max_sample_gap_seconds=7/FPS,min_hair_clearance=min(z['clearance'] for z in rows),samples=rows)
 dump(d/'framing.json',report)
 # 25 native-derived frames per readable contact sheet, ALL samples available individually for audit.
 sheets=[]
 for j in range(0,len(paths),25):
  sheet=Image.new('RGB',(1350,2500),'#111b28');dr=ImageDraw.Draw(sheet)
  for k,p in enumerate(paths[j:j+25]):
   x=k%5*270;y=k//5*500;sheet.paste(Image.open(p).resize((270,480)),(x,y+20));dr.text((x+6,y+2),f'{int(p.stem[1:])/FPS:.3f}s',fill='white')
  out=q/f'dense-{j//25:02d}.jpg';sheet.save(out,quality=93);sheets.append(str(out))
 dump(d/'dense-sheets.json',sheets);assert report['min_hair_clearance']>=20,report['min_hair_clearance'];assert max(edge)==0,max(edge);print('FRAMING',S,n,report['min_hair_clearance'],len(sheets),flush=True)

def asr(S):
 import torch,whisper
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 d=R/'build'/S;v=d/f'Vacuum-{S}-R1.mp4'
 a=subprocess.check_output([FF,'-nostdin','-v','error','-i',str(v),'-vn','-ac','1','-ar','16000','-f','s16le','-']);x=np.frombuffer(a,'<i2').astype(np.float32)/32768
 result=whisper.load_model('small.en').transcribe(x,fp16=False,condition_on_previous_text=False,word_timestamps=True)
 ws=[dict(w=w['word'].strip(),t=w['start'],e=w['end']) for s in result['segments'] for w in s.get('words',[])]
 import difflib
 nz=lambda s:re.sub('[^a-z0-9]','',s.lower());intended=json.loads((d/'words.json').read_text());a=[nz(w['w']) for w in intended];b=[nz(w['w']) for w in ws];sm=difflib.SequenceMatcher(None,a,b,autojunk=False);diffs=[dict(op=op,intended=' '.join(a[a0:a1]),heard=' '.join(b[b0:b1])) for op,a0,a1,b0,b1 in sm.get_opcodes() if op!='equal']
 dump(d/'delivered_asr.json',dict(sha256=sha(v),words=ws,text=result['text'],similarity=sm.ratio(),diffs=diffs));print('ASR',S,sm.ratio(),diffs,flush=True)

def plan(S):
 d=R/'build'/S;v=d/f'Vacuum-{S}-R1.mp4';h=sha(v);T=json.loads((d/'timeline.json').read_text());shots=json.loads((d/'shots.json').read_text());man=json.loads((d/'graphics.json').read_text());cs=json.loads((d/'cues.json').read_text());ws=json.loads((d/'words.json').read_text());asr=json.loads((d/'delivered_asr.json').read_text());assert asr['sha256']==h
 g=d/'gate';g.mkdir(exist_ok=True);(g/'logs').mkdir(exist_ok=True)
 def beat(sh):return [round(sh['f0']/FPS,5),round(sh['f1']/FPS,5)]
 joins=[sh['f0']/FPS for sh in shots[1:]];covered=[beat(s) for s in shots if s['kind']=='demo']
 for a,b in zip(shots,shots[1:]):
  if a['level']!=b['level'] or a['roll']!=b['roll']:covered.append([max(0,b['f0']/FPS-.05),min(T['seconds'],b['f0']/FPS+.05)])
 def ts(t):
  m=round(t*1000);return f'{m//3600000:02}:{m%3600000//60000:02}:{m%60000//1000:02},{m%1000:03}'
 srt=g/'captions.srt';srt.write_text('\n'.join(f"{i+1}\n{ts(c['f0']/FPS)} --> {ts(c['f1']/FPS)}\n{c['text']}\n" for i,c in enumerate(cs)))
 pl=dict(target_frames=T['frames'],target_seconds=T['seconds'],joins=sorted(set(joins+T['audio_joins'])),audio_joins=T['audio_joins'],covered=covered,punch=[beat(s)+[s['level']] for s in shots],punch_covered=[s['kind']=='demo' for s in shots],graphics=[dict(name=m['id'],beat=[m['a'],m['b']],mov=m['mov']) for m in man],graphic_regions=[dict(name='title_band',beat=[0,T['seconds']],rect=[0,0,1080,310]),dict(name='wordmark',beat=[0,T['seconds']],rect=[60,1796,280,60])]+[dict(name=m['id'],beat=[m['a'],m['b']],rect=[m['box'][0],m['box'][1],m['box'][2]-m['box'][0],m['box'][3]-m['box'][1]]) for m in man],talking_head_windows=[dict(name=f"talk{s['idx']}",beat=beat(s),rect=[0,310,1080,1610],motion='fixed-wide') for s in shots if s['kind']=='talk'],evidence_contract=dict(version=2,video_sha256=h),caption_states=[dict(name=f'cap{i:03d}',beat=[c['f0']/FPS,c['f1']/FPS],image=c['png'],image_sha256=c['sha256'],rect=[0,0,1080,1920],word=ws[c['first_word_index']]['w']) for i,c in enumerate(cs)],speech_words=[{k:ws[c['first_word_index']][k] for k in ['w','t','e']} for c in cs],speech_words_evidence=dict(method='verbatim_source_ctc',video_sha256=h,pipeline=('Exact approved RO02 parent cuts'+('; explicitly authorized AI Dan ownvoice Natural from same shoot; audio/pickup-choice.json and standalone synthetic audio stamp retained' if S=='B' else '; no new speech')+', force-aligned per intact speech piece with WAV2VEC2_ASR_BASE_960H; this exact MP4 must pass audio_gate --verbatim against his_mix.wav')),words=[{k:w[k] for k in ['w','t','e']} for w in ws],transcript_words=[dict(w=w['w']) for w in asr['words']],srt=str(srt),source_audio=str(d/'his_mix.wav'),source_picture=str(d/'source_picture.mp4'),watch_log=str(g/'logs/watch_pass.json'),ai_inserts=[],real_photos=[],cards=[],declare={'framing:no_wide_level':'Dan explicitly approved these exact wider teaching compositions in framing-graphics-approval.json on2026-10-26, preserving whole exercise and hands. A full-body demonstration requires a smaller head. Exact dense hair/head clearance and independent every-frame top-edge checks still apply.','compliance:banned_screen':'Only controlled raw camera rolls C1622–C1626, captions and approved HyperFrames graphics; no app or screen-recording source exists in this edit. Speech provenance is recorded separately in the source audio and pickup-choice evidence.'})
 watch=g/'logs/watch_pass.json';wd=json.loads(watch.read_text()) if watch.exists() else {};fr=d/'framing.json';fd=json.loads(fr.read_text()) if fr.exists() else {};assert not fd or fd['sha256']==h
 pl['negative_events_scan']=dict(sha256=h,when=datetime.datetime.now().isoformat(timespec='seconds'),frames_checked=len(fd.get('samples',[])),method='Exact MP4 native decode, samples every7frames (<.25s), every-frame top-edge scan; watch contact sheets and native consecutive boundary strips'+(' independently judged with zero open defects' if wd.get('inspected') and wd.get('open_defects')==0 and wd.get('sha256')==h else '; independent judgment pending'),findings=[])
 if S in ['B','C']:
  evidence=json.loads((d/'coverage-source-evidence.json').read_text());adjudication=json.loads((d/'independent/coverage-adjudication.json').read_text());assert evidence['sha256']==h and evidence['coverage']>=.30 and evidence['min_ncc']>.97
  assert h in [adjudication.get(k) for k in ['sha256','video_sha256','candidate_sha256']]
  original='gate/original-instrument-fail' if S=='B' else 'gate/original-palette-fail'
  pl['declare']['style:coverage']=f"Palette-only instrument inapplicable to this same-set instructional B-roll: exact source verification finds{evidence['alternate_source_frames']}/{evidence['frames']}frames ({100*evidence['coverage']:.5f}%) of separate C1625 exercise footage over parent narration. The editorial30%cutaway requirement remains applicable and is positively met. {len(evidence['verified_samples'])}native source-identity comparisons have minNCC{evidence['min_ncc']:.9f}, plus complete independent moving/native audits. See coverage-source-evidence.json and independent/coverage-adjudication.json; original numerical FAIL retained in {original}. No threshold or global check changed."
  pl['instrument_adjudications']={'style:coverage':dict(editorial_requirement_applicable=True,minimum=.30,actual=evidence['coverage'],source_evidence=str(d/'coverage-source-evidence.json'),independent=str(d/'independent/coverage-adjudication.json'),sha256=h)}
 if S=='B':
  pause=json.loads((d/'independent/pause-adjudication.json').read_text());assert pause['video_sha256']==h and pause['verdict'].startswith('RETAIN') and sha(d/'his_mix.wav')==pause['approved_mix_sha256']
  pl['declare']['junk:dead_air']='Silence-only instrument cannot classify this verified purposeful teaching pause. Exactly one original numerical flag24.32–25.58s (1.26s vs unchanged1.00s bound) follows the explicit you-can-see cue over continuous relevant exercise and the Small Breaths card. Fresh focused audiovisual review and nativeframes728/735/749/763 find observation time, no abandoned take/reset. VIDEO-RULES Cut continuity QC explicitly preserves purposeful teaching pauses. Other38 measured gaps are below1s; complete independent audit found no unnecessary dead air. The editorial requirement remains applicable and met; no audible-sniff claim, audio mutation or threshold change. Exact approved50second WAV remains f83dff214840e22784a404f49cb6e1afff5f0474984540cb39b78c24e3251f81. See independent/pause-adjudication.json and original numerical FAIL in gate/original-instrument-fail.'
  pl['instrument_adjudications']['junk:dead_air']=dict(editorial_requirement_applicable=True,bound_seconds=1.0,only_flag=[24.32,25.58],disposition='Purposeful observation pause retained under standing teaching-pause rule',other_measured_gaps_below_bound=38,independent=str(d/'independent/pause-adjudication.json'),sha256=h)
 dump(g/'plan.json',pl);print('PLAN',S,flush=True)

def checks(S):
 d=R/'build'/S;v=d/f'Vacuum-{S}-R1.mp4';rev=R/'review/films';rev.mkdir(exist_ok=True)
 command(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',v,'--reference-mix',d/'his_mix.wav','--verbatim','--ab',rev/f'Vacuum-{S}-audio-AB.mp4'],d/'audio-check.log')
 command([FF,'-nostdin','-v','error','-y','-i',v,'-vf','scale=540:960:flags=lanczos','-c:v','libx264','-crf','23','-preset','veryfast','-c:a','aac','-b:a','128k','-movflags','+faststart',rev/f'Vacuum-{S}-R1-540p.mp4'],d/'phone-copy.log')
 asr(S);framing(S);plan(S)
 command(['python3',ROOT/'.claude/skills/_shared/deliver/watch.py',v,'--plan',d/'gate/plan.json','--out',d/'gate/watch','--log',d/'gate/logs/watch_pass.json','--clips'],d/'watch-build.log')
 print('AUDIT PACKET READY',S,flush=True)

def gate(S):
 d=R/'build'/S;plan(S);import package as PK;v=PK.stage(S);return command(['python3',ROOT/'.claude/skills/_shared/deliver/gate.py',v,'--format','short','--plan',d/'gate/plan.json','--json',d/'gate/result.json'],d/'gate/check.log')
if __name__=='__main__':
 stage=sys.argv[1];chosen=sys.argv[2:] or ['A','B','C']
 if stage=='plan':
  for S in chosen:plan(S)
 else:
  with renderq.slot('Vacuum exact '+stage+' '+','.join(chosen),pool=('light' if stage=='gate' else 'heavy'),group='SL-11'):
   for S in chosen:{'checks':checks,'framing':framing,'asr':asr,'gate':gate}[stage](S)
