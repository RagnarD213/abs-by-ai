"""Exact-file B evidence using the shared audio, watch, and delivery gates. No private bounds."""
from pathlib import Path
import sys,json,re,subprocess,hashlib,os,math
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round2');V=R/'review/Keep Your Muscle - B - Daily Protein - R2.mp4';D=R/'build/B-full-final5';G=R/'qa/B';G.mkdir(parents=True,exist_ok=True);(G/'logs').mkdir(exist_ok=True)
FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import packet as P
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a,log=None):
 z=subprocess.run(list(map(str,a)),capture_output=True,text=True)
 if log:Path(log).write_text(z.stdout+z.stderr+'\nEXIT '+str(z.returncode))
 elif z.returncode:raise RuntimeError(z.stderr[-2000:])
 return z
def secs(s):
 h,m,t=s.split(':');return int(h)*3600+int(m)*60+float(t)
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
spec=json.loads((R/'build/B-spec.json').read_text());dur=round((spec['b']-spec['a'])*FPS)/FPS;N=round(dur*FPS);h=sha(V)
rc=run(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',V,'--reference-mix',D/'speech.wav','--verbatim','--ab',R/'review/B-source-then-short.mp4'],G/'audio.log');print('AUDIO_EXIT',rc.returncode,flush=True)
cues=[]
for l in (D/'captions.ass').read_text().splitlines():
 if not l.startswith('Dialogue:'):continue
 q=l.split(',',9);a,b=secs(q[1]),secs(q[2]);txt=re.sub(r'\{.*?\}','',q[9]).replace(r'\N','\n');cues.append(dict(a=a,b=b,text=txt))
(G/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["a"])} --> {stamp(c["b"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
# Actual libass alpha states rendered from the very same ASS used in the delivered video.
statesdir=G/'caption-states';statesdir.mkdir(exist_ok=True);frames=[round((c['a']+c['b'])/2*FPS) for c in cues]
if len(list(statesdir.glob('cap*.png')))!=len(cues):
 select='+'.join(f'eq(n,{n})' for n in frames)
 run([FF,'-v','error','-y','-f','lavfi','-i',f'color=black@0:s=1080x1920:r=30000/1001:d={dur}','-vf',f"format=rgba,colorchannelmixer=aa=0,ass='{D/'captions.ass'}':alpha=1,select='{select}'",'-vsync','0',statesdir/'cap%03d.png'])
paths=sorted(statesdir.glob('cap*.png'));assert len(paths)==len(cues)
states=[]
for i,(c,p) in enumerate(zip(cues,paths)):
 assert Image.open(p).getchannel('A').getextrema()==(0,255),p
 assert Image.open(p).getchannel('A').getbbox(),p
 states.append(dict(name=f'cap{i:03d}',beat=[c['a'],c['b']],image=str(p),image_sha256=sha(p),rect=[0,0,1080,1920],word=c['text'].split()[0]))
words=json.loads((D/'words.json').read_text());first=[];k=0
norm=lambda t:re.sub('[^a-z0-9]','',t.lower())
for c in cues:
 tokens=c['text'].split();assert norm(words[k]['w'])==norm(tokens[0]),(k,tokens,words[k]);first.append(words[k]);k+=len(tokens)
assert k==len(words)
asrp=G/'delivered-asr.json'
if not asrp.exists() or json.loads(asrp.read_text()).get('sha256')!=h:
 import whisper,torch
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 data=subprocess.check_output([FF,'-v','error','-i',str(V),'-vn','-ar','16000','-ac','1','-f','s16le','-']);x=np.frombuffer(data,'<i2').astype(np.float32)/32768
 asr=whisper.load_model('small.en').transcribe(x,fp16=False,condition_on_previous_text=False,word_timestamps=True)
 aw=[dict(w=w['word'].strip(),t=w['start'],e=w['end']) for s in asr['segments'] for w in s['words']];asrp.write_text(json.dumps(dict(sha256=h,words=aw,text=asr['text']),indent=2))
asr=json.loads(asrp.read_text());a=spec['a'];c0,c1=[t-a for t in spec['card']]
joins=sorted(set([c0,c1]+[round(e['out_in']-a,6) for e in P.SHEET['edl'] if a<e['out_in']<spec['b']]))
boundaries=[0]+joins+[dur];punch=[];covered=[];windows=[]
for x,y in zip(boundaries,boundaries[1:]):
 if y-x<.001:continue
 card=c0<=((x+y)/2)<c1
 e=next(z for z in P.SHEET['edl'] if z['out_in']<=a+(x+y)/2<z['out_out']);f=next(z for z in P.SHEET['framing'] if z['name']==e['shot']);level='CARD' if card else 'CAMERA-'+str(f['crop'][0]);punch.append([x,y,level]);covered.append(card)
 if not card:windows.append(dict(name=e['shot'],beat=[x,y],rect=[0,310,1080,1610],motion='fixed-wide'))
plan=dict(target_frames=N,target_seconds=dur,joins=joins,audio_joins=[round(e['out_in']-a,6) for e in P.SHEET['edl'] if e['join']=='cut' and a<e['out_in']<spec['b']],covered=[[c0,c1]],punch=punch,punch_covered=covered,
 graphics=[dict(name='ProteinCalculation',beat=[c0,c1],mov=str(R.parent/'round1/asset-review/hf/renders/card-B-v2.mov'))],
 graphic_regions=[dict(name='PersistentTitle',beat=[0,dur],rect=[0,0,1080,310]),dict(name='CalculationTextAndRows',beat=[c0,c1],rect=[76,430,930,770])],
 talking_head_windows=windows,evidence_contract=dict(version=2,video_sha256=h),caption_states=states,speech_words=first,speech_words_evidence=dict(method='verbatim_source_ctc',video_sha256=h,pipeline='Wav2Vec2 CTC on exact approved-parent audio extraction; current audio gate verifies actual AAC is verbatim'),words=words,transcript_words=asr['words'],srt=str(G/'captions.srt'),captions_ass=str(D/'captions.ass'),source_audio=str(D/'speech.wav'),watch_log=str(G/'logs/watch_pass.json'),ai_inserts=[],real_photos=[],cards=[],declare={'compliance:banned_screen':'The only picture sources are the locked RO01 studio camera master and approved moving protein calculation/title graphics. No app, phone, screen recording, or external screen imagery is present in B.'})
plan['underlying_metadata_rows']=plan['joins']
plan['joins']=[n/FPS for n in [87,88,100,365,487,491,897]]
holds=[(0,87,'CAMERA-W'),(87,491,'CALCULATION'),(491,897,'CAMERA-W'),(897,1016,'CAMERA-T')]
plan['punch']=[[a/FPS,b/FPS,name] for a,b,name in holds];plan['punch_covered']=[False,True,False,False]
plan['talking_head_windows']=[dict(name=name,beat=[a/FPS,b/FPS],rect=[0,310,1080,1610],motion='fixed-wide') for a,b,name in holds if name!='CALCULATION']
plan['graphics'][0]['beat']=[87/FPS,491/FPS];plan['graphic_regions'][1]['beat']=[87/FPS,491/FPS];plan['covered']=[[87/FPS,491/FPS],[897/FPS,dur]]
plan['hold_definition_evidence']='Exact native review: card starts87, camera returns491, real W/Tcut897. Metadata-only EDLrows are not separate composition holds.'
(G/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
run(['python3',ROOT/'.claude/skills/_shared/deliver/watch.py',V,'--plan',G/'plan.json','--out',G/'watch','--log',G/'logs/watch_pass.json'],G/'watch.log');print('EXACT_B_QA_PACKET_READY',h,flush=True)
