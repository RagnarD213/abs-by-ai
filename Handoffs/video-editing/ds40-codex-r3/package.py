from pathlib import Path
import subprocess,sys,json,hashlib
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';A=R/'.claude/skills/_shared/audio'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R3 packaging and gates')
for name,pic in [('sample','wide'),('dark','dark'),('hair','hair')]:
 subprocess.run([F,'-y','-v','error','-i',str(W/f'{pic}-picture.mp4'),'-i',str(W.parent/'round2/review/media/balanced.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(D/f'{name}.mp4')],check=True)
subprocess.run([F,'-y','-v','error','-i',str(D/'sample.mp4'),'-vf','scale=540:960','-c:v','libx264','-crf','21','-preset','fast','-threads','2','-c:a','copy','-movflags','+faststart',str(D/'phone.mp4')],check=True)
# Extracted AAC bytes must be identical to the selected R2 movie.
hashes={}
for name,path in [('approved',W.parent/'round2/review/media/balanced.mp4')]+[(n,D/f'{n}.mp4') for n in ['sample','dark','hair','phone']]:
 data=subprocess.check_output([F,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-']);hashes[name]=hashlib.sha256(data).hexdigest()
assert len(set(hashes.values()))==1
(W/'audio-identity.json').write_text(json.dumps(hashes,indent=2))
for name in ['sample','dark','hair','phone']:
 cmd=[sys.executable,str(A/'audio_gate.py'),str(D/f'{name}.mp4'),'--untreated',str(W/'voice-balanced.wav.audio_untreated.json')]
 if name=='sample':cmd+=['--ab',str(D/'reference-ab.mp4')]
 result=subprocess.run(cmd,stdout=open(W/f'audio-{name}.log','w'),stderr=subprocess.STDOUT);print('AUDIO',name,result.returncode,flush=True)
p=json.loads((W/'plan.json').read_text());p['scope']='Dan requested a 10-second wide hair-flicker revision only. Balanced voice, warmer color, full native framing locked. No full edit.';p.pop('negative_events_scan',None);p['watch_log']=str(W/'watch/watch_pass.json');(W/'plan.json').write_text(json.dumps(p,indent=2))
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(D/'sample.mp4'),'--plan',str(W/'plan.json'),'--out',str(W/'watch'),'--log',str(W/'watch/watch_pass.json')],stdout=open(W/'watch.log','w'),stderr=subprocess.STDOUT,check=True)
print('WATCH READY',flush=True)
for name in ['sample','dark','hair','phone']:
 pp=dict(p)
 if name!='sample':pp['watch_log']=str(W/f'watch-{name}/watch_pass.json')
 (W/f'plan-{name}.json').write_text(json.dumps(pp,indent=2))
 result=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(D/f'{name}.mp4'),'--format','organic9x16','--plan',str(W/f'plan-{name}.json')],stdout=open(W/f'deliver-{name}.log','w'),stderr=subprocess.STDOUT);print('DELIVER',name,result.returncode,flush=True)
print('PACKAGE DONE',flush=True)
