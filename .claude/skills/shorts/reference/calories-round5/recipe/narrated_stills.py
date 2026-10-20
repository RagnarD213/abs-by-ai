from pathlib import Path
import sys,json,wave,hashlib
P=Path(__file__).parent;W=P.parent;OLD=W.parent/'round3';O=W/'review'
sys.path.insert(0,str(P));from frame_compositor import still
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/framecheck'));from gate import require_pass
records={};configs={}
for S,duration,switch in [('D',2.3023,1.15)]:
 require_pass(str(W/f'frames/{S}01-start.png'),str(W/f'frames/{S}01-end.png'))
 for which,t in [('start',.5),('end',4.1 if S=='A' else 1.7)]:still(S,which,t).save(O/f'frames/{S}01-{which}-composed.jpg',quality=94)
 src=OLD/f'build/{S}/audio.wav';out=O/f'{S}01-narration.wav'
 with wave.open(str(src),'rb') as a:
  params=a.getparams();n=round(duration*params.framerate);data=a.readframes(n)
  with wave.open(str(out),'wb') as b:b.setparams(params);b.writeframes(data)
 with wave.open(str(out),'rb') as b:assert b.readframes(n)==data
 duration=n/params.framerate
 cues=json.loads((OLD/f'build/{S}/cues.json').read_text());times=sorted(set([0.0,switch]+[c['a'] for c in cues if c['a']<duration]+[c['b'] for c in cues if c['b']<duration]));slides=[]
 for i,t in enumerate(times):
  name=f'frames/{S}01-context-{i:02d}.jpg';which='start' if t<switch else 'end';still(S,which,t+.00001).resize((540,960)).save(O/name,quality=93);slides.append({'at':t,'src':name})
 configs[S+'01']={'audio':out.name,'duration':duration,'slides':slides}
 records[S]={'audio_source':str(src),'audio_preview':str(out),'frames_trimmed_to':n,'sample_rate':params.framerate,'duration':duration,'pcm_exact_prefix':True,'pcm_sha256':hashlib.sha256(data).hexdigest(),'frame_switch':switch,'status':'synchronized still placeholders only; Flow motion not generated','title_source':'same approved R3 title still for placeholder display'}
(W/'records/narrated-still-config.json').write_text(json.dumps(configs,indent=2));(W/'records/context-build.json').write_text(json.dumps(records,indent=2));print('Exact narration prefixes and synchronized still contexts ready')
