from full import R,ROOT,FPS,prepare,render,dump
import json,subprocess,finish,renderq
with renderq.slot('Vacuum B ownvoice opening and graphic clearance',pool='heavy',group='SL-11'):
 d=R/'build/B';prepare('B');T=json.loads((d/'timeline.json').read_text())
 man=json.loads((d/'graphics.json').read_text())
 for m,parent in zip(man,[507.2,578.5]):
  z=next(s for s in T['seg'] if s['kind']=='parent' and s['parent_a']<=parent<s['parent_b']);a=round((z['a']+parent-z['parent_a'])*FPS)/FPS;dur=m['b']-m['a'];m.update(a=a,b=a+dur)
 dump(d/'graphics.json',man)
 with open(d/'pre-render-junk.log','w') as log:
  rc=subprocess.run(['python3',str(ROOT/'.claude/skills/_shared/cut/junk.py'),str(d/'his_mix.wav'),'--words',str(d/'words.json'),'--out',str(d/'pre-render-junk.json')],stdout=log,stderr=subprocess.STDOUT).returncode
 assert rc==0
 choice=json.loads((R/'audio/pickup-choice.json').read_text())
 if choice['kind'].startswith('AI'):
  rc=finish.command(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',choice['file'],'--synthetic'],d/'pickup-audio-gate.log');assert rc==0,'Ownvoice generated pickup gate failed'
 render('B');finish.checks('B')
