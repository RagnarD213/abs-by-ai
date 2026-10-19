from pathlib import Path
import sys,json,base64,random
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/shortad-from-longform/reference/kit9x16'));import ai_calls
api=ai_calls.provider('gemini',str(W/'review-costs.jsonl'));results=[]
for n in range(2):
 keys=['baseline','balanced','clearer','fuller'];random.Random(200+n).shuffle(keys);mapping=dict(zip('ABCD',keys))
 parts=[{'text':'Independently listen to four level-matched mixes of the same camera speech. Assess actual heard quality, without favoring processing. Judge naturalness, intelligibility, body, warmth, intact word tails, and absence of harshness or artificial processing. Differences may be small; ties are allowed. Return JSON {"scores":{"A":{"naturalness":0-10,"clarity":0-10,"body":0-10,"specific_issue":"..."},...},"preference":"A/B/C/D/tie","reason":"...","transcript":"...","clipped_words":false}. Do not invent faults. Assess only audio, not the opinions or claims in speech.'}]
 for label,key in mapping.items():parts.extend([{'text':label},{'inline_data':{'mime_type':'audio/wav','data':base64.b64encode((W/f'voice-{key}.wav').read_bytes()).decode()}}])
 out=api._call('gemini-3.1-pro-preview',parts,'r2-blind-audio',max_tokens=2500);results.append({'mapping':mapping,'result':out});(W/'listening.json').write_text(json.dumps(results,indent=2));print(json.dumps(results[-1]),flush=True)
print('cost',api.ledger.total(),flush=True)
