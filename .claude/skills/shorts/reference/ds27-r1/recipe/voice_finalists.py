from pathlib import Path
import subprocess,sys,json,os,random,shutil,re
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];O=W/'audio';Q=W/'review';F=str(R/'Media/video_edit/bin/ffmpeg');A=R/'.claude/skills/_shared/audio';os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-27'
eq='highpass=f=70,equalizer=f=140:t=q:w=1.0:g=1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0,equalizer=f=120:t=q:w=0.8:g=3.0'
for k,dry in [('bass-smooth',False),('bass-dry',True)]:
 cmd=[sys.executable,str(A/'voice_chain.py'),'--in',str(O/'source-30.wav'),'--out',str(O/(k+'.wav')),'--work',str(O/(k+'-work')),'--eq',eq,'--no-expander-because','C1719 five blind rankings heard chopped endings on expanded bass twice and default three times; compare complete word tails.']
 if dry:cmd+=['--dereverb-because','C1719 raw room EDT 58.7 ms; room echo heard in untreated four of five blind rankings, saved under audio/trial-*/result.txt.']
 p=subprocess.run(cmd,capture_output=True,text=True);(O/(k+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr[-1000:]
 subprocess.run([F,'-v','error','-nostdin','-y','-i',str(O/(k+'.wav')),'-c:a','libmp3lame','-b:a','128k',str(Q/('voice-'+k+'.mp3'))],check=True)
opts=['original','bass','bass-smooth','bass-dry'];results=[]
question='Inspect all four level-matched audio options fully. Same 30 seconds. Reference is a different approved film for tone only. Rate each naturalness, natural complete word tails, echo, bass boom, harshness, processing artifacts. Never infer processing from labels. Return JSON only: {"scores":{"clip_A.mp3":{"score":8,"room":false,"chopped":false,"fault":"..."}},"ship":"clip_A.mp3"}. Use all actual filenames.'
for i in range(5):
 d=O/f'final-trial-{i+1}';d.mkdir(exist_ok=True);rng=random.Random(7127+i);m=dict(zip('ABCD',rng.sample(opts,4)))
 for l,k in m.items():shutil.copyfile(Q/('voice-'+k+'.mp3'),d/('clip_'+l+'.mp3'))
 (d/'prompt.txt').write_text(question);(d/'map.json').write_text(json.dumps(m));p=subprocess.run([sys.executable,str(W/'recipe/gemini_listen.py'),str(d/'prompt.txt'),str(Q/'voice-reference.mp3')]+[str(d/('clip_'+l+'.mp3')) for l in rng.sample(list(m),4)],capture_output=True,text=True,env=dict(os.environ,GM='gemini-3.1-pro-preview'));(d/'result.txt').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout[-500:]
 j=json.loads(re.search(r'\{.*\}',p.stdout.split('USAGE')[0],re.S).group());j['mapping']=m;results.append(j);(O/'final-ranking.json').write_text(json.dumps(results,indent=2));print('FINAL TRIAL',i+1,{m[re.search('clip_([A-Z])',n).group(1)]:v for n,v in j['scores'].items()},flush=True)
summary={}
for k in opts:
 vals=[v for r in results for n,v in r['scores'].items() if r['mapping'][re.search('clip_([A-Z])',n).group(1)]==k];summary[k]=dict(mean=sum(v['score'] for v in vals)/len(vals),scores=[v['score'] for v in vals],chopped=sum(v.get('chopped',False) for v in vals),room=sum(v.get('room',False) for v in vals))
(O/'final-summary.json').write_text(json.dumps(summary,indent=2));print(summary,flush=True)
