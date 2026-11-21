from pathlib import Path
import json,sys,os
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];os.environ['GATE_GROUP']='DS-27';sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech
for name in ['start-original','restart-original']:
 result=speech.transcribe(str(W/'review'/(name+'.wav')),model='small.en');(W/'evidence'/(name+'-words.json')).write_text(json.dumps(result,indent=2));print(name,result,flush=True)
