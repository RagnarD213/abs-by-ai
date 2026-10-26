"""Include actual inherited raw-source audio edits even when continuous exercise picture covers them."""
from full import R,F,FPS,dump
import json,sys
for S in (sys.argv[1:] or ['A','B','C']):
 p=R/'build'/S/'timeline.json'
 if not p.exists():continue
 T=json.loads(p.read_text());joins=[z['a'] for z in T['seg'][1:]];inherited=[]
 for left,right in zip(F.S,F.S[1:]):
  if left['roll']==right['roll'] and left['src_f1']==right['src_f0']:continue
  cut=right['out_f0']/FPS
  for z in T['seg']:
   if z['kind']=='parent' and z['parent_a']<cut<z['parent_b']:
    t=z['a']+cut-z['parent_a'];joins.append(t);inherited.append(dict(output=t,parent=cut,left=left['id'],right=right['id']))
 T['audio_joins']=sorted(set(round(t,6) for t in joins));T['inherited_audio_joins']=inherited;dump(p,T);print(S,T['audio_joins'])
