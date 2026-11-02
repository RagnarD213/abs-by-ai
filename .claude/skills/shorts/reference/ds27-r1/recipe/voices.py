from pathlib import Path
import subprocess,json,os,sys,shutil,random,re,collections
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];O=W/'audio';Q=W/'review';F=str(R/'Media/video_edit/bin/ffmpeg');A=R/'.claude/skills/_shared/audio';O.mkdir(exist_ok=True)
os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-27'
def ff(args):subprocess.run([F,'-v','error','-nostdin','-y']+list(map(str,args)),check=True)
source=json.load(open(W/'source.json'));start=json.load(open(W/'edl.json'))[0]['start']
raw=O/'source-30.wav';srcmap=source['lav']
pieces=json.load(open(W/'edl.json'));remaining=30.;parts=[]
for i,p in enumerate(pieces):
 dur=min(p['end']-p['start'],remaining);part=O/f'raw-part-{i}.wav'
 ff(['-ss',p['start'],'-i',source['path'],'-t',dur,'-map',srcmap['map'],'-af',srcmap['filter'],'-ar',48000,'-ac',1,part]);parts.append(part);remaining-=dur
 if remaining<0.001:break
cat=O/'raw-parts.txt';cat.write_text(''.join("file '"+str(p)+"'\n" for p in parts))
ff(['-f','concat','-safe',0,'-i',cat,'-c','copy',raw])
# Audit only: no dereverb can be selected merely from the room number.
base='highpass=f=70,equalizer=f=140:t=q:w=1.0:g=1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0'
opts={'original':['--finish-only'],'default':[],'warm':['--eq',base+',equalizer=f=120:t=q:w=0.8:g=1.5'],'bass':['--eq',base+',equalizer=f=120:t=q:w=0.8:g=3.0']}
for key,args in opts.items():
 out=O/(key+'.wav');inp=raw
 if key=='original':
  inp=O/'raw-stereo.wav';ff(['-i',raw,'-af','pan=stereo|c0=c0|c1=c0',inp])
 if not out.exists():
  p=subprocess.run([sys.executable,str(A/'voice_chain.py'),'--in',str(inp),'--out',str(out),'--work',str(O/(key+'-work'))]+args,capture_output=True,text=True)
  (O/(key+'.log')).write_text(p.stdout+p.stderr)
  if p.returncode:raise RuntimeError(key+': '+p.stderr[-1000:])
 ff(['-i',out,'-c:a','libmp3lame','-b:a','128k',Q/('voice-'+key+'.mp3')]);print('VOICE READY',key,flush=True)
ff(['-i',A/'reference/muhammad_16x9_voice.flac','-t',30,'-c:a','libmp3lame','-b:a','128k',Q/'voice-reference.mp3'])
(O/'options.json').write_text(json.dumps(opts,indent=2))
question='You are a dialogue mixer. Inspect all four audio files fully. They are the same 30 seconds, level matched. Reference is a different approved film for tone only. Score each option 1-10 for natural finished voice, room echo, thinness, boom, harshness, sibilance and intact word tails. Return JSON only: {"scores":{"clip_A.mp3":{"score":8,"room":false,"chopped":false,"fault":"..."}},"ship":"clip_A.mp3"}. Score every actual filename. Do not infer processing from letters.'
results=[]
for i in range(5):
 d=O/f'trial-{i+1}';d.mkdir(exist_ok=True);rng=random.Random(2711+i);mapping=dict(zip('ABCD',rng.sample(list(opts),4)))
 for letter,key in mapping.items():shutil.copyfile(Q/('voice-'+key+'.mp3'),d/('clip_'+letter+'.mp3'))
 (d/'prompt.txt').write_text(question);(d/'mapping.json').write_text(json.dumps(mapping))
 p=subprocess.run([sys.executable,str(W/'recipe/gemini_listen.py'),str(d/'prompt.txt'),str(Q/'voice-reference.mp3')]+[str(d/('clip_'+l+'.mp3')) for l in rng.sample(list(mapping),4)],capture_output=True,text=True,env=dict(os.environ,GM='gemini-3.1-pro-preview'))
 (d/'result.txt').write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError('Audio review request failed: '+p.stdout[-500:])
 result=json.loads(re.search(r'\{.*\}',p.stdout.split('USAGE')[0],re.S).group());result['mapping']=mapping;results.append(result);(O/'ranking.json').write_text(json.dumps(results,indent=2));print('BLIND TRIAL',i+1,{mapping[re.search('clip_([A-Z])',n).group(1)]:v['score'] for n,v in result['scores'].items()},flush=True)
summary={}
for key in opts:
 vals=[v for r in results for n,v in r['scores'].items() if r['mapping'][re.search('clip_([A-Z])',n).group(1)]==key]
 summary[key]={'mean':sum(v['score'] for v in vals)/len(vals),'scores':[v['score'] for v in vals],'room':sum(bool(v.get('room')) for v in vals),'chopped':sum(bool(v.get('chopped')) for v in vals)}
(O/'summary.json').write_text(json.dumps(summary,indent=2));print('SUMMARY',summary,flush=True)
