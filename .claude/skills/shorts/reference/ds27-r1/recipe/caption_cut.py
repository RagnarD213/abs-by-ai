from pathlib import Path
import sys,os,json
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];os.environ['GATE_GROUP']='DS-27';sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech
ws,method=speech.transcribe(str(W/'voice.wav'),model='small.en');(W/'evidence/full-voice-words.json').write_text(json.dumps(dict(method=method,words=ws),indent=2));edl=json.load(open(W/'edl.json'));words=[]
for v in ws:
 t=v['t'];p=next(p for p in edl if p['n0']/(30000/1001)<=t<p['n1']/(30000/1001));words.append(dict(w=v['w'].strip(),t0=t,t1=v['e'],src=p['start']+t-p['out']))
# Preserve the audible names. No unheard text is added.
for w in words:
 if w['w'].lower()=='like':w['w']='Light'
chunks=[];cur=[]
for w in words:
 if cur and (len(cur)>=3 or w['t0']-cur[-1]['t1']>.55):chunks.append(cur);cur=[]
 cur.append(w)
 if w['w'].endswith(('.',',','!','?')):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
(W/'words_out.json').write_text(json.dumps(words,indent=2));(W/'caption-chunks.json').write_text(json.dumps(chunks,indent=2))
print('TIMED CUT',len(words));print(' '.join(v['w'] for v in words));print([(v['t0'],v['w']) for v in words if 27<v['t0']<39])
