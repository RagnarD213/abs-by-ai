"""Exact A evidence for the maintained audio/watch/delivery gates."""
from pathlib import Path
import sys,json,re,subprocess,hashlib,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round3');D=R/'build';G=R/'qa/A-final-clean';G.mkdir(parents=True,exist_ok=True);(G/'logs').mkdir(exist_ok=True)
spec=json.loads((D/'A-spec.json').read_text());V=Path(spec['file']);FPS=30000/1001;dur=spec['seconds'];h=spec['sha256'];FF=str(ROOT/'Media/video_edit/bin/ffmpeg');SH=ROOT/'.claude/skills/_shared'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args,log=None):
 z=subprocess.run(list(map(str,args)),capture_output=True,text=True)
 if log:Path(log).write_text(z.stdout+z.stderr+'\nEXIT '+str(z.returncode))
 elif z.returncode:raise RuntimeError(z.stderr[-3000:])
 return z
def secs(t):
 a,b,c=t.split(':');return int(a)*3600+int(b)*60+float(c)
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
z=run(['python3',SH/'audio/audio_gate.py',V,'--reference-mix',D/'reference-mix.wav','--verbatim','--ab',R/'review/A-source-then-short.mp4'],G/'audio.log');print('A_AUDIO_EXIT',z.returncode,flush=True)
cues=[]
for l in (D/'captions.ass').read_text().splitlines():
 if not l.startswith('Dialogue:'):continue
 q=l.split(',',9);cues.append(dict(a=secs(q[1]),b=secs(q[2]),text=re.sub(r'\{.*?\}','',q[9]).replace(r'\N','\n')))
(G/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["a"])} --> {stamp(c["b"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
statesdir=G/'caption-states-alpha';statesdir.mkdir(exist_ok=True)
frames=[round((c['a']+c['b'])/2*FPS) for c in cues];select='+'.join(f'eq(n,{n})' for n in frames)
if len(list(statesdir.glob('cap*.png')))!=len(cues):run([FF,'-v','error','-y','-f','lavfi','-i',f'color=black@0:s=1080x1920:r=30000/1001:d={dur}','-vf',f"format=rgba,colorchannelmixer=aa=0,select='{select}',ass='{D/'captions.ass'}':alpha=1",'-vsync','0',statesdir/'cap%03d.png'])
states=[]
for i,(c,p) in enumerate(zip(cues,sorted(statesdir.glob('cap*.png')))):
 im=Image.open(p);assert im.getchannel('A').getextrema()==(0,255);assert im.getchannel('A').getbbox()
 states.append(dict(name=f'cap{i:03d}',beat=[c['a'],c['b']],image=str(p),image_sha256=sha(p),rect=[0,0,1080,1920],word=c['text'].split()[0]))
assert len(states)==len(cues)
words=json.loads((D/'words.json').read_text());first=[];k=0;norm=lambda t:re.sub('[^a-z0-9]','',t.lower())
for c in cues:
 tokens=c['text'].split();assert norm(words[k]['w'])==norm(tokens[0]);first.append(words[k]);k+=len(tokens)
assert k==len(words)
asrp=G/'delivered-asr.json'
if not asrp.exists() or json.loads(asrp.read_text()).get('sha256')!=h:
 import whisper,torch
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 data=subprocess.check_output([FF,'-v','error','-i',str(V),'-vn','-ar','16000','-ac','1','-f','s16le','-']);x=np.frombuffer(data,'<i2').astype(np.float32)/32768
 a=whisper.load_model('small.en').transcribe(x,fp16=False,condition_on_previous_text=False,word_timestamps=True)
 aw=[dict(w=w['word'].strip(),t=w['start'],e=w['end']) for s in a['segments'] for w in s['words']];asrp.write_text(json.dumps(dict(sha256=h,words=aw,text=a['text']),indent=2))
asr=json.loads(asrp.read_text());intro=spec['intro'];ai_end=spec['ai_end'];curls_end=spec['curls_end'];near=spec['near_at'];ca,cp=spec['card'];card=R.parent/'round1/asset-review/hf/renders/card-A-v2.mov'
chip=G/'ai-label.png';im=Image.new('RGBA',(310,58),(19,47,73,235));dr=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',33);dr.text((16,11),'AI-GENERATED',font=font,fill='white',anchor='lt');im.save(chip)
plan=dict(target_frames=spec['frames'],target_seconds=dur,joins=[ai_end,intro,curls_end,near,ca,cp],audio_joins=[intro],covered=[[0,curls_end],[near,ca],[ca,dur]],punch=[[0,ai_end,'AI'],[ai_end,curls_end,'CURLS'],[curls_end,near,'CAMERA-W'],[near,ca,'CAMERA-T'],[ca,cp,'TRAINING'],[cp,dur,'PUSHUPS']],punch_covered=[True,True,False,False,True,True],graphics=[dict(name='TrainingProgression',beat=[ca,cp],mov=str(card))],graphic_regions=[dict(name='PersistentTitle',beat=[0,dur],rect=[0,0,1080,310]),dict(name='TrainingTextAndRows',beat=[ca,cp],rect=[76,430,930,770]),dict(name='AI-Disclosure',beat=[0,ai_end],rect=[66,354,310,58])],talking_head_windows=[dict(name='CAMERA-W',beat=[curls_end,near],rect=[0,310,1080,1610],motion='fixed-wide'),dict(name='CAMERA-T',beat=[near,ca],rect=[0,310,1080,1610],motion='fixed-wide')],evidence_contract=dict(version=2,video_sha256=h),caption_states=states,speech_words=first,speech_words_evidence=dict(method='verbatim_source_ctc',video_sha256=h,pipeline='CTC on exact approved Voice2 plus approved-master audio; same offsets and continuous source range, current audio gate checks actual AAC against exact reference mix'),words=words,transcript_words=asr['words'],srt=str(G/'captions.srt'),captions_ass=str(D/'captions.ass'),source_audio=str(D/'reference-mix.wav'),watch_log=str(G/'logs/watch_pass.json'),ai_inserts=[dict(beat=[0,ai_end],file=spec['motion'])],real_photos=[],cards=[],label_tracks=[dict(name='AI-Generated opening',kind='ai',beat=[0,ai_end],image=str(chip),image_sha256=sha(chip),rect=[66,354,310,58],visibility='full')],declare={'compliance:banned_screen':'Only approved RO01 studio camera footage, complete real pushups, moving training/title graphics and approved object-only weights/medication AI B-roll; no app, phone, screens or banned UI.'})
(G/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
z=run(['python3',SH/'deliver/watch.py',V,'--plan',G/'plan.json','--out',G/'watch','--log',G/'logs/watch_pass.json'],G/'watch.log');assert z.returncode==0,(G/'watch.log').read_text()[-2000:]
print('A_QA_PACKET_READY',h,flush=True)
