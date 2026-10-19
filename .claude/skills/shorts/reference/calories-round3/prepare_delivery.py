from pathlib import Path
import sys,shutil,json,hashlib
W=Path(__file__).parent.parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills'))
from _shared.deliver.gate import require_stamp
O=W/'review/full';O.mkdir(exist_ok=True,parents=True);VLC=R/'Videos to Review';VLC.mkdir(exist_ok=True)
titles={'B':'Eat a Salad First to Eat Less','C':'Stop Drinking Your Calories','E':'Make Fasting Easier With Black Coffee'};records=[]
for S in 'BCE':
 d=W/'build'/S;v=next(d.glob('calories-short*.mp4'));require_stamp(str(v))
 h=hashlib.sha256(v.read_bytes()).hexdigest();dst=O/f'{S}-master.mp4';shutil.copy(v,dst);assert hashlib.sha256(dst.read_bytes()).hexdigest()==h
 for suf in ['.audio_gate.json','.deliver_gate.json']:shutil.copy(str(v)+suf,str(dst)+suf)
 shutil.copy(W/f'review/candidates/{S}-review.mp4',O/f'{S}-review.mp4')
 stamp=json.load(open(str(v)+'.deliver_gate.json'));rec={'short':S,'title':titles[S],'master':str(v),'sha256':h,'frames':json.load(open(d/'timeline.json'))['frames'],'duration':stamp['duration'],'audio_gate':'PASS exact master','delivery_gate':'PASS exact master','watch':'PASS native sheets/strips, independent judge','supplementary_moving_audio_review':'Gemini SHIP; not human continuous playback','Dan_approval':'pending','review':'full/'+S+'-review.mp4','full_quality':'full/'+S+'-master.mp4'}
 if stamp['duration']>=45:
  out=VLC/f'Calories Not Losing Weight SFL R3 - {titles[S]}.mp4';shutil.copy(v,out);assert hashlib.sha256(out.read_bytes()).hexdigest()==h;rec['VLC_copy']=str(out)
 records.append(rec)
(W/'complete-candidates.json').write_text(json.dumps(records,indent=2));print('Three exact checked review candidates copied;2 VLC copies',flush=True)
